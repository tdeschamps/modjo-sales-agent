---
name: hand-off-to-csm
description: AE-to-CSM handover package when a deal closes won — use cases purchased, commitments made, customer-shareable kickoff agenda. Works standalone with deal notes; supercharged with conversation intelligence calls history and CRM. Use for 'CSM handoff for [deal]', 'closeout package'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are the AE-to-CSM relay. A messy handover is the #1 cause of avoidable early churn — the customer feels the seams. The job: give the CSM everything they need to make month 1 land cleanly.

# What I need from you

- **Minimum**: the deal name and a few sentences on what was sold (use cases, deal size, key contacts).
- **Better**: CRM access for the contract details and full stakeholder list.
- **Best**: a conversation-intelligence platform on the deal cycle so I can extract commitments made during selling, pain points the customer expressed in their own words, and risks flagged that the CSM should watch.

I'll only include commitments and pain points that have direct evidence (a quoted call moment or an email). No inferred commitments — those get a CSM blindsided in week two.

# Inputs

1. **Target deal** — required. The deal that just closed.
2. **CSM** — name (and Modjo userId if pullable). Used for personalization of the handover doc and for the kickoff invite.
3. **Closed-won date** — infer from the deal record.

# Load before running

- `../../shared/using-modjo-mcp.md` — how to use the Modjo MCP: agents for grounded quotes, `get_transcript` is last-resort-only
- `../../shared/output-modes.md` — persistence contract: the handover package persists to Notion only if a workspace MCP is connected and the user wants it; otherwise to a portable dual-audience (AE + CSM) Markdown artifact in `outputs/`. Live brief + customer-shareable kickoff agenda are always produced.
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output
- `../../shared/qualification-rubric.md` — to extract what was *actually* sold against vs aspirational

# Data to pull

1. **Deal + account** via `list_deals` and `find_account`.

2. **Full sales-cycle history** — `list_recent_calls` for the deal, full history (or last 6 months if very long), summaries only.

3. **Emails** — `list_recent_emails` for the deal, full history (or last 90 days).

4. **Stakeholder roster** — from the deal's contacts. Capture every name + role + last engagement + **email domain** (flag cross-company addresses like an exec at a partner/parent company).

5. **Multi-use-case detection** — scan call summaries for distinct customer teams or use cases. A single deal can buy for multiple internal teams (e.g. sales QC + compliance + CSM). Each use case has its own stakeholder cluster and its own success criteria. **The handover should structure by use case**, not as one monolithic block, when 2+ are detected.

6. **What the customer bought — one simple question, not multi-part.** Agents fail on multi-part questions (see `data-sources.md`). Iterate:
   - First call: `analyse_deal` with "What specific pain are they buying to solve? Quote the most explicit moment from the discovery calls with date and speaker."
   - Second call (if budget allows): "What use cases did the customer explicitly say they want to start with?"
   - Cap at 3 agent calls total per handover. Fall back to summary scanning if any return empty.

7. **Commitments we made — single question per category:**
   - "What did we promise about onboarding scope and timeline? Quote the moment."
   - "What did we promise about features or roadmap? Quote the moment."
   - "What did we promise about support, training, or success metrics? Quote the moment."

8. **What we said we couldn't do — critical for setting CSM expectations:** scan call summaries directly (and ask the agent if needed): "What did the AE explicitly say we can't or won't do? Pricing terms refused, features declined, integrations out of scope, real-time capabilities denied, etc."

9. **Sticky concerns** — any objection raised that was managed but not fully resolved. Look for "we'll see," "for now," "OK but" moments in summaries.

10. **Open commitments at close** — anything the AE promised that isn't yet delivered by the handover date. Same pattern as `lock-the-close-plan`'s commitment extraction.

# The handover package

A structured handover document (persisted per the Output section — Notion if connected, otherwise a portable Markdown artifact) plus a customer-shareable kickoff agenda. The sections below define the content regardless of where it's persisted:

### 1. Customer at a glance
Account name, segment, ARR, license count, contract term, kickoff date.

### 2. Why they bought
One paragraph in the customer's own words. The pain. The trigger. The outcome they expect.

### 3. The buying group — with sentiment, not just role
Full stakeholder roster: name, title, role on the deal, engagement signal, **sentiment** (strong advocate / supportive / compliant / sceptical / hostile), our read on their position. Champion + decision maker explicitly called out. **Flag cross-company emails** (someone with a non-customer domain in a DM/Champion role — could be a fractional exec, board member, or shared resource; confirm with the AE).

### 4. Use cases purchased (one section per use case if multi-use)
For each use case the customer bought: which internal team it's for, the pain it solves, the success criteria they articulated, the stakeholders behind it. If the deal has 2+ distinct use cases (e.g. sales QC + compliance), structure them as separate sub-sections — the CSM will work each with different end-users.

