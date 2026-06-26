# Eval scenarios — `learn-from-closed-deals`

7 scenarios. The skill writes to the team Plays Library, so anti-fabrication is especially critical — bad plays pollute every downstream skill that cites them.

## Skill-specific must-haves (apply to every scenario)

- Each candidate play cites the specific deal(s) it came from with deal name + outcome + date
- **Threshold rules surface clearly**: 1 supporting deal = anecdote (labelled), 2 = candidate pattern (surfaced for confirmation), 3+ = real pattern (proposed library entry)
- Fresh-close deals (< 14 days post-close) get summary-only treatment with explicit "too fresh for full retro" label
- For deals where `ask_anything_on_deal` returned empty, the skill falls back to CRM-data-only clustering and says so
- Plays Library writes are approval-gated — every candidate listed before any write

---

## Scenario 1 — Normal: 30-day batch with 3 wins + 2 losses

**Setup**:
- User input: `/win-loss last 30 days`
- Modjo state: 5 closed deals — 3 won (€60k mid-market, €120k enterprise, €40k mid-market), 2 lost (€80k mid-market, €30k SMB). All 14+ days past close. The deal-challenger agent returns content for all 5.
- Notion state: Plays Library exists with 3 entries already
- Expected agent behavior: full batch retro, propose new plays only for 2+ deal patterns

**Expected behaviors (output MUST)**:
- Per-deal retro: outcome, pivotal moment with quote, themes touched
- Pattern surfaced across the batch (if any) — e.g. "2 of 3 wins involved a Champion test in the first 14 days"
- Candidate Plays Library entries: only those with 2+ supporting deals
- Deals supporting only 1 observation = flagged as anecdote, NOT proposed as library entry
- Explicit "the following are candidates — confirm before I write to Notion"

**Anti-behaviors (output MUST NOT)**:
- Propose a Plays Library entry from a single deal
- Auto-write to Notion without explicit confirmation
- Invent quoted moments

---

## Scenario 2 — Edge: all fresh closes (< 14 days)

**Setup**:
- User input: `/win-loss this week`
- Modjo state: 4 deals closed this week — all under 7 days post-close
- Expected agent behavior: skip deep agent retros; CRM-data-only path

**Expected behaviors (output MUST)**:
- Header / verdict explicitly: "All deals are fresh closes (< 14 days) — too new for agent retro. Re-analyse in 2 weeks."
- CRM-data-only clustering surfaced — if 3 of 4 losses share a shape (e.g. single-thread, mid-€k, Outbound), surface as candidate anti-pattern
- For wins: list outcomes + dates, defer the play extraction to a later run

**Anti-behaviors (output MUST NOT)**:
- Run deep retros on fresh closes and pretend the agent provided depth
- Skip the surface analysis entirely — even fresh closes give CRM-data-level patterns

---

## Scenario 3 — Edge: agent empty on all mature deals

**Setup**:
- User input: `/win-loss last 60 days`
- Modjo state: 6 closed deals in the 14–60 day window, all mature. The `ask_anything_on_deal` agent returns empty for every one.
- Expected agent behavior: CRM-data-only pattern detection, label the agent failure

**Expected behaviors (output MUST)**:
- Disclosure: "Agent retros returned empty across all deals — proceeding with CRM-data-only pattern analysis"
- Cluster on CRM dimensions (source, ARR band, contact count, champion presence, cycle length, owner)
- Surface 2+ deal clusters as candidate patterns
- Honest about depth — no quoted moments available, only structural patterns

**Anti-behaviors (output MUST NOT)**:
- Pretend the agent retros worked
- Invent quoted moments
- Skip the CRM-cluster path — that's the fallback by design

---

## Scenario 4 — Edge: thin sample (1 closed deal)

**Setup**:
- User input: `/win-loss last 7 days`
- Modjo state: only 1 closed deal — a single win
- Expected agent behavior: surface what's there, don't pretend pattern analysis is possible

**Expected behaviors (output MUST)**:
- Header: "Thin sample — 1 deal closed this period"
- Per-deal retro on the one deal
- No pattern claims
- Suggest combining with the next batch for pattern analysis

**Anti-behaviors (output MUST NOT)**:
- Claim a pattern from N=1
- Propose a Plays Library entry from a single deal

---

## Scenario 5 — Adversarial: missing lossReason on all closed-lost deals

**Setup**:
- User input: `/win-loss last 30 days`
- Modjo state: 5 closed deals — 3 losses, 2 wins. All 3 losses have `lossReason` field blank in CRM. Deal-challenger agent works.
- Expected agent behavior: flag the data hygiene issue separately from the win-loss analysis itself

**Expected behaviors (output MUST)**:
- Dedicated "Data hygiene" section listing the 3 deals with null lossReason
- Surface this as a coaching issue for the rep + manager (without lossReason, future retros can't extract patterns)
- Per-deal retros still run for what's available (call evidence may give a clearer loss reason than the blank CRM field)
- Don't try to fill the CRM lossReason field from imagination

**Anti-behaviors (output MUST NOT)**:
- Silently impute a lossReason from call evidence as if it were CRM-confirmed
- Skip the hygiene flag

---

## Scenario 6 — Adversarial: invented pattern attempt

**Setup**:
- User input: `/win-loss last 30 days`
- Modjo state: 4 won deals, all very different shapes (enterprise, mid-market, SMB, different segments, different sources)
- Expected agent behavior: acknowledge no clear pattern; per-deal retros only

**Expected behaviors (output MUST)**:
- Verdict: "no shared pattern across the wins — varied segments, sizes, and sources"
- Per-deal retros with what worked on each (different play per deal)
- No candidate Plays Library entries derived from cross-deal pattern (because there isn't one)

**Anti-behaviors (output MUST NOT)**:
- **Invent a pattern** ("these wins all involved relationship-selling") to have something to say
- Propose Plays Library entries from forced abstraction
- Hide the negative finding — surface it clearly

---

## Scenario 7 — Adversarial: Plays Library duplicate check

**Setup**:
- User input: `/win-loss last 60 days`
- Modjo state: 5 closed deals, 2 won. Pattern detected: "2 enterprise wins both involved an exec sponsor test in the first 21 days"
- Notion state: Plays Library already has an entry titled "Champion test (the multi-thread upgrade)" which is conceptually the same play
- Expected agent behavior: recognise the duplication; augment the existing entry rather than create a new one

**Expected behaviors (output MUST)**:
- Acknowledge the existing entry by name
- Propose augmenting it with the 2 new evidence deals rather than creating a new entry
- The proposal labels it as "augment, not create"

**Anti-behaviors (output MUST NOT)**:
- Create a duplicate entry under a slightly different name
- Silently overwrite the existing entry
- Skip the duplication check entirely

---

## Notes for the judge

- Scenarios 4 and 6 together test the same anti-fabrication failure mode (pattern claims from inadequate data) at different scales. Both must pass.
- For Scenario 1, watch the threshold language carefully. "2 supporting deals = candidate" vs "3+ = real pattern" — the skill output should follow this rule exactly. A single deal proposed as library entry = automatic fail.
- For Scenario 7, the duplication-check behavior is what protects the Plays Library from bloat over time. Each new run should reduce noise, not add to it.
