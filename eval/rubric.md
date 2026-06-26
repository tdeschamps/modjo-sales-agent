# Grading rubric — Modjo Sales Agent

The standard a skill output has to clear to be considered "working." Six dimensions, each scored 0 / 1 / 2. Maximum 12.

**Pass threshold**:
- **Aggregate ≥ 10/12**
- **No single dimension scored 0**
- **Skill-specific must-haves all present** (defined per scenario)

A skill that scores 11/12 but has a 0 on anti-fabrication does not pass. Fabrication is unrecoverable — better to score 8/12 with honest gaps than 12/12 with one invented quote.

---

## Dimension 1 — Specificity

Does every claim cite real evidence, or does the output hedge with generic prose?

- **0 — Fail** — Output reads like a generic sales coaching template. Phrases like "the rep recently mentioned," "we've seen similar deals," "this account has growth potential" without any specific deal name, date, or quoted moment.
- **1 — Partial** — Some claims are specific (deal name + date) but others hedge. Mix of "Acme Q3 expansion on 2026-04-18: 'we need this by end of quarter'" and "the team has shown interest in growing."
- **2 — Pass** — Every load-bearing claim cites a deal name + date + (when applicable) a quoted moment. Vague language is reserved for genuinely uncertain claims, which are themselves labelled as inference.

**Calibration**: imagine a rep reading the output and asking "where did you get that?" — they should be able to point at a citation for every claim that drives an action.

---

## Dimension 2 — Anti-fabrication

When the data was missing, did the skill say so or invent a finding?

- **0 — Fail** — Output contains a finding, theme, stakeholder, commitment, or precedent that isn't in the input data. Examples: invented a champion name when CRM had no champion tagged; claimed a deal lost to "Competitor X" when no competitor field was set; reported a "week-over-week MEDDPICC delta" on a baseline run with no prior log.
- **1 — Partial** — Output hedged where it should have explicitly labelled a gap. E.g. surfaced something as a "trend" when there was only one data point. Or used "likely" / "appears to" without disclosing the underlying uncertainty.
- **2 — Pass** — Every gap in data is explicitly named. Baseline weeks are labelled. Agent-empty responses are surfaced ("agent returned empty — falling back to CRM-data-only"). Sample size flagged ("3 deals analysed — anecdote, not pattern"). Starter plays tagged as such. No inventions.

**Calibration**: anti-fabrication is the most important dimension. A 0 here = automatic overall fail regardless of other scores.

---

## Dimension 3 — Action quality

Is the drafted next-step sendable as-is by the rep, or does it have placeholders / generic phrasing?

- **0 — Fail** — No action drafted, or action is a generic instruction ("follow up with the buyer"). Placeholders like `[PROSPECT NAME]` or `[REFERENCE PRIOR CALL]` left unfilled. Drafts reference invented context.
- **1 — Partial** — Action drafted with real names and context but reads like a template — generic structure, common phrasing the buyer has seen before. Or: the recommended action is right but the draft is light.
- **2 — Pass** — Drafted email / Slack / talk-track is ready to send. Real prospect first names, real prior context referenced (with date), tone matched to the situation. Signed as the rep. Reading it, the rep should be able to copy and paste.

**Calibration**: would the rep actually send this without rewriting it?

---

## Dimension 4 — Honesty about uncertainty

Are sample-size, baseline-run, and data-quality caveats surfaced where applicable?

- **0 — Fail** — Skill claims confidence the data doesn't support. E.g. "this pattern across deals" with N=1. Or runs `coach-this-rep` for a rep with no prior logged weeks and presents a week-over-week trend table.
- **1 — Partial** — Some uncertainty surfaced but the headline confidence is overstated. E.g. mentions sample size in a drill-down but leads with "we've established this pattern."
- **2 — Pass** — Every uncertainty surfaced clearly: "baseline week — no historical compare," "thin sample — anecdote, not pattern," "starter play — no team-specific precedent yet," "ICP file not configured — fit score unavailable," "agent returned empty for this deal — analysed from CRM data only."

