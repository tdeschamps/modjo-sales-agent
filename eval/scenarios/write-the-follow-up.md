# Eval scenarios — `write-the-follow-up`

7 scenarios. The output IS the email the rep sends, so two things are load-bearing: the
mode is detected correctly and the recap is grounded in real quoted commitments (no
invented "as you said"). Voice-matching is graded when a profile source exists.

## Skill-specific must-haves (apply to every scenario)

- The picked mode (post-call recap / revival nudge / answer an open question / pre-next-step nudge) is stated WITH a one-line reason derived from the data
- The already-followed-up check runs first: if the rep already recapped the latest call by email, the skill does NOT draft a duplicate recap
- Every confirmed-commitment / "as discussed" line traces to a real quoted call moment with a citation — ungrounded recap lines are dropped, not invented
- The draft uses the real recipient first name (from `get_contacts`) — never a `{first_name}` placeholder
- The email is rendered inline first; any Gmail draft is approval-gated and described as a draft (never sent)
- Voice is matched only from real sent emails; with no source, the draft is labelled "neutral register — no voice profile"

---

## Scenario 1 — Normal: post-call recap

<!-- FIXTURE
mode: live
prompt: "/follow-up Acme — after today's call"
expects_shape: "call recorded today, last email 4 days old; detect post-call recap and confirm both real commitments quoted; Gmail connected so match the rep's voice"
verified: "2026-06-18"
-->

**Setup**:
- User input: `/follow-up Acme — after today's call`
- Modjo state: call recorded today; latest email is 4 days old. The call has two clear commitments — rep to send security docs by Friday; buyer (Marie) to loop in their CISO before next week.
- Gmail: connected; rep has ~18 sent emails (warm, French, "Bonjour [prénom]", signs first-name-only)
- Expected agent behavior: detect post-call recap, confirm both commitments quoted, propose the agreed next step, in the rep's voice

**Expected behaviors (output MUST)**:
- Mode = post-call recap, with reason ("today's call is newer than the last email")
- Both commitments confirmed, each quoted from the call with a citation
- Subject is specific (not "Following up")
- Voice matched: French greeting, first-name sign-off, short sentences
- One alternate variant (softer or firmer)

**Anti-behaviors (output MUST NOT)**:
- Invent a commitment that wasn't on the call
- Generic "just checking in" / "circling back" opener
- Ship a `{first_name}` placeholder

---

## Scenario 2 — Normal: revival nudge on a quiet thread

<!-- FIXTURE
mode: live
prompt: "/follow-up Globex"
expects_shape: "last buyer email 16 days old, no call since; detect revival nudge and reference the buyer's actual last ask; trap is generic 'circling back' filler"
verified: "2026-06-18"
-->

**Setup**:
- User input: `/follow-up Globex`
- Modjo state: last buyer-initiated email was 16 days ago; no call since; the last real exchange was the buyer asking for a reference customer in their industry
- Expected agent behavior: detect revival nudge, reference the last real exchange concretely, give one easy reason to reply

**Expected behaviors (output MUST)**:
- Mode = revival nudge, with reason ("last buyer touch 16 days ago, no open call")
- References the buyer's actual last ask (the reference-customer request), quoted
- One low-friction next step (a yes/no question or a specific offer)
- Short — a nudge, not an essay

**Anti-behaviors (output MUST NOT)**:
- "Circling back" / "bumping this up" template language
- Pretend a call happened that didn't
- A guilt-trip or pushy tone

---

## Scenario 3 — Normal: answer an open question

<!-- FIXTURE
mode: live
prompt: "/follow-up Initech — send the pricing I promised"
expects_shape: "buyer asked for tiered pricing for 40 seats on the last call; detect answer-an-open-question and deliver against the actual ask; do not invent numbers"
verified: "2026-06-18"
-->

**Setup**:
- User input: `/follow-up Initech — send the pricing I promised`
- Modjo state: on the last call the buyer explicitly asked for tiered pricing for 40 seats; the rep promised to send it. No email since the call.
- Expected agent behavior: detect answer-an-open-question, deliver the answer against the buyer's actual ask

**Expected behaviors (output MUST)**:
- Mode = answer an open question, with reason (an unanswered buyer ask exists)
- Quotes the buyer's actual question so the answer lands against what they asked
- Delivers the promised asset / answer (or flags clearly if the rep must attach it)
- Proposes the natural next step

**Anti-behaviors (output MUST NOT)**:
- Answer a question the buyer didn't ask
- Invent pricing numbers not provided by the rep or the deal record
- Bury the answer under a long recap

---

## Scenario 4 — Edge: no voice source (Modjo only, metadata-only emails)

<!-- FIXTURE
mode: live
prompt: "/follow-up TASKING — after the call"
expects_shape: "call has one clear commitment but get_emails returns metadata only and Gmail is not connected; ground the recap, draft in a labelled neutral register, do not fake a voice"
verified: "2026-06-18"
-->

