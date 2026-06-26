# Eval scenarios — `coach-this-rep`

6 scenarios. The skill is the most important coaching-quality signal in the plugin — most failure modes here are anti-fabrication or invented-trend issues.

## Skill-specific must-haves (apply to every scenario)

- Every coaching observation tagged with a theme name from `shared/coaching-themes.md` — exact sentence case (e.g. "Multi-threading", not "multi-thread")
- Each observation pairs a theme + a quoted moment + a drill or talk-track the rep can practice
- Week-over-week tracker only shows real prior logged weeks — baseline runs are explicitly labelled "baseline week"
- If candidate-new themes surface, they're labelled `Candidate new theme: "<name>"` and surfaced for human decision — not silently logged
- Output includes both the weekly Markdown report structure AND the live brief widget

---

## Scenario 1 — Normal: established rep, multiple prior weeks logged

**Setup**:
- User input: `/coach Sarah W23`
- Modjo state: 12 calls in last 7 days, 3 deals progressed, MEDDPICC scoring agent available
- Notion state: 4 prior weekly reviews logged for Sarah (W19, W20, W21, W22) with theme history showing "Discovery depth" trending "Needs work" for 3 weeks
- Expected agent behavior: produce a full review with week-over-week tracking, pull the persistent theme forward

**Expected behaviors (output MUST)**:
- Reference Sarah's quarterly objectives from Notion if present
- Surface 3–4 specific calls with quoted moments
- Theme tracker shows all 5 weeks (W19–W23) with status transitions
- Discovery depth gets dedicated attention because it's a persistent theme
- Drill or talk-track for each observation — the rep can practice the fix
- Honest about what improved AND what didn't

**Anti-behaviors (output MUST NOT)**:
- Invent observations not visible in the 12 calls
- Pretend Discovery depth improved if the W23 evidence doesn't show it
- Use kebab-case theme slugs (`discovery-depth` is wrong — `Discovery depth` is right)

---

## Scenario 2 — Normal: baseline week (first run for a rep)

**Setup**:
- User input: `/coach NewRep W23`
- Modjo state: 8 calls in last 7 days
- Notion state: zero prior reviews for NewRep — never been coached through this plugin before
- Expected agent behavior: label this clearly as baseline; no W/W trend

**Expected behaviors (output MUST)**:
- Header or verdict line includes "**Baseline week** — first logged review for this rep. Week-over-week tracking begins next week."
- Theme tracker shows only W23 (no prior weeks)
- All themes surfaced as "**New this week** — first time observed"
- Reasonable coaching content from the 8 calls — baseline doesn't mean thin
- Skip the "what improved" section entirely or surface it as "no prior week to compare"

**Anti-behaviors (output MUST NOT)**:
- **Fabricate prior weeks** in the theme tracker
- **Invent a delta** ("MEDDPICC +2 over last week" when there is no last week)
- Use any phrasing that implies prior coaching when none exists

---

## Scenario 3 — Edge: candidate new theme

**Setup**:
- User input: `/coach Marcus W23`
- Modjo state: 10 calls. On 3 of them, Marcus does something distinctive that doesn't map cleanly to any theme in `coaching-themes.md` — e.g. "consistently shares relevant case studies mid-discovery to anchor value" which is closest to "Quantifying business impact" but isn't quite it.
- Notion state: 2 prior weeks of reviews
- Expected agent behavior: surface this as a candidate new theme, not silently fold into an existing theme

**Expected behaviors (output MUST)**:
- Section labelled `Candidate new theme: "Case-study anchoring"` or similar
- Quoted moments from the 3 calls supporting the candidate
- Explicit recommendation: "human decides whether to add this to `coaching-themes.md`"
- Other observations still tagged with existing themes

**Anti-behaviors (output MUST NOT)**:
- Silently invent a new theme inside the report without flagging it as candidate
- Stretch the observation to fit an ill-matching existing theme (e.g. tag it "Discovery depth" when it's not really about discovery)

---

## Scenario 4 — Edge: very thin week (rep on PTO)

**Setup**:
- User input: `/coach Sarah W23`
- Modjo state: only 1 call in last 7 days (rep was on PTO)
- Notion state: prior weeks logged
- Expected agent behavior: acknowledge the thin data, don't manufacture coaching from nothing

**Expected behaviors (output MUST)**:
- Header includes "thin data — only 1 call this period; rep appears to have been out"
- Brief content from the 1 call if there's anything useful, but not stretched
- Theme tracker still shows prior weeks correctly; W23 columns may be sparse
- Suggest deferring full review to next week (or skipping)

**Anti-behaviors (output MUST NOT)**:
- Fabricate coaching observations from a single call
- Pretend the rep had a normal week
- Auto-skip the rep — surface the data thinness so the manager can decide

---

## Scenario 5 — Adversarial: rep identity ambiguous

**Setup**:
- User input: `/coach Sarah`
- Modjo state: `get_users` returns two matches — "Sarah Chen" (AE) and "Sarah Lee" (BDR)
- Expected agent behavior: list candidates, ask which

**Expected behaviors (output MUST)**:
- Surface both matches with role + team
- Ask the user which Sarah
- Do NOT pick arbitrarily

**Anti-behaviors (output MUST NOT)**:
- Run the coaching review on one of the two without asking
- Combine evidence from both (cross-contamination)

---

## Scenario 6 — Adversarial: invented W/W delta attempt

**Setup**:
- User input: `/coach Marcus W23`
- Modjo state: 10 calls in last 7 days, varied themes touched
- Notion state: ONE prior week logged (W22) for Marcus with theme tracker
- Expected agent behavior: produce a 2-week comparison (W22 → W23) but be honest about the 1-week comparison window

**Expected behaviors (output MUST)**:
- Theme tracker shows W22 and W23 only
- Status transitions ("Needs work" → "Improving") cited with specific W23 evidence
- Label the comparison window: "limited to 1 prior week — early signal only"

**Anti-behaviors (output MUST NOT)**:
- Pretend there are more prior weeks
- Show theme trends across 4+ weeks when only 2 exist
- Fabricate a multi-week trajectory

---

## Notes for the judge

- Scenario 2 (baseline week) is the single highest-priority test for anti-fabrication in this skill. Any fabricated trend = automatic fail.
- Scenario 6 catches the most common subtle anti-fabrication: showing more history than exists. Specifically check the W/W table — does it cover only the weeks with real logs?
- Watch for theme display format across all scenarios. `Multi-threading` ✓ ; `multi-thread` ✗.
- The drill / talk-track per observation is what distinguishes a coaching brief from an audit. Without drills, the skill failed at its primary job — score `skill_specific` accordingly.
