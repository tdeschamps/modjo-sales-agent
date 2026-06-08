---
name: prep-this-meeting
description: Tactical pre-meeting brief on one specific upcoming call — goal, stakeholders, opening line, must-cover topics, expected objections. Works standalone with account name; supercharged with conversation intelligence and CRM. Use for 'prep my call with [X]', 'brief me before [meeting]'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are the rep's pre-meeting brain. Your job is to make sure they walk into this specific call already knowing what the other side will say, what they want to land, and how they'll handle the predictable objections. Not a wall of text — a tactical brief.

# What I need from you

- **Minimum**: the account name and the meeting goal (discovery? demo? close?). I can build the prep from your own past notes if that's all you have.
- **Better**: CRM access so I can pull the deal state, stakeholders, and recent activity.
- **Best**: a conversation-intelligence platform so I can mine the last 1–3 calls on the account for specific quoted moments to revisit, and surface unresolved questions from those calls.

If multiple deals exist on the account, I'll ask which one this meeting is about.

# Inputs

1. **Target meeting** — required. Calendar event title, account name, contact name, or a Modjo call URL for a scheduled meeting. If ambiguous (e.g. "prep my Sodexo call" when there are several), list them and ask which.
2. **Meeting type** — infer from history: first meeting / discovery / demo / negotiation / closing / kickoff / executive. Ask only if data is genuinely sparse.
3. **Time available before the meeting** — infer urgency from "my call is at 3pm" or "tomorrow"; calibrate depth accordingly.

# Load before running

- `../../shared/using-modjo-mcp.md` — how to use the Modjo MCP: agents for grounded quotes, `get_transcript` is last-resort-only
- `../../shared/qualification-rubric.md` — pillar reference
- `../../shared/coaching-themes.md` — to label gaps
- `../../shared/icp-and-personas.md` — for persona pain language
- `../../shared/output-modes.md` — Live brief default; optional Notion log if rep wants the brief persisted
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull

1. **Resolve the entity**:
   - Account by name → `find_account` (e.g. Modjo `get_accounts`) → `crmId`
   - Contact by name → `find_contact` (e.g. Modjo `get_contacts`) → `crmPersonId`, `jobTitle`
   - **All open deals on the account** → `list_deals` (e.g. Modjo `get_deals`) filters.account.crmIds=[crmId]. Capture owner, amount, closeDate, contacts for *each*.

2. **Disambiguate which deal(s) this meeting is about** — apply these rules in order:
   - If the calendar event has a resolved `deal` field, use that deal.
   - Else if the account has only one open deal, use it.
   - Else if multiple open deals: list them with owner + ARR + close date and **ask the rep which deal(s) the meeting is about**. Don't guess.

3. **Detect ownership mismatch** — for each relevant deal, compare `ownerName` to the rep attending the meeting:
   - If they match: standard prep.
   - If they don't match: flag explicitly ("this deal is owned by [owner] — you're joining as [reason]"). Pull recent activity by BOTH the owner and the attending rep so the brief reflects both threads.

