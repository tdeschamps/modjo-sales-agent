# Content model — the shared artifact spec

This is the **single source of truth** for what the Modjo Sales Agent produces. Every skill's
output is one or more **artifacts**; every artifact is built from a shared **component
vocabulary**; every component has a defined form in each medium. Skills stop inventing their own
headings — they compose named components.

The companion files:
- `artifact-design.md` — the visual tokens + the interactive (evolved-Munro) CSS for the rendered forms.
- `native-artifact.md` — the recipe for emitting a native interactive artifact + the fallback chain.
- `output-modes.md` — the delivery channels and the hard rules (never auto-send, never write CRM, …).
- `shared/reference/deal-review-beauhurst.html` — a **real, working reference artifact** that
  implements this model end-to-end. When in doubt, copy it.

---

## 1. Artifact taxonomy — four classes

An artifact is classified by the properties that actually change how it must be built:
**audience · lifespan · channel · whose voice**.

| Class | Audience | Lifespan | Headline channel | Voice | Native interactive artifact? |
|---|---|---|---|---|---|
| **A — Ephemeral brief** | Rep (sometimes +mgr) | Read once, act, discard | Interactive artifact (static-leaning) | Agent-analytic | Light. Static Munro + collapsed drill-down; full interactivity only when the data warrants it (e.g. a heavy `start-the-day`). |
| **B — Persisted record** | Rep **and** manager | Durable — re-read across weeks, parsed by future runs | **Interactive artifact (headline)** + portable Markdown | Agent-analytic | **Yes — the flagship class.** |
| **C — Customer-facing sendable** | The customer / champion | Sent once, then it's theirs | Markdown / Gmail draft (interactive later) | The **rep's** voice (or neutral customer-pro) | Designed now, shipped later — content wall first. |
| **D — Internal draft / nudge** | Rep's own use, or a colleague | Sent once | Slack draft / Gmail draft / inline | The rep's voice | **No.** A draft is text bound for another compose box. |

A skill **declares which classes it emits**. Multi-class skills are the rule, not the exception.

### Skill → class map

| Skill | Class(es) | Note |
|---|---|---|
| `start-the-day` | A (+ D drafts inside cards) | Daily brief; embeds drafted actions |
| `prep-this-meeting` | A | Opener + rebuttals, used live |
| `review-the-pipeline` | A (+ D) | At-risk drafted nudge |
| `audit-the-forecast` | A (+ D) | Hygiene + buyer-touch draft |
| `forecast` | A | Internal number; deliberately not output-driven |
| `account-research` | A (+ D) | Drafted first-touch |
| `competitive-intelligence` | A (+ D talk tracks) | Battlecard is reference; talk tracks sendable |
| `spot-expansion-signals` | A (+ D) | Known precision caveat — see memory |
| `learn-from-similar-deals` | A | Coaching reference |
| `sales-router` | A | Pure routing, no data fetch |
| `audit-this-deal` | **A + B** (+ D) | Widget + persisted analysis + drafted move. The reference artifact. |
| `score-this-call` | A (+ B log, + D next-time email) | Scorecard + optional persisted coaching point |
| `unstick-this-deal` | **D** (+ A diagnosis) | The output *is* the drafted move |
| `write-the-follow-up` | **C / D** | The email itself; Gmail draft handoff |
| `build-net-new-pipeline` | A + **D** | Ranked targets + drafted first-touches |
| `coach-this-rep` | **B** (+ A live view) | The dual-audience case; the interactive prototype |
| `prep-the-1on1` | **B** (+ A) | 1:1 agenda, persisted, parseable |
| `learn-from-closed-deals` | **B** (+ A) | Win-loss → Plays Library |
| `lock-the-close-plan` | **B + C** (+ A) | Internal MAP **and** customer MAP — two separate artifacts |
| `hand-off-to-csm` | **B + C** (+ A) | Handover (B) + customer kickoff agenda (C) |

**The two-artifact rule:** when a skill emits both B and C (`lock-the-close-plan`,
`hand-off-to-csm`), they are **separate artifacts of different classes** — never one document with
an "internal" and a "customer" section. The class boundary is what guarantees no internal content
leaks to the customer (see §5).

---

## 2. The component vocabulary

Every artifact is composed of these components. Each is defined once, in three forms:
**interactive** (the headline native artifact), **static widget** (the no-JS fallback render), and
**markdown** (the portable `.md`). Skills pick and order components freely and may add a
skill-specific block — they just don't reinvent a heading style for a component already named here.

