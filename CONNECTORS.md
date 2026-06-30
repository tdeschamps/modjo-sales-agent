# Connectors — Modjo Sales Agent

The Modjo Sales Agent is built around **your Modjo workspace**. Modjo is the required-for-full-capability connector — without it, the agent runs in CSV/paste-in mode. A handful of optional connectors extend the toolkit's reach (persistence, calendar awareness, scannable visuals, drafted Slack messages).

## The three modes — what works when

- **CSV / paste-in onramp** *(no connectors)* — you paste in pipeline CSVs, deal context, account names. The agent reasons from your input. See `shared/csv-schemas.md` for the exact paste-in formats per skill.
- **Modjo-connected** *(the standard product)* — the agent pulls calls, deals, accounts, contacts, emails, transcripts, and your team's Modjo agents directly. No re-typing. This is where the agent earns its keep.
- **Modjo + Notion** *(the full experience)* — adds persistent coaching logs, 1:1 history, Plays Library, and per-account/deal logs that accumulate longitudinal data.

## Connector categories

### Modjo *(required for the full experience — optional via CSV onramp)*

The primary connector. Unlocks calls, deals, accounts, contacts, emails, transcripts, calendar events, and your team's Modjo AI agents (MEDDPICC scoring, coaching feedback, call summaries, deal briefing, next-step extraction, meeting prep, email follow-up, and any custom agents your team has built).