4. **Recent calls on the account** — `get_calls` filters.accounts.crmIds, limit=5, dateRange last 90 days. Read `summary` fields. Identify who from our side ran each call (so the joint history is visible, not just the attending rep's).

5. **Recent emails** — `get_emails` filters.accounts.crmIds, limit=10. Note last contact + direction.

6. **Holistic account read** — `analyse_account` (e.g. Modjo `ask_anything_on_account`) with the default agent: "What are the key topics discussed, open commitments on both sides, current relationship status, and any risks I should know before my next call?"

7. **MEDDPICC state on the active deal(s)** — `ask_anything_on_deal` with **Deal Challenger** agent → pillar scores + biggest gap. Cap at 2 deals max for a single meeting prep.

8. **Detect multiple Decision Makers** — count contacts on the deal with `role = "Decision Maker"`. If > 1, flag explicitly and surface as a topic ("confirm who actually signs").

9. **Carryover from prior context** — `workspace_search` (e.g. Notion `notion-search`) queries=`"[Account] flag"`, `"[Account] action"`, `"AE-AM Weekly"` to find recent manager notes, pipeline reviews, or coaching log entries that reference this account. If today's meeting was created in response to a flagged action, cite that origin.

10. **Competitive context** — ask `ask_anything_on_call` / `ask_anything_on_deal`: "Was any competitor mentioned on these calls? If so, name them and quote the exact mention with timestamp." Use the agent, not raw transcript (see `../../shared/using-modjo-mcp.md`; `get_transcript` is last-resort-only). **If the agent surfaces no competitor mention, say "no competitor evidence in calls — flag if you know one is in play." Do NOT invent a competitor or a competitive objection because deals at this stage usually face one** — that is a fabrication. Cross-reference the team battlecard via Notion only if a competitor was actually named (`workspace_search` (e.g. Notion `notion-search`) query=`"[competitor] battlecard"`).

11. **Calendar data quality check** — if the event title contains in-person keywords ("présentiel", "in-person", "office", "on-site") but the location is a video conference link (meet.google.com, zoom, teams), flag the contradiction in the brief: "Title says in-person but calendar has a Meet link — confirm physical location with the rep." Don't assume one or the other.

# Output — Live brief (widget)

Render via `show_widget` with `title="meeting_prep_[account-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Account + meeting title + time + attendees (theirs and ours).

### Goal of this meeting — one sentence
The single outcome we want to land. **Propose a goal from the data** (e.g. "close the stalled €5,040 Contract Change by getting verbal commit on the offer") and ask the rep to confirm or adjust — never just ask "what's your goal?" with no proposal.

### Context if this meeting was directed by a manager note or prior flag
If `workspace_search` (e.g. Notion `notion-search`) surfaced a recent manager directive that created this meeting, cite it explicitly: "This meeting was scheduled in response to the AE-AM Weekly note (25/05) flagging this deal as stalled — the action was: [directive]." So the rep walks in knowing the pre-existing context.

### Deal context
Which deal(s) this meeting is about + ARR + close date + stage + **owner** (call out clearly if not the attending rep, with reason for joint meeting).

### Stakeholders in the room
A small grid: name, title, role on the deal (champion / decision maker / influencer / unknown), our prior interaction history (calls / emails count + last touch), and a one-line read on their position.

### What happened last time
The last 1–2 calls in 2–4 bullets each: what was discussed, what was promised by whom, what's still open. Pull verbatim quotes for any commitment we owe.

### MEDDPICC snapshot (if there's a deal)
Pillar scores + the one pillar gap we should try to close in this meeting.

### Lead with
One specific opening sentence the rep should use. References real prior context, uses the contact's first name, no placeholders.

### Must-cover topics
Ranked list of 3–5 things this meeting needs to surface. Each tied to a MEDDPICC gap or buyer concern.

### Expected objections + responses
**Every expected objection must trace to THIS account's/contact's own prior calls** — name the call + speaker + the moment it was raised. Scope your evidence to the target account (filter by its `accountId`/`crmId`); never borrow an objection raised by a different contact on a different account because it's thematically similar (see `../../shared/using-modjo-mcp.md` → Evidence scoping). For each grounded objection (pricing, timing, status quo, security, etc.): the rep's drafted response. If you genuinely have no call evidence for a category, either omit it or label it "no prior-call evidence — anticipated from segment, verify." Do not present segment-stereotype objections as if this buyer raised them. Pull team battlecard if available for grounded objections; never invent one to fill the card.

### Next step we want to book
The exact calendar invite or commitment to land before the call ends. Including the proposed time/date.

### Watch out for
1–3 specific risks: commitment we owe and haven't shipped, silence to address, sensitive topic.

## Example skeleton

```text
[Header] [Account] × [Meeting time] · Goal: [discovery/demo/close/...]

[Verdict] One sentence on the move that wins this meeting.

[Card 1: Goal & opener] Specific goal · Drafted opening line
[Card 2: Stakeholders] Names · Roles · Last touch · Our read
[Card 3: Must-cover topics] 3–5 bullets · Why each matters here
[Card 4: Expected objections] Each with a reframe and a quoted basis
[Card 5: Watch for] Risk · How to handle live

[Drill-down (optional)] Last 3 calls quoted · Full stakeholder map · Deal MEDDPICC
```

# Optional outputs

- **Notion** — if the rep asks to persist the brief, create a page under the account's coaching/deal page.
- **Slack draft** — if a teammate is joining, draft a Slack handoff brief for them.

# Rules

- **Under 600 words in the rendered widget.** This is a brief, not a report.
- **No placeholders.** Real names, real prior context, real quotes.
- **Every objection response is a sendable line** the rep could actually say.
- **The "Lead with" line is non-negotiable** — find a specific, prior-context-referencing opener even if you have to dig.
- **If data is thin** (first meeting, no prior calls), say so plainly and switch to first-principles prep: research the account via `ask_anything_on_account` or, if no Modjo data exists, suggest a quick LinkedIn pass and offer to redo prep with that.
- **Never invent stakeholder positions or buyer quotes.** If you don't know where someone stands, say "position unknown."
- **Names** come from `get_deals.contacts` or `get_contacts` lookup — never from the calendar event email alone. If a contact is labelled "Billing Contact" in CRM but has a real name elsewhere on the same deal, use the real name.
- **Multiple Decision Makers is not a typo** — if CRM has 3 DMs, that's a real political question. Surface it as a topic for the meeting rather than picking one arbitrarily.
