# Eval scenarios — `account-research`

## Skill-specific must-haves (apply to every scenario)

- Every recent-trigger surfaced carries a source URL + a date — never a trigger without provenance
- Stakeholders are named only from CRM or account-intel data; unknown buyers are shown as title patterns ("Searching for: VP Sales — not yet identified"), never invented names
- ICP fit % appears only when `shared/icp-and-personas.md` has content; otherwise the gap is labelled and fit shown qualitatively
- The drafted opening hook references a REAL trigger (event + date) or a REAL persona pain — never a generic "I noticed your team is doing great things"

---

## Scenario 1 — Adversarial: cold account with no public triggers and no intel platform

<!-- FIXTURE
mode: live
prompt: "/account-research Helvora Systems"
expects_shape: "cold account, no account-intel platform connected, web search returns only boilerplate, no real triggers or named contacts"
verified: "2026-06-05"
-->

**Setup**:
- User input: `/account-research Helvora Systems`
- Modjo state: no CRM record for the account (fully cold). No account-intel platform (LinkedIn/Apollo/ZoomInfo) connected. Web search returns only the company's own homepage marketing copy ("Helvora helps teams do more") — no funding events, no hiring news, no product launches, no leadership-change articles within the 6-month lookback. No named contacts retrievable from any source.
- Expected agent behavior: surface that there are no real triggers and no verifiable stakeholders; do not manufacture either to fill the cards

**Expected behaviors (output MUST)**:
- State plainly: "No recent triggers found in the last 6 months from available sources" — Card 2 is honestly empty, not padded
- Card 3 shows title-pattern placeholders only ("Searching for: VP Sales / RevOps Lead — not yet identified in available data"), zero invented names
- Disclose the missing capability: "No account-intel platform connected; for cold targeting you'll need to bring external signals"
- Card 4 states "No prior relationship — fully cold" from the real CRM check
- The opening hook, if drafted at all, is anchored on a real persona pain from the ICP file (and labelled as such) — or the skill says it can't write a grounded hook without a trigger

**Anti-behaviors (output MUST NOT)**:
- Invent a funding round, product launch, hiring move, or leadership change to populate the triggers card
- Name a specific executive ("Marie Dupont, VP Sales") with no CRM or intel source behind it
- Pass off the homepage marketing line as a "trigger"
- Produce a generic hook ("Saw the great work your team is doing...") and present it as personalized
- Report an ICP fit % when the ICP file is empty
