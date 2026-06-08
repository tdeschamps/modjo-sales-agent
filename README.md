# Modjo Sales Agent

<p align="center">
  <img src="https://gifrific.com/wp-content/uploads/2014/01/Jordan-Belfort-Pound-Chest-at-Restaurant-The-Wolf-of-Wall-Street.gif" alt="The name of the game: close." width="480">
</p>

> **Your Modjo data, weaponized.** 18 AI skills that prep your meetings, audit your deals, score your calls, coach your reps, and hunt your expansion — straight off your Modjo conversations. The agent already read every call. Now it does the work.

**Stop digging through call recordings. Start closing.** Every morning brief, deal audit, pipeline review, and coaching session — pulled from what your buyers *actually said*, drafted and ready, in 90 seconds. No copy-paste. No "what did they say on the last call?" The agent read it. It remembers. It acts.

```text
/plugin marketplace add tdeschamps/modjo-sales-agent
/plugin install modjo-sales-agent
```

— then `/modjo-sales-agent:start-day` and watch your day get triaged for you. Full install options below. ⬇️

## What it is

The Modjo Sales Agent turns your Modjo conversation intelligence into automated sales workflows. Every skill is built around a real sales job-to-be-done and runs on your Modjo calls, deals, accounts, contacts, emails, and AI agents directly. No re-typing, no copy-paste, no asking "what did this rep say on the last call?" — the agent reads it and acts on it.

**Why reps actually keep it open:**

- 🌅 **Walk in already prepped** — `/start-day` and `/prep-meeting` turn this morning's calendar into a battle plan built from real call history.
- 🎯 **Never wing a deal review** — `/audit-deal` scores MEDDPICC from what buyers said, not what the CRM wishes were true.
- 📞 **Every call makes you sharper** — `/score-call` grades the call and hands you the exact line to say next time.
- 🔭 **See the upside first** — `/expansion-scan` and `/review-pipeline` surface the deals and signals you'd have missed.
- 🧠 **Coaching that sticks** — `/coach` tracks each rep's themes week over week with quoted evidence, not vibes.
- 🚫 **It won't make stuff up** — missing evidence gets flagged, never invented. (We built a whole eval harness to prove it.)

## Install & first run

This repo is a self-contained Claude Code plugin **and** marketplace. After the two-command install above, reload and run your first skill:

```text
/reload-plugins
/modjo-sales-agent:start-day
```

> Plugin skills are namespaced — every command is `/modjo-sales-agent:<command>` (e.g. `/modjo-sales-agent:audit-deal Acme`). This prevents conflicts with other plugins.

### Other ways to install

| Method | Command | When to use |
|---|---|---|
| **Marketplace** (recommended) | `/plugin marketplace add tdeschamps/modjo-sales-agent` → `/plugin install modjo-sales-agent` | Normal install + easy updates |
| **Try without installing** | `claude --plugin-dir /path/to/modjo-sales-agent` | Kick the tires locally first |
| **Clone then load** | `git clone https://github.com/tdeschamps/modjo-sales-agent && claude --plugin-dir ./modjo-sales-agent` | Local dev / customizing skills |

### Update / uninstall

```text
/plugin marketplace update modjo-sales-agent     # pull the latest version
/plugin uninstall modjo-sales-agent
```

