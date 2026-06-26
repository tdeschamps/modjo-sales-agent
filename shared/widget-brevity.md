# Widget brevity — every skill's output discipline

A consistent set of brevity rules every artifact must respect. This file is the load-bearing reference; each SKILL.md says "render per `shared/widget-brevity.md`" rather than duplicating the rules.

**Visual design:** brevity is *what* goes in the artifact; `shared/artifact-design.md` is *how it looks* — the Munro editorial system (cream canvas, Bark Brown ink, whisper-weight grotesque, flat hairline cards, one Deep Teal action), now extended for the interactive medium. The two files compose: ≤350 words / ≤5 cards (this file), rendered in the Munro style (that file). The classes and component vocabulary are in `content-model.md`.

**The brevity cap applies to the DEFAULT VIEW.** For a static widget or Markdown, that's the whole thing. For a **native interactive artifact**, that's the **collapsed view** — see "Brevity in the interactive medium" below.

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

## Brevity in the interactive medium

A native interactive artifact (`native-artifact.md`) can hold more than a static widget, because
depth lives behind interaction. The cap adapts — it does not disappear:

- **The default COLLAPSED view must pass the 90-second scan.** Header → verdict line → 3–5 visible
  cards → anti-fabrication flags. ≤ 350 visible words *in the collapsed state*.
- **Content behind an interaction does not count against the cap.** An expandable evidence card, a
  collapsed stakeholder map, a click-to-reveal scorecard pillar — these are the native equivalent
  of the old "Drill-down (optional)" section. They're free.
- **Never collapsible:** the verdict line and every anti-fabrication flag. Honesty is never
  something the rep has to expand to find.
- The **Markdown projection keeps the original flat cap** and pushes depth into its explicit
  drill-down — the same content, just static.
- `eval/rubric.md` Dim 5 grades the **collapsed** view, not the expanded DOM.

So: the interactive artifact's first screen is held to the same 90-second discipline as a static
widget; everything richer is one click away, not on the surface.

## Persisted-artifact (Class B) brevity — a softened cap

A persisted record (`content-model.md` class B) is re-read across weeks, so it may carry more than
a read-once widget — but the discipline holds in spirit:

- **Still leads with the verdict line**, and still surfaces the Manager-lens callout near the top.
- **Still cuts empty sections** (no "what worked" with nothing in it; no manager-actions with < 2).
- May exceed 350 words for the durable detail (the full plan, the evidence section), but the
  **scannable summary** at the top must still pass the 90-second test on its own.
- The interactive projection of a Class B artifact collapses that durable detail behind reveals, so
  its *default view* still meets the standard interactive cap above.

## Audit: am I hitting the cap?

After rendering, count what's in the **default view**: visible words, cards, drill-downs. For a
static widget or Markdown, that's the whole document. For an interactive artifact, that's the
**collapsed** state. If words > 350, cards > 5, or no verdict line — cut. Don't ship over budget.
