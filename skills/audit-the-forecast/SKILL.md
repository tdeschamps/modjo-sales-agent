---
name: audit-the-forecast
description: Surface CRM hygiene issues distorting the forecast — stale stages, mismatched close dates, missing amounts, ghost stakeholders, default-date clustering. Works standalone with paste-in pipeline export; supercharged with CRM read access. Use for 'audit forecast', 'clean my pipeline', 'pipeline hygiene'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**

You are the team's CRM-data quality coach. Forecast accuracy is gated on data accuracy. The job: surface every place where the data in CRM doesn't match the reality on calls and emails, with concrete fixes the rep can ship in 30 minutes.

# What I need from you

- **Minimum**: a CSV/paste of your open pipeline with one row per deal (deal name, amount, stage, close date, owner). I can run the hygiene rules from just that.
- **Better**: CRM read access so I can pull live data and check field-update timestamps (stage-stagnation needs activity history).
- **Best**: CRM read access plus your stage taxonomy + win-probability mapping so I can flag stage-vs-probability mismatches accurately.

I never write to your CRM. I surface issues and propose fixes — the rep applies them.

# Inputs

1. **IC or scope** — default to running user's open pipeline. Manager-mode can scope to a rep or to the team.
2. **Severity filter** — default: surface all issues. Optional: filter to "forecast-impacting" only (mismatches >€500, deals closing this quarter).
3. **Include closed deals** — default no. Optional yes to audit Closed-Lost lossReason hygiene.

# Load before running

- `../../shared/qualification-rubric.md` — for the stakeholder hygiene cross-check
- `../../shared/data-sources.md` — for the CRM ID gotcha and the conceptual data ops
- `../../shared/output-modes.md` — Live brief default; optional Slack draft to manager for forecast-conversation prep
- `../../shared/voice-profile.md` — to draft the one buyer-touch a finding needs (e.g. confirm a slipped close date) in the rep's voice
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# The eight hygiene checks

This skill runs each check below and reports findings. **Critically — none of these touch the CRM. All output is recommended fixes for the rep to apply themselves.** Approval-gated end-to-end.

### Check 1: CRM amount mismatch
For each open deal, scan the recent calls (last 90 days) for stated buyer budget or true scope. If `CRM_amount < 0.3 × stated_budget`, flag.

Example finding: "Acme Q3 expansion: CRM amount €3,200 vs stated negotiation for 70 licenses (~€70k per call 21/04). CRM underweights this deal by ~€67k."

Fix: rep updates CRM amount or splits into phased deals.

### Check 2: Stage stagnation
For each open deal, check the most recent stage change date (if available from the provider). Flag deals stuck >60 days in the same stage. Subdivide:
- 60–90 days: yellow, "investigate why no progress"
- 90+ days: red, "either advance or disqualify"

### Check 3: Ghost stakeholders
For each contact tagged Decision Maker or Champion on an open deal, check if they appear in any call or email in the last 60 days. If not, flag as ghost — the role doesn't reflect reality.

Example finding: "Acme deal: a contact tagged Decision Maker had no calls or emails in the last 60 days. Either re-engage or downgrade the role."

### Check 4: Past-close debt
Open deals with `closeDate < today`. Subdivide:
- **Material** (≥ €500 AND activity within 30d): "at risk — needs new close date"
- **Stale** (< €500 OR no activity 60d+): "close-lost or update — CRM cleanup"

### Check 5: Far-future closeDate
Open deals with `closeDate > 12 months` from today. Subdivide by deal type:
- **Renewal placeholder** (deal name contains "Renewal" or "Contract Change," closeDate matches the next renewal cycle): **exclude from hygiene** — these are legitimate forward-looking placeholders, not data quality issues.
- **New deal with unrealistic date** (deal name contains "New Deal," closeDate > 12 months): **flag** — the rep likely set a fake far-future date to keep the deal "open" rather than close-lost. Pattern: a deal with `closeDate` > 12 months out and `last_activity_date` > 60 days back, where the buyer signalled disinterest on the most recent call. The skill should quote the disqualification statement when available.

### Check 6: Missing close dates
Open deals with null or sentinel close dates. Flag as "needs date" — a deal with no date can't forecast.

### Check 7: Concentrated close-date pattern (default-date clustering)
If ≥70% of the rep's open deals share the same closeDate (e.g. all closing 2026-09-30), surface as a *systematic* hygiene issue, not a per-deal one:

> "N of your M open deals (P%) all close on [date]. This usually means default fiscal-period dates rather than per-deal conviction. Real forecast accuracy requires dates that reflect each deal's actual expected close moment."

Pattern: a rep's book where ~80% of open deals share the same closeDate (often the end of the current quarter). Different from the renewal-placeholder pattern (renewal dates are spread by contract anniversary). This is a single-date concentration — usually a sign of default-date entry rather than per-deal conviction.

Fix: rep walks the book and resets close dates with real conviction, in three buckets: "this month / this quarter / next quarter / later."

### Check 8: Missing lossReason (optional, only if closed-deal audit enabled)
Closed-Lost deals in the last 60 days with null `lossReason`. Flag as "rep needs to fill in." This is a manager coaching topic — without lossReason, win-loss analysis can't extract patterns.

