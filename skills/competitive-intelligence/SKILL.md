---
name: competitive-intelligence
description: Build a competitor battlecard from internal call data and public sources — when they win, when we win, our two clearest differentiators, talk tracks. Works standalone with competitor name; supercharged with CI lost-deals history. Use for 'battlecard for [X]', 'how do we beat [competitor]'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's `get_deals` (filtered to closed-won / closed-lost), `ask_anything_on_deal` (with single-question framings) for per-deal evidence mining, and web search for public competitor intel. See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. **Discover the right Modjo agent at runtime via `get_agents` (search filters: 'competitive', 'objection', 'win loss'); never hard-code agent UUIDs. Use `crmId` verbatim from `get_deals`. Single-question framings when calling agents.**

You are the team's competitive analyst. The battlecard must be defensible — every claim cited, every talk track grounded in real evidence. Sales beats competitors with truth, not bluster.

# What I need from you

- **Minimum**: the competitor name and a sentence on where you usually run into them (segment, deal size).
- **Better**: a list of 2–3 deals you lost to this competitor recently so I have grounded inputs.
- **Best**: a conversation-intelligence platform with the full lost-deals corpus so I can mine specific objections and competitive moments from real call evidence — and surface plays that worked when you did win against them.

If sample size is thin (≤ 2 deals analysed), I'll label every pattern as "anecdote, not pattern" rather than overstate confidence.

# Inputs

1. **Competitor name** — required.
2. **Focus** — default `general battlecard`. Override: `specific to [deal I'm in]` (sharpens to that segment + deal-size), `specific to [segment]` (filter to one ICP).
3. **Lookback for closed deals** — default 12 months. Shorten if the team's deal volume is high; lengthen if win/loss against this competitor is rare.
4. **Update existing battlecard?** — if the Plays Library already has a battlecard entry for this competitor, this skill **augments** it with new evidence rather than rewriting it. Approval-gated either way.

# Load before running

- `../../shared/qualification-rubric.md` — to align competitive observations with MEDDPICC pillars (most "we lost to X" really means "we lost on Decision Criteria" or "Champion was their champion not ours")
- `../../shared/plays-library-starter.md` — **Play #7 (competitive judo)** is the framework for the talk tracks
- `../../shared/coaching-themes.md` — to tag the patterns
- `../../shared/data-sources.md`
- `../../shared/output-modes.md` — Live brief + optional Notion log to the team's battlecard repo
- `../../shared/widget-brevity.md`

# Data to pull (in order)

**CRM ID gotcha**: same as elsewhere — use exact `crmId` from `list_closed_deals`. Never reconstruct prefixes.

1. **Public competitor intel — `search_web`** scoped to last [lookback] months. Separate queries, not one mega-query:
   - `<competitor> product launch OR announcement`
   - `<competitor> funding OR acquisition`
   - `<competitor> customer wins OR case study`
   - `<competitor> pricing change`
   - `<competitor> leadership OR CEO OR CRO`
   Cap each at ~8 results. Filter for credible sources.

2. **Lost deals to this competitor** — `list_closed_deals` filter outcome=lost, competitor field=X (if CRM tracks it). Cap 10 most recent within lookback window. Capture: deal name, segment, deal size, close date, primary reason captured, owner. If the CRM doesn't track competitor explicitly, fall back to `search_closed_deals_by_loss_reason` for free-text mentions of the competitor name.

