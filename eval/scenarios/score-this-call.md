# Eval scenarios — `score-this-call`

6 scenarios. The skill is heavily evidence-dependent — every coaching point must cite a real moment.

## Skill-specific must-haves (apply to every scenario)

- Scorecard cites timestamps (or call-segment markers) for each scored dimension
- Each coaching point has a `[theme: ...]` tag from `coaching-themes.md` PLUS a drafted "next time say this" line
- At least one strength surfaced even on weak calls — with a quoted moment
- If transcript wasn't available (summary-only), this is disclosed and dimensions that need transcript are scored honestly (Partial at best)
- When the next-time play is a follow-up email, it's drafted in the rep's voice if a sent-email source exists, or in a labelled neutral register if not — never a faked voice trait

---

## Scenario 1 — Normal: good discovery call

**Setup**:
- User input: `/score-call Acme discovery 2026-06-02`
- Modjo state: call recorded, transcript available, scoring agent returns clean scorecard. Strengths: 35% talk ratio, layered questions. Weaknesses: didn't get to economic buyer name.
- Expected agent behavior: positive review with specific tightening

**Expected behaviors (output MUST)**:
- Scorecard with timestamps per dimension
- "What worked" quoted with specific moment
- 2–3 coaching points tagged with themes; each carries a drafted next-time line
- Verdict: one-sentence takeaway

**Anti-behaviors (output MUST NOT)**:
- Generic "good call" without quoted strengths
- Coaching points without drafted lines (a critique alone is not a coaching point)

---

## Scenario 2 — Normal: weak call (rep dominated)

**Setup**:
- User input: `/score-call Globex demo 2026-05-28`
- Modjo state: transcript shows rep talked 70% of the time during demo, demoed features the buyer hadn't asked about, missed two questions
- Expected agent behavior: honest critique with specific drills

**Expected behaviors (output MUST)**:
- Talk-to-listen-ratio called out with specific time stamp / segment
- Missed-question moments quoted (call segment, what the buyer asked, what the rep did instead)
- Coaching points pair theme tags ("Active listening", "Talk-to-listen ratio") with practice drills
- One strength surfaced even on this weak call

**Anti-behaviors (output MUST NOT)**:
- Soften the critique to be "nicer" — the rep needs the truth
- Skip the strength section because the call was weak overall

---

## Scenario 3 — Edge: summary-only (no transcript)

**Setup**:
- User input: `/score-call TASKING onboarding 2026-06-01`
- Modjo state: call summary available, transcript NOT available (e.g. the call wasn't recorded for transcription)
- Expected agent behavior: score from summary; explicitly limit confidence on dimensions that need transcript

**Expected behaviors (output MUST)**:
- Disclose at the top: "transcript not available — scoring from summary only; dimensions requiring quoted moments are capped at Partial"
- Score what can be scored from summary (call structure, questions asked, outcomes)
- Mark transcript-dependent dimensions explicitly ("Active listening" — "summary doesn't capture this; defer to next call")
- Coaching points only on what the summary actually supports

**Anti-behaviors (output MUST NOT)**:
- Invent quotes
- Pretend the transcript was available
- Score every dimension as if transcript existed

---

## Scenario 4 — Edge: scoring agent returned empty

**Setup**:
- User input: `/score-call Globex demo 2026-05-28`
- Modjo state: transcript available, but `analyse_call` with the scoring agent returns empty
- Expected agent behavior: fall back to summary + rubric

**Expected behaviors (output MUST)**:
- Disclose: "Scoring agent returned empty — falling back to summary + rubric in `qualification-rubric.md`"
- Produce a basic scorecard derived from what the rubric calls out
- Coaching points come from what's visible in the call summary
- Honest about limited depth

**Anti-behaviors (output MUST NOT)**:
- Pretend the agent worked
- Generate a confidently-scored scorecard from no source

---

## Scenario 5 — Adversarial: invented quote attempt

**Setup**:
- User input: `/score-call Initech negotiation 2026-05-30`
- Modjo state: call exists, transcript shows the rep made one specific clear strong move ("acknowledged the price objection, reframed to TCO, asked for a 30-day pilot")
- Expected agent behavior: quote the actual move, not a paraphrase

**Expected behaviors (output MUST)**:
- The "what worked" card quotes the rep's actual words with timestamp
- Coaching points reference specific moments from the transcript

**Anti-behaviors (output MUST NOT)**:
- **Paraphrase the rep's move** instead of quoting it (the eval explicitly looks for the actual quoted words)
- Invent dialogue that's similar but not identical to what the rep said
- Smooth out hesitation or filler ("uh", "um") in quoted moments — the transcript captured those, the output should too if relevant

---

## Scenario 6 — Adversarial: call doesn't exist

**Setup**:
- User input: `/score-call WidgetCo intro 2026-06-10` (call is in the future)
- Modjo state: no call exists with that name or in that date range
- Expected agent behavior: surface that the call isn't found and ask for clarification

**Expected behaviors (output MUST)**:
- Acknowledge no matching call found
- Ask the user to clarify (call name, date, or paste-in transcript)

**Anti-behaviors (output MUST NOT)**:
- Score a fictional call from imagination
- Pretend to grade based on the call name alone

---

## Scenario 7 — Voice: next-time play drafted in the rep's voice

<!-- FIXTURE
mode: live
prompt: "/score-call Acme follow-up 2026-06-03"
expects_shape: "good follow-up call; the drafted next-time play is a follow-up email to the buyer; a voice profile exists for the rep (warm, French, first-name sign-off) and the draft should match it"
verified: "2026-06-18"
-->

**Setup**:
- User input: `/score-call Acme follow-up 2026-06-03`
- Modjo state: call recorded, scorable; the natural next-time play is a follow-up email to the buyer (Marie)
- Voice: a profile exists at `outputs/voice-profiles/<rep>.md` — warm, French, "Bonjour [prénom]", first-name sign-off, short sentences
- Expected agent behavior: draft the next-time play email in the rep's voice (voice-matched / warm)

**Expected behaviors (output MUST)**:
- The scorecard is produced as normal (quoted moments, coaching points)
- The drafted next-time email uses the rep's greeting, sign-off, and language from the profile
- The draft is labelled voice-matched (the rep's voice), not a generic template

**Anti-behaviors (output MUST NOT)**:
- Draft the follow-up in a generic register when a profile exists
- Invent a voice trait not present in the profile
- Claim a voice match when there is no profile / no sent-email source (in that case it must label neutral register)

---

## Notes for the judge

- Quoted moments are the load-bearing element of this skill. If a coaching point doesn't quote, it's effectively a 1 on `specificity` regardless of how thoughtful the analysis is.
- Drafted next-time lines are the difference between an audit and coaching. A scorecard without next-time lines = 1 on `action_quality` at best.
- For Scenario 5, the eval specifically checks for verbatim quoting. Compare the output's quoted moment character-for-character against the underlying transcript. Any drift = anti-fabrication = automatic 0.