| Component | Interactive form | Static-widget form | Markdown form |
|---|---|---|---|
| **Verdict line** | `.verdict` 30px whisper — **never collapsible** | same, static | `> **Verdict:** …` after H1 |
| **Anti-fabrication flag** | inline italic label — **never collapsible, never hidden** | same | `*Baseline week — …*` |
| **Evidence card** | `.card` → click to expand the quote | `.card` with quote shown | `### claim` + `> "quote" — source · date` |
| **Scorecard** | interactive pillars — **click a pillar to reveal its evidence**; a 0-scored pillar shows "Scored 0 …", **never a fabricated quote** | static pillar list + evidence | table (Pillar / Score / Evidence) + a `RUBRIC:` codeline |
| **Stakeholder table** | collapsible; >5 rows behind a reveal | static table; >5 → drill-down | MD table |
| **Plan block** | label/value rows (step · date · owner) | same | `### plan` + dated rows |
| **Drafted-action block** | `.card.accent-cobalt` + the draft + a **Copy** button — **no send path** | same, with Copy | `> Subject:` / `> body` blockquote, labelled with voice-match status |
| **Manager-lens callout** | one `.card.accent-aubergine` — the manager's takeaway pointer | same | `> **Manager lens:** …` |
| **Drill-down** | native collapse affordance | labelled "Drill-down (optional)" | `### Drill-down (optional)` + links |
| **Trend chart** (data-viz) | Chart.js, draws once on open; **baseline week = points + annotation, never a fabricated line** | static snapshot table | MEDDPICC-snapshot table + "trend in interactive view" note |

Consistency comes from the **component set**, not from identical headings. The rich, bespoke
per-skill content survives — `eval/rubric.md` Dim 6 (skill-specific quality) explicitly protects
it. Example: the Beauhurst deal review's headings all map cleanly —

| Beauhurst heading | Component |
|---|---|
| Hygiene flags | evidence cards (a hygiene strip = evidence cards with the highest-signal flags) |
| MEDDPICC scorecard | scorecard |
| Stakeholder map | stakeholder table |
| Pivotal moment | evidence card |
| Manager lens | manager-lens callout |
| Two-week plan | plan block |
| Drafted next move | drafted-action block |
| Watch out for | drill-down / footer |

---

## 3. One content model → two projections

A Class A/B artifact is, logically, an **ordered list of typed components** (the vocabulary
above). The skill authors that list once; it is **projected** into two media:

- **Native interactive artifact** (headline) — rendered per `native-artifact.md` using the
  evolved-Munro tokens in `artifact-design.md`.
- **Portable Markdown** (fallback) — written to `outputs/` per the markdown forms above.

**Parity is by construction:** both projections carry the **same components in the same order**.
The only difference is presentation. An interactive scorecard degrades to a static markdown pillar
table; a live trend chart degrades to the snapshot table + a "trend in interactive view" note.
Nothing in the headline view exists that the fallback can't represent.

Classes **C and D are prose-native** — a customer email and a Slack nudge have no widget twin, so
there is nothing to keep in parity. They skip the content model.

### Data model — snapshot at generation

The interactive artifact **bakes in the data the skill already pulled**. It does **not** call
Modjo / Notion / any MCP at open time — most artifact sandboxes can't, and a half-loading artifact
is worse than a static one. "Refresh" means **re-run the skill**. (Live re-query is a host-gated
enhancement for environments that support it — not the baseline.)

---

## 4. Persisted records (Class B) — optional machine-readable front-matter

Class B records are re-read by **future runs** (e.g. `coach-this-rep` reads the last 6 weeks to
compute week-over-week deltas). To make that robust — parsing structure instead of regexing prose —
a persisted `.md` **may** carry YAML front-matter. It is **optional** and **invisible** when the
body is pasted into Notion / email / Slack, so it never costs paste-friendliness.

```markdown
---
skill: audit-this-deal
entity: Beauhurst
date: 2026-06-05
class: B
components: [verdict, evidence-card, scorecard, stakeholder-table, evidence-card, manager-lens, plan, drafted-action]
---

# Deal Review — Beauhurst · 2026-06-05
…
```

The body still follows the markdown component forms in §2. A future run reads the front-matter to
locate blocks; if there's no front-matter, it falls back to the prose template as today.

---

## 5. Dual-audience → the Manager-lens callout

Persisted (Class B) artifacts serve the rep **and** their manager. The old rigid
`— For the rep — / — For the manager —` split is **dropped** (it had 0% adoption — it fights how
reps actually organize content, by the deal's substance).

Instead:
- The **body stays substance-organized** (the default reader is the rep — the actions and drafts
  are theirs, no header needed).
- One **Manager-lens callout** carries the manager's takeaway: the risk/health call, the one thing
  to raise in the 1:1, where to intervene. It's a **pointer into** the shared body, not a duplicate
  section.
- The shared **verdict line** is read by both.

This matches what good outputs already do organically (the 1:1 agenda's "What I need from you"
lines are manager-lens tags inline). It needs no knowledge of *who asked* — so it works even when
the rep-vs-manager identity is ambiguous.

### The Class-C content wall

A customer-facing (Class C) artifact carries **zero internal content**. The Manager-lens callout,
the MEDDPICC scorecard, the Source/evidence column, the hygiene flags — these are **structurally
absent** from a Class C artifact, not merely hidden behind a toggle. This is why B and C are
**separate artifacts**: the wall is a class boundary, enforced by construction, not a styling
choice that could be toggled wrong.

---

## 6. Brevity in the interactive medium

The 90-second-scan discipline (`widget-brevity.md`) still governs — but for the interactive
medium it applies to the **default collapsed view**: header → verdict → 3–5 visible cards →
anti-fabrication flags must pass the scan. **Depth behind an interaction does not count against
the cap** — the collapse affordance is the native equivalent of the old "Drill-down (optional)"
section. The Markdown projection keeps the original flat cap and pushes depth into its explicit
drill-down. (`eval/rubric.md` Dim 5 grades the **collapsed** view, not the expanded DOM.)
