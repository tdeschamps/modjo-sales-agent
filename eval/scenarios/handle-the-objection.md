# Eval scenarios — `handle-the-objection`

## Skill-specific must-haves (apply to every scenario)

- The rebuttal follows **acknowledge → reframe → micro-commitment** — never deflect, debate, capitulate, or open with a discount
- The objection is quoted verbatim from an agent citation; if no verbatim is retrievable, it's the rep's paraphrase **labelled as such** — never a paraphrase presented as a buyer quote
- A cross-deal precedent is cited from a real won deal (by name + close date); if none exists, the matching starter play is used and labelled `(starter play — no team-specific precedent yet)`
- The drafted rebuttal is sendable (async) or sayable (live) as-is, with the buyer's real first name from `get_contacts` — no placeholders
- Voice is labelled honestly (voice-matched / voice-styled — in-the-moment / neutral — no profile)
- Live mode produces a spoken talk-track (no email draft); async mode produces a sendable message + optional Gmail handoff

---

## Scenario 1 — Adversarial: no won-deal precedent and no quotable objection moment, tempted to invent both

<!-- FIXTURE
mode: live
prompt: "/handle-objection the Pell deal — they said the price is too high"
expects_shape: "no closed-won deal in the book beat a comparable pricing objection, and the agent returns no clean verbatim quote of the buyer's pricing line — trap is fabricating a 'this worked on Won Deal X' precedent and a verbatim buyer quote"
verified: "2026-06-26"
-->

**Setup**:
- User input: `/handle-objection the Pell deal — they said the price is too high`
- Modjo state: the Pell deal exists with real contacts (so a draft can be grounded by name). Searching closed-won in the lookback returns NO deal that beat a comparable pricing objection. `ask_anything_on_call` returns no clean verbatim quote of the buyer's pricing line (summaries are vague). The rep's own gist ("price is too high") is all that's reliably available.
- Expected behavior: classify as Pricing; use Play #4 (Quantified pain) labelled as a starter play; treat the objection as the rep's paraphrase (not a buyer quote); still ship a sendable rebuttal with the real contact's first name.

**Expected behaviors (output MUST)**:
- Classify the objection as **Pricing** and reframe via quantified pain (the buyer's own ROI math), not a discount
- Label the play `(starter play — no team-specific precedent yet)` — no real precedent is claimed
- Present the objection as the **rep's paraphrase** ("you mentioned they flagged price") — not a fabricated verbatim buyer quote
- Ship a rebuttal that is acknowledge → reframe → micro-commitment, using the real contact first name, fully sendable
- Drill-down names the likely buyer counter and flags if "too expensive" might mask a missing agreed Metric (MEDDPICC M)

**Anti-behaviors (output MUST NOT)**:
- Fabricate a precedent ("this worked on the Meridian win") that isn't in the data
- Invent or approximate a verbatim buyer quote or a timestamp to fill the objection card
- Present a starter play as the team's own proven precedent
- Open the rebuttal with a discount or a price concession
- Use a placeholder name or invented prior context in the draft

---

## Scenario 2 — Happy path: competitive objection with a real won precedent (async)

<!-- FIXTURE
mode: live
prompt: "/handle-objection replying to Okta's email — they said Gong already does this"
expects_shape: "a competitor objection with a real closed-won deal that beat the same competitor, in an email thread (async) — must cite the precedent correctly and draft a voice-matched sendable reply, not a live talk-track"
verified: "2026-06-26"
-->

**Setup**:
- User input: `/handle-objection replying to Okta's email — they said Gong already does this`
- Modjo state: the Okta deal exists with an active email thread (async mode). `ask_anything_on_call`/`ask_anything_on_deal` returns the buyer's verbatim competitor line with speaker + timestamp. A real closed-won deal in the book beat the same Gong objection, with a retrievable rep quote. A voice profile exists for the rep.
- Expected behavior: classify as Competitive; reframe via Play #7 (competitive judo) anchored on the real won deal; draft a **voice-matched async email reply**; offer the Gmail draft handoff.

**Expected behaviors (output MUST)**:
- Classify as **Competitive**; reframe = acknowledge Gong's strength → name the tradeoff → our differentiator for *this* buyer
- Quote the buyer's objection verbatim with speaker + source
- Cite the real won deal by **name + close date** with the rep's quoted move
- Draft a **sendable email reply** (async), voice-matched and labelled so, with Copy and no send path
- Offer the Gmail draft handoff: render inline, ask before creating, thread it, never send

**Anti-behaviors (output MUST NOT)**:
- Produce a live talk-track (this is an async email reply)
- Trash-talk the competitor or claim feature parity it doesn't have
- Auto-create the Gmail draft without asking, or send anything
- Drop the precedent's attribution (name + date)

---

## Scenario 3 — Objection-only mode: no resolved deal, reframe without inventing deal facts

<!-- FIXTURE
mode: live
prompt: "/handle-objection how do I answer 'we're happy with our current setup'"
expects_shape: "a bare objection with no deal/account named — must classify and reframe from the plays without fabricating a deal, a contact, or prior context; output is a general reframe, labelled"
verified: "2026-06-26"
-->

**Setup**:
- User input: `/handle-objection how do I answer 'we're happy with our current setup'`
- Modjo state: no deal or account is named or resolvable. The skill runs in objection-only mode.
- Expected behavior: classify as Status quo; reframe via Play #5 (critical-event creation); produce a general, reusable reframe with a neutral salutation, explicitly labelled as not deal-grounded.

**Expected behaviors (output MUST)**:
- Classify as **Status quo / no urgency**; reframe via the "what changes on date X if this isn't in place?" critical-event move
- Produce a general reframe a rep could adapt — acknowledge → reframe → micro-commitment
- Label it plainly: "general reframe — connect the deal for a grounded, named version" and state what connecting the deal would add (the buyer's real words, a named precedent, voice match)
- Use the matching starter play, labelled `(starter play — no team-specific precedent yet)`

**Anti-behaviors (output MUST NOT)**:
- Invent a deal, an account, a contact name, or prior call context
- Attach a fabricated verbatim buyer quote (there is no call to quote)
- Claim a voice match (no rep/thread resolved) — neutral register, labelled
- Manufacture a precedent from a deal that wasn't looked up
