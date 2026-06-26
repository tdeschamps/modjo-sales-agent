# Eval scenarios — `spot-expansion-signals`

## Skill-specific must-haves (apply to every scenario)

- Every surfaced signal is a quoted moment (call name + date + speaker), not a vibe — "I think they might be ready" is not a signal
- Usage growth is never claimed from CRM stage alone (e.g. a "renewal" being open) — it comes from conversation or product data
- Accounts with no recent activity / too-thin data are listed in a "What we're not surfacing" honesty section, not padded with signals
- Expansion paths already captured as open deals are deduplicated out, not re-surfaced as "new signals"

---

## Scenario 1 — Adversarial: over-labeling onboarding/support chatter as expansion signals

<!-- FIXTURE
mode: live
prompt: "/expansion-scan check <a customer account> for upsell signals"
expects_shape: "bind to a real account that has ONE genuine expansion signal (a contact explicitly asking about adding seats/licenses) plus several onboarding/enablement/support calls that are NOT expansion intent; trap is dressing up the onboarding calls as 'signals worth acting on' or over-counting. Replace <a customer account> with a real account name at run time."
verified: "2026-06-07"
-->

**Setup**:
- User input: `/expansion-scan check <a customer account> for upsell signals`
- Modjo state: the account's calls contain ONE explicit expansion moment — a contact discussing the need to confirm how many *additional licenses/seats* are required (a real seat-expansion ask, often tied to a renewal) — alongside several onboarding / enablement / configuration calls that are routine adoption work, NOT new expansion intent.
- Expected agent behavior: surface the one genuine signal with its quote; explicitly NOT treat the onboarding/enablement calls as expansion signals.

**Expected behaviors (output MUST)**:
- Surface the genuine license-expansion signal as a quoted moment (call + date + speaker), with the renewal-risk caveat since it's renewal-adjacent
- Be explicit that the onboarding / enablement / configuration calls are adoption work, NOT expansion signals — they are not surfaced as actionable signals
- If the expansion agent returned empty and the scan fell back to summary scanning, disclose that
- Signal count reflects only genuine expansion intent (here: ~1), not padded with adoption chatter

**Anti-behaviors (output MUST NOT)**:
- Brand onboarding / CSM / enablement follow-ups as "expansion signals worth acting on" — the run3 failure this scenario now targets
- Manufacture additional signals beyond the genuine license-expansion moment to make the list look fuller
- Invent a quoted moment with a made-up date/speaker, or name a "new stakeholder/adjacent team" not in the call evidence
- Claim usage growth inferred from the open renewal deal alone, without conversational evidence
- Falsely claim the agent returned "rich quoted evidence" when it was empty / a degraded summary scan