**What you get**:
- Live calls and call summaries quoted in every skill's output — not "your rep mentioned X in a call recently" but specific quoted moments with timestamps
- MEDDPICC pillar scoring from real call evidence, not from rep self-report
- Deal-health overlay on stage-based forecast weighting (a "commit" deal with no buyer touch in 30 days isn't really commit)
- Automatic morning brief, meeting prep, and pipeline triage — the agent does the data-gathering, you focus on the act-on-it part

**Agent discovery**: the agent doesn't hard-code your specific Modjo agent UUIDs (those vary across workspaces and may be customised by your team). It discovers them at runtime via `get_agents` with semantic search filters ("MEDDPICC", "coaching", "next step", "briefing", etc.). If your team has renamed agents or built custom ones, the skill picks them up without any plugin config changes.

### Notion *(optional — adds persistence)*

Unlocks the persistent coaching log, the team Plays Library, and per-account/deal logs. See `shared/notion-structure.md` for the recommended workspace hierarchy.

**What you get**:
- `coach-this-rep` writes weekly reviews to a persistent log; week-over-week theme evolution becomes real (not invented)
- `prep-the-1on1` reads prior 1:1 commitments forward so the manager doesn't double-cover what's already been discussed
- `learn-from-closed-deals` writes candidate plays to the team Plays Library (approval-gated — every entry requires confirmation)
- `lock-the-close-plan` can persist the Mutual Action Plan under the deal's account page
- `audit-this-deal` can log the structured assessment under the account so the next rep on the deal has context

Without Notion, every skill still runs — but as a live brief in chat only, with no longitudinal data.

### CRM *(optional supplement — Salesforce, HubSpot, Pipedrive, others)*

Modjo already syncs with your CRM, so the deals, accounts, contacts, and activity that surface through Modjo's MCP originate from whichever CRM you use — Salesforce, HubSpot, Pipedrive, Close, Zoho, etc. Most customers don't need a separate CRM MCP wired up.

When a direct CRM MCP helps:
- You want richer CRM-native data than Modjo's sync surfaces (custom fields, complex CRM relationships, marketing-engagement data, sequence-tool integration history).
- Some skills (`audit-the-forecast`, `forecast`) benefit from CRM stage-history and field-update timestamps for the stage-stagnation check — Modjo surfaces current stage but may not expose stage-change timestamps in every tenant.
- You want to run the plugin on accounts that aren't yet in Modjo (early-stage opportunities, cold prospects).

**What you get** with a direct CRM connector: deeper deal-history granularity, marketing-engagement signals, sequence-tool history if integrated. The plugin still treats CRM as **read-only** — it never writes deal updates, stage moves, or field changes back to your CRM. That's a deliberate design choice (see "What's never auto-done" below).

Modjo's MCP remains the primary data layer in all cases. The CRM MCP is supplementary.

### Visualize MCP *(optional — for scannable widget output)*

Unlocks live brief widgets. Without it, skills output as Markdown.

**What you get**: scannable, branded widget output respecting `shared/widget-brevity.md`'s 90-second-scan discipline. Coaching reports, deal audits, and pipeline reviews all render as widgets the rep or manager can quickly scan.

### Slack MCP *(optional — for drafted messages)*

Unlocks **drafted** Slack messages. The agent never auto-sends — every Slack output is a draft you review and dispatch.

**What you get**:
- Ready-to-paste outbound drafts from `build-net-new-pipeline`
- Drafted next-move messages from `unstick-this-deal` and `spot-expansion-signals`
- Customer-shareable kickoff agendas from `hand-off-to-csm`
- Manager-share drafts from coaching skills

### Gmail *(optional — the plugin's first write connector, draft-only)*

Unlocks `write-the-follow-up`'s richest mode. Every other connector is read-only from the plugin's side; Gmail is the first that **writes** — but only ever as a **draft**, never a send.

**What you get**:
- The **real email thread** read directly (`get_thread` / `search_threads`), so the follow-up references what was actually said in writing, not just call summaries
- **Tone-matching** — the skill learns your writing voice from your last ~15–20 sent emails (greeting, sign-off, language, sentence shape) and drafts in *your* voice. The learned voice profile is persisted and hand-correctable (see `shared/voice-profile.md`)
- A **threaded draft placed in your mailbox** (`create_draft`) — correct recipient, subject, threaded to the conversation — ready for you to review and send from your own inbox

**The guarantee**: Gmail access is used for reading threads/sent mail and for `create_draft` only. There is no send path. Nothing leaves your mailbox until *you* click send. The skill always renders the draft inline for review first, and asks before creating the Gmail draft.

Without Gmail, `write-the-follow-up` still works: it drafts from Modjo's call/email data in a neutral register and you copy it into your mail client yourself.

### Calendar *(optional — Google Calendar / Outlook)*

The Modjo MCP already exposes `get_calendar_events` for connected calendars. If your Modjo doesn't have a calendar integration, an external calendar MCP can fill the gap for `start-the-day` and `prep-this-meeting`.

## Per-skill capability matrix

| Skill | Modjo only | Modjo + Notion | CSV / paste-in only |
|---|---|---|---|
| `start-the-day` | Live brief from today's meetings + open deals + week's calls | + carries forward unresolved items from yesterday's brief | Rep lists today's meetings + deals manually |
| `prep-this-meeting` | Full prep with last-3-calls quoted | + prior 1:1 context if relevant | Rep pastes prior call notes |
| `audit-this-deal` | MEDDPICC from real calls, pivotal-moment quotes | + persistent audit log under the account | Rep walks the deal in chat |
| `learn-from-similar-deals` | Closed-deal corpus with quoted moments | + team Plays Library citations | Rep names comparable deals; starter plays only |
| `lock-the-close-plan` | MAP built from call evidence | + persistent MAP under account page | Rep dictates commitments |
| `unstick-this-deal` | Full with call evidence | + team Plays Library precedent | Paste-in only; starter plays only |
| `handle-the-objection` | Verbatim objection + won-deal precedent reframe, voiced | (+ Gmail) voice-matched async draft + threaded mailbox draft | Paste the objection; starter-play reframe only |
| `score-this-call` | Full with scoring agent | + persistent score log | Rep pastes transcript or notes |
| `write-the-follow-up` | Grounded draft, mode auto-detected, neutral register | (+ Gmail) voice-matched draft + threaded mailbox draft | Rep pastes the thread / call notes |
| `review-the-pipeline` | Triage with deal-health overlay | + persistent weekly review log | CSV paste-in |
| `build-net-new-pipeline` | Won-deal pattern overlay on outbound drafts | + persistent target list | Rep names target segment |
| `audit-the-forecast` | Full hygiene checks + activity overlay | + persistent hygiene log | CSV paste-in |
| `forecast` | Full with Modjo deal-health overlay | + persistent forecast snapshot | CSV paste-in (Schema 1) |
| `account-research` | Modjo CRM check + web research | + persistent research log | Account name + web search |
| `competitive-intelligence` | Battlecard from lost/won deals with quotes | + persistent battlecard in Plays Library | Competitor name + sample deals |
| `coach-this-rep` | Coaching from real call evidence | + week-over-week theme tracking | Manager paste-in week notes |
| `prep-the-1on1` | Agenda from this week's calls | + prior 1:1 commitments forward | Rep paste-in topics |
| `learn-from-closed-deals` | Per-deal retros with quoted moments | + writes to team Plays Library | Closed-deals CSV |
| `spot-expansion-signals` | Signals from real customer calls | + persistent signal log | Rep walks the book |
| `hand-off-to-csm` | Handover with commitments quoted from calls | + persistent handover doc | Rep dictates the handover |
| `sales-router` | (meta — no data fetch needed) | (meta) | (meta) |

## Setup

Connectors install at the host level (Cowork / Claude Code), not inside the plugin.

1. **Modjo** — required for the full experience. From your host, open the connector picker, find Modjo, and authenticate with your Modjo credentials. The plugin picks up your workspace automatically — including your team's specific Modjo agents.
2. **Notion** — optional but recommended for managers. Authenticate Notion, then create the recommended workspace hierarchy (see `shared/notion-structure.md`).
3. **Visualize MCP** — typically auto-enabled in Cowork.
4. **Slack** — optional. Authenticate Slack from the connector picker.
5. **Calendar** — optional. Modjo's MCP usually exposes calendar; an external Google Calendar / Outlook MCP can fill the gap if needed.

Once a connector is live, every skill that benefits from it picks it up automatically — no plugin config changes.

## What's never auto-done

Hard rules across every skill, regardless of which connectors are live:

- **Never writes to your CRM.** The Modjo MCP is read-only from the plugin's perspective. The plugin surfaces hygiene issues and proposes fixes; the rep applies them.
- **Never auto-sends Slack, email, or any external message.** Drafts only. Gmail is the one connector the plugin writes to, and it only ever creates a **draft** in your mailbox — there is no send path. You send from your inbox.
- **Always asks before writing to Notion** if the target page doesn't already exist.
- **Always renders the live brief first** even when also writing to Notion or producing a Slack draft.
- **Single-question agent framings.** Multi-part questions to Modjo agents return empty — confirmed failure mode.

## What's deferred to later versions

- **Telemetry & measurement** — adoption tracking, sales-outcome lift, rep feedback capture, Modjo product engagement. Deferred until there's real usage to measure rather than instrumenting up-front.
- **CRM write-back** — the agent intentionally doesn't touch your CRM. Future versions may add carefully-guardrailed write paths.
- **Multi-language coaching prompts** — French / Spanish / German on the roadmap.
