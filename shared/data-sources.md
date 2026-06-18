# Data sources — the Modjo operation map

The skills in this plugin are built for **your Modjo workspace**. They use Modjo's calls, deals, accounts, contacts, emails, transcripts, and AI agents as their primary data layer. If Modjo isn't connected yet, every skill falls back to a CSV/paste-in onramp (see `csv-schemas.md`) so reps can try the toolkit before fully wiring up their Modjo.

This file maps the conceptual operations each skill performs to the Modjo MCP tools that execute them, and documents the runtime-discovery pattern for Modjo's AI agents.

## Hard rules

1. **Skills don't hard-code agent UUIDs.** Modjo customers configure their own agents — agent UUIDs vary across tenants. Skills always discover agents at runtime via `get_agents` with a search filter (e.g. "MEDDPICC", "coaching", "next step"). Never write a literal UUID in skill prose.
2. **Skills don't reconstruct CRM IDs.** Modjo's `crmId` field exposes the underlying CRM's exact ID — Salesforce, HubSpot, Pipedrive, Close, Zoho, or whichever CRM the customer uses. Use it verbatim. Tenants commonly have multiple ID formats coexisting (sandboxes, merged instances, mixed CRM sources). Always use the exact `crmId` from `get_deals` or `get_accounts`. A wrong id returns "deal not found" silently.
3. **Single-question framings when calling Modjo agents.** Multi-part questions return empty — a confirmed failure mode. If you need to score multiple MEDDPICC pillars, make separate calls.
4. **CSV/paste-in is always offered as a fallback** for reps who haven't enabled Modjo yet, or for sensitive deals where the rep doesn't want the skill to auto-pull data.

## The Modjo MCP surface — operation map

| Conceptual op (what skill says) | Modjo tool | Returns | Notes |
|---|---|---|---|
| `find_user(name | email)` | `get_users` filtered by name/email | userId, role, team | Always resolve userId first; never assume |
| `find_account(name)` | `get_accounts` filtered by name | accountId, crmId, owners | Returns crmId verbatim — use as-is |
| `find_contact(name | email | accountId)` | `get_contacts` | contactId, title, account, last_touch | |
| `list_recent_calls(userIds | accountIds | dealIds, dateRange)` | `get_calls` | callId, summary, participants, deal | Use date range and limits — Modjo can return large payloads |
| `list_recent_emails(userIds | accountIds | dealIds, dateRange)` | `get_emails` | emailId, subject, sender, deal | |
| `list_calendar_events(userIds, dateRange)` | `get_calendar_events` | eventId, time, account, attendees | Pre-resolves account/deal when calendar invite has them |
| `list_open_deals(userIds | accountIds, filters)` | `get_deals` filters.status=Open | dealId, crmId, amount, stage, closeDate, contacts | |
| `list_closed_deals(userIds | accountIds, filters)` | `get_deals` filters.status=Won/Lost | dealId, crmId, outcome, closeDate, lossReason | |
| `get_transcript(callId)` | `get_transcript` | verbatim text + timestamps | Use only when a quote is load-bearing; transcripts are heavy and often overflow — see "Large results" below |
| `analyse_deal(crmId, question, [agentUuid])` | `ask_anything_on_deal` | structured agent answer | Single-question framings. Use `crmId` verbatim. |
| `analyse_account(accountId, question, [agentUuid])` | `ask_anything_on_account` | structured agent answer | Same single-question rule |
| `analyse_call(callId, question, [agentUuid])` | `ask_anything_on_call` | structured agent answer | |
| `score_deal_meddpicc(crmId)` | discover MEDDPICC-capable agent via `get_agents` (search="MEDDPICC"), then `ask_anything_on_deal(crmId, question, agentUuid)` | pillar scores + evidence | One agent call per pillar. Never multi-part. |
| `discover_agents(search)` | `get_agents` with search filter | list of agent UUIDs + names + descriptions | Cache the result; don't call multiple times per skill run |

### Gmail — optional, draft-only (used by `write-the-follow-up`)

Gmail is an optional connector and the plugin's **only write surface** — and it writes drafts only, never sends. Used by `write-the-follow-up` to read the real thread, learn the rep's voice, and place a threaded draft in the mailbox.

