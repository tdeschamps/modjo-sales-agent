# Modjo Sales Agent — Evaluation suite

The Tier-1 functional-quality eval for the plugin. Tests whether the highest-leverage skills produce outputs that meet the rubric — specificity, anti-fabrication, action quality, honesty about uncertainty, structure, skill-specific quality.

This is one piece of a larger eval ladder. See "How this fits the broader eval" at the bottom.

## What's here

```
eval/
├── README.md           ← you are here
├── rubric.md           ← 6-dimension grading rubric, 0/1/2 each, pass = 10/12 + no zeros
├── judge-prompt.md     ← LLM-judge prompt template for scoring outputs at scale
└── scenarios/
    ├── audit-this-deal.md          ← 7 scenarios
    ├── coach-this-rep.md           ← 6 scenarios
    ├── score-this-call.md          ← 6 scenarios
    ├── prep-this-meeting.md        ← 6 scenarios
    └── learn-from-closed-deals.md  ← 7 scenarios
```

Total: 32 scenarios across the 5 highest-leverage Modjo-native skills.

## How to run the eval (manual)

For each (skill, scenario) pair:

1. **Read the scenario** in `scenarios/<skill>.md`. It specifies the user input, the Modjo state, the expected behaviors, the anti-behaviors, and the skill-specific must-haves.

2. **Set up the Modjo state** that the scenario describes. Two paths:
   - **Live**: pick a real deal/rep/account in your Modjo workspace that matches the scenario's shape. Run the skill against it.
   - **Mocked**: use Modjo's API to return synthetic data matching the scenario shape, or paste-in the scenario data as the user input.

3. **Run the skill** in the plugin (slash command or natural-language invocation). Capture the rendered output verbatim — widget Markdown, Notion writes, Slack drafts.

4. **Grade with the LLM-judge**. Open a fresh chat with a strong judge model (Claude Opus 4.6 or Sonnet 4.6), paste the prompt template from `judge-prompt.md` with the four placeholders filled in:
   - `{SKILL_NAME}` — e.g. `audit-this-deal`
   - `{SCENARIO_BLOCK}` — the full scenario from `scenarios/<skill>.md`
   - `{PLUGIN_OUTPUT}` — the verbatim output from step 3
   - `{RUBRIC}` — paste `rubric.md`

5. **Read the judge output**. Structured YAML with per-dimension scores, reasoning, and a PASS/FAIL verdict. Record the result.

6. **Run 3 times** (output is stochastic). Use the lowest score as the floor signal.

7. **For failures**: read the judge's `top_coaching_note` + `anti_patterns_observed`. Fix the skill's SKILL.md or shared/ refs. Re-run the failing scenario. Re-run all other passing scenarios to check for regressions.

## Pass / fail thresholds

**Per scenario**:
- Aggregate ≥ 10/12
- No dimension scored 0
- No anti-behavior from the scenario's MUST-NOT-DO list triggered

**Per skill**:
- All scenarios for that skill pass

**Plugin-level Tier-1 pass**:
- All 5 skills pass all their scenarios

This is a strict bar. The expectation is that early runs will fail several scenarios — that's the eval doing its job. Each failure points at something specific to fix.

## What to do with results

Track per scenario:
- Date of run
- Plugin version (e.g. `v0.1.0` or a git commit)
- Judge model used
- 3 runs × aggregate score
- PASS / FAIL
- Anti-patterns observed (if any)
- Action taken (skill rule changed? scenario updated? "not yet fixed"?)

A simple Notion table or spreadsheet works fine. The data accumulates across plugin versions — you should see scenarios that fail in v0.1.0 stop failing in v0.2.0, with the specific change cited.

## Growing the eval set

The eval is not static. Every new failure mode you encounter in the wild becomes a new scenario:

1. A rep reports a bad output ("the brief invented a champion who doesn't exist")
2. Reproduce the failure with a real or synthetic input matching that shape
3. Add a new scenario to the relevant `scenarios/<skill>.md` file as an adversarial case
4. Fix the skill so it passes
5. The scenario stays in the suite forever — regression boundary

This is how a small suite grows into a real safety net. After 6 months of running, the suite might be 80–120 scenarios. After a year, 200+. Each scenario maps to a specific failure mode the team has actually seen.

## What this eval does NOT cover

The Tier-1 eval is functional quality. It says nothing about:

- **Adoption** — do reps actually use the plugin? Measured separately via behavioral logging (Tier 2).
- **Outcome lift** — do deals close faster, win-rate improve, MEDDPICC scores progress? Measured separately via matched-control comparison (Tier 3).
- **Rep satisfaction** — explicit 1–5 ratings + free-text feedback (Tier 2, runs alongside adoption).

A plugin can pass Tier 1 100% and still fail in the market if reps don't adopt it. A plugin that fails Tier 1 will almost certainly fail Tier 2 and 3 — bad outputs erode trust fast.

Order of operations:
- **Tier 1** (this eval): run before any user touches the plugin. Iterate until it passes.
- **Tier 2** (adoption + ratings): run during internal dogfood (3–5 reps, 2 weeks).
- **Tier 3** (outcome lift): run on one flagship skill at customer scale once Tier 2 shows engagement.
- **Tier 4** (customer beta): same eval, customer reps. Only after Tier 3 shows signal.

## Cost & time estimate

For Tier 1 on these 5 skills with 32 scenarios:

- Setup per scenario: ~10 minutes (find the matching state, run the skill, capture output)
- LLM-judge per scenario: ~30 seconds compute, ~5 seconds of attention
- 3 runs per scenario: ~30 minutes per scenario including setup
- Total: ~16 hours of focused work for the first full eval pass
- Subsequent passes after fixes: much faster (~2–4 hours per pass once scenarios are wired up)

If 16 hours feels like a lot, prioritise: run all `audit-this-deal` and `coach-this-rep` scenarios first (those are the highest-stakes skills with the most anti-fabrication risk). The other three skills can wait a week.

## Why this rubric, not something fancier

The six dimensions cover what matters in a sales-coaching context:
- **Specificity + Anti-fabrication** — does the output reflect reality?
- **Action quality + Honesty about uncertainty** — can the rep act on it without re-checking?
- **Structure** — will the rep actually read it?
- **Skill-specific quality** — does the skill do its specific job?

Alternative rubrics (RAGAS, ROUGE, BLEU, semantic similarity scores) all measure surface-level text quality. Sales-coaching outputs are evaluated by what they do for the rep, not how they read in isolation. The rubric is designed to catch the failure modes that actually erode trust in the field.