**Calibration**: would a sales-ops analyst reading this brief know exactly which findings to trust at what confidence?

---

## Dimension 5 — Structure (the brevity / scan discipline)

Does the output respect `shared/widget-brevity.md`?

- **0 — Fail** — No verdict line at top. Or > 5 cards in the main view. Or > 350 visible words (excluding headers). Or sections that should be drill-down are inline. Manager-prompts sections with < 2 real actions. Empty "what worked" sections included instead of cut.
- **1 — Partial** — Verdict line present and most cards land, but one of: minor over-cap on words (350–450), six cards instead of five, drill-down content inline rather than collapsed.
- **2 — Pass** — Header band → verdict line → 3–5 cards → optional drill-down. Within budget. Skip-empty-sections discipline respected (no filler cards).

**Calibration**: a busy rep should be able to scan the brief in 90 seconds and know what matters.

---

## Dimension 6 — Skill-specific quality

Defined per skill. Each scenario file lists the must-haves for that skill. Examples:

- **`audit-this-deal`** — RUBRIC scorecard shows pillar:score with one evidence quote per pillar; biggest exposure named; 2-week plan dated and owner-assigned per row.
- **`coach-this-rep`** — every coaching observation tagged with a theme from `coaching-themes.md`; weekly review carries a drill or talk-track, not just a critique; week-over-week tracker only shows real logged weeks.
- **`score-this-call`** — scorecard cites timestamps; coaching points have a drafted "next time say this" line.
- **`prep-this-meeting`** — opening line is grounded in a quoted moment from the last 1–3 calls (not generic); must-cover topics derived from CRM + call evidence; expected objections are real (heard before) with reframes.
- **`learn-from-closed-deals`** — each candidate play cites the deal it came from; 2+ supporting deals = play, 1 = anecdote (labelled).

A 0 on this dimension = the skill failed to do what it specifically promises, even if other dimensions look fine.

---

## Scoring sheet

For each scenario × skill output, produce:

```
Specificity:          [0/1/2] — [one-line reason]
Anti-fabrication:     [0/1/2] — [one-line reason]
Action quality:       [0/1/2] — [one-line reason]
Honesty:              [0/1/2] — [one-line reason]
Structure:            [0/1/2] — [one-line reason]
Skill-specific:       [0/1/2] — [one-line reason]
                      —————
Aggregate:            [X/12]
Pass / Fail:          [PASS / FAIL]
Anti-pattern flags:   [list specific anti-patterns observed, e.g. "invented stakeholder name", "claimed pattern with N=1"]
```

A FAIL on aggregate < 10, on any 0 score, or on any anti-pattern in the scenario's MUST-NOT-DO list is unrecoverable for that run.

---

## Calibration: what good and bad look like

A real example of each dimension being graded — designed to anchor judges.

### Dimension 1 (Specificity) — calibration

**0 score**: *"The buyer has shown interest in expansion. We should follow up to discuss next steps."*

**2 score**: *"On the 2026-05-14 call, Pierre (CTO) said 'we need to figure out the Italian rollout by Q3 or we'll have to push to next year' (12:34 timestamp). Drafted Slack to your champion: 'Pierre — re Italy timeline. Want to lock a 30-min with your local lead in the next two weeks? Here's what we'd cover...' "*

### Dimension 2 (Anti-fabrication) — calibration

**0 score**: a skill output that includes "MEDDPICC week-over-week: +2 on Champion (W18 → W22), +1 on Metrics" — when the run was the first ever for this rep and no prior logs exist.

**2 score**: same skill, same rep, surfaces "**Baseline week** — first logged review for this rep. Week-over-week tracking begins next week."

### Dimension 6 (Skill-specific, `audit-this-deal`) — calibration

**0 score**: skill produces a MEDDPICC scorecard with all 8 pillars rated 1 (Partial) and no evidence quoted under any pillar. Reads like the rubric was applied without looking at the data.

**2 score**: scorecard has explicit scores per pillar, each with one quoted moment (call name + date + speaker), AND the "biggest exposure" section names a specific pillar gap + a dated action to close it.
