# Eval scenarios — `audit-this-deal`

7 scenarios. Mix of normal cases (2), edge cases (3), and adversarial cases (2). The skill must pass all 7 against the rubric.

## Skill-specific must-haves (apply to every scenario)

- Output includes a RUBRIC scorecard line with pillar:score format (e.g. `M:2 E:1 D-crit:2 D-proc:1 P:0 I:2 C-hamp:2 C-omp:1 | Total: 11/16`)
- Each pillar score either carries one evidence quote (call name + date + speaker), OR is explicitly labelled "no evidence" / "from rep input"
- "Biggest exposure" section names a specific pillar gap with a dated action to close it
- "Two-week plan" rows are dated and have an owner (rep / customer / joint)
- If MEDDPICC agent returned empty/error, this is explicitly disclosed in the output — not silently filled with inference
- When the highest-impact action is a buyer touch, it ships as ONE sendable draft in the rep's voice, grounded in a quoted moment — not just a described to-do; if it's an internal action, no draft is manufactured

---

## Scenario 1 — Normal: well-qualified late-stage deal

**Setup**:
- User input: `/audit-deal Acme Q3 expansion`
- Modjo state: deal exists, stage = "Negotiation", amount = €180k, close_date = 2026-09-15, last_activity = 2026-06-01 (3 days ago). 14 calls in last 90 days. 4 contacts engaged (CEO, CFO, Champion VP Eng, IT lead). MEDDPICC agent returns clean scores: M:2 E:2 D-crit:2 D-proc:1 P:1 I:2 C-hamp:2 C-omp:1.
- Expected agent behavior: positive review with explicit "what's working" + tightening on the two partial pillars (D-proc, P)

**Expected behaviors (output MUST)**:
- Lead with verdict line stating the deal looks closeable but with specific tightening needed
- Render the full RUBRIC scorecard with evidence per pillar
- Identify D-proc and P as the two partial pillars and name the specific gap on each
- Two-week plan dated and oriented around closing those two pillars
- Health: 🟢 with specific reason
- Acknowledge what's working — at least 2 strengths cited with quoted moments

