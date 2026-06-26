# Eval scenarios — `prep-this-meeting`

6 scenarios. The skill is high-frequency (every rep, every meeting) so the structure / brevity dimension matters more than for any other.

## Skill-specific must-haves (apply to every scenario)

- Opening line is grounded in a quoted moment from the last 1–3 calls OR a real CRM-tracked event — NOT generic
- Must-cover topics are derived from CRM + call evidence, not invented
- Expected objections are real (heard before on this account or in this segment), not speculative
- Stakeholders list cites last-touch date per contact + a one-line read on each
- Brief stays at 350 words / ≤ 5 cards — this is the highest-frequency skill so cap discipline is critical

---

## Scenario 1 — Normal: discovery call on existing account

**Setup**:
- User input: `/prep-meeting Acme discovery tomorrow`
- Modjo state: account exists, 2 prior calls (intro 2 weeks ago, discovery 1 week ago). Open deal in qualification stage. 3 contacts in CRM. Last call summary mentions buyer concerns about implementation timing.
- Expected agent behavior: full prep grounded in the prior calls

**Expected behaviors (output MUST)**:
- Verdict: the move that wins this meeting in one sentence
- Drafted opening line quotes a real moment from the prior call ("Last week you mentioned X — wanted to start with how that's evolved")
- Must-cover topics include the implementation-timing concern with the specific quote
- Stakeholder map shows the 3 contacts with last-touch + read
- 2–3 expected objections, each grounded in a real prior moment OR an established account pattern

**Anti-behaviors (output MUST NOT)**:
- Generic opening line ("Thanks for taking the call")
- Invent a buyer concern not in the call summary
- Skip the prior-calls section — this is the highest-value evidence

---

## Scenario 2 — Normal: demo for new prospect

**Setup**:
- User input: `/prep-meeting NewProspect demo`
- Modjo state: account exists, 1 prior call (qualifying), 2 contacts identified
- Expected agent behavior: demo-shaped prep

**Expected behaviors (output MUST)**:
- Verdict oriented around demo: what specific scenarios to show
- Must-cover topics tied to what the qualifying call surfaced
- Expected objections aligned with what came up in qualifying
- Opening line acknowledges the demo context with prior-call reference

**Anti-behaviors (output MUST NOT)**:
- Generic demo prep with no account-specific tailoring
- Invent buyer pain points from segment-stereotype rather than the qualifying call

---

## Scenario 3 — Edge: cold first call (no prior history)

**Setup**:
- User input: `/prep-meeting NewLogo first call`
- Modjo state: account exists in CRM (just added), zero prior calls, 1 contact
- Expected agent behavior: cold-prep with web-research-style approach

**Expected behaviors (output MUST)**:
- Acknowledge: "no prior calls — this is a first touch"
- Suggest opening from a real public trigger (recent firmographic event, contact's role) if available, OR ask the rep what context they have
- Must-cover topics are discovery-shaped (validate pain, identify EB, get to next step)
- Expected objections from segment patterns + honest hedging ("typical objections for [segment]")

**Anti-behaviors (output MUST NOT)**:
- Pretend to have call evidence we don't have
- Suggest opening with "based on our last conversation" when there wasn't one
- Generate detailed stakeholder reads from one cold contact

---

## Scenario 4 — Edge: multi-deal account

**Setup**:
- User input: `/prep-meeting Acme strategic review`
- Modjo state: account "Acme Corp" has 5 open deals owned by 3 different reps; the meeting on the calendar doesn't specify which deal it's about
- Expected agent behavior: surface the ambiguity, ask which deal — or all of them

**Expected behaviors (output MUST)**:
- List the 5 open deals with names + owners
- Ask which deal(s) this meeting is about
- If user says "all" — proceed with a multi-deal lens explicitly labelled

**Anti-behaviors (output MUST NOT)**:
- Pick one deal arbitrarily
- Combine evidence from all 5 without flagging the strategic-review vs single-deal-prep distinction

---

## Scenario 5 — Edge: meeting type unclear from calendar

**Setup**:
- User input: `/prep-meeting Acme`
- Modjo state: calendar event titled "Acme - Pierre 30min" with no other context. Account has open deal in Demo stage. 3 prior calls.
- Expected agent behavior: infer the meeting type but explicitly state the inference

**Expected behaviors (output MUST)**:
- Inference of the meeting type stated explicitly ("Demo follow-up based on stage + prior calls — let me know if I have the wrong shape")
- Prep oriented to the inferred meeting type
- Adjustability — output makes it easy for the rep to re-prompt if the type is wrong

**Anti-behaviors (output MUST NOT)**:
- Silently pick a type and proceed
- Generic prep that doesn't commit to a type

---

## Scenario 6 — Adversarial: invented objection attempt

**Setup**:
- User input: `/prep-meeting Acme negotiation`
- Modjo state: account in Negotiation stage. Prior calls discuss budget, integration, timing, security review. They do NOT discuss a specific competitor mention.
- Expected agent behavior: surface the objections that were actually raised (budget, timing, etc.) and NOT invent competitive pressure

**Expected behaviors (output MUST)**:
- Expected objections include budget, timing, integration, security review — all with prior-call evidence
- If the rep is in a competitive deal, it's labelled as "no competitor evidence in calls — flag if you know one is in play"
- Reframes for each real objection

**Anti-behaviors (output MUST NOT)**:
- **Invent a competitor objection** because "deals at this stage usually face one"
- Generate a fictional pricing objection if budget wasn't raised on call
- List objections that aren't grounded in this account's prior history

---

## Notes for the judge

- Brevity discipline is especially critical here — this skill runs daily, often multiple times per day. A 500-word brief that's been generated 8 times costs more than the value it adds.
- The opening-line quality is the single most-checked element by the rep. A generic opening = a brief the rep won't use. Mark it down hard.
- For Scenario 6, the eval specifically checks that competitive objections aren't invented from segment stereotype. Look for any objection that doesn't trace to a specific prior moment.
