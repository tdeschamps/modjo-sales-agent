# Widget brevity — every skill's output discipline

A consistent set of brevity rules every widget output must respect. This file is the load-bearing reference; each SKILL.md says "render per `shared/widget-brevity.md`" rather than duplicating the rules.

**Visual design:** brevity is *what* goes in the widget; `shared/artifact-design.md` is *how it looks* — the Munro editorial system (cream canvas, Bark Brown ink, whisper-weight grotesque, flat hairline cards, one Deep Teal action). Every widget uses that design's drop-in CSS + skeleton. The two files compose: ≤350 words / ≤5 cards (this file), rendered in the Munro style (that file).

## The 90-second test

Anthropic's Claude for Small Business skills set the bar: a rep should be able to read the rendered output in 90 seconds and know what to do. That's roughly **300 visible words and 3–5 cards/sections**, not 1000 words and 12 sections.

Every widget must pass: *"Could a busy rep scan this in 90 seconds and act?"*

## Hard caps per widget

- **Total visible words: ≤ 350.** Headers and labels don't count; body content does. If you can't hit this, you're trying to do two skills at once — split.
- **Maximum 5 cards/sections** in the main view. More than 5 means at least one belongs in optional drill-down or another skill.
- **One verdict line at the top.** Always lead with the single most important sentence. A rep who reads only that should know what matters.
- **Every card carries a drafted action or specific quote.** If a card has neither, cut it.

## Structural pattern (apply to every widget)

1. **Header band** (1 line) — entity name, period, single most important number
2. **Verdict line** (1 sentence) — what to take away
3. **The body — 3 to 5 cards max** — each one specific, quoted/cited, action-oriented
4. **Optional drill-down section** — explicitly labelled "Drill-down (optional)" — for the detailed table, the full stakeholder map, the full plan, etc. The user opens this if they want depth. Skipping it doesn't lose the headline.

## What gets cut, by default

These sections are *almost always* cut unless they carry unique value the body cards can't:

- **"What worked / what to keep doing"** when there are no concrete cards' worth of strengths — fold the strength into the relevant card instead
- **Stakeholder maps** longer than 5 rows — move to drill-down
- **MEDDPICC scorecard tables** with > 2 deals scored — show one inline, rest in drill-down
- **Pattern-of-the-period sections** in daily/weekly skills — pick one, drop the rest
- **Trend charts** on baseline-week runs (no real history yet) — skip the chart; render the current state only
- **Multi-track / multi-section breakdowns** when only one section has content
- **"Manager actions" sections** with fewer than 2 real actions — fold the single action into the body

## What stays even when tight

These are non-negotiable load-bearing elements:

- The verdict line
- The single most important hygiene finding (when present)
- Drafted actions / sendable talk tracks (the whole point of "intervene, don't audit")
- Any explicit anti-fabrication labelling ("baseline week", "no comparable in our book", "agent returned empty — falling back to summary")
- Approval-gated output disclosures ("this is a Slack draft, you send it")

## How to hit the cap when the data is rich

When real data offers more cards than the cap allows:

1. **Rank by actionability.** A card with a drafted action beats a card with a finding.
2. **Rank by quoted-evidence quality.** A card with a verbatim quote beats a card with inferred analysis.
3. **Rank by impact.** A finding about the rep's biggest exposure beats a finding about a minor hygiene issue.
4. **Pick the top 5.** Move the rest to the drill-down section labelled clearly. Don't drop them silently — name them so the rep knows what's been pruned.

## How to handle very thin data

When the data is sparse enough that the widget would have < 3 cards even with everything included:

- Render fewer cards (3 is the floor, not the ceiling)
- Lead with the data-quality flag: "Limited data on [entity] — here's what's there + what's needed to render the full brief"
- Suggest the specific data fix that would unlock more (run `audit-the-forecast` for amount/stage issues, run `find_user` for unresolved rep, ask the rep to paste relevant context)

## Drill-down pattern

When a widget needs depth, the structure is:

```
[Main view: verdict + 3–5 essential cards, ≤ 350 words]

---

### Drill-down (optional)
- Full stakeholder map ([N rows])
- Full MEDDPICC scorecard ([N deals])
- Trend history ([N weeks])
- All hygiene findings ([N issues])
```

Each drill-down section is a single line link/header in the main view. The rep opens it only if they want.

## Audit: am I hitting the cap?

After rendering a widget, count: visible words, cards, drill-downs. If words > 350, cards > 5, or no verdict line — cut. Don't ship over budget.
