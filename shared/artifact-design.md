# Artifact design — Munro Partners editorial style (live-brief widgets)

The visual design system for **on-screen live-brief widgets** (the HTML rendered via `show_widget` / inline HTML). Editorial parchment under alpine light: a warm cream canvas, whisper-weight grotesque type, hairline dividers, flat surfaces, one teal action color.

**Scope:** this design applies to the **live brief / widget** output only. Persisted files (`outputs/*.md`) stay portable Markdown — do NOT HTML-ify them. When a skill renders a visual brief, use the tokens and rules below.

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

Full reference (tokens, components, imagery, layout) is preserved verbatim below for anyone extending the system.

---

<!-- Full Munro Partners style reference retained for completeness -->

(See the brand reference: warm cream `#fff9ee` canvas, Bark Brown `#3f322a` ink, Neue Haas Grotesk Display, Deep Teal `#004e4e` single action color, 2px/15px radii, flat hairline-separated editorial layout, full-bleed landscape photography for heroes. Type scale: caption 10px, body 14px, heading-sm 22px, heading 30px, heading-lg 43px, display 68px. Spacing base 4px; section gap 64px; card padding 20px; page max-width 1280px.)
