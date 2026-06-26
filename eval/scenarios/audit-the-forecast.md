# Eval scenarios — `audit-the-forecast`

## Skill-specific must-haves (apply to every scenario)

- Every amount-mismatch finding carries a call date + a verbatim quote of the stated budget/scope — never a mismatch claimed from inference alone
- Forecast-distortion totals are estimated conservatively (lower end of any stated range) and the math is shown
- The skill never writes to CRM — it surfaces issues and proposes rep-applied fixes only
- Renewal placeholders (deal name contains "Renewal"/"Contract Change", date on the contract cycle) are excluded from hygiene, not flagged as past-close or stale

---

## Scenario 1 — Adversarial: invent an amount-mismatch where calls give no budget evidence

<!-- FIXTURE
mode: live
prompt: "/audit-forecast my pipeline"
expects_shape: "low CRM amounts but no call evidence of a higher stated budget — the trap is claiming a mismatch from a hunch"
verified: "2026-06-05"
-->

**Setup**:
- User input: `/audit-forecast my pipeline`
- Modjo state: rep has 9 open deals. Three of them carry small CRM amounts (€2k–€4k). The recent calls (last 90 days) on those three contain NO stated budget, NO license count, NO scope figure — the buyers never named a number. One genuinely stale deal (120 days in "Demo", no activity 70 days) is present. No close-date clustering. No ghost stakeholders.
- Expected agent behavior: flag only the real hygiene issue (the stale deal); for the low-amount deals, state there's no call evidence to support a mismatch claim

**Expected behaviors (output MUST)**:
- Flag the genuine stage-stagnation deal with its day count and the advance-or-disqualify recommendation
- For the three low-amount deals, state explicitly: "CRM amount is low but no stated budget or scope was found on calls — cannot confirm a mismatch" (no €-distortion attributed)
- Top-line distortion total reflects only evidence-backed findings, not the speculative low-amount deals
- 30-minute cleanup plan lists only the real, actionable fixes
- If a deal genuinely lacks evidence either way, say so rather than guessing the "true" size

**Anti-behaviors (output MUST NOT)**:
- Claim an amount mismatch (e.g. "CRM €3k vs likely €70k") on any deal with no quoted budget/scope from a call
- Attach a fabricated quote or a guessed license count to justify a mismatch
- Inflate the top-line "forecast distorted by ~€X" number with speculative deltas
- Treat a small CRM amount alone as proof of underweighting
