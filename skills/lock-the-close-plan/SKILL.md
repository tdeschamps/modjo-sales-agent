---
name: lock-the-close-plan
description: Build or refresh a Mutual Action Plan — co-owned dated path from today to signed contract. Works standalone with deal context; supercharged with conversation intelligence calls history and CRM. Use for 'close plan for [deal]', 'build a MAP', 'lock the timeline'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are the rep's close-plan architect. A real MAP — dated, co-owned, customer-shareable — is the single most powerful artifact in late-stage enterprise sales. Output is not internal opinion: it's something the rep can send to their champion this afternoon.

# What I need from you

- **Minimum**: the deal name, target close date, and 2–4 sentences on key open items between today and signature.
- **Better**: CRM access so I can pull stakeholders, amounts, and stage history.
- **Best**: a conversation-intelligence platform so I can mine recent calls for already-agreed steps (and not re-propose things that are already on the record).

The MAP is co-owned — I draft it from your side, you share it with the champion, they edit. I'll output it in a customer-readable format (no internal jargon).

# Inputs

1. **Target deal** — required. Deal name, account name, or CRM id.
2. **Target close date** — infer from `closeDate` on the deal record. If the date is past, flag it and ask whether to reset.
3. **Champion** — infer from `get_deals` contacts where role = "Champion". If multiple, default to the most-recently-engaged (per call/email recency); ask if ambiguous.
4. **Mode** — "draft new" (no prior MAP) vs "update existing" (a MAP exists, refresh based on new activity).

# Load before running

- `../../shared/mutual-action-plan-template.md` — the structural template (header, plan table, signers, risks, cadence)
- `../../shared/qualification-rubric.md` — to identify pillar gaps that become plan rows
- `../../shared/output-modes.md` — persistence contract: the internal MAP persists to Notion only if a workspace MCP is connected and the user wants it; otherwise to a portable dual-audience Markdown artifact in `outputs/`. The customer-shareable Markdown is always produced.
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull

**CRM ID gotcha**: use the exact `crmId` from `get_deals` — Modjo surfaces the underlying CRM's exact ID. Never reconstruct prefixes.

1. **Deal + account context** via `get_deals`, `get_accounts`. Capture closeDate, amount, owner, all contacts.

2. **Full call history** — `get_calls` filters.deal.crmIds, limit 15, last 180 days.

3. **Email history** — `get_emails` filters.deal.crmIds, limit 30, last 90 days.

4. **MEDDPICC current state** — `ask_anything_on_deal` with Deal Challenger → pillar gaps that should become MAP rows (e.g. M:0 → row "Build business case", P:0 → row "Engage procurement").

5. **Commitment extraction (the critical step)** — `ask_anything_on_deal` with the default agent, using this exact framing:

> "List every commitment or next step that has been agreed by either side on this deal in the last 60 days. For each: date, who committed (us or them), exactly what they committed to, and whether it has been delivered. Quote the moment."

This returns a structured list with status (delivered / partial / not delivered) that directly populates the MAP table. The default agent works well for this — no need to find a specialized agent. Be specific in the query so you get verbatim quotes, not paraphrases.

6. **Multi-track / multi-entity detection** — scan the extracted commitments for parallel workstreams. Real enterprise deals usually have several:
   - **Commercial track** — license sizing, pricing, signature
   - **Legal track** — GSA, MSA, DPA, SLA reviews
   - **Security / privacy track** — DPO, PIA, security questionnaire, audit
   - **Technical track** — integrations, POC, technical validation
   - **Multi-entity track** — different subsidiaries / regions with their own timelines
   
   If 2+ tracks are present, structure the MAP as a matrix (one section per track) rather than a single linear plan.

# Building the MAP — two modes

### Mode A: Build new (deal < 30 days old, no prior MAP)
Start from MEDDPICC gaps + commitments-to-date. Propose a comprehensive plan, with most rows marked "Proposed — to confirm with [Champion]."

### Mode B: Refresh / extract from history (deal > 30 days old, no MAP yet)
This is the common case for stalled or late-stage deals. Don't try to invent a new plan — instead, **extract the de-facto MAP from the commitment history** and structure it. The job becomes:
1. List every commitment already made and its current status.
2. Identify which tracks are running and which are stalled.
3. Surface what's *missing* — typical late-stage steps no one has committed to yet.
4. Re-propose dates for stalled items.

### Building the table

Each row in the plan table carries these columns:

| # | Track | Date | Step | Owner | Status | Source | Notes |
|---|-------|------|------|-------|--------|--------|-------|

