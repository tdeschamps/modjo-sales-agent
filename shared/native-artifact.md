# Native interactive artifact — the recipe

The **headline deliverable** of a Class A/B skill is a native interactive Claude Artifact: a
self-contained, single-file interactive view rendered in the host. It supersedes the old
hand-rolled `show_widget` HTML as the primary rendered output. The portable Markdown is the
fallback — **always written**, never skipped.

This file is the how-to. The what (taxonomy, components, parity) lives in `content-model.md`; the
visual tokens + interactive CSS live in `artifact-design.md`. The proven, working example is
`shared/reference/deal-review-beauhurst.html` — **read it before authoring a new one**.

---

## What "native interactive artifact" means here

A single self-contained document — inline-styled HTML with vanilla JS, optionally one CDN charting
lib (Chart.js) — handed to whatever artifact surface the host exposes. The plugin does not ship or
guarantee a specific render tool; render tools (`show_widget`, `cowork__create_artifact`) are
**host-provided** and may be absent. So the recipe is written by *content*, and the fallback chain
(below) is load-bearing.

`coach-this-rep` is the **prototype to generalize** — it already emits an interactive,
chart-bearing view. New interactive artifacts follow its proven patterns, described by content
rather than bound to the `cowork__` tool name.

---

## Snapshot at generation — no live MCP

The artifact **bakes in the data the skill already pulled**. It does **not** call Modjo / Notion /
any MCP when it opens. Reasons: most artifact sandboxes can't reach MCP; a half-loading artifact is
worse than a static one; and a snapshot is reproducible. Bake the data into a JS constant at the
top of the script:

```js
// SNAPSHOT DATA — baked at generation, no MCP calls.
const PILLARS = [ { key:"E", name:"Economic buyer", score:0, scoredZero:true,
                    ev:"No budget signer identified or contacted." }, … ];
```

"Refresh" = re-run the skill. (Live re-query on open is a host-gated enhancement for environments
that support it — not the baseline; never assume it.)

---

## The honesty rules — non-negotiable, enforced in the artifact

The artifact is held to the same anti-fabrication bar as every output (`eval/rubric.md` Dim 2, the
auto-fail dimension). In the interactive medium specifically:

- **A 0-scored pillar reveals an honest absence statement, never a fabricated quote.** The
  reference artifact renders `Scored 0. No budget signer identified or contacted.` for each
  zero pillar — there is no invented evidence behind any expander.
- **Corrections are shown, not hidden.** The Beauhurst C-hamp 1→0 correction sits behind a
  disclosure that is *always reachable*, with the rationale — it is not silently applied.
- **Baseline weeks never get a fabricated trend line.** A trend chart with one real data point
  renders a single point + a "Baseline week" annotation — never an interpolated line.
- **The verdict line and anti-fabrication flags are never collapsible and never hidden.** Honesty
  isn't something the user has to expand to find.
- **Drafted-action blocks have a Copy button and no send path.** There is no "Send" affordance in
  any artifact — drafts are sent by the human from their own inbox (see `output-modes.md`).

---

## Defensive rendering (learned from `coach-this-rep`)

If the artifact uses Chart.js or any chart:

- Wrap the `<canvas>` in a `position: relative` div with an **explicit height** — a bare canvas
  with `maintainAspectRatio:false` renders blank/collapsed to 0px.
- Defer chart init to `DOMContentLoaded`.
- Include a **fallback message if `Chart` is undefined** (the CDN may be blocked) — show the
  snapshot table instead, never a blank box.
- Draw the chart **once on open**; never loop or auto-animate repeatedly.

For all interactive artifacts:

- **Expand/collapse via measured `max-height`** (see the reference's `toggleRegion`) so reveals
  animate smoothly and reflow correctly.
- Every interactive control carries `aria-expanded`; provide a visible focus outline (the one
  allowed 2px Deep Teal outline).
- **Respect `prefers-reduced-motion`** — collapse all transitions to instant.
- No external network calls except an optional chart CDN. No trackers, no fonts that block render
  (the font stack falls back to system grotesques).

---

## The fallback chain (always degrade gracefully)

Render tools are host-provided, not plugin-guaranteed. Never emit a broken artifact:

1. **Native interactive artifact** (headline) — when the host can render it.
2. **Static Munro widget** — if interactive rendering is unsupported, the same components without JS
   (everything visible, nothing behind a toggle).
3. **Portable Markdown** — **always written to `outputs/`, regardless** of whether 1 or 2 succeeded.

**Detect, don't assume.** If unsure the host can render an interactive artifact, write the Markdown
and *offer* the artifact ("Want me to render this as an interactive deal-review you can click
through?") rather than emit something that might break. The Markdown is the floor; the artifact is
the ceiling.

---

## The Class-C content wall (customer-facing artifacts)

Designed now, shipped behind its own review. When a customer-facing interactive artifact is built
(e.g. a checkable MAP the rep sends the buyer), it carries **zero internal content** — no MEDDPICC,
no Source column, no hygiene flags, no Manager-lens callout. These are **structurally absent** from
the artifact's data model, not hidden behind a toggle that could be left on. Because B and C are
separate artifacts (`content-model.md` §5), the wall is a class boundary enforced by construction.
Until the content-leak review ships, **do not generate a customer-facing interactive artifact** —
fall back to the stripped customer Markdown (`outputs/maps/…`).

---

## Authoring checklist

- [ ] Components and order match the Markdown projection (parity — `content-model.md` §3).
- [ ] Data is a baked snapshot; no MCP at open.
- [ ] Verdict line + anti-fabrication flags visible, not collapsible.
- [ ] 0-scored / baseline / missing-evidence states are honest, never invented.
- [ ] Drafted actions: Copy only, no send.
- [ ] `aria-expanded` + focus outlines + `prefers-reduced-motion` respected.
- [ ] Chart (if any) is defensively rendered with a `Chart`-undefined fallback.
- [ ] Default collapsed view passes the 90-second scan (`widget-brevity.md`).
- [ ] Portable Markdown written to `outputs/` regardless.
- [ ] Class C: no internal content; gated behind the content-leak review.
