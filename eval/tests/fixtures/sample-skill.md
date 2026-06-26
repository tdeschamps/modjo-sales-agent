# Eval scenarios — `sample-skill`

## Skill-specific must-haves (apply to every scenario)

- Output includes a verdict line at the top

---

## Scenario 1 — Normal: live deal

<!-- FIXTURE
mode: live
prompt: "/audit-deal Planity France"
deal_crmId: "006MI00000toSpRYAU"
expects_shape: "open deal, no Champion contact"
predicates:
  - deal_status: ["Open"]
  - no_contact_role: "Champion"
verified: "2026-06-04"
-->

**Setup**:
- User input: `/audit-deal Planity France`
- Modjo state: deal exists, no champion tagged.

**Expected behaviors (output MUST)**:
- Lead with a verdict line
- Score Champion 0 with "no champion identified"

**Anti-behaviors (output MUST NOT)**:
- Invent a champion
- Score Champion above 0 without evidence

---

## Scenario 2 — Synthetic: injected state

<!-- FIXTURE
mode: synthetic
prompt: "/audit-deal Initech Q4"
synthetic_context: |
  Deal "Initech Q4": stage Negotiation, CRM amount EUR5000.
  Calls show buyer negotiating ~EUR80k.
expects_shape: "hygiene-heavy deal (synthetic)"
verified: "2026-06-04"
-->

**Setup**:
- User input: `/audit-deal Initech Q4`

**Expected behaviors (output MUST)**:
- Surface the amount mismatch

**Anti-behaviors (output MUST NOT)**:
- Treat EUR5000 as the real deal size