| Conceptual op | Gmail tool | Returns / does | Notes |
|---|---|---|---|
| `read_thread(threadId)` | `get_thread` | full thread bodies | The real written exchange — richer than Modjo's email metadata |
| `search_threads(query)` | `search_threads` | matching threads | Find the thread for an account/contact; also pull the rep's recent **sent** mail for the voice profile |
| `create_email_draft(to, subject, body, threadId)` | `create_draft` | creates a **draft** in the mailbox | **Never sends.** Always threaded to the conversation. Approval-gated — ask before creating; render the draft inline first. |

There is no send tool in the plugin's Gmail usage by design. See `voice-profile.md` for how sent mail becomes the rep's voice profile, and `output-modes.md` for the draft handoff contract.

## Large results — the file-spill recovery protocol (load-bearing)

Heavy Modjo calls — especially `get_transcript`, but also large `get_calls` / `ask_anything_*` results — frequently exceed the tool-output token limit. When that happens the tool does **not** fail and does **not** return the data inline. Instead it returns a message like:

> `Error: result (57,268 characters) exceeds maximum allowed tokens. Output has been saved to /…/tool-results/<tool>-<id>.txt … Use offset and limit parameters … read … in sequential chunks until 100% has been read.`

**This is not a failure — the full data is on disk and you are required to read it.** When you see a "saved to … exceeds maximum allowed tokens" message:

1. **Read the spilled file** at the given path with the Read tool, in sequential `offset`/`limit` chunks, until you have covered the portion you need (for a load-bearing quote, read until you find and can quote the exact moment; for a full review, read 100%).
2. **Only then** quote verbatim — the quotes and timestamps must come from the file you actually read, not from the call summary.
3. **If, and only if, you cannot read the spilled file** (path missing, unreadable), treat it as transcript-unavailable: say "**summary-only — full transcript not read**", emit **no** verbatim quotes and **no** timestamps, and score transcript-dependent dimensions Partial at best.

**Never** respond to a spill message by falling back to the summary while presenting summary-derived content as if it were verbatim transcript. Claiming "full transcript read" or emitting `MM:SS` timestamps when you only read the summary is fabrication — the single worst failure mode across every skill in this plugin.

## Agent discovery — the runtime pattern

Every skill that needs a specialized agent (MEDDPICC scoring, sales coaching, next-step extraction, objection analysis) discovers it at runtime. Here's the canonical pattern, with the search filters that map to common Modjo agent catalogs:

```
agents = get_agents(filter: { search: "MEDDPICC" })   // or: "deal challenger", "qualification", "meddic"
if agents.length > 0:
    use agents[0].uuid in ask_anything_on_deal(crmId, question, agentUuid=agents[0].uuid)
else:
    // fall back to default agent — omit agentUuid, put the rubric directly in the question
    ask_anything_on_deal(crmId, question)
```

Search filters that work across most Modjo tenants (workspaces commonly publish agents with these names or close variants):

- **MEDDPICC / deal qualification** → `"MEDDPICC"`, `"deal challenger"`, `"qualification"`, `"MEDDIC"`, `"deal qualifier"`
- **Sales coaching / call scoring** → `"coach"`, `"scoring"`, `"call quality"`, `"call qualifier"`
- **Call summary** → `"summary"`, `"call summary"`
- **Next-step / commitment extraction** → `"next step"`, `"commitments"`, `"actions"`, `"next stepper"`
- **Deal briefing** → `"briefing"`, `"deal briefing"`
- **Meeting preparation** → `"prepper"`, `"meeting prep"`, `"meeting prepper"`
- **Email follow-up drafting** → `"follow up"`, `"email follow up"`
- **Objection analysis** → `"objection"`
- **Win/loss analysis** → `"win loss"`, `"retro"`, `"win/loss"`

If no matching agent exists in the customer's workspace, the skill falls back to the default agent with the rubric in the question. If even the default agent returns empty (or Modjo isn't connected), the skill operates on call summaries + rep paste-in — every skill has a documented fallback chain.

## Modjo + Notion together — the persistence layer

A Modjo-only setup runs every skill in live-brief mode (output rendered as a widget, no persistence). Adding Notion unlocks the persistence layer:

- **Coaching workspace** — `coach-this-rep` writes weekly reviews; `prep-the-1on1` reads prior 1:1 commitments forward
- **Plays Library** — `learn-from-closed-deals` writes; `learn-from-similar-deals`, `unstick-this-deal`, `lock-the-close-plan` read
- **Account / deal logs** — `audit-this-deal`, `lock-the-close-plan`, `spot-expansion-signals` can persist their output under the account's page

See `notion-structure.md` for the recommended Notion hierarchy.

Notion writes are always approval-gated. The plugin never auto-creates pages or auto-modifies existing ones.

## CSV / paste-in fallback (when Modjo isn't connected yet)

This is the onramp mode. A rep who hasn't fully enabled Modjo can still try the toolkit by pasting in:

- An open-pipeline CSV (for `audit-the-forecast`, `review-the-pipeline`, `forecast`)
- Today's meetings as a CSV or list (for `start-the-day`, `prep-this-meeting`)
- Deal context as structured paste-in (for `audit-this-deal`, `lock-the-close-plan`, `unstick-this-deal`, etc.)
- A target-accounts CSV (for `build-net-new-pipeline`)
- A customer-book CSV (for `spot-expansion-signals`)
- Closed-deals CSV (for `learn-from-closed-deals`)

Full schemas are in `csv-schemas.md`. The reasoning that runs is the same — only the data input changes. Once the rep enables Modjo, the same skills run on live data automatically.

## Graceful degradation per skill — what works when

| Skill | Full Modjo + Notion | Modjo-only (no Notion) | CSV / paste-in only |
|---|---|---|---|
| `start-the-day` | Full | Live brief, no historical compare | Rep lists today's meetings |
| `prep-this-meeting` | Full with prior 1:1 context | Full live brief | Rep pastes prior call notes |
| `audit-this-deal` | Full + Notion log | MEDDPICC + evidence, no log | Rep walks the deal in chat |
| `learn-from-similar-deals` | Full + team Plays Library | Full minus team plays | Rep names comparable deals; starter plays only |
| `lock-the-close-plan` | MAP + Notion persistence | MAP rendered, no persistence | Rep dictates commitments |
| `unstick-this-deal` | Full with Plays Library | Full minus team plays | Paste-in situation |
| `score-this-call` | Full with scoring agent | Manual scoring from rubric | Rep pastes transcript + notes |
| `write-the-follow-up` | Grounded draft, neutral register (+ Gmail: voice-matched + threaded mailbox draft) | Same — Gmail layers on top of either | Rep pastes the thread / call notes |
| `review-the-pipeline` | Full + Notion review log | Full live brief | CSV paste-in |
| `build-net-new-pipeline` | Full + ICP file | Full minus ICP-scored fit | Rep names target segment |
| `audit-the-forecast` | Full hygiene checks | Full | CSV paste-in |
| `hand-off-to-csm` | Full + Notion handover doc | Live brief only | Rep dictates the handover |
| `spot-expansion-signals` | Full + Notion signal log | Live brief only | Rep walks the book |
| `account-research` | Full with account-intel platform | Web + Modjo CRM check | Account name only |
| `competitive-intelligence` | Full battlecard with quotes | Manual deal analysis | Competitor name only |
| `forecast` | Full + Modjo deal-health overlay | Stage-band weighting only | CSV paste-in |
| `sales-router` | (meta — no data fetch) | (meta) | (meta) |
| `coach-this-rep` | Full coaching with weekly compare | Full minus week-over-week | Manager paste-in week notes |
| `prep-the-1on1` | Full with prior 1:1 forward | Full minus prior-1:1 forward | Rep paste-in topics |
| `learn-from-closed-deals` | Full with plays write | Full minus library write | Closed-deals CSV |

## Rules every skill must follow

1. **Resolve userId via `get_users` first** when the skill takes a rep name. Never assume the userId; the running user's email is the most reliable anchor.
2. **Use `crmId` verbatim from `get_deals` / `get_accounts`.** Never reconstruct.
3. **Discover agents, don't hard-code UUIDs.** Even when shipping to a single customer, agent UUIDs vary by environment (staging vs prod, sub-tenant overrides). Always `get_agents`.
4. **Single-question framings when calling agents.** Multi-part returns empty.
5. **Document the fallback for each data dependency.** If transcripts aren't available, say "summary-only" — don't pretend.
6. **CSV paste-in is a real first-class mode**, not a degraded one. Some reps will use it because they want explicit control over what the skill sees.
