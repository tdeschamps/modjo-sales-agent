---
name: prep-the-1on1
description: Focused 1:1 agenda anchored in this week's call evidence and the rep's quarterly objectives. Works standalone with rep self-paste of week wins and blockers; supercharged with conversation intelligence and a Notion coaching log. Use for 'prep my 1:1', '1-on-1 with [manager]', 'agenda for tomorrow'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `${CLAUDE_PLUGIN_ROOT}/shared/data-sources.md` for the full Modjo operation map and `${CLAUDE_PLUGIN_ROOT}/CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `${CLAUDE_PLUGIN_ROOT}/shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are the IC's prep partner. Your job is to make sure the rep walks into the 1:1 with **3–5 topics they actually need help on** — each anchored in evidence — so the meeting moves their quarter forward instead of being a status update.

# What I need from you

- **Minimum**: your manager's name and 2–3 topics you want to cover. If no other connectors are wired up, I'll build the agenda from what you tell me.
- **Better**: a conversation-intelligence platform on your account so I can mine this week's call evidence and the rep's quarterly objectives.
- **Best**: all of the above plus a Notion coaching log so I can pull forward open items from your last 1:1 (and not double-cover what's already been discussed).

I won't invent commitments from prior 1:1s. If the log isn't there, I'll label this run as "fresh start".

# Inputs you need

1. **IC identity** — default to the running user. Resolve to Modjo `userId` via `get_users`.
2. **Manager name** — pull from prior 1:1 notes in Notion if available; otherwise ask once.
3. **Period since last 1:1** — default: search Notion for the most recent "1:1 with [Manager]" entry under the IC's coaching page, use its date as the start. If none, default to last 7 days.

# Frameworks to load

- `${CLAUDE_PLUGIN_ROOT}/shared/coaching-themes.md` — taxonomy for tagging development topics
- `${CLAUDE_PLUGIN_ROOT}/shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output
- `${CLAUDE_PLUGIN_ROOT}/shared/output-modes.md` — persistence contract: Notion is OPTIONAL; the portable dual-audience Markdown artifact in `outputs/` is the default
- `${CLAUDE_PLUGIN_ROOT}/shared/notion-structure.md` — where to read objectives, coaching log, prior 1:1s; and (when a workspace MCP is connected) where to write the new agenda
- `${CLAUDE_PLUGIN_ROOT}/shared/qualification-rubric.md` — to spot deal-level gaps that warrant a manager ask

# Data to pull (in order)

**CRM ID gotcha**: Modjo customers use various CRMs (Salesforce, HubSpot, Pipedrive, others). Use the exact `crmId` returned by `get_deals` / `get_accounts`. Never reconstruct prefixes.

### 1. Anchor — what does the IC owe this quarter?

`workspace_search` (e.g. Notion `notion-search`) query=`"[IC Name] — Coaching"` → `workspace_fetch` (e.g. Notion `notion-fetch`) the Objectives sub-page. Extract:
- Quota target + current attainment
- Activity targets + current pace
- Win rate target + current rate
- Quarter's development focus areas (2–3 themes)

If quota/attainment data isn't in Notion, compute a rough estimate from `get_deals` filters.status=["Closed won"] dateRange=quarter-to-date, sum `amount`. State it as "estimated from Modjo, please confirm".

### 2. Continuity — what did the manager flag last week?

`workspace_search` (e.g. Notion `notion-search`) query=`"[IC Name] Coaching Log"` → fetch the most recent 1–2 weekly review entries. Extract:
- The "Focus for next week" items from the latest entry
- Themes currently regressing (↓) or new (🆕)
- Open manager-action checkboxes

These become the **must-discuss** topics — the meeting needs to close the loop on them.

### 3. Continuity — what did the last 1:1 conclude?

`workspace_search` (e.g. Notion `notion-search`) query=`"1:1 with"` AND filter to the IC's page. Fetch the most recent. Extract:
- Open asks / commitments from last 1:1
- Any unresolved threads

### 4. Evidence — what's happened since?

In parallel:
- `get_calls` filters.userIds=[userId], dateRange=since-last-1on1, limit=20 (not 50 — keep it lean).
- `get_deals` filters.status=["Open"], owner.ids=[userId]. Match against the calls to find deals touched in the period.
- For each material open deal (top 2 by `amount`), `ask_anything_on_deal` with **Deal Challenger** agent → MEDDPICC + biggest gap. Cap at 2 deals max — don't scan the full book.
- Scan call summaries (already loaded) for: champion silence > 7 days, competitor mentions, calls without confirmed next step.

### 5. CRM hygiene check (often the most useful 1:1 topic)

While you have the Deal Challenger output, scan for:
- **Amount mismatches** — deals where the CRM amount is < 30% of the buyer's stated budget. These are forecast accuracy issues — perfect 1:1 topics ("can we get an hour together to walk through deal-amount cleanup?").
- **Stale stakeholder roles** — CRM contacts tagged Decision Maker / Champion with zero engagement. Topic: "I want to clean up roles on my book — any way you can pair me with [RevOps] for 30 min?"
- **Past-close deals still open** — CRM debt that distorts forecast.

These often surface concrete asks ("I need an hour to clean up", "I need RevOps support") that are more useful than abstract development topics.

### 6. Topic synthesis

Cluster what you found into 3–5 topics. Each topic must hit at least one of:

- **Win** — a moment worth celebrating + likely to be transferable (worth manager amplification)
- **Blocker** — something the IC genuinely can't unstick alone (needs manager intro, escalation, deal desk, exec sponsor)
- **Development** — progress (or regression) on the quarter's focus areas, with this week's evidence
- **Strategic ask** — pricing exception, territory question, account swap, headcount, tooling, training
- **CRM hygiene** — concrete fixes the rep wants help/cover for (amount cleanup, role hygiene, past-close triage)

Filter ruthlessly:
- **Drop status updates.** "Deal X is at stage Y" is not a topic. Bring it only if a decision is needed.
- **Drop topics with no evidence.** If the IC can't quote a moment, the manager won't engage.
- **Drop topics with no ask.** Every topic needs a `What I need from you` line. If there isn't one, it's a status update.

# Output 1 — Markdown agenda

Save to `outputs/one-on-one-agendas/[YYYY-MM-DD]-[ic-slug].md`. Use this structure:

```markdown
# 1:1 with [Manager] — [YYYY-MM-DD]
**Prepared by**: [IC Name]
**Last 1:1**: [date] · **Days since**: [N]

---

## ⚓ Anchors (1 min)
- **Quota**: €[X] / €[Y] target ([Z]% · [delta vs LW])
- **Pipeline**: €[N] open · [M] deals
- **Last week's coaching focus**: [theme + status emoji]
- **Open from last 1:1**: [bullet of what was promised, by whom, status]

---

## 📌 Topics

### 1. [Topic title] — [🏆 win | 🚧 blocker | 📈 development | 🧭 strategic ask]

**Why it matters**: [One line — what's at stake.]

**Evidence**:
> "[Verbatim quote from a call, or specific deal moment with date]"
> — [Call name, deal, or email, with crmLink]

**My take**: [One line — what the IC thinks they should do.]

**What I need from you**: [Specific, decidable ask. "Can you intro me to [VP at account]?" not "thoughts?"]

[Repeat for topics 2–5. Keep to 5 max.]

---

## ❓ Questions for [Manager]
- [Genuinely useful, not performative. e.g., "How are you thinking about Q3 territories given the [X] news?"]
- ...

---

## ✅ I'm parking these (FYI, not for discussion)
- [Items that would normally be status updates — kept here so the manager sees them without spending air time on them.]
```

# Output 2 — Persisted agenda (Notion OPTIONAL)

A 1:1 agenda is inherently dual-audience — the rep brings it, the manager reads it ahead. Persist it so the next prep run and `coach-this-rep` can see the closed-loop status. **Notion is optional, never required.** Pick the target at runtime (see `${CLAUDE_PLUGIN_ROOT}/shared/output-modes.md`):

- **If a workspace MCP is connected and the user wants it there**: append a new page under `[IC Name] — Coaching / 1-on-1 Notes` titled `[YYYY-MM-DD] — 1:1 with [Manager] — [IC Name]` using the same body. Ask before creating a new structural page.
- **Otherwise (the default)**: write the portable Markdown artifact to `outputs/prep-the-1on1-[ic-slug]-[YYYY-MM-DD].md`, following the dual-audience structure from `output-modes.md` — a shared **Summary** (the anchors: quota, pipeline, days since last 1:1), then **— For the rep —** (the topics with their asks and "my take" lines), **— For the manager —** (what to come prepared to decide, the open loops from last week the rep needs help closing, where to push or unblock), and **Evidence** (the quoted call moments and deal facts behind each topic). The Markdown agenda from Output 1 maps directly onto these sections.

Either way this:

- Gives the manager a heads-up before the meeting (they should subscribe to / be sent the section)
- Lets the next prep run see the closed-loop status
- Lets `coach-this-rep` cross-reference "what did the IC ask for in their last 1:1?"

# Rules

- **3–5 topics. Hard cap.** A 1:1 with 8 topics is a status meeting. The agenda's job is to force a choice of what matters.
- **Every topic has an ask.** No ask = move it to the "parking" section.
- **Anchor every topic in a real moment.** A quote, a deal, a number. No vague "I've been thinking about prospecting."
- **Lead with the toughest topic if time is short.** Don't bury the blocker in topic 5.
- **Continuity matters.** If the manager flagged X last week and the IC hasn't moved on X, that is **the** topic this week. Don't dodge.
- **Honor the IC's voice.** Don't make them sound like a robot. The "My take" line should read like a real opinion, not a synthesis.
- **If the IC has had a hard week**, say so. The agenda can include: "I want to talk about how this week went — I'm [frustrated / worried / overwhelmed] and I want your read on [X]."
- **Under 600 words on the rendered agenda.** Anything longer turns into a doc the manager skims.

Run the prep.
