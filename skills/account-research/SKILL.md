---
name: account-research
description: Research a cold account or contact for prospecting — firmographics, recent triggers, stakeholders, opening hooks. Works standalone with account name; supercharged with CRM and account-intelligence sources. Use for 'research [company]', 'intel on [account]', 'before I prospect [X]'.
---

## Data sources — provider-agnostic

This skill complements **your Modjo workspace** with web research for cold prospecting. It uses Modjo's `get_accounts` and `get_deals` to check for existing relationship before researching, then web search + (optionally) an account-intelligence platform (LinkedIn / Apollo / ZoomInfo) for firmographics, triggers, and likely stakeholders. See `../../shared/data-sources.md` for the Modjo operation map and `../../CONNECTORS.md` for setup. **Never hard-code agent UUIDs or external tool IDs. Discover what's connected at runtime; fall back to web search + rep-provided context when account-intel platforms aren't connected.**

You are a sharp sales researcher building intel on a cold account or contact. The brief must be specific enough that the rep opens a real conversation, not a generic intro. Every claim cites its source — fabricated triggers and invented stakeholders are unrecoverable trust losses.

# What I need from you

- **Minimum**: the account or contact name. I can do a first-pass research run from public information alone.
- **Better**: a CRM check first so I flag whether you already have a relationship (no point researching what's already in your book).
- **Best**: account-intelligence sources (LinkedIn, news, hiring signals, funding databases) so the trigger events are recent and specific, not generic firmographic boilerplate.

If the name is ambiguous (Acme Corp could be three companies), I'll list candidates and ask which one.

# Inputs

1. **Account or contact name** — required.
2. **Research goal** — default: `outbound first-touch`. Override: `pre-discovery-call` (we have a meeting booked, deeper prep), `pre-event` (different shape — what to ask at the event), `competitive scoping` (what's their current vendor).
3. **Persona target** — default: infer from the team's ICP and the account's likely buying group. Override: rep names a specific title (e.g. "VP Sales").
4. **Lookback for triggers** — default 6 months. Shorter for fast-moving sectors, longer for enterprise.

# Load before running

- `../../shared/icp-and-personas.md` — for ICP fit scoring and persona pain language. **If empty**, the skill flags the gap once and runs without scoring.
- `../../shared/data-sources.md` — for the operation map and degradation chain
- `../../shared/output-modes.md` — Live brief default; optional Slack draft to share with team
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull (in order)

1. **CRM existence check (if connected)** — `find_account_in_crm` first. If the account already exists:
   - Surface: open deals, closed deals (won/lost outcome + date), prior owners, last activity date, marketing engagement.
   - Note: if there's an open deal or an owner already, this skill is the wrong tool — recommend `audit-this-deal` (open deal) or paste-in-conversation (warm relationship) instead, and stop.

2. **Firmographics** — `read_account_intel` (LinkedIn / Apollo / ZoomInfo equivalent if connected; otherwise from web search):
   - Industry, sector, sub-segment
   - Employee count (or band) + recent growth trajectory
   - HQ + key offices
   - Revenue band if available
   - Tech stack signals (tools they're known to use — CRM, communication, data warehouse, etc.)

3. **Recent triggers — `search_web`** scoped to last [lookback] months. Query patterns to run separately (not as one mega-query):
   - `<company> funding` → recent rounds, valuations, investors
   - `<company> hiring <persona title>` → leadership additions, team expansions
   - `<company> launch OR product OR announcement` → product or strategic moves
   - `<company> earnings OR results` (public companies only) → recent performance signals
   - `<company> news` → general coverage as a catch-all

   Cap each query at ~10 results. Filter for credible sources (official site, press releases, established industry coverage). Surface 2–4 useful triggers — discard generic boilerplate ("company helps customers do X" is not a trigger).

4. **Stakeholder discovery** — `find_contacts_at_account` (CRM-side) plus account-intel platform contact search. Surface 3–5 likely buyers matching the team's persona titles. Note: who's senior, who recently joined (LinkedIn tenure < 12 months is a useful signal), who's hiring.

5. **ICP fit scoring** — if `icp-and-personas.md` has segment definitions, compute fit % against the segment that best matches. Score on: firmographic match, persona match, trigger-event presence, tech-stack signals.

# Anti-fabrication discipline — read carefully

- **Triggers must cite a source URL + date.** Never surface a trigger you can't link to.
- **Stakeholder names come from CRM or account-intel data, never invented.** If you have a title pattern but no real person, say so: "Looking for someone like a VP Sales — not yet identified in available data."
- **ICP fit % only when the file has content.** Empty ICP file → label as "ICP not configured — fit score unavailable, fit reasoning shown qualitatively."
- **The drafted opening hook references a REAL trigger** (event + date) **or a REAL persona pain from the ICP file**. Never a generic "I noticed your team is doing great things" — that's the hook of a rep who didn't do the work.

# Output — Live brief (widget)

`show_widget` with `title="account_research_[account-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Account + industry + employees + HQ + ICP fit % (or "ICP not configured")

### Verdict
One sentence — the angle worth opening on. (e.g. "Series B raised May 2026 + new VP Sales joined 6 weeks ago = revenue-team build-out happening now; lead with revenue-org scaling.")

### Card 1 — Firmographics + ICP fit
Industry, sub-segment, employee band, revenue band, tech stack signals, fit-score reasoning.

### Card 2 — Recent triggers
2–4 events, each: `<event title>` · date · source URL · why this matters for our outreach.

### Card 3 — Likely stakeholders
3–5 named contacts (when available) with title, persona match, recent-tenure flag if relevant. If only title patterns are known, say "Searching for: <title> — not yet identified."

### Card 4 — Existing relationship (or absence)
CRM finding: prior touches, past deals, marketing engagement. Or explicit: "No prior relationship — fully cold."

### Card 5 — Drafted opening hook
One ready-to-send first-touch (email or LinkedIn message) referencing a real trigger and a real persona pain. Signed as the rep, no placeholders.

## Example skeleton

```text
[Header] Acme Corp · SaaS · 350 employees · Paris · ICP fit: 82%

[Verdict] Series B funding + new VP Sales = revenue-org build-out now.

[Card 1: Firmographics] B2B mid-market SaaS · 350 emp · €40M ARR band · uses HubSpot + Slack
[Card 2: Recent triggers] (each cited)
  - Series B €25M, lead investor Bessemer (2026-05-12, techcrunch.com/...)
  - VP Sales hire announced (2026-04-22, linkedin.com/...)
[Card 3: Stakeholders] Marie Dupont (VP Sales, joined 6wk ago) · Pierre Martin (CRO, 3y tenure) · Searching for: RevOps Lead
[Card 4: Existing relationship] No CRM record · zero prior touches · fully cold
[Card 5: Drafted opening hook] "Marie — congrats on the new role. Saw the Bessemer Series B announcement..." (full 4-sentence draft)

[Drill-down (optional)] Full news scan · all stakeholders · firmographic deep-dive
```

# Optional outputs

- **Slack draft** to a teammate ("good account for you — research attached") — never auto-sent.
- **Notion log** under an `Accounts being researched` page if the user wants the brief persisted. Approval-gated.

# Rules

- Never invent a funding event, product launch, leadership change, or executive name. Every trigger cites a source URL + date.
- Never surface a stakeholder by name without a verifiable source (CRM or account-intel platform). Title patterns ("Looking for a VP Sales") are honest; invented names are not.
- ICP fit % only when `icp-and-personas.md` has content. Otherwise label the gap.
- If the account already exists in CRM with an open deal or recent owner activity, recommend `audit-this-deal` or paste-in-conversation instead and don't run the cold-research workflow.
- The opening hook is grounded in a real trigger or a real persona pain. Never generic.
- Approval-gated for any Slack draft or Notion log.
- Single-question framing if calling any account-intel agent. Multi-part questions return empty.
