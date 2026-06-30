# Artifact design — Munro Partners editorial style (live-brief widgets)

The visual design system for **rendered artifacts** — the native interactive Claude Artifact
(headline) and the static-widget fallback. Editorial parchment under alpine light: a warm cream
canvas, whisper-weight grotesque type, hairline dividers, flat surfaces, one teal action color. The
base tokens (below) define the look; the **Evolved Munro — interactivity layer** (further down)
adds interaction states, motion, and data-viz styling for the interactive medium.

**Scope:** this design applies to **rendered** output (interactive artifact + static widget) only.
Persisted files (`outputs/*.md`) stay portable Markdown — do NOT HTML-ify them; their component
forms live in `content-model.md` §2. Parity between the rendered and markdown forms is governed by
`content-model.md` §3. When a skill renders a visual artifact, use the tokens and rules below; for
how to emit and degrade the interactive artifact, see `native-artifact.md`.

## The rules that matter most (don't break these)

- **Canvas is Cream Parchment `#fff9ee`** — never pure white as the page base. Paper White `#ffffff` is only for elevated cards.
- **Text/borders are Bark Brown `#3f322a`** — never `#000000` for body, headings, or borders. Ink black only inside form inputs (rare in our briefs).
- **One typeface:** Neue Haas Grotesk Display (fallback Inter). Display headline at **weight 400** (it whispers); 600 for subheads; 700 only for small-caps section labels and wordmarks.
- **Flat — no shadows, no gradients, ever.** Separate content with 1px Stone `#c5bdb3` hairlines and the cream/paper contrast, not boxes or elevation.
- **2px border-radius** for cards, badges, buttons. **15px** only for images. Never mix.
- **Deep Teal `#004e4e`** is the single filled action color — reserve for exactly one primary action per view. (Note: the design's "Agent Prompt Guide" mentions Iris `#a56eff` as a filled action variant; prefer Deep Teal for the one primary action, Iris only as a card accent border.)
- **Accent border cards:** cream fill, 1px chromatic border (Aubergine `#560e4b`, Iris `#a56eff`, Cobalt `#3074f9`, or Ice Blue `#bfebfe`) — one accent per card. Use sparingly for the verdict / most important card.
- **Section labels:** 12px, weight 700, UPPERCASE, letter-spacing 0.017em, Bark Brown. No accent line — the casing does the work.
- **Body:** 14px/1.43 Bark Brown on cream. Never larger than 16px or smaller than 14px for body.
- **Data tables:** stacked rows, 1px Stone hairlines between, label in Earth `#796e65` left, value in Bark Brown right-aligned. No header row, no zebra striping.

## Drop-in CSS (paste into the widget `<style>`)

```css
:root{
  --cream:#fff9ee; --paper:#ffffff; --ink:#3f322a; --warm-gray:#9f968c;
  --stone:#c5bdb3; --earth:#796e65; --teal:#004e4e; --aubergine:#560e4b;
  --iris:#a56eff; --cobalt:#3074f9; --ice:#bfebfe;
  --font:'Neue Haas Grotesk Display',Inter,'Helvetica Neue',ui-sans-serif,system-ui,sans-serif;
}
body{background:var(--cream);color:var(--ink);font-family:var(--font);
  font-size:14px;line-height:1.43;letter-spacing:.24px;margin:0;padding:40px;
  max-width:1280px;}
h1,.display{font-weight:400;font-size:43px;line-height:1.09;letter-spacing:.39px;margin:0 0 20px;}
.verdict{font-weight:400;font-size:30px;line-height:1.13;letter-spacing:.39px;}
.label{font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.017em;color:var(--ink);margin:0 0 8px;}
p{font-size:14px;line-height:1.43;color:var(--ink);max-width:680px;}
hr{border:0;border-top:1px solid var(--stone);margin:40px 0;}
.card{background:var(--cream);border:1px solid var(--stone);border-radius:2px;padding:20px;margin:0 0 20px;}
.card.accent-aubergine{border-color:var(--aubergine);}
.card.accent-iris{border-color:var(--iris);}
.card.accent-cobalt{border-color:var(--cobalt);}
.card.accent-ice{border-color:var(--ice);}
.row{display:flex;justify-content:space-between;border-top:1px solid var(--stone);padding:8px 0;}
.row .k{color:var(--earth);} .row .v{color:var(--ink);text-align:right;}
.btn{background:var(--teal);color:#fff;font-weight:600;font-size:12px;text-transform:uppercase;
  letter-spacing:.018em;padding:10px 20px;border:0;border-radius:2px;}
.btn-ghost{background:none;border:0;color:var(--ink);font-weight:600;font-size:12px;
  text-transform:uppercase;letter-spacing:.018em;padding:10px 12px;}
img{border-radius:15px;}
/* health dots: use color sparingly, on cream */
.health-red{color:#c67700;} .health-amber{color:var(--amber,#c67700);} .health-green{color:var(--teal);}
```

## Widget skeleton (how a brief should be structured)

```html
<style>/* the CSS above */</style>
<p class="label">DEAL REVIEW · ACME Q3 · 2026-06-07</p>
<p class="verdict">One-sentence verdict in whisper-weight 30px.</p>
<hr>
<div class="card accent-aubergine">
  <p class="label">Biggest exposure</p>
  <p>The specific risk, with a quoted moment.</p>
</div>
<div class="card">
  <p class="label">Two-week plan</p>
  <div class="row"><span class="k">Reset close date</span><span class="v">by Jun 14 · rep</span></div>
  <div class="row"><span class="k">Develop a champion</span><span class="v">by Jun 21 · joint</span></div>
</div>
```

## Don'ts (from the reference, condensed)

- No `#000` text/borders, no pure-white canvas, no shadows, no gradients, no radius >2px on non-image elements, no stacked accent colors in one card, no weight-700 body copy, no body text outside 14–16px, no Saffron/Amber as primary CTAs.

---

## Evolved Munro — the interactivity layer

The tokens above were built for static widgets. The **headline output is now a native interactive
artifact** (`native-artifact.md`), so the system extends with interaction states, motion, and
data-viz styling. The governing rule is unchanged: **editorial restraint**. Interactivity must feel
**premium, not gamified** — elevation comes from the cream/paper contrast and hairlines, never from
shadows or bounce. The working reference is `shared/reference/deal-review-beauhurst.html`.

### Interaction states

- **Hover** uses the existing cream→paper contrast as elevation (no shadow). A row/control gets a
  **1px Deep Teal left-edge** on hover.
- **Focus** — a **2px Deep Teal outline** (`outline-offset:-2px` inside controls). This is the one
  allowed outline, for accessibility. Never remove focus visibility.
- **Expanded** cards keep the paper fill + an accent left-border; the chevron rotates 180°.
- **Active** (button press) — a 1px `translateY` only. No scale, no glow.

### Motion

- **120ms** for state changes (hover, color), **200–240ms** for reveals (expand/collapse).
- Easing `cubic-bezier(.2,0,.2,1)` — no overshoot, no spring.
- Charts **draw once on open**, never loop.
- **`@media (prefers-reduced-motion: reduce){ *{transition-duration:0ms !important;} }`** — always
  include it.

### Data-viz tokens

- Canvas stays **cream**; gridlines are **Stone at 50%** opacity.
- Categorical ramp from the existing palette: **Deep Teal (primary series) → Aubergine → Iris →
  Cobalt → Ice**. Deep Teal always carries the main series.
- **2px flat lines, no area fills, ever.** Bars are flat cream-on-stone with a single accent.
- Dials/health reuse the existing `.health-*` colors — no new reds.
- **Sparklines:** 1px, and only render with **≥2 real data points** (one point is a dot + a
  "baseline" note, never a line).

### Drop-in interactivity CSS (extends the base CSS)

```css
:root{ --ease:cubic-bezier(.2,0,.2,1); }
/* hover elevation via contrast + teal edge, never shadow */
.pillar-btn,.disclose-btn{transition:background .12s var(--ease);border-left:2px solid transparent;}
.pillar-btn:hover,.disclose-btn:hover{background:var(--paper);border-left-color:var(--teal);}
.pillar-btn:focus-visible,.disclose-btn:focus-visible{outline:2px solid var(--teal);outline-offset:-2px;}
/* chevron + measured-height reveal */
.chev{transition:transform .2s var(--ease);} [aria-expanded="true"] .chev{transform:rotate(180deg);}
.pillar-ev,.disclose-region{max-height:0;overflow:hidden;transition:max-height .2s var(--ease);}
.btn{transition:opacity .12s var(--ease);} .btn:hover{opacity:.88;} .btn:active{transform:translateY(1px);}
@media (prefers-reduced-motion: reduce){ *{transition-duration:0ms !important;} }
```

JS pattern for a measured-height reveal (so it animates and reflows correctly):

```js
function toggleRegion(btn, region){
  const open = btn.getAttribute("aria-expanded") === "true";
  btn.setAttribute("aria-expanded", String(!open));
  region.style.maxHeight = open ? "0px" : (region.scrollHeight + 24) + "px";
}
```

---

## Component forms — markdown side

`artifact-design.md` governs the *rendered* (interactive / static-widget) forms. The **markdown
form** of each component — for the portable `.md` fallback — is defined in `content-model.md` §2.
The two are kept in parity by the content model (`content-model.md` §3): same components, same
order, different medium. Design tokens here apply to rendered views only; the `.md` stays plain,
paste-friendly Markdown and carries no CSS.

---

Full reference (tokens, components, imagery, layout) is preserved verbatim below for anyone extending the system.

---

<!-- Full Munro Partners style reference retained for completeness -->

(See the brand reference: warm cream `#fff9ee` canvas, Bark Brown `#3f322a` ink, Neue Haas Grotesk Display, Deep Teal `#004e4e` single action color, 2px/15px radii, flat hairline-separated editorial layout, full-bleed landscape photography for heroes. Type scale: caption 10px, body 14px, heading-sm 22px, heading 30px, heading-lg 43px, display 68px. Spacing base 4px; section gap 64px; card padding 20px; page max-width 1280px.)