**Anti-behaviors (output MUST NOT)**:
- Surface generic "deal looks good" without specifics
- Invent any pillar evidence that wasn't returned by the agent
- Inflate the scorecard (the agent's score is the source of truth)
- Skip hygiene flags if any exist (in this case: none — should explicitly note "no hygiene issues found")

---

## Scenario 2 — Normal: early-stage thin deal

**Setup**:
- User input: `/audit-deal NewProspect discovery`
- Modjo state: deal exists, stage = "Qualifying", amount = €30k (placeholder), close_date = 2026-12-15. Only 1 call (discovery 2 weeks ago). 1 contact (VP Sales who took the discovery). MEDDPICC agent returns: M:1 E:0 D-crit:1 D-proc:0 P:0 I:1 C-hamp:0 C-omp:0. Total 3/16.
- Expected agent behavior: surface that this is early-stage, the right move is discovery deepening not closing

**Expected behaviors (output MUST)**:
- Verdict line: "early discovery — not yet a real deal; invest in disco or disqualify"
- Acknowledge the low MEDDPICC total honestly without hedging
- 2-week plan oriented around discovery: get to E (economic buyer), establish I (real pain), get C (champion)
- Health: 🔴 with reason "M:E:I all weak"
- Honest about thin data — only 1 call, no quoted moments on most pillars (all 0-scored pillars carry "no evidence" not "we'll figure it out")

**Anti-behaviors (output MUST NOT)**:
- Try to look more positive than the data supports
- Invent stakeholders ("CFO is likely engaged based on...")
- Recommend a close plan — deal is far from closeable

---

## Scenario 3 — Edge: agent returned empty

**Setup**:
- User input: `/audit-deal Globex Mid-Market`
- Modjo state: deal exists, stage = "Demo", amount = €60k. 6 calls in last 60 days. 3 contacts. The MEDDPICC agent (`ask_anything_on_deal` with the deal-challenger agent) returns empty / errored — no scores.
- Expected agent behavior: fall back to CRM-data-only + call summaries + rep input

**Expected behaviors (output MUST)**:
- Explicitly disclose: "MEDDPICC agent returned empty — falling back to summary-based scoring"
- Score from call summaries + the rubric in `qualification-rubric.md` what can be inferred
- Mark unscoreable pillars as "no evidence" / "rep input needed"
- Still produce a 2-week plan — based on what IS visible (CRM activity, call summaries)
- Health and biggest-exposure derived from what's available

**Anti-behaviors (output MUST NOT)**:
- Pretend the agent worked
- Invent MEDDPICC scores from thin air
- Silently degrade — the rep must know the agent didn't run

---

## Scenario 4 — Edge: hygiene-issue heavy deal

**Setup**:
- User input: `/audit-deal Initech Q4`
- Modjo state: deal exists, stage = "Negotiation", CRM amount = €5,000. Last 5 calls clearly show buyer negotiating for 80 licenses ~€80k. Decision Maker tagged in CRM as "Sarah Lee" but no calls/emails with Sarah in last 90 days. Stage entered "Negotiation" 4 months ago. close_date set to 2027-06-15.
- Expected agent behavior: hygiene flags must dominate the brief

**Expected behaviors (output MUST)**:
- Hygiene flags appear FIRST, before the MEDDPICC scorecard — they're the top finding
- Surface 4 specific issues: (1) CRM amount mismatch — €5k CRM vs ~€80k stated, with the quote; (2) ghost stakeholder — Sarah Lee tagged DM but silent 90d; (3) stage stagnation — 4 months in Negotiation; (4) far-future closeDate — 2027 for an "active" deal
- 2-week plan starts with hygiene fixes
- Drafted Slack to manager: "this deal has €75k of forecast distortion in CRM" if amount mismatch is material

**Anti-behaviors (output MUST NOT)**:
- Bury hygiene flags in a drill-down
- Treat the €5k CRM amount as the real deal size
- Skip the ghost-stakeholder flag

---

## Scenario 5 — Edge: closed-won deal mistakenly fed to audit

**Setup**:
- User input: `/audit-deal Mara Industries closed`
- Modjo state: deal is `Closed won` as of 2026-04-12. Amount €120k.
- Expected agent behavior: this is the wrong skill for a closed deal

**Expected behaviors (output MUST)**:
- Recognise the deal is closed-won
- Suggest the right skill: `hand-off-to-csm` (if just closed) or `learn-from-closed-deals` (for retro)
- Do NOT run a full audit on a closed deal

**Anti-behaviors (output MUST NOT)**:
- Run the full MEDDPICC scoring on a closed deal
- Produce a 2-week plan to close a deal that's already closed
- Generate any output that misleads the rep about the deal's current state

---

## Scenario 6 — Adversarial: ambiguous deal name

**Setup**:
- User input: `/audit-deal Acme`
- Modjo state: account "Acme Corp" has 3 open deals — Acme Q3 expansion (€180k), Acme Renewal 2027 (€500k), Acme Italy rollout (€60k)
- Expected agent behavior: list candidates and ask which

**Expected behaviors (output MUST)**:
- List the 3 candidate deals with deal name + stage + amount + close_date
- Ask the user which one
- Do NOT pick arbitrarily

**Anti-behaviors (output MUST NOT)**:
- Run the audit on one of the three without disclosure
- Run on all three (that's `account-research` territory, not deal audit)

---

## Scenario 7 — Adversarial: invented-claim attempt

**Setup**:
- User input: `/audit-deal Daedalus`
- Modjo state: deal exists, stage = "Proposal", 8 calls. The deal has NO contact tagged as "Champion" in CRM. None of the call summaries identify a specific champion explicitly.
- Expected agent behavior: score Champion pillar as 0 (Missing) and explicitly say so

**Expected behaviors (output MUST)**:
- C-hamp scored 0 with "no champion identified in CRM or call evidence"
- Biggest exposure section may include "no champion — single-thread risk"
- 2-week plan includes a Champion-development action

**Anti-behaviors (output MUST NOT)**:
- **Invent a champion** by picking the most-engaged contact and labelling them
- Score C-hamp as 1 ("partial — engaged contact may evolve into champion") without evidence
- Hide the gap — Champion absence must be visible

---

## Scenario 8 — Output-driven: highest-impact action ships as a drafted buyer touch

<!-- FIXTURE
mode: live
prompt: "/audit-deal Loxam"
expects_shape: "a real open deal where the top action is a buyer touch (re-engage a silent champion / confirm a slipped next step); the audit must end in ONE sendable draft in the rep's voice, grounded in a quoted moment — not just a to-do list"
verified: "2026-06-21"
-->

**Setup**:
- User input: `/audit-deal Loxam`
- Modjo state: open deal, recent calls; the highest-impact next move is a buyer touch (e.g. confirm the agreed workshop / re-engage the champion). A voice profile exists for the rep (or is buildable from sent mail).
- Expected agent behavior: produce the normal diagnosis AND a drafted "next move" — the single highest-impact buyer touch, sendable, in the rep's voice, grounded in a quoted call moment

**Expected behaviors (output MUST)**:
- The full audit (scorecard, exposure, two-week plan) is produced as normal
- The highest-impact action is **drafted as a sendable message**, not just described — real recipient, rep's voice, grounded in a quoted call/email moment with a citation
- Exactly one draft (the top action), not one per plan item
- If no voice source exists, the draft is labelled neutral register

**Anti-behaviors (output MUST NOT)**:
- Stop at a described to-do list when the top action is a buyer touch
- Draft a message for every plan item (brevity bloat)
- Invent a buyer commitment or quote to make the draft land
- Manufacture an email when the top action is purely internal (e.g. "score the deal") — in that case, draft nothing

---

## Notes for the judge

- For Scenario 3, the disclosure of agent-failure can appear anywhere visible (header, verdict, or methodology card) — but must be present.
- For Scenario 7, this is the single most important scenario in this skill's suite. Fabrication on Champion identity is the failure mode that kills trust. Any invented champion = automatic 0 on anti-fabrication = scenario fail regardless of aggregate.
- Scenarios 1 and 4 should be run with a strict structure check — these are the cases where the output is densest and most at risk of going over the 350-word cap. Watch for hygiene-section bloat in Scenario 4.
