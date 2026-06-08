# Qualification rubric — methodology-agnostic interface

Single source of truth for how the deal-execution and coaching skills score qualification. **This file ships with MEDDPICC as the default content**, but the plugin is methodology-agnostic — teams using BANT, SPICED, MEDDIC, or homegrown frameworks should replace this file's content with their own rubric using the same structural interface.

## The interface every skill expects

A qualification rubric, regardless of methodology, must provide:

1. **A fixed set of pillars** (named, ordered) — e.g. MEDDPICC has 8, BANT has 4, SPICED has 5
2. **A 0 / 1 / 2 scoring scale** per pillar (Missing / Partial / Validated)
3. **Concrete evidence requirements** per pillar — what does "good" look like, what's the anti-pattern
4. **An output line format** so downstream skills can parse pillar scores consistently
5. **A total score bands** for what action the band triggers (early discovery / active selling / late stage / closeable)

Skills read this file abstractly. The rep's prose says "score the deal on the team's qualification rubric." The actual pillar names come from this file's content. **Skills should never hard-code pillar names like "M:_ E:_ ..." in their output prose** — the output format token is defined here.

## Default rubric: MEDDPICC

The plugin ships with MEDDPICC because it's the most common enterprise qualification framework. If your team uses something different, **copy the corresponding file from `qualification-rubrics/`** (BANT, SPICED, MEDDIC variants are provided) over this file's content. Or write your own following the same structure.

## MEDDPICC scoring

| Pillar | 0 — Missing | 1 — Partial | 2 — Validated |
|---|---|---|---|
| **M — Metrics** | No quantified business impact mentioned. | Generic value claim ("save time") with no number. | Specific $ / % / time metric the prospect confirmed matters. Tied to a baseline. |
| **E — Economic buyer** | Unknown or not identified. | Name known, never met or engaged. | Met live; confirmed they sign off; we know their priorities. |
| **D — Decision criteria** | No criteria captured. | Vague preferences ("ease of use, price"). | Written or spoken list of weighted criteria; we know what "winning" looks like. |
| **D — Decision process** | Unknown. | Some steps known ("legal review at some point"). | Mapped stages, owners, expected dates, current step. |
| **P — Paper process** | Unknown. | Procurement/legal mentioned, no detail. | Vendor onboarding, security review, MSA template, signature flow all documented. |
| **I — Identify pain** | Pain unclear or surface-level. | Pain named but cost of inaction not quantified. | Specific pain + cost of inaction + emotional weight from the prospect's own words. |
| **C — Champion** | No champion. | Coach / friendly contact, but no proof of advocacy. | Has fought for us internally; can name our differentiators; has political capital. |
| **C — Competition** | Unknown. | Competitor named, positioning unclear. | We know who's in it, why they're in it, our differentiation, prospect's lean. |

**Total**: 0–16. Bands:

- **0–5** — Early discovery. Disqualify or invest in disco.
- **6–10** — Active selling. Pillar-by-pillar gaps drive the next-step plan.
- **11–14** — Late stage. Focus on paper process, legal, mutual close plan.
- **15–16** — Closeable. If still slipping, the gap is execution, not qualification.

## Output line format (MEDDPICC variant)

When a skill emits a pillar score, use this exact format so downstream skills can parse it:

```
RUBRIC: M:2 E:1 D-crit:2 D-proc:1 P:0 I:2 C-hamp:2 C-omp:1 | Total: 11/16
```

The leading `RUBRIC:` token tells downstream skills which methodology is in use. Other methodologies use different pillar names (see `qualification-rubrics/`).

## How skills source pillar evidence

In order of preference:

1. **Use a methodology-matching agent** if your CI platform has one. For MEDDPICC, common agent names include "Deal Challenger," "MeddicValidator," "MEDDPICC scorer." Discover via `discover_agents` with search filter "MEDDPICC" or "qualification" or your methodology name.
2. **Use the platform's default agent** with the rubric in the question. Single-question framings per pillar (multi-part agent questions return empty — confirmed failure mode).
3. **Score from call summaries + the rep's input** if no agent is available. The skill walks the rep through pillars verbally and the rubric defines what evidence to look for.

Never report a pillar score without at least one direct quote or specific evidence reference. "M:2" with no metric named is filler.

## Bands → action mapping

Skills that consume the rubric (audit-this-deal, lock-the-close-plan, review-the-pipeline, coach-this-rep) should treat the bands as triggers:

- **0–5 / Early discovery**: skill should either disqualify the deal or invest in a fresh discovery cycle
- **6–10 / Active selling**: skill produces a pillar-gap-driven 2-week plan
- **11–14 / Late stage**: skill produces a mutual action plan (or recommends invoking `lock-the-close-plan`)
- **15–16 / Closeable**: skill watches for execution gaps, not qualification ones
