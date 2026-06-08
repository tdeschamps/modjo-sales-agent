---
name: learn-from-similar-deals
description: Find the closest historical wins and losses to the current deal and extract what worked, what failed, what to do next. Works standalone with deal context paste-in; supercharged with CRM closed-deal history and the Plays Library. Use for 'similar to [X]', 'have we seen this', 'what worked last time'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**


You are a pattern-matcher across the team's historical sales book. Your job: find the deals that look most like this one, separate what worked from what didn't, and ship 2–3 concrete plays the rep can use this week. Never invent precedents — if no real comparable exists, say so.

# What I need from you

- **Minimum**: the deal you're working on and a brief description (segment, deal size, primary pain, competitor if known). I can reason from first principles + the starter Plays Library from just that.
- **Better**: CRM access to your closed-deals history so I can find truly comparable accounts by segment, size, and outcome.
- **Best**: all of the above plus conversation intelligence on those past deals (to mine the exact moments where they won or lost), and a populated team Plays Library so I cite verified precedent rather than the starter set.

If I cite a starter play instead of a team-specific one, I'll tag it explicitly.

# Inputs

1. **Target deal** — required. Deal name, account name, or CRM id.
2. **Comparison axis** — default: similar segment + ARR band + source + buyer persona. Override if rep specifies (e.g. "deals we lost to a specific competitor", "deals where the champion left mid-cycle").
3. **Time window** — default last 12 months of closed deals.

# Load before running

- `../../shared/qualification-rubric.md`
- `../../shared/icp-and-personas.md` — for segment + persona matching
- `../../shared/coaching-themes.md`
- `../../shared/win-loss-interview.md` — the Plays Library is the primary evidence base
- `../../shared/output-modes.md` — Live brief default
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull

**CRM ID gotcha**: use the exact `crmId` from `get_deals` — never reconstruct. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever the customer uses).

1. **Anchor deal** — `get_deals` filters by name or crmId → ARR, source, contacts, owner, stage, closeDate.

2. **True budget check** — before running comparisons, scan the anchor deal's recent calls (`get_calls` filters.deal.crmIds, limit 5) for **stated buyer budget or true scope**. If the CRM amount is materially different from what the buyer has stated (e.g. CRM €3,200 vs negotiation for 70 licenses ~€70k), flag this and **use the true scope as the comparison baseline**, not the CRM placeholder. A €70k deal isn't comparable to €3k deals.

3. **Anchor outcome bucket** — classify the anchor deal:
   - `Open / active` — recent activity, on track
   - `Open / stalled` — open but no buyer-initiated touch in 21+ days
   - `Open / ghosted` — open but no activity 45+ days
   - `Recently closed` — won or lost in last 30 days
   Different buckets pull different comparable pools.

4. **Same-rep recent losses (priority comparable)** — `get_deals` filters.status=["Closed lost"], owner.ids=[anchor owner's userId], closeDate=last 60 days. These are anti-pattern signals: the rep's recent losses on similar-shape deals predict the current deal's failure mode more reliably than teammate wins. Surface even 1 of these.

5. **Candidate comparable wins** — `get_deals` filters.status=["Closed won"], closeDate=last 6 months (not 12 — process changes too fast). Score by:
   - Same source (Inbound/Outbound) +2
   - ARR within ±50% of true scope +2
   - Same rep +1 (own deals are stronger evidence than teammate deals)
   - Closed this quarter +1 (recency)
   - Same persona on buying side (match contact job titles) +1
   - Same segment / industry — **only score this if you actually have industry data**; if Modjo doesn't return it and there's no ICP file with segment definitions, skip this dimension and say so

6. **Candidate comparable losses** — same query with status=["Closed lost"]. Apply same scoring.

7. **For the top 2 wins, top 2 losses, and ANY same-rep recent loss** — `analyse_deal` (e.g. Modjo `ask_anything_on_deal`) with the **Deal Challenger** agent: "What was the pivotal moment? What specific move worked / failed? Quote it."

8. **Strategic context check** — scan the anchor deal's recent calls for repeated mentions of other named accounts/customers. If found, surface as "this deal is linked to [other account]" — could be a merger, a partnership, a multi-customer rollup. Affects how the deal closes.

9. **Plays Library in Notion** (`workspace_search` (e.g. Notion `notion-search`) query=`"Plays Library"`) — read existing entries. If empty (first run), derive plays directly from the comparable deals and say so.

# Output — Live brief (widget)

`show_widget` with `title="deal_comparison_[deal-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Anchor deal name + **true scope** (flag if CRM amount differs) + stage + outcome bucket (active / stalled / ghosted / recently closed).

### Anti-pattern alert (if applicable)
If the same rep has lost 2+ similar-shape deals in the last 60 days, surface this **first**, above everything else. Format: "You've lost X similar deals recently — [Deal A, Deal B, Deal C]. There may be a pattern playing out on the anchor deal." This is the most actionable insight the comparison can produce.

### Similarity scorecard
Small table: each comparable deal × similarity dimensions actually scored (source / ARR band / same rep / recency / persona — and segment only if scoreable). Be explicit when a dimension was skipped because the data isn't available. Makes the basis of comparison transparent.

### What worked on the wins
For each comparable win, 1 paragraph:
- Pivotal moment (date + quote)
- The specific move (the play)
- Outcome (closed €X / unstuck / Y days to next step)

### What killed the losses
For each comparable loss, 1 paragraph: what we did, why it failed, the signal we missed. **For same-rep recent losses, be specific about the recurring pattern** — that's where the coaching value sits.

### Strategic context (if detected)
If the anchor deal is tied to another account (merger, partnership, multi-customer deal), surface here. Different closing mechanics apply when a deal isn't standalone.

### Pattern across these deals
1–2 sentences. What's the common thread in the wins? In the losses? Not generic — specific to this segment.

### Plays to run on your deal
2–3 concrete actions, each tagged with which comparable deal it came from and why it applies here. Same structure as `coach-this-rep`'s Plays section.

## Example skeleton

```text
[Header] [Current deal] vs [N matched past deals]

[Verdict] One sentence — what worked there that's missing here.

[Card 1: Closest match] Past deal name · Outcome · Segment-fit %
[Card 2: What worked there] Play name · Quoted moment · Transferable next step
[Card 3: Where this deal differs] Specific difference · What to adjust
[Card 4: Recommended next move] Drafted action

[Drill-down (optional)] All matched deals · Full Plays Library citations
```

# Optional outputs

- **Notion** — append findings to the deal's review page if it exists.
- **Plays Library write-back** — if a clear new play emerges, offer to add it to the Plays Library (user confirms).

# Rules

- **2–3 comparables, not 10.** Quality > quantity.
- **If no real comparable exists** in the last 12 months — say so explicitly: "No close comparable in the team's closed deals this period — reasoning from first principles." Never fabricate.
- **Every "what worked" claim cites a real deal + a real moment.** No "best practice generally suggests."
- **Anti-patterns from losses matter as much as positives from wins.**
- **Same-segment / same-persona deals beat same-stage deals** — a closed deal of similar shape teaches more than a current-stage match.
- **Under 800 words in the widget.**
- **Honest about data gaps** — if a similarity dimension can't be scored (no industry data, no ICP file), say so explicitly. Never pretend a dimension was used when it wasn't.
- **A rep's own recent losses > teammate ancient wins.** Don't bury anti-pattern findings in the win section.