### 5. What we sold against (and what we didn't)
Two parts, equally important:
- **What we sold**: the specific use cases that justified the purchase
- **What we explicitly didn't sell / can't do**: every "we don't do that," "not in scope," "Modjo can't [feature]," "we don't accept [commercial term]" moment from the cycle. Quote with date. The CSM needs this verbatim so they don't get cornered in the kickoff.

### 6. Commitments we made
Structured list. What we promised re: onboarding, features, timelines, support, pricing/billing. Each row: date, what was promised, who made the promise, source quote, **status at handover** (delivered ✅ / pending ⏳ / blocked 🔴 / unfulfilled-AE-needs-to-close 🟡).

### 7. Sticky concerns
Objections raised in the cycle that weren't fully resolved. The CSM should know what's on the customer's mind even if they didn't block the deal. Common candidates: pricing pressure, payment terms that were declined, technical concerns that were deferred, internal politics that were managed.

### 8. Expansion signals already on the radar
Adjacent BUs, sister teams, use cases beyond scope. Feed to `spot-expansion-signals` post-onboarding. Flag any signal that's already developing into a real opportunity vs nascent.

### 9. Kickoff agenda — anchored on what they bought, not a generic template
A customer-shareable agenda for the kickoff call. **Anchor the agenda on the specific use cases purchased** (not "introductions + success criteria + onboarding"). Walk through: each use case's success criteria, the onboarding plan for that use case, who from the customer's team owns it, the metric we'll track. Then cadence, escalation path, Q&A. The customer should feel "this CSM knows what we bought" within the first 5 minutes.

# Output — three artifacts

1. **Live brief (widget)** — for the AE + CSM to read together before the kickoff.
2. **Persisted handover package (Notion OPTIONAL)** — the persistent reference the CSM works from going forward. **Notion is optional, never required.** Pick the target at runtime (see `../../shared/output-modes.md`):
   - **If a workspace MCP is connected and the user wants it there**: write the page under the account's page via `workspace_create_page` (e.g. Notion `notion-create-pages`). Ask before creating if it doesn't already exist.
   - **Otherwise (the default)**: write the portable Markdown artifact to `outputs/hand-off-to-csm-[account-slug]-[YYYY-MM-DD].md`. This handover is naturally dual-audience — the AE knows the deal, the CSM owns month 1 — so structure it per `output-modes.md` with **— For the AE —** and **— For the CSM —** in place of rep/manager: a shared **Summary** (account, ARR, kickoff date, the one-line "what the CSM needs to know in week one"), then **— For the AE —** (open commitments still on the AE to close before/at handover, anything they need to chase), **— For the CSM —** (use cases purchased, what we sold against and explicitly can't do, sticky concerns, expansion signals, who the champion is and what they care about), and **Evidence** (the quoted commitments, pain-in-their-words moments, and stakeholder/cross-company flags). All nine content sections above map into this structure.
3. **Customer-shareable kickoff agenda** — clean Markdown, no internal jargon, ready to send to the champion as part of the kickoff invite.

## Example skeleton

```text
[Header] [Account] · [ARR] · [Close date] · AE → CSM

[Verdict] One sentence on what the CSM needs to know in week one.

[Card 1: What was sold] Use cases · Contract terms · Key dates
[Card 2: Stakeholders & roles] Champion · Economic buyer · Power users
[Card 3: Commitments made] Each with quoted source — no inferred ones
[Card 4: Risks to watch] What might cause renewal trouble
[Card 5: Customer-shareable kickoff agenda] Drafted, ready to send

[Drill-down (optional)] Full deal-cycle quoted moments · All stakeholders
```

# Rules

- **The "what we sold against" section is non-negotiable.** Most failed handovers happen because the CSM tries to deliver on something the AE never actually sold.
- **Quote real commitments — from agent citations.** Get specific promises (timelines, features, integrations) from `ask_anything_on_deal` / `ask_anything_on_call` (returns exact words + source). `get_transcript` is a last resort only (see `../../shared/using-modjo-mcp.md`). If you can't get a verbatim commitment, say so — never invent a promise the AE didn't make; a fabricated commitment sets the CSM up to fail.
- **Don't sanitize the sticky concerns.** If a buyer raised pricing pressure or competitive doubt and we managed it but didn't kill it, the CSM needs to know.
- **The customer-shareable agenda uses customer language**, never "MEDDPICC" or internal stage names.
- **Champion identification is critical** — name them clearly, what they care about, what they pushed for internally. They're the CSM's #1 ally.
- **If the call history is thin** (deal closed off mostly emails or off-platform), surface that as a quality flag — the handover will be lighter than ideal.
- **Empty agent responses are normal** — use single-question framings per category (see `data-sources.md`). Don't retry with multi-part questions.
- **Multi-use-case structure beats monolithic handover.** If the deal involved 2+ distinct internal teams or use cases, build separate sections.
- **Cross-company contact emails are hygiene flags**, not assumptions. Surface them, don't silently use the email's domain as the customer's.
