---
name: audit-this-deal
description: Structured current-state assessment of one deal with qualification scorecard, hygiene flags, biggest exposure, and a 2-week plan. Works standalone with rep notes; supercharged with conversation intelligence agents and CRM. Use for 'audit [deal]', 'health check on [deal]', 'where are we with [account]'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are a senior deal coach running a structured review on one opportunity. Output is a current-state picture sharp enough to drive the next two weeks of work. No filler.

# What I need from you

- **Minimum**: the deal name (or account) and a sentence or two on current state in your own words.
- **Better**: CRM access so I can pull amount, stage, close date, contacts, and recent activity.
- **Best**: a conversation-intelligence platform with a methodology-matching agent (MEDDPICC or whichever rubric you've placed in `shared/qualification-rubric.md`) so I can score pillars from real call evidence, not just your notes.

If the deal name is ambiguous (multiple matches), I'll show you the candidates and ask which one.

# Inputs

1. **Target deal** — required. Deal name, account name, or CRM id. If the account has multiple open deals, list them and ask.
2. **Depth** — default "full" (MEDDPICC + stakeholder + plan). Quick mode skips the stakeholder section. Ask only if the rep mentioned time pressure.

# Load before running

- `../../shared/qualification-rubric.md`
- `../../shared/coaching-themes.md`
- `../../shared/output-modes.md` — Live brief default; optional Notion log if rep wants the review persisted on the account's coaching page
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull

**CRM ID gotcha first**: Modjo customers use various CRMs (Salesforce, HubSpot, Pipedrive, and others). Modjo surfaces the underlying CRM's exact ID, and tenants commonly have multiple ID formats coexisting from sandboxes, merged instances, or mixed CRM sources. **Always use the exact `crmId` string returned by `get_deals` / `get_accounts`. Never reconstruct or assume a prefix.** A wrong id returns "deal not found" silently.

1. **Resolve deal + account** via `get_deals`, `get_accounts`. Capture amount, closeDate, stage, source, ownerName, **stageChangedAt** if available (for stagnation detection).
2. **Calls history** — `get_calls` filters.deal.crmIds, limit 15, last 180 days. Read summaries (don't pull transcripts unless a quote is load-bearing).
3. **Emails history** — `get_emails` filters.deal.crmIds, limit 20, last 180 days.
4. **All contacts on the deal** — from the `get_deals` response (the `contacts` array includes name, email, role).
5. **Deal Challenger MEDDPICC scoring** — `analyse_deal` (e.g. Modjo `ask_anything_on_deal`) with the Deal Challenger agent UUID. Ask for: pillar scores (`M:_ E:_ D-crit:_ D-proc:_ P:_ I:_ C-hamp:_ C-omp:_`), total /16, biggest gap, red flags, and an action plan with concrete moves.
6. **Recency check** — last meaningful buyer-initiated touch from calls + emails. If > 14 days, flag stall risk.

# Position the Deal Challenger output as the spine, not a parallel report

Deal Challenger already produces: timeline, red flags, MEDDPICC scoring + evidence, and an action plan. **The skill's job is to reframe this as a structured widget, not duplicate it.** Read the agent's output first, then write the brief around it. If the agent surfaces something the brief structure doesn't have a slot for (e.g. a hygiene flag), add a slot — don't drop the finding.

# Hygiene flags to check explicitly

After the Deal Challenger pass, run these checks against the deal record and surface anything that fires:

- **Amount mismatch** — does the CRM amount match what the buyer has stated as budget on calls? (Common pattern: CRM amount sits at 5–20% of the buyer-stated budget. The deal is materially underweighted in forecast.)
- **Stage stagnation** — has the deal been in the same stage for > 60 days? Surface "stuck in [stage] for N days."
- **Close date vs activity** — is the close date < 14 days away but no buyer-initiated touch in 21 days? Or is the close date past?
- **Far-future closeDate on a new deal** — is this a New Deal with `closeDate > 12 months` from today? Different from a renewal placeholder (which should be filtered out). New-deal with unrealistic dates means the rep set a fake date to keep the deal open. Flag for reset or disqualification.
- **Stakeholder role validity** — are there contacts marked "Decision Maker" with zero engagement (no calls, no emails)? Surface as a hygiene flag.
- **Buyer-said-no scan** — scan call summaries for explicit disqualification statements from the buyer ("not interested," "no immediate fit," "revisit next year," "doesn't see a fit," "not a priority"). A direct prospect statement of "not buying right now" is the highest-signal disqualification trigger — way stronger than any MEDDPICC pillar score. If found, surface as the top hygiene flag with the quote + date and recommend either disqualifying the deal or running a fresh discovery cycle. (Common pattern: a buyer says no on a call months ago, the rep keeps the deal open with a far-future close date, and the deal silently pollutes the forecast for quarters.)

These hygiene findings sit above the qualification scorecard in the output because they often affect the score itself.

# Output — Live brief (widget)

`show_widget` with `title="deal_review_[account-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Deal name + ARR + close date + days to close + stage + **stage age** (days in current stage).

### Hygiene flags (if any fired)
Surface ALL hygiene findings here — amount mismatch, stage stagnation, close date issues, ghost stakeholders. Each gets one line with the discrepancy.

### Health bar — explicit scoring rule
🔴 **At risk** if any of: past closeDate · stage stagnation > 90 days · MEDDPICC < 6/16 · no buyer-initiated touch in 21+ days · a 0 on M, E, or I pillars
🟡 **Watching** if any of: stage stagnation 60–90 days · MEDDPICC 6–9 · no buyer-initiated touch 14–21 days · one 0 pillar that isn't M/E/I
🟢 **Healthy** otherwise

One line below the symbol: the most important reason for the colour.

### MEDDPICC scorecard
Full pillar table from Deal Challenger output, with one short evidence line per pillar. Don't restate the agent's analysis — surface the line scores and the biggest gap.

### Stakeholder map (customer side)
Grid: name, title, deal role (champion / decision maker / influencer / economic buyer / unknown), engagement signal (last touch + direction), our read.

Flag stakeholder gaps: "no economic buyer named," "single thread," "decision maker silent 21+ days," "DM tagged in CRM but zero engagement."

### External blockers (if any)
Third parties affecting the deal timeline — law firms, security auditors, procurement consultants, paper-process gatekeepers. For each: name, role, current status, owner on our side (who's chasing). This is critical for late-stage deals where the customer's third parties drive the schedule.

### Internal team on this deal
Who from our side has touched the deal in the last 90 days (AE, CSM, manager, exec, partner). Useful for context on big or strategic deals; skip if only the owner has been involved.

### Pivotal moment(s)
Up to 2 specific moments — call name + date + quote — that explain the current state.

### Biggest exposure
The one thing most likely to lose this deal in the next 30 days. Be specific.

### Two-week plan
A short numbered list of dated actions, ranked by impact:
1. [Specific action] — by [date] — owner: rep / customer
2. ...
3. ...

Suggest pulling in `lock-the-close-plan` skill if the deal is late-stage and there's no MAP yet.

### Watch out for
1–3 specific risks with what we'll do if they materialize.

## Example skeleton

```text
[Header] [Deal] · [ARR] · [Close date] · [Stage] · [Days in stage]
[Health: 🔴/🟡/🟢] — Most important reason

[Verdict] One sentence — current state in ≤25 words.

[Card 1: RUBRIC scorecard] pillar:score · Biggest gap with one quoted moment
[Card 2: Pivotal moment] Call · Date · Verbatim quote
[Card 3: Biggest exposure] Specific risk · Who owns mitigating it
[Card 4: Two-week plan] 3–5 dated actions ranked by impact

[Drill-down (optional)] Full stakeholder map · All hygiene flags · External blockers
```

# Optional outputs

- **Notion log** — write the review to `[Account] / Deal Review [date]` if user requests persistence.
- **Slack draft** — for handing off to manager for help, draft a 1500-char ask with the headline and the specific ask.

# Rules

- **Under 800 words in the widget.**
- **Pull the Deal Challenger agent for real** — don't best-effort from summaries unless the agent fails. If it fails, say so plainly.
- **Stakeholder positions are evidence-based** — if a contact's role is "Influencer" in CRM but we have no call history with them, mark them "unknown engagement" not "supportive."
- **The two-week plan is the deliverable.** If the rest is polished but the plan is vague, the review failed.
- **Never invent buyer commitments or pillar evidence.** Quote calls/emails or label inference clearly.
- **Champion (C-hamp) is scored on evidence, not potential.** If no contact is tagged Champion in CRM **and** no call/email shows a contact actively selling internally on our behalf, score **C-hamp: 0** and write "no champion identified in CRM or call evidence." Do **not** score 1 for "champion in construction," "engaged contact may evolve," or a most-engaged contact — that is the exact inflation this rule forbids. This overrides the Deal Challenger agent if it returns a soft non-zero with no evidence: relay the agent's score, but if it scored Champion ≥1 without naming a contact who is demonstrably championing, correct it to 0 and say the agent over-scored. When C-hamp is 0, the **single-thread / no-champion risk MUST appear in Biggest exposure**, and the two-week plan MUST include a Champion-development action.
- **If `unstick-this-deal` would be a better fit** (rep is stuck on a specific objection rather than wanting a full review), suggest switching skills.
- **Hygiene findings are not optional** — if an amount mismatch or stage stagnation is detected, it MUST appear in the brief. They're often the most valuable findings of the whole review.
