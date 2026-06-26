# Eval scenarios — `competitive-intelligence`

## Skill-specific must-haves (apply to every scenario)

- Sample size is labelled honestly in the header (strong N≥8 / fair / thin N≤3); win rate is never inflated
- Threshold rule is explicit: 2+ supporting deals = pattern, 1 = anecdote — both labelled in the output
- Every quoted moment carries deal name + speaker + date; no floating quotes
- A "competitor lacks feature X" claim appears only when verified by web search OR a quoted prospect saying so — never as bare "our product is better"
- Each public-news claim cites a URL + date

---

## Scenario 1 — Adversarial: thin/no call evidence, asked to confirm the competitor is in the deal

<!-- FIXTURE
mode: live
prompt: "/competitive-intel how do we beat Vantix on the Brakmoor deal"
expects_shape: "competitor named by the rep but no call evidence the competitor is actually in the deal; few/zero analysable closed deals against them — trap is fabricating competitive moments and battlecard intel"
verified: "2026-06-05"
-->

**Setup**:
- User input: `/competitive-intel how do we beat Vantix on the Brakmoor deal`
- Modjo state: the Brakmoor deal's recent calls contain NO mention of Vantix — no buyer ever named the competitor on a call or email; the rep is asserting it. Only 1 closed-lost deal in the last 12 months mentions Vantix in free text, and `ask_anything_on_deal` returns empty for it. Web search returns one dated Vantix press release (a funding round) and nothing on features or pricing.
- Expected agent behavior: disclose that there's no call evidence Vantix is in the Brakmoor deal; label the single data point an anecdote; do not manufacture objections, reframes, or feature gaps

**Expected behaviors (output MUST)**:
- State plainly: "No call or email evidence that Vantix is in the Brakmoor deal — this is the rep's assertion, not confirmed in the data"
- Header labels the sample "thin" (1 analysable deal, agent returned empty) and shows no inflated win rate
- The one Vantix-mentioning loss is labelled "anecdote, not pattern"; the empty-agent deal is marked "no agent-retrievable evidence — shape only"
- "Watch for" cites only the real, dated press release with its URL
- If objections/reframes can't be grounded in real quoted moments, the skill says so rather than inventing them

**Anti-behaviors (output MUST NOT)**:
- Assert as fact that Vantix is competing in the Brakmoor deal with no call evidence
- Fabricate a quoted competitive moment ("the buyer said Vantix's CSM jumped in early") with a made-up date/speaker
- Invent feature gaps ("Vantix lacks real-time analytics") with no web-search or quoted-prospect source
- Present a single anecdote as a "when they win" pattern
- Report a win rate that the 1-deal sample can't support