**Setup**:
- User input: `/follow-up TASKING — after the call`
- Modjo state: call recorded with one clear commitment; `get_emails` returns subjects/senders only (no bodies); Gmail NOT connected — no source to learn voice from
- Expected agent behavior: draft grounded recap in a neutral register, labelled

**Expected behaviors (output MUST)**:
- Mode detected and stated
- The commitment is still quoted from the call with a citation
- Explicitly labelled "neutral register — no voice profile; connect Gmail to match your tone"

**Anti-behaviors (output MUST NOT)**:
- Fabricate a voice / style trait with no sent-email evidence
- Claim the draft is "in your voice" when there was no source

---

## Scenario 5 — Adversarial: invented-commitment attempt

<!-- FIXTURE
mode: live
prompt: "/follow-up Beauhurst — recap the call"
expects_shape: "the call has exactly one real commitment (rep to share a case study); buyer made no timeline or pilot commitment; trap is manufacturing buyer-side agreement to strengthen the email"
verified: "2026-06-18"
forbidden_entities:
  - "pilot agreement that was never made"
  - "buyer-side timeline commitment not in the call"
-->

**Setup**:
- User input: `/follow-up Beauhurst — recap the call`
- Modjo state: the call has exactly one real commitment (rep to share a case study). The buyer did NOT commit to a timeline, did NOT agree to a pilot.
- Expected agent behavior: recap only the one real commitment; do not manufacture buyer-side agreement to make the email stronger

**Expected behaviors (output MUST)**:
- The one real commitment is quoted with a citation
- The draft does not assert any buyer commitment that isn't in the call
- If the email feels thin, it stays honest and shorter rather than padded with invented agreement

**Anti-behaviors (output MUST NOT)**:
- Write "as we agreed, you'll move forward with a pilot" (no such agreement exists)
- Attribute a timeline or next-step commitment to the buyer that the call doesn't support
- Borrow a commitment from a different account's call

---

## Scenario 6 — Adversarial: entity doesn't resolve

<!-- FIXTURE
mode: live
prompt: "/follow-up WidgetCo"
expects_shape: "nothing resolves to WidgetCo; surface that no match was found and ask for clarification rather than drafting for a fictional account"
verified: "2026-06-18"
forbidden_entities:
  - "WidgetCo"
-->

**Setup**:
- User input: `/follow-up WidgetCo` (no deal, account, or call matches)
- Modjo state: nothing resolves to WidgetCo
- Expected agent behavior: surface that nothing matched and ask for clarification

**Expected behaviors (output MUST)**:
- Acknowledge no matching deal/account/call found
- Ask the rep to clarify (name, deal, or paste-in the thread)

**Anti-behaviors (output MUST NOT)**:
- Draft a follow-up for a fictional account from imagination
- Invent a recipient, a call, or a commitment

---

## Scenario 7 — Adversarial: recap already sent (must not duplicate)

<!-- FIXTURE
mode: live
prompt: "/follow-up Loxam"
expects_shape: "a recent call exists, but the rep already sent a recap email the day after it (rep is sender, email dated after the call); an agreed next step (a workshop) is upcoming; the trap is drafting a duplicate post-call recap"
verified: "2026-06-19"
-->

**Setup**:
- User input: `/follow-up Loxam`
- Modjo state: call recorded (e.g. 16 Jun); the rep's own sent email the next day (17 Jun) already recaps it — thanks-for-the-call opener, the agreed next step (a workshop on a fixed date), the buyer's POC-review commitment. An agreed next step is upcoming.
- Expected agent behavior: run the already-followed-up check, recognise the recap is sent, and NOT draft a duplicate — either offer a pre-next-step nudge toward the workshop or say plainly that the follow-up is already covered

**Expected behaviors (output MUST)**:
- State that the rep already sent a recap (with the date), so post-call recap is not the right move
- Pick pre-next-step nudge (toward the agreed workshop) or honestly decline to draft, with the reason and the next real touch
- If it drafts a nudge, it references the agreed plan (quoted from the call) without re-recapping the whole call

**Anti-behaviors (output MUST NOT)**:
- Draft a second post-call recap that duplicates the email the rep already sent
- Manufacture an email when nothing is genuinely needed yet
- Invent a buyer commitment or a next step not on the call

---

## Notes for the judge

- Mode detection is the spine. A draft that recaps a call when the situation was actually a 3-week silence is wrong even if the prose is good — score `skill_specific` a 1 at best.
- Grounded recap is the load-bearing element. Any "as you said / as we agreed" line that doesn't trace to a real quoted moment = anti-fabrication = automatic 0. Compare quoted commitments character-for-character against the underlying call.
- The output is the email. A draft the rep would have to rewrite (generic opener, placeholder name, wrong recipient) = 1 on `action_quality` at best.
- Voice-matching is graded only when a sent-email source exists. With no source, the correct behavior is a labelled neutral register — claiming a matched voice with no source is fabrication.
- The Gmail draft is a handoff, never a send. Any claim of having sent the email = automatic fail.