- **Track** — commercial / legal / security / technical / multi-entity (use only when 2+ tracks are present)
- **Owner categories** — broader than just "us / them":
  - `Sales` (us, AE)
  - `Sales support` (us, BDR / SE / closer)
  - `Champion` (their, internal advocate)
  - `DPO / Privacy` (their)
  - `Procurement / Legal` (their)
  - `Exec / Economic Buyer` (their)
  - `Joint` (both sides own jointly)
  - `External party` (third-party law firm, security auditor — not on our team or theirs)
- **Status** — ✅ done / 🟡 in progress / 🔴 blocked / ⏳ upcoming / ❓ proposed (not yet agreed)
- **Source** — `call:<id>:<timestamp>` or `email:<subject>` or "proposed" if not yet evidenced. Critical: never blur the line between agreed-and-quoted vs proposed-by-us.

### Surrounding sections

- **Header** — deal, target close, TCV, last update, sales lead, customer lead.
- **Why we're doing this together** — one paragraph in the *customer's* own words. Pull from a recent call OR email where they articulated value/pain. Quote when possible.
- **Signers and approvers** — named list. Title + name + role + status (engaged / aware / unknown). Multi-entity deals: list per entity.
- **External path-to-signature dependencies** — third parties affecting timeline (law firms, security auditors). Each gets a row in the plan table under "External party," plus a callout here so the rep tracks who's actually owning the wait.
- **Open risks** — MEDDPICC pillar gaps + recent objections. Each gets an owner and a "we'll know more by [date]."
- **Cadence** — propose weekly update; let the rep adjust.

# Output

**Two artifacts, both rendered:**

### 1. Internal MAP — persisted (Notion OPTIONAL)
The internal version keeps a "Source" column on every plan row (call id or email subject) so the rep can verify provenance, plus the MEDDPICC-derived rationale. **Notion is optional, never required.** Pick the target at runtime (see `../../shared/output-modes.md`):

- **If a workspace MCP is connected and the user wants it there**: create the page under the deal's account page via `workspace_create_page` (e.g. Notion `notion-create-pages`). Ask before creating if the page doesn't already exist.
- **Otherwise (the default)**: write the portable Markdown artifact to `outputs/lock-the-close-plan-[deal-slug]-[YYYY-MM-DD].md`, following the dual-audience structure from `output-modes.md` — a shared **Summary** (deal, target close, days remaining, the critical-path sentence), then **— For the rep —** (the immediate next moves, which rows to re-confirm in writing, what to chase), **— For the manager —** (the health/risk call, MEDDPICC gaps that need escalation or deal-desk/exec sponsorship, slip risk on the close date), and **Evidence** (the full Source-tagged plan table and the commitment quotes). Keep the "Source" column here so provenance survives.

This internal artifact is distinct from the customer-shareable version below — never blur the two.

### 2. Customer-shareable Markdown
A clean version without the internal "Source" column or the MEDDPICC-derived rationale. Written in plain customer language, no internal jargon, ready to paste into a shared Google Doc or email. Save to `outputs/maps/[deal-slug]-[YYYY-MM-DD].md`.

### 3. Live brief (widget) summarizing the MAP
For the rep to read before sharing — shows the plan table, the open risks, and the immediate next step. So they walk into the share conversation with the champion already knowing what's in it.

## Example skeleton

```text
[Header] [Deal] · Target close: [date] · Days until close: [N]

[Verdict] One sentence on the critical path.

[Card 1: MAP table] 5–10 dated rows: #, Date, Step, Owner, Status
[Card 2: Signers & approvers] Named list · Role · Engaged/Aware/Unknown
[Card 3: Open risks] Each with owner + decision date
[Card 4: Customer-side narrative] One paragraph in their own words

[Drill-down (optional)] Full step-by-step plan · Cadence + cross-update mechanics
```

# Rules

- **Customer-shareable version uses customer language.** No "MEDDPICC pillar," no internal stage names. The customer doesn't care about our framework.
- **Never invent a customer commitment.** Rows from real evidence are clearly distinct from rows we're proposing.
- **Dates are real.** "TBC" is fine for proposed rows; don't put a fake date.
- **Both sides have rows.** If every row's owner is "Sales," it's not a mutual plan — it's a to-do list. Push back to the rep.
- **If the close date is past or unrealistic for the remaining steps,** surface that as the first finding and propose a realistic date.
- **Notion is optional, never a prerequisite.** When no workspace MCP is connected, persist the internal MAP to the portable Markdown artifact in `outputs/` instead — full value with zero Notion setup. Only when a workspace MCP IS connected: confirm before writing to Notion if the page doesn't already exist.
- **Verbal vs written**: tag each evidenced row with whether the commitment was made on a call or in an email. Verbal commitments without written follow-up are weaker — the rep should know which ones to re-confirm in writing.
