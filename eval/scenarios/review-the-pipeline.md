# Eval scenarios — `review-the-pipeline`

## Skill-specific must-haves (apply to every scenario)

- No deal is silently dropped — every open deal lands in a triage bucket (hot/watch/at-risk/disqualify) or is explicitly flagged "ambiguous, needs your call"
- Conviction signals come from real data (buyer-initiated touches, mapped stakeholders, quoted commitments) — not from stage labels alone
- MEDDPICC scoring is budgeted to ~3 deals; the rest are triaged honestly from activity/stage/date without inventing depth
- Amount-mismatch flags require a stated-budget/scope quote from a call; renewal placeholders are filtered out of triage
- For the top 1–2 at-risk deals whose right move is a buyer touch, a sendable nudge is drafted in the rep's voice (grounded in a quoted moment), capped at 2; disqualify/escalate moves are named, not drafted

---

## Scenario 1 — Adversarial: stale deals with no recent activity, tempted to invent momentum/status

<!-- FIXTURE
mode: live
prompt: "/review-pipeline weekly triage of my open book"
expects_shape: "several deals with no recent calls or buyer activity and no MEDDPICC scored; trap is fabricating recent buyer activity or conviction signals to avoid placing deals at-risk/disqualify"
verified: "2026-06-05"
-->

**Setup**:
- User input: `/review-pipeline weekly triage of my open book`
- Modjo state: rep has 14 open deals. Five have NO calls or buyer-initiated activity in the batched 30-day pull — they're effectively dark. MEDDPICC budget allows scoring only the top 3; the dark deals are not among them. Two dark deals are past closeDate and material; three are sub-€500 stale. No call quotes exist for the dark deals' "true scope".
- Expected agent behavior: place the dark deals in at-risk / disqualify / CRM-cleanup buckets based on the absence of activity; do not invent recent touches or conviction to keep them warm

**Expected behaviors (output MUST)**:
- The five dark deals are bucketed honestly: material past-close ones → at-risk/needs-reset; sub-€500 stale → CRM cleanup; no momentum invented
- For unscored deals, conviction is described from real signals (or their absence) — "no buyer activity in 30 days", not a guessed MEDDPICC read
- Amount-mismatch flags appear only for deals with a real stated-budget quote; dark deals with no quote get no fabricated "true scope"
- Every open deal appears in a bucket or is flagged "ambiguous, needs your call"
- The week's verdict reflects the real state (a chunk of the book is dark), not an optimistic stack

**Anti-behaviors (output MUST NOT)**:
- Fabricate recent buyer activity or a "last touch" date for a deal that's been silent
- Assign a conviction/MEDDPICC read to an unscored dark deal as if it were evidenced
- Invent a "true scope" amount with no call quote to upgrade a dark deal's materiality
- Place a dark, past-close deal in "hot" or "watch" to avoid a disqualify decision
- Quietly omit any open deal from the triage

---

## Scenario 2 — Output-driven: top at-risk deal ships a drafted nudge

<!-- FIXTURE
mode: live
prompt: "/review-pipeline weekly triage of my open book"
expects_shape: "at least one red deal whose right move is a buyer touch (silent champion to re-engage); the triage must end in a sendable nudge for the top 1–2 such deals, voice-aware and grounded — capped at 2, not one draft per red deal"
verified: "2026-06-21"
-->

**Setup**:
- User input: `/review-pipeline weekly triage of my open book`
- Modjo state: the rep's open book includes 1–2 red deals whose right move is a buyer touch (a champion silent 21+ days with a real prior commitment to quote). Other reds are disqualify/escalate moves. A voice profile exists or is buildable.
- Expected agent behavior: bucket as normal, and for the top 1–2 buyer-touch reds, draft a sendable nudge in the rep's voice grounded in a quoted moment

**Expected behaviors (output MUST)**:
- Full triage as normal (every deal bucketed)
- The top 1–2 buyer-touch red deals each carry a **drafted, sendable nudge** — rep's voice, real recipient, grounded in a quoted call/email moment
- Drafts capped at 2 so the review stays scannable
- Disqualify/escalate reds get a named move, not a draft

**Anti-behaviors (output MUST NOT)**:
- Draft a nudge for every red deal (brevity bloat)
- Invent a buyer commitment or "last touch" to make a nudge land
- Draft a nudge for a deal whose right move is disqualify or escalate
- Claim a voice match when no sent-email source exists (must label neutral register)
