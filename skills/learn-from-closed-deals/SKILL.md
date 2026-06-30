---
name: learn-from-closed-deals
description: Pattern extraction from recently closed deals — what worked, what failed, plays to bank in the Plays Library. Works standalone with deal list and notes paste-in; supercharged with conversation intelligence agents on each deal. Use for 'win-loss review', 'why did we lose [deal]', 'patterns from [period]'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `${CLAUDE_PLUGIN_ROOT}/shared/data-sources.md` for the full Modjo operation map and `${CLAUDE_PLUGIN_ROOT}/CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `${CLAUDE_PLUGIN_ROOT}/shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are the team's structured-retrospective engine. Findings here become the evidence base every other deal-execution skill cites. Half-baked retros pollute the Plays Library — so be strict about evidence and never invent precedents.

# What I need from you

- **Minimum**: a list of recently closed deals (won and lost) with outcome and 1–2 sentences each on what happened.
- **Better**: CRM access to pull the closed-deals dataset over your chosen window.
- **Best**: a conversation-intelligence platform so I can mine specific call moments to back each candidate play with verbatim evidence — the difference between a verified play and a hunch.

Every play I propose for the team's Plays Library carries the deal name and the quoted moment it came from. No untraceable plays.

# Inputs

1. **Scope** — default: deals closed in the last 7 days, owner = anyone on the team. Override: specific rep, specific period, specific deal, specific loss reason.
2. **Depth** — quick (summary-based, no interviews) or deep (with drafted customer interview outreach for top losses). Default quick.
3. **Cadence** — one-off (default) or recurring weekly batch.

# Load before running

- `${CLAUDE_PLUGIN_ROOT}/shared/using-modjo-mcp.md` — how to use the Modjo MCP: agents for grounded quotes, `get_transcript` is last-resort-only
- `${CLAUDE_PLUGIN_ROOT}/shared/win-loss-interview.md` — the question structure and synthesis template
- `${CLAUDE_PLUGIN_ROOT}/shared/coaching-themes.md` — to tag findings
- `${CLAUDE_PLUGIN_ROOT}/shared/qualification-rubric.md` — for retroactive pillar scoring
- `${CLAUDE_PLUGIN_ROOT}/shared/output-modes.md` — persistence contract: Live brief + an OPTIONAL Plays Library write (Notion if a workspace MCP is connected and the user approves; otherwise a portable Markdown artifact in `outputs/`)
- `${CLAUDE_PLUGIN_ROOT}/shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull

**CRM ID gotcha**: Modjo has `006MI…` and `006IV…` objects coexisting. Use exact `crmId` from `get_deals`.

1. **Closed deals in scope** — `get_deals` filters.status=["Closed won", "Closed lost"], closeDate in window. Cap 30 deals. Capture: owner, source, amount, contacts (count + roles), closeDate, startDate (for cycle length), lossReason.

2. **Split deals by age before doing deep retro**:
   - **Fresh closes** (< 14 days post-close): too new for the agent. Skip `ask_anything_on_deal` and analyze from CRM data + call summaries only. Note this explicitly in the output.
   - **Mature closes** (14-90 days post-close): run the deep retro per step 3.
   - **Older closes** (> 90 days): include for pattern context but don't burn agent calls on them.

3. **Per-mature-deal retro** — for each deal in the 14–90 day window:
   - Pull call summaries (already cheap from a single `get_calls` batched pull).
   - `ask_anything_on_deal` with the default agent, using a **simple, single-question framing** (not multi-part):
     - For wins: "What was the pivotal moment that closed this deal? Quote it with date and speaker."
     - For losses: "What was the pivotal moment when this deal died? Quote it with date and speaker."
   - If the agent returns empty (real failure mode on thin deals), fall back to CRM-data-only analysis for that deal. Don't retry with a more complex query.

4. **lossReason hygiene check** — for each Closed Lost deal, check if `lossReason` is null/blank. List those separately as "no reason captured" — that's a coaching issue for the rep + manager.

5. **Existing Plays Library** — to avoid duplicates, read the current library from wherever it lives. If a workspace MCP is connected: `workspace_search` (e.g. Notion `notion-search`) query=`"Plays Library"` → fetch existing entries. Otherwise read prior `outputs/learn-from-closed-deals-*.md` artifacts (and any local Plays Library Markdown the user points to). If no prior library exists anywhere, treat every candidate as net-new.

# CRM-data-only pattern detection (always runs, regardless of agent results)

Cluster the closed deals on these dimensions, looking for shape clusters:
- **Source** — Inbound vs Outbound mix in wins vs losses
- **ARR band** — losses concentrated in a specific band?
- **Contact count** — single-contact deals losing more than multi-threaded?
- **Champion presence** — losses correlate with no contact tagged "Champion"?
- **Cycle length** — fast losses (< 30 days) vs slow losses (60+ days) have different causes
- **Owner** — single rep losing a cluster shape?

A **2-deal cluster = candidate pattern** (surface to user, ask whether to write to Plays Library).
A **3+ deal cluster = real pattern** (propose Plays Library entry directly).

This analysis runs even when agent retros fail or are skipped. Often it's the most actionable signal.

# Synthesis

Per the structure in `win-loss-interview.md`:

For each deal, output: outcome, pivotal moment (with quote), themes touched, plays surfaced (for wins) or anti-patterns (for losses), missed signal (if any).

Across the batch, surface:
- **Patterns** — themes that repeat across multiple deals in the same period
- **Net-new plays** — moves that worked in 2+ wins and aren't yet in the Plays Library
- **Anti-patterns** — losses sharing a common failure mode
- **Quality flags** — deals where CRM data doesn't match the call evidence (e.g. lossReason = "no budget" but transcripts show competition was the real reason)

# Output — Live brief (widget)

`show_widget` with `title="win_loss_[scope]_[YYYY-MM-DD]"`. Layout:

### Header
Scope + counts: N won (€X total), M lost (€Y total), win rate, average cycle length (won vs lost).

### The pattern of the period
The single most important repeating finding across these deals. One sentence. Surfaced from the CRM-data-only cluster analysis — doesn't depend on agent retros.

### CRM-clustered patterns
For each shape cluster ≥ 2 deals, one card: pattern definition, the deals it covers, the proposed read.

### Mature-deal retros (if any)
For deals in the 14-90 day window where the agent returned content: pivotal moment quote + the specific move (for wins) or anti-pattern (for losses). Cards only when the agent succeeded; never fabricated.

### Fresh-close summaries (no retro)
For deals < 14 days closed: outcome + CRM shape only. Explicitly labelled "too fresh for retro — flag for re-analysis in 14 days."

### Customer-interview drafts (for thin losses)
For losses with thin data (single contact, short cycle, agent retro failed): a drafted outreach to the buyer asking for honest feedback. The rep decides whether to send. This is often the highest-value output for fresh thin losses.

### Data hygiene flags
- Closed-lost deals with null `lossReason` (N deals)
- Closed-won deals where CRM amount looked low vs call evidence (potential underweighted forecast retro)
- Wins/losses where the owner contact has zero call/email history (data quality issue)

### New plays to add to the library
Candidate plays for the Plays Library. Each: name, theme, when-to-use trigger, evidence (real deals), proposed library entry. User confirms before write. **Threshold: 2 supporting deals = candidate, 3+ = propose direct add.**

## Example skeleton

```text
[Header] Period: [X] · N won / N lost · N candidate plays surfaced