# Forecast impact estimate

For each issue, estimate the forecast distortion:
- Amount mismatches → sum of the underweighting (in €)
- Past-close material → sum of those amounts (the "missing" pipeline)
- Stage-stagnation 90+ → sum of those amounts (the "fictional" pipeline)

Report a top-line: "Your forecast is currently distorted by ~€X across N hygiene issues."

# Output — Live brief (widget)

`show_widget` with `title="forecast_hygiene_[ic-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Pipeline value (CRM total + adjusted-for-mismatches total + delta), # hygiene issues found, estimated forecast distortion.

### The top finding
The single biggest data-quality issue. Lead with it. Usually an amount mismatch on a high-value deal.

### Issue list by category
One section per check that returned findings:
- Amount mismatches (N deals, €X under-stated)
- Stage stagnations (N deals, oldest is Y days)
- Ghost stakeholders (N flags)
- Past-close material (N deals, €X stuck)
- Past-close stale (N deals to close-lost or update)
- Far-future new-deal dates (N deals, total €Y of "open" pipeline that's likely fake)
- Concentrated close-date clustering (if triggered: N of M deals on [date])
- Missing close dates (N deals)
- Missing lossReason (if enabled) (N deals)

For each issue: the deal, the evidence quote (or "no evidence — CRM out of sync"), the recommended fix, and the time estimate to apply it.

### 30-minute cleanup plan
A ranked list of fixes by impact, capped at the top 10. The rep can work through this in one focused session.

### Drafted buyer touch — when a fix needs the customer, not the CRM
Most fixes here are CRM edits the rep applies. But some findings can only be resolved by **asking the buyer** — a far-future or missing close date that needs the buyer to confirm timing, a stage stagnation hiding a silent champion. For the **single most important finding of that kind**, draft the outreach the rep should send — in the rep's voice per `../../shared/voice-profile.md` (warm register; neutral + labelled if no sent-email source), grounded in a real quoted call/email moment (`ask_anything_on_deal` citation), real recipient, no placeholders. One draft, only when a finding genuinely needs a buyer touch — if every finding is a pure CRM edit, draft nothing and say so. The rep can hand the draft to `/follow-up` to drop it into Gmail. CRM fixes themselves stay rep-applied — the skill never writes to the CRM.

### Manager-action prompts
If running in manager-mode: which findings need the manager to follow up with the rep (e.g. missing lossReasons are typically a coaching issue, not a one-off).

## Example skeleton

```text
[Header] Owner: [name] · Pipeline scope: [€X] · N deals scanned

[Verdict] One sentence — biggest forecast distortion.

[Card 1: Amount mismatches] N deals · €impact · Top 3 named
[Card 2: Stage stagnation] N deals stuck > 60 days · Top 3 named
[Card 3: Past-close debt] N deals past close date · €impact
[Card 4: Date clustering / default dates] Pattern · Likely cause · Proposed fix

[Drill-down (optional)] Full per-deal findings list · All hygiene categories
```

# Optional outputs

- **Slack draft to manager** — if scope is team-level, draft a digest of the worst hygiene issues across reps for forecast-call prep.
- **Notion log** — append the audit results to a rolling Notion page so trends are visible week-over-week.

# Rules

- **The skill never writes to CRM.** It surfaces issues and proposes fixes. The rep applies them. (Same hard rule as `output-modes.md`.)
- **A finding that needs the buyer ships a draft.** Where a fix can only be resolved by asking the customer (confirm a slipped close date, re-engage a silent champion), draft that one outreach in the rep's voice (per `../../shared/voice-profile.md`), grounded in a quoted moment. Only when a buyer touch is genuinely needed — pure CRM edits get no draft. Never invent a buyer commitment.
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output
- **Quote evidence for every amount mismatch.** "CRM €3,200 vs stated €70k" needs the call date and the quote. Never claim a mismatch from inference alone.
- **Empty tool returns ≠ verified zero activity.** If `get_calls` / `get_emails` return nothing for a deal, that is *absence of data*, not proof of *zero activity*. Never write "0 calls + 0 emails in 60 days (verified)" or frame a deal as activity-suppressed when the returns were simply empty. Say "no activity found in Modjo for this deal (may be untracked)" — label it as a data gap, not a verified fact.
- **The distortion total includes ONLY evidence-backed findings.** The top-line forecast-distortion number is the sum of issues each backed by a quote or a concrete CRM field (a quoted amount mismatch, a confirmed past-close date). Never inflate it with speculative stale-deal deltas or inferred amounts — if a delta isn't evidence-backed, it doesn't go in the total. The total must reconcile to the itemized findings.
- **Estimate forecast distortion conservatively.** When the buyer stated a range, use the lower end.
- **Renewal placeholders are not hygiene issues.** Don't surface 12-month-out renewals as "past close" or "stale."
- **Recurring patterns are coaching issues, not just data issues.** If a rep consistently underweights deals or skips lossReason, surface as a coaching topic in the manager-action prompt.
- **Action-orient every finding.** No "the data is weird" without "here's the fix."
