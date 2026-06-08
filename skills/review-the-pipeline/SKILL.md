---
name: review-the-pipeline
description: Weekly portfolio triage — hot/watch/at-risk/disqualify buckets, hygiene flags, a recommended action per material deal. Works standalone with rep-listed deals; supercharged with conversation intelligence agents and CRM. Use for 'pipeline review', 'weekly triage', 'what needs my time'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are running a weekly pipeline review with the rep — or the rep is reviewing their own. The job is hard prioritization: which deals get attention, which get disqualified, which need help from the manager. Honest scoring beats optimistic stacking.

# What I need from you

- **Minimum**: your name, OR a pasted list of open deals (name, amount, stage, close date). With paste-in only, I'll triage by stage and date logic.
- **Better**: CRM access to your open book so I can pull the live state without you typing it.
- **Best**: all of the above plus a conversation-intelligence platform so I can rank by deal *health* (recent activity, sentiment, MEDDPICC pillar gaps) rather than just stage and date.

I'll never silently drop deals — every open deal on your book is either in a triage bucket (hot/watch/at-risk/disqualify) or explicitly flagged as "ambiguous, needs your call".

# Inputs

1. **IC** — default to running user. `find_user` (e.g. Modjo `get_users`) → `userId`.
2. **Window** — default: deals with closeDate in the current quarter + any open deal past closeDate. Override if rep names a different window.
3. **Mode** — IC self-review (default) or manager-led review of a specific rep (changes tone and adds manager-action items).

# Load before running

- `../../shared/qualification-rubric.md`
- `../../shared/coaching-themes.md`
- `../../shared/output-modes.md` — Live brief default; optional Notion log for the manager-led case
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull

**CRM ID gotcha**: use exact `crmId` from `get_deals` — Modjo customers use various CRMs (Salesforce, HubSpot, Pipedrive, others) and surface the underlying CRM's exact ID. Never reconstruct prefixes.

1. **Open deals owned by IC** — `get_deals` filters.status=["Open"], owner.ids=[userId], limit 50. Capture amount, closeDate, source, stage, contacts.

2. **Activity recency — one batched call, not per-deal** — `get_calls` with `userIds=[userId]`, `dateRange=last 30 days`, `limit=50`. Then join client-side: for each deal, find the most recent call by checking call summaries / dealId / accountCrmId. This is 1 tool call instead of 15.

3. **MEDDPICC scoring — strict budget** — run Deal Challenger via `ask_anything_on_deal` on **at most 3 deals**: the top commit, the highest at-risk, one closing this month. Skip the rest entirely — don't even score "lighter from summaries." A pipeline review doesn't need MEDDPICC on 50 deals; it needs honest triage on all 50 and deep scoring on the 3 that matter.

4. **CRM hygiene scan — run before triage** — for each open deal:
   - **Amount mismatch**: scan call summaries (already loaded) for mentions of stated budget or true scope. If CRM amount is < 30% of stated budget, flag the deal. List these at the top of the review — they're the single biggest source of forecast distortion.
   - **Past closeDate + still Open**: flag, but subdivide:
     - Material (≥ €500 ARR + recent activity within 30d) → "at risk, needs reset"
     - Stale (< €500 ARR OR no activity 60d+) → "CRM cleanup — close-lost or update date"
   - **Long-dated renewals** (deal name contains "Renewal" or "Contract Change," closeDate matches the renewal cycle) → "renewal placeholders, not active forecast" — filter out of triage entirely.
   - **Far-future new deals** (deal name is "New Deal," closeDate > 12 months out) → **flag, don't filter** — these are usually fake dates set to keep dead deals open. Surface as candidates for audit-the-forecast cleanup or disqualification. Different from renewal placeholders.
   - **Stage stagnation** > 60 days in same stage (if `stageChangedAt` is available) → flag.

5. **Prior pipeline review** (carryover) — `workspace_search` (e.g. Notion `notion-search`) query=`"[IC] pipeline review"` → fetch the most recent. Carry over any deal flagged disqualify-candidate or at-risk that's still open. A second-time flag is more urgent than a first-time flag.

# Triage logic — runs on the filtered pool, not the raw 50

Triage only the deals that remain after hygiene filtering:
- Renewals dated > 9 months out → excluded (placeholder bucket)
- Sub-€500 past-close stale deals → excluded (CRM cleanup bucket)

Score each remaining deal on three axes:

