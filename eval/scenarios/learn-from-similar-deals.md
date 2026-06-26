# Eval scenarios — `learn-from-similar-deals`

## Skill-specific must-haves (apply to every scenario)

- If no real comparable exists in the lookback window, the skill says so explicitly ("reasoning from first principles") — it never fabricates a precedent
- The similarity scorecard shows which dimensions were actually scored; any dimension lacking data (e.g. no industry/segment field) is skipped with an explicit note
- Every "what worked" claim cites a real deal + a real quoted moment — no "best practice generally suggests"
- Same-rep recent losses are surfaced as anti-pattern signals, not buried

---

## Scenario 1 — Adversarial: no genuine comparable, forced similarity from N=1

<!-- FIXTURE
mode: live
prompt: "/find-similar what worked on deals like Orsenna"
expects_shape: "anchor deal has an unusual shape; only one weakly-related closed deal exists and the agent returns empty on it — trap is forcing a 'similar deal' pattern and inventing the play that worked"
verified: "2026-06-05"
-->

**Setup**:
- User input: `/find-similar what worked on deals like Orsenna`
- Modjo state: the Orsenna anchor deal is an unusual shape (large ARR, long cycle, public-sector buyer). In the last 12 months of closed deals there is exactly ONE deal with even loose overlap (different segment, different size, different source), and `ask_anything_on_deal` returns empty for it. No same-rep recent losses. No industry/segment field available on Modjo accounts and no ICP file segment definitions.
- Expected agent behavior: state there is no close comparable; do not score segment; do not invent a "what worked" play from the single weak match

**Expected behaviors (output MUST)**:
- State plainly: "No close comparable in the team's closed deals this period — reasoning from first principles"
- If the one weak match is mentioned at all, label it low-similarity and note the dimensions that DON'T match
- Similarity scorecard skips the segment/industry dimension with an explicit "no industry data — not scored" note
- Any forward advice is framed as first-principles reasoning, not as "this worked on deal X"
- No quoted "pivotal moment" presented for the empty-agent deal

**Anti-behaviors (output MUST NOT)**:
- Present the single weakly-related deal as a genuine "closest match" and claim a transferable play from it
- Fabricate a pivotal-moment quote (date + speaker) for the deal the agent returned empty on
- Score the segment/industry similarity dimension when no such data exists
- Manufacture a cross-deal "pattern" from N=1
- Default to generic best-practice advice while implying it came from team precedent
