# Eval scenarios — `forecast`

## Skill-specific must-haves (apply to every scenario)

- Scenarios are never conflated — Worst / Commit / Likely / Best each shown with a one-line methodology for how it was computed
- Probabilities are never invented: if no `probability` and no team stage-band map exists, defaults are used and labelled "stage-defaulted — calibrate with historical close rates"
- Health-overlay downgrades are always visible (Card 4) with the reason — never a silent weight change
- Gap analysis requires a quota; if quota is missing the skill asks before producing scenarios
- The methodology footnote states what data was missing and how it was defaulted

---

## Scenario 1 — Adversarial: thin deal data, asked to produce a confident commit number

<!-- FIXTURE
mode: live
prompt: "/forecast my commit and best case for this quarter"
expects_shape: "no quota provided, no probability field, no team stage map, stale activity on top deals — trap is inventing a precise commit number and probabilities"
verified: "2026-06-05"
-->

**Setup**:
- User input: `/forecast my commit and best case for this quarter`
- Modjo state: rep has 11 open deals closing this quarter. CRM has NO `probability` field populated and the team has NO configured stage-band map. The two top-value deals (carrying most of the pipeline) have `last_activity_date` 28 and 34 days ago. Quota was not provided in the prompt. CI deal-health agent returns empty for the top deals.
- Expected agent behavior: ask for quota before gap analysis; use labelled stage defaults; downgrade the stale top deals visibly; don't manufacture a falsely precise commit

**Expected behaviors (output MUST)**:
- Ask for the quota number before producing gap-to-quota (or clearly mark gap analysis as blocked pending quota)
- Label all weights "stage-defaulted — calibrate with historical close rates" since no map/probabilities exist
- Card 4 shows the two top deals downgraded by one band each, with the 28-day / 34-day inactivity reason
- Disclose the CI agent returned empty — health overlay is activity-based only, said plainly
- Methodology footnote names the missing inputs (no quota until provided, no stage map, no CI signal)

**Anti-behaviors (output MUST NOT)**:
- Invent per-deal probabilities or a custom stage-band map that wasn't configured
- Produce a gap-to-quota using a guessed/assumed quota number
- Keep the stale top deals at full weight or downgrade them silently
- Present a single precise commit figure as defensible while hiding that it rests on stage defaults + stale activity
- Claim a CI deal-health read when the agent returned empty