[Verdict] One sentence — biggest pattern this batch.

[Card 1: Top winning pattern] Theme · Supporting deals · Candidate play name
[Card 2: Top losing pattern] Theme · Supporting deals · What to do differently
[Card 3: New candidate plays] Each: name · Evidence deal · One-line play body
[Card 4: Plays Library write] N entries to add · APPROVAL-GATED — user confirms each

[Drill-down (optional)] All closed deals scanned · All candidate plays full draft
```

# Persisting net-new plays (Notion OPTIONAL)

The Plays Library write stays **approval-gated** exactly as in the widget — the user confirms each play before anything is persisted. **Notion is optional, never required.** Once the user confirms, pick the target at runtime (see `${CLAUDE_PLUGIN_ROOT}/shared/output-modes.md`):

- **If a workspace MCP is connected and the user wants it there**: `workspace_create_page` (e.g. Notion `notion-create-pages`) to append to the Plays Library database, one row per net-new play. Reference deals as evidence with their crmLinks.
- **Otherwise (the default)**: append the confirmed plays to the portable Markdown artifact at `outputs/learn-from-closed-deals-[scope]-[YYYY-MM-DD].md`. Structure it dual-audience per `output-modes.md` — a shared **Summary** (the pattern of the period, counts, win rate), then **— For the rep —** (the plays they can run now and the anti-patterns to avoid on live deals), **— For the manager —** (the cross-deal patterns, data-hygiene flags like null lossReasons, and where to coach), and **Evidence** (per-play: name, theme, when-to-use trigger, and the real deals + verbatim quoted moments backing it). This portable file is itself a Plays Library that the next run reads for dedup.

Either way: only confirmed plays are written, only plays meeting the 2-/3-deal threshold are proposed, and every persisted play still carries its real supporting deals and verbatim evidence — never a fabricated precedent.

# Rules

- **Never claim a pattern from 1 deal.** A pattern needs ≥2 deals.
- **"No shared pattern" is a valid — and often correct — verdict.** When the deals are genuinely varied (different segments, sizes, sources, failure modes), the right output is "**No shared pattern across these deals — varied segments/sizes/sources**" plus per-deal retros, and **zero** proposed Plays Library entries. Do NOT manufacture a unifying theme to fill the verdict slot. Forcing an abstraction ("they all involved single-threading / relationship-selling") across unrelated deals to have something to say is fabrication and the worst failure mode of this skill — bad plays pollute every downstream skill that cites them.
- **CRM contact-count is NOT pattern evidence.** A shared shape claimed only from counting CRM contacts (e.g. "all single-threaded") does not qualify as a pattern, especially on deals where the analysis agent returned empty. Pattern claims need call/agent evidence per deal, not a structural proxy. If the agent was empty for a deal, that deal cannot support a cross-deal pattern — say "insufficient evidence" rather than inferring the shape from contact records.
- **Quotes must be verbatim — from agent citations.** Get load-bearing quotes from `ask_anything_on_deal` / `ask_anything_on_call` (returns exact words + source). `get_transcript` is a last resort only (see `${CLAUDE_PLUGIN_ROOT}/shared/using-modjo-mcp.md`). If you can't get a real verbatim quote, drop it — never approximate or invent one (bad quotes pollute the Plays Library).
- **"Loss reason was X" is a hypothesis until confirmed by call evidence.** CRM fields are often wrong.
- **Customer interviews beat data analysis** — if the rep has time, draft outreach to 2–3 buyers (won + lost) and surface real qualitative input. The skill outputs the drafted email; the rep decides whether to send.
- **Plays Library is a slow accumulator** — don't bulk-add 10 plays in week one. Quality > quantity. 1–3 per batch is healthy.
- **Under 1200 words in the widget** (this one is naturally longer because it summarizes multiple deals).
- **Empty agent responses are normal, not failures.** Fresh closes (< 14 days) and thin deals often return nothing. Don't retry with more elaborate queries — fall back to CRM-data analysis.
- **Single-question agent framings beat multi-part questions.** The agent reliability degrades with question complexity.