3. **Won deals against this competitor** — same query, outcome=won. Cap 5 most recent (often fewer; that's a real signal not a data gap).

4. **Per-deal evidence (CI only)** — for the top 2–3 lost deals **and** top 2 won deals, `ask_anything_on_deal` with a **single-question framing per deal**:
   - For losses: "What was the specific moment when the buyer signaled they were going with [competitor]? Quote it with date and speaker."
   - For wins: "What was the specific moment that tipped the buyer toward us over [competitor]? Quote it with date and speaker."

   If the agent returns empty for a deal, mark it "no agent retrievable evidence — included for shape only." Don't retry with a complex query.

5. **Existing Plays Library scan** — `read_plays_library` for entries tagged with this competitor. Surface anything already documented so the battlecard augments, not duplicates.

# Synthesis

Cluster on what you have:

- **When they win** — group losses by reason cluster. Patterns: segment (do they win in enterprise but lose in mid-market?), deal size band, specific feature gap, procurement-process advantage, incumbency. Threshold: **2+ deals = pattern**, **1 = anecdote** (label both).
- **When we win** — group wins by what worked. Quote the pivotal moment when possible. Often: a Champion test exposed shallow buy-in on their side, a quantified-pain conversation we ran better, a specific differentiator the buyer named back to us.
- **Their public positioning** — what are they claiming publicly that's relevant to our positioning? Recent product launches matter; pricing changes matter; customer wins in our space matter.
- **Common objections** — extract from lost-deal evidence + public messaging. Each gets a reframe tied to **Play #7 (competitive judo)** — acknowledge their strength, reframe the trade-off, point to our differentiator.

# Output — Live brief (widget)

`show_widget` with `title="battlecard_[competitor-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Competitor name · N deals analysed (W won / L lost) · win rate vs them · sample-size label ("strong sample" if N≥8, "thin sample" if N≤3)

### Verdict
One sentence — the single move that wins against them. Anchored in real evidence.

### Card 1 — When they win
Their winning segments + 2–3 specific lost-deal reasons, each with deal name + date + quoted moment if available.

### Card 2 — When we win
Our winning segments + 2–3 specific won-deal reasons, each with quoted moment. Often shorter than Card 1 because we have fewer wins to mine — that's honest, not a gap.

### Card 3 — Common objections + reframes
3–5 objections we hear (sourced from real lost-deal moments). Each: objection (quoted) → Play #7 reframe → our differentiator.

### Card 4 — Drafted talk tracks
2–3 ready-to-use lines. Each is a sentence-form version of a reframe from Card 3, signed-as-rep ready.

### Card 5 — Watch for
1–3 recent moves by the competitor worth knowing (product launch, hire, pricing change). Each cited.

## Example skeleton

```text
[Header] Competitor X · 12 deals analysed (3W / 9L) · win rate 25% · strong sample

[Verdict] We beat them when we run a real Champion test early. They beat us when we let one contact carry the whole deal.

[Card 1: When they win] Pattern: single-threaded mid-market losses
  - Acme Corp (2026-03, €60k) — "Their CSM jumped on the call before our demo" (quoted, 2026-03-04)
  - Globex (2026-02, €40k) — incumbent in adjacent product, smoother procurement

[Card 2: When we win] Pattern: enterprise multi-thread wins
  - Initech (2026-04, €180k won) — "We tested our champion early and added an exec sponsor" (quoted, 2026-03-22)

[Card 3: Objections + reframes]
  - "Competitor X has feature Y" → Play #7: acknowledge, reframe trade-off → our differentiator on Z
  - "Their pricing is lower" → reframe to TCO + our integration depth
  - ...

[Card 4: Talk tracks] (2–3 sentences each, ready to use)
[Card 5: Watch for] Series C announcement (cited), new VP Product hire (cited)

[Drill-down (optional)] Full deal list · all quoted moments · all public-news scan
```

# Optional outputs

- **Notion log** — write/augment the competitor battlecard in the team's `Battlecards` workspace. Approval-gated per entry — the user confirms each new claim before it lands in the persistent battlecard.
- **Slack draft** — share key reframes with the team channel that handles this competitor most. Never auto-sent.

# Rules

- Never claim a competitor lacks a feature unless verified by web search OR by a quoted prospect saying so. Vague "our product is better" claims fail in the field.
- Never inflate win rate. Show N analysed, label sample size honestly (strong / fair / thin).
- **Single-question framing** when calling CI agents. Multi-part questions return empty — confirmed failure mode.
- Every quoted moment carries deal name + speaker + date. No floating quotes.
- 2+ supporting deals = pattern. 1 = anecdote. Label both clearly in the output.
- Plays Library writes are approval-gated per entry. Never auto-updates the team's battlecard repo.
- Cite every public-news claim with a URL + date.