**Prerequisite:** the [Modjo MCP](CONNECTORS.md) connected in your host for the full experience. Not on Modjo yet? Every skill also runs in CSV / paste-in mode — see `shared/csv-schemas.md`. Next step after install: the [Setup](#setup) section below.

## How it works

Three layers, in order of how much capability they unlock:

1. **Your Modjo workspace** *(required for the full experience)* — the agent uses Modjo's MCP to pull calls, deals, accounts, contacts, emails, transcripts, and your team's Modjo agents (MEDDPICC scoring, coaching, next-step extraction, briefing, etc.). Agents are discovered at runtime — your team's specific agent names and UUIDs are picked up automatically.
2. **Notion** *(optional — adds persistence)* — coaching logs, 1:1 history, Plays Library, account/deal logs. Without Notion, every skill still runs as a live brief in the chat; with Notion, the toolkit accumulates longitudinal data the manager can come back to.
3. **CSV paste-in onramp** *(optional fallback)* — if you haven't enabled Modjo yet, every skill accepts a CSV or paste-in equivalent. See `shared/csv-schemas.md`. Once you turn Modjo on, the same skills run on live data automatically.

See `CONNECTORS.md` for the per-connector capability matrix.

## The 19 skills

**Daily rhythm**

| Skill | Slash command | What it does |
|---|---|---|
| `start-the-day` | `/start-day` | Morning brief — today's meetings + 3 deals to move + 1 pattern from this week's calls |
| `prep-this-meeting` | `/prep-meeting [account]` | Deep prep for one specific upcoming call |

**Per-deal execution**

| Skill | Slash command | What it does |
|---|---|---|
| `audit-this-deal` | `/audit-deal [name]` | Current-state assessment with MEDDPICC from real calls |
| `learn-from-similar-deals` | `/find-similar [deal]` | Comparable past wins/losses with the play that worked |
| `lock-the-close-plan` | `/close-plan [deal]` | Build or refresh the customer-shareable Mutual Action Plan |
| `unstick-this-deal` | `/stuck-on [deal]` | 90-second tactical answer when a deal is stuck |
| `score-this-call` | `/score-call [call]` | Score one call + drafted next-time play |

**Portfolio view**

| Skill | Slash command | What it does |
|---|---|---|
| `review-the-pipeline` | `/review-pipeline` | Weekly triage — hot/watch/at-risk/disqualify with drafted actions |
| `build-net-new-pipeline` | `/build-pipeline [segment]` | Net-new target list with personalised outbound drafts |
| `audit-the-forecast` | `/audit-forecast` | CRM hygiene issues distorting forecast + a 30-min cleanup plan |
| `forecast` | `/forecast` | Worst/Commit/Likely/Best with gap-to-quota and swing deals |

**Prospecting & competitive**

| Skill | Slash command | What it does |
|---|---|---|
| `account-research` | `/account-research [name]` | Cold account intel for prospecting + drafted opening hook |
| `competitive-intelligence` | `/competitive-intel [name]` | Battlecard from your lost/won deals + public intel |

**Coaching & reflection**

| Skill | Slash command | What it does |
|---|---|---|
| `coach-this-rep` | `/coach [rep]` | Manager-driven weekly review with theme tracking week-over-week |
| `prep-the-1on1` | `/prep-1on1` | Focused 1:1 agenda anchored in real call evidence |
| `learn-from-closed-deals` | `/win-loss` | Pattern extraction from closed deals → Plays Library entries |

**Post-sale**

| Skill | Slash command | What it does |
|---|---|---|
| `spot-expansion-signals` | `/expansion-scan` | Upsell signals from your customer calls + book activity |
| `hand-off-to-csm` | `/csm-handoff [deal]` | AE→CSM handover package with commitments quoted from calls |

**Meta**

| Skill | Slash command | What it does |
|---|---|---|
| `sales-router` | `/router` | Not sure which skill to invoke? Describe what you need, get routed |

## How outputs work

Every skill has the same output contract:

1. **Live brief** *(default)* — rendered as a scannable widget in the chat (verdict line + 3–5 cards + optional drill-down, ≤ 350 words per the 90-second-scan discipline in `shared/widget-brevity.md`), styled per the editorial design system in `shared/artifact-design.md`
2. **Persisted artifact** *(optional, approval-gated)* — for skills that benefit from persistence (coaching, MAP, audits, expansion logs, plays library). **Notion is optional**: if a workspace MCP is connected it writes there; otherwise it writes a portable, dual-audience Markdown file to `outputs/` structured for both the rep and their manager (Summary · For the rep · For the manager · Evidence)
3. **Slack draft** *(optional, approval-gated)* — for skills that produce something rep-shareable (talk tracks, outbound, escalation prep)

Hard rules across every skill:

- **Never auto-sends.** Slack drafts are drafts. Notion writes ask before creating new pages.
- **Never writes to your CRM.** The agent surfaces issues and proposes fixes; you apply them.
- **Single-question agent framings.** Multi-part agent questions return empty — confirmed failure mode.
- **Anti-fabrication.** No invented quotes, themes, deltas, or precedents. Missing evidence is labelled, not silently filled in.

## Setup

1. **Connect Modjo** — the agent looks for your workspace's Modjo MCP. From your host (Cowork / Claude Code), open the connector picker and authenticate Modjo.
2. *(Optional)* **Connect Notion** — for persistence. Create a top-level page called `Sales Coaching` with sub-pages per IC (`[IC Name] — Coaching`) and a `Plays Library` page. See `shared/notion-structure.md` for the recommended hierarchy.
3. *(Optional)* **Fill in `shared/icp-and-personas.md`** if you want `build-net-new-pipeline` and `learn-from-similar-deals` to score against your real ICP rather than inferred patterns.
4. **Try a skill.** `/start-day`, `/audit-deal [your hardest open deal]`, or `/coach [a rep's name]` — pick one.

Without Modjo connected, every skill still runs in CSV/paste-in mode. See `shared/csv-schemas.md` for the exact paste-in formats.

## Design principles

- **Modjo-first.** The agent is built for Modjo customers. The CSV paste-in path exists as an onramp, not as the primary mode.
- **Agent discovery, not hard-coded UUIDs.** The agent discovers your team's Modjo agents at runtime via `get_agents`. Customers with renamed or custom agents work without plugin changes.
- **Approval-gated external writes.** Notion writes and Slack drafts require explicit user confirmation.
- **Anti-fabrication discipline.** Codified in every skill's `# Rules` section. Baseline weeks are labelled. Missing evidence is named.
- **Theme tracking is real or absent.** Theme tracker only shows weeks with real logged entries — no back-filled history, no manufactured deltas.

## Per-skill structure

Every SKILL.md follows the same pattern:

1. Frontmatter — `name` + `description` (≤ 310 chars, "Works with Modjo / CSV onramp" framing)
2. `## Data sources` preamble — pointer to the Modjo operation map
3. Role-assertion line
4. `# What I need from you` — Minimum / Better / Best tiers, user-facing
5. `# Inputs` — procedural detail Claude follows
6. Frameworks-to-load — shared refs
7. `# Data to pull` — Modjo MCP operations in order
8. `# Output` + `## Example skeleton` — concrete widget shape with placeholders
9. `# Rules` — anti-fabrication, approval-gates, never-write-CRM

## v0.1.0 notes

- 19 skills, all implemented. None are stubs.
- Methodology rubric stays swappable — ships with MEDDPICC; teams using BANT / SPICED / MEDDIC can swap the file content from `shared/qualification-rubrics/`.
- `forecast` requires the user to provide a quota — gap analysis without a quota is meaningless, so the skill asks rather than assumes.
- `competitive-intelligence` is honest about sample size — battlecards built from ≤ 3 lost deals are labelled "anecdote, not pattern."
- `sales-router` is pure routing — no data fetch, no connector dependency.

## What's not in v0.1

- **Telemetry & measurement infrastructure** — deferred until there's real usage to measure. The skill outputs are designed to be measurable later (every skill ends with a structured next-action that can be tracked downstream).
- **CRM write-back** — the agent never writes to your CRM. Future versions may add carefully-guardrailed write paths.
- **Multi-language coaching prompts** — French/Spanish/German prompts on the roadmap.