1. **Conviction** — qualification depth (MEDDPICC total if scored, plus signals from recent calls).
2. **Momentum** — buyer-initiated activity in last 14 days, stage progression vs static.
3. **Materiality** — **true scope ARR** (use the true budget from hygiene scan, not the CRM amount if mismatched) + strategic value.

Bucket:
- 🔴 **At risk** — overdue + material, or stalled (>21 days no activity) on a deal we need this quarter
- 🟠 **Watch** — slowing momentum, mid conviction, material
- 🟢 **Hot** — high conviction + momentum + material, just keep the rhythm
- ⚫ **Disqualify candidate** — low conviction + low momentum + past/near close date (and material enough to justify the disqualify decision rather than CRM cleanup)

**Quarter-end weighting**: if today is in the last 30 days of the quarter, deals closing this quarter outrank deals closing next quarter at every materiality level.

# Output — Live brief (widget)

`show_widget` with `title="pipeline_review_[ic-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Pipeline value (CRM total, **true-scope adjusted total**, weighted), # deals after filtering, # past close date, # at risk, this-week wins. Show the gap if true-scope > CRM: "your CRM understates pipeline by €X across N deals."

### CRM hygiene flags — surface first
- Amount mismatches (N deals, €Y understated)
- Past-close stale debt (N deals to close-lost or update)
- Renewal placeholders excluded (N deals, €Y — for context only)
- Stage stagnations > 60d

### The week's verdict — one sentence
The single most important thing about this pipeline state right now.

### At risk (🔴) — disqualify or rescue this week
Card per deal: name, ARR, days inactive, why it's red, and a single specific action (disqualify / book the unstick call / escalate to manager). Drafted action where possible.

### Hot (🟢) — protect the momentum
Card per deal: name, ARR, what's working, what to keep doing. Don't over-engineer wins.

### Watch (🟠) — give it one more cycle
Card per deal: name, ARR, the specific signal we're watching for + the date we'll re-decide.

### Disqualify candidates (⚫)
Compact list (not full cards) — name, ARR, days inactive, one-line reason. Force a triage choice.

### Pipeline shape
Brief stats: how the bucket distribution compares to a healthy shape for this rep's role/segment. Surface dependencies (e.g. "60% of forecast in 2 deals — concentration risk").

### Recommended focus this week
Top 3 deals to spend most time on, in order. Why each.

## Example skeleton

```text
[Header] Pipeline value: [€X] · N deals · N past close · N at risk · Week wins: N

[Verdict] One sentence — the most important thing about this pipeline state.

[Card 1: At risk (🔴)] Top deal · ARR · Why · Drafted unstick move
[Card 2: Hot (🟢)] Top deal · ARR · What to protect
[Card 3: Hygiene flags] Top 3 findings · €impact each
[Card 4: Recommended focus this week] Top 3 deals · Why each, ranked

[Drill-down (optional)] Full bucket lists · Disqualify candidates · Pipeline-shape stats
```

# Optional outputs

- **Notion** — write the review to the rep's coaching page (manager-led mode default).
- **Slack draft** — for the rep to share the at-risk list with manager and ask for help.

# Rules

- **Disqualifications are part of the review, not a side note.** Surface them clearly.
- **MEDDPICC scoring budget = 3 deals.** Don't burn tool calls on a 50-deal pipeline.
- **Conviction signals come from real data** — recent buyer-initiated touches, mapped stakeholders, quoted commitments. Not stage labels.
- **Don't assert a clean bill you can't verify.** Statements like "0 past close" or "nothing overdue" are claims — only make them if you actually checked close dates/activity for the deals in question. If call-recency or data is limited, say "no overdue deals found in the data checked" — never present an unverified clean status as fact.
- **Silent / auto-dated deals get triaged, not hidden.** Deals with no recent activity and a suspicious auto-set close date must each land in a bucket or be explicitly flagged "ambiguous — needs rep confirmation." Do not aggregate them into a single "CRM hygiene" line that lets ~25 real deals disappear from the review.
- **Concentration risk matters** — if 60%+ of forecast sits in 1–2 deals, flag it.
- **Under 1000 words in the widget.**
- **Manager-led mode is not just gentler in tone** — it surfaces only the top 5 deals that matter for this rep this week + one explicit "what does the rep need from you" section. A 50-deal triage is for the IC; a manager wants the high-leverage subset.
- **Disqualify-second-time-flagged deals are urgent.** If a deal was flagged disqualify-candidate last review and is still open, surface it above the standard at-risk bucket.
