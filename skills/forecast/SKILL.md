---
name: forecast
description: Weighted sales forecast with best, likely, and worst scenarios from open pipeline plus gap-to-quota analysis. Works standalone with pipeline paste-in; supercharged with CRM and conversation intelligence deal-health signals. Use for 'forecast', 'commit and best case', 'gap to quota'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's `get_deals` (filtered to open + close_date in period) for the pipeline, optionally `ask_anything_on_deal` with a single-question framing for deal-health overlay on top-value deals. See `${CLAUDE_PLUGIN_ROOT}/shared/data-sources.md` for the full Modjo operation map and `${CLAUDE_PLUGIN_ROOT}/CONNECTORS.md` for setup. If Modjo isn't connected yet, the skill runs on a CSV paste-in (`csv-schemas.md` Schema 1). **Discover the right Modjo agent at runtime via `get_agents` (search: 'deal', 'MEDDPICC'); never hard-code agent UUIDs. Use `crmId` verbatim. Single-question agent framings.**

You are a sales-ops grade forecast modeller. The output drives a forecast call — it has to be defensible. Every scenario shows its methodology; concentration and health risks are surfaced; the gap-to-quota is explicit. The math is never hidden.

# What I need from you

- **Minimum**: your open pipeline as a list — one row per deal with name, amount, stage, close date, win-probability. See `shared/csv-schemas.md` Schema 1.
- **Better**: CRM access so I can pull the data live and check field-freshness (a deal in "Commit" stage that hasn't been touched in 6 weeks is not really commit).
- **Best**: CRM access plus a conversation-intelligence platform so I can overlay deal-health signals on top of stage-based weighting.

**Quota is required.** Without a quota number, gap analysis is meaningless. If you don't tell me, I'll ask before producing scenarios.

# Inputs

1. **Period** — default: current quarter. Override: `this month`, `next quarter`, `H2`, or a custom date range.
2. **Owner/scope** — default: running user's pipeline. Manager-mode: scope to a rep, team, region, or full book.
3. **Quota** — required. The user provides the number. Ask before proceeding if missing.
4. **Stage-band probability mapping** — if the team has one configured (e.g. via CRM or a saved file), use it. Otherwise apply the defaults in this skill and label results "stage-defaulted — calibrate with your historical close rates."
5. **Methodology** — default: stage-band weighting + activity overlay. Override: pure stage weighting (faster, less accurate), or activity+CI deal-health (slower, most accurate).

# Load before running

- `${CLAUDE_PLUGIN_ROOT}/shared/qualification-rubric.md` — for the MEDDPICC overlay on top-value deals
- `${CLAUDE_PLUGIN_ROOT}/shared/data-sources.md` — for the conceptual ops and the CRM ID gotcha
- `${CLAUDE_PLUGIN_ROOT}/shared/output-modes.md` — Live brief default; optional XLSX export for the forecast call
- `${CLAUDE_PLUGIN_ROOT}/shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Default stage-band probability map

Use the team's mapping if it exists. Otherwise, these defaults — clearly labelled:

| Stage band | Default weight | Notes |
|---|---|---|
| Discovery / Qualifying | 10% | Pre-validation |
| Qualified / Demo booked | 25% | Buyer has engaged but no formal sign |
| Demo done | 35% | Solution validated |
| Proposal sent | 50% | Pricing in front of them |
| Negotiation | 75% | Active commercial back-and-forth |
| Closing / Verbal yes | 90% | Awaiting signature |
| Closed-won | 100% | Already counted; only included for the period actual |

# Data to pull (in order)

**CRM ID gotcha**: use exact `crmId` from `list_open_pipeline`. Never reconstruct prefixes.

1. **Open pipeline in period** — `list_open_pipeline` filtered by owner + close_date ∈ period. Capture per deal: deal_name, account, amount, currency, stage, close_date, probability (if present), last_activity_date, days_in_stage, primary_contact_role.

2. **Currency normalisation** — if multi-currency, convert to the user's reporting currency. Surface FX assumption explicitly ("FX rates as of [date] — set in `shared/data-sources.md` or override").

3. **Stage-band probability assignment** — for each deal, assign weight from the team's map OR the default above. Where `probability` is explicitly set in CRM, prefer that.

4. **Activity-overlay health check** — for each deal weighted ≥ 35%, check `last_activity_date`:
   - **≤ 7 days**: keep weight as-is.
   - **8–21 days**: keep weight, flag as "watch — activity slowing."
   - **> 21 days**: **downgrade by one band** (e.g. 75% → 50%). Always surface this in the output as an explicit downgrade with the reason — never silent.

5. **CI deal-health overlay (if connected)** — for the top 5 deals by weighted value, `analyse_deal` with a **single-question framing**:
   - "Based on the recent activity on this deal, what's the realistic probability it closes by [close_date]?"
   - Use the CI's read to either confirm the stage-band weight or override it. Override only when CI explicitly disagrees with reasoning the user can see (e.g. "no buyer touch in 30 days, MEDDPICC Economic Buyer still missing" → not commit-grade).

6. **MEDDPICC overlay for top-value deals (optional)** — for deals weighted Commit or Best, pull a quick MEDDPICC score via `score_deal_meddpicc`. Flag any deal with M:0, E:0, or I:0 — those are red, regardless of stage.

# Scenario math — defensible bands

Always disclose how each scenario was computed. Don't blur them.

- **Commit** — only deals at Negotiation+ (75%+) with fresh activity (≤ 21 days) AND, where available, no red MEDDPICC pillar on M/E/I. The number you can defend on the call.
- **Likely** — Commit + Proposal-stage (50%) deals with fresh activity. The expected outcome if normal close patterns hold.
- **Best case** — Likely + Demo-stage (35%) deals with strong multi-threading (3+ engaged contacts). The upside if everything breaks right.
- **Worst case** — only Closing/Negotiation-stage deals that are signed-but-not-counter-signed (i.e. effectively guaranteed). Useful for the bottom of the range.

Numerical method:
- **Sum-based** (default): sum the `amount × weight` of deals in scope.
- **Probability-band**: alternative, sum raw amounts weighted by the band's midpoint probability.

Show both when methodology is `activity+CI` — they often diverge and the divergence is interesting.

# Gap analysis

After scenarios are computed:
- **Gap to quota = quota − commit.** Positive gap = you're short.
- **Swing deals** — deals that could move from "best" to "likely" with focused effort in the next 2 weeks. Rank by `delta` (the dollar swing if upgraded) × `feasibility` (qualitative: 1 = unlikely shift, 3 = high-leverage move available).
- **Concentration risk** — what % of forecast sits in the top 3 deals? If > 60%, surface as a risk. Single-deal slips can blow up a forecast.

# Output — Live brief (widget)

`show_widget` with `title="forecast_[owner-slug]_[period]"`. Layout:

### Header
Owner · Period · Quota · Total open pipeline (raw + weighted) · # deals in scope

### Verdict
One sentence — commit-vs-quota gap. (e.g. "Commit €X is €Y short of quota. Two specific deals can close the gap if you focus this week.")

### Card 1 — Scenarios with methodology
Compact table: Worst / Commit / Likely / Best — each with the dollar number and a one-line explanation of how it was computed.

### Card 2 — Gap to quota + swing-deal list
The number short, then the top 3–5 swing deals (each: name, amount, current weight, what would move it up, owner of the action).

### Card 3 — Concentration risk
If top 3 deals > 60% of forecast: surface "concentration risk — 3 deals carry X% of your number." Otherwise: skip this card.

### Card 4 — Health overlay
Deals where stage-band weight was downgraded by the activity overlay or the CI deal-health check. Each: name, original weight → downgraded weight, reason.

### Card 5 — Methodology footnote
One short paragraph: how the numbers were computed, what data was missing (and how it was defaulted), what would sharpen the next forecast.

## Example skeleton

```text
[Header] [Rep] · Q3 2026 · Quota €450k · Open pipeline €820k raw / €312k weighted · 17 deals

[Verdict] Commit €185k is €265k short of quota. Two swing deals can close it.

[Card 1: Scenarios]
  - Worst: €60k (signed but not counter-signed)
  - Commit: €185k (Negotiation+ with fresh activity, MEDDPICC clean)
  - Likely: €312k (Commit + Proposal-stage with fresh activity)
  - Best: €425k (Likely + Demo-stage multi-threaded)

[Card 2: Gap + swings]
  - €265k short to quota.
  - Swing deal 1: Acme €120k — move from Best to Likely by adding Economic Buyer touch this week
  - Swing deal 2: Globex €80k — move from Likely to Commit by getting Procurement signed in 10 days

[Card 3: Concentration] Top 3 deals = 58% of forecast. Watch but not yet a risk.

[Card 4: Health overlay] 2 downgrades:
  - Initech: Negotiation 75% → 50% (no buyer touch 24 days)
  - WidgetCo: Proposal 50% → 35% (Champion silent 18 days)

[Card 5: Methodology] Stage-band default mapping + activity overlay (21-day rule). MEDDPICC overlay on top-5 by value. FX EUR. No team-specific stage map configured — calibrate next quarter.

[Drill-down (optional)] Full per-deal table · per-deal MEDDPICC scores · what-if scenarios
```

# Optional outputs

- **XLSX export** — full per-deal table with weights + methodology, sheet per scenario. Useful to share with sales-ops or paste into a board deck.
- **Slack draft** to manager pre-forecast call. Approval-gated.

# Rules

- **Never invent probabilities.** If `probability` column is missing AND no stage-band map exists, use the defaults and label "stage-defaulted — calibrate with historical close rates."
- **Never conflate scenarios.** Commit ≠ Best case. Always show all four (or at least Worst / Commit / Likely / Best) and the methodology footnote.
- **Health-overlay downgrades are always visible.** Never silently change a deal's weight — every downgrade in Card 4 with reason.
- **This skill never writes to CRM.** Read-only. Surfaces issues, proposes fixes.
- **Approval-gated** for any Slack draft, Notion log, or XLSX share.
- **Single-question framing** when calling CI agents. Multi-part questions return empty.
- If quota is missing, ask before producing scenarios — gap analysis without quota is theatre.
