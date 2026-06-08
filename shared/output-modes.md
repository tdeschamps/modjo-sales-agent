# Output modes

Every skill in this plugin supports three output modes. The skill picks the right combination based on the type of artifact; never invent a fourth mode (e.g. auto-sending to Slack) without explicit user consent.

## 1. Live brief (default)

Render the output as a visual widget via `mcp__visualize__show_widget` (HTML/CSS). **All live-brief widgets follow the Munro editorial design system in `artifact-design.md`** — cream parchment canvas, Bark Brown ink, whisper-weight grotesque, flat hairline-separated cards, one Deep Teal action. Use the drop-in CSS and widget skeleton from that file; do not invent a different look. The user reads it and copies what they need. No external writes.

**Persisted files stay portable Markdown** (mode 2) — the Munro design applies to the on-screen widget, NOT to the `.md` artifacts (Markdown carries no CSS and must stay paste-friendly).

**Use for**: prep-this-meeting briefs, start-the-day, audit-this-deal, review-the-pipeline snapshots, win-loss readouts.

## 2. Persisted artifact — Notion OPTIONAL, portable Markdown is the default

Skills that produce something worth keeping (a coaching log, a 1:1 agenda, a close plan, a win-loss readout, a CSM handover) persist it. **Notion is optional, never required.** Decide the target at runtime:

- **If a Notion (or equivalent workspace) MCP is connected** and the user wants it persisted there: write a structured page via `workspace_create_page` / `workspace_update_page`, following `notion-structure.md`. Always search before creating to avoid duplicates, and always ask before creating a new structural page.
- **If no workspace MCP is connected** (the common case): write a **portable Markdown artifact** to disk at `outputs/<skill>-<entity>-<YYYY-MM-DD>.md`. No external dependency, opens anywhere, and the user can later paste it into Notion/email/Slack. This is the default — never block a skill's value on Notion being set up.

Detect, don't assume: if you're unsure whether a workspace MCP is available, default to the Markdown artifact and mention Notion is available as an option if they connect it.

### The portable artifact format — dual-audience (rep + manager)

Persisted artifacts serve BOTH the rep (managee) and their manager, so structure every artifact in three parts:

```markdown
# <Skill> — <Entity> · <Date>

## Summary
<3-5 line shared snapshot both audiences read first: the verdict, the state, the one number that matters.>

## — For the rep —
<What the rep does next: dated actions, drafts to send, the specific moves. Practical and personal.>

## — For the manager —
<What the manager needs to see: risk/health call, where to coach or intervene, what to ask in the 1:1. No fluff the rep section already covers.>

## Evidence
<Quoted moments / deal facts / citations that back the above — so neither audience has to take a claim on faith.>
```

Skills whose output is inherently single-audience (e.g. a pure outbound draft) may omit a role section, but most coaching/deal/pipeline artifacts should carry both. Keep the same brevity discipline as the live brief.

**Use for**: coach-this-rep log entries, prep-the-1on1 agendas, lock-the-close-plan, win-loss findings, hand-off-to-csm packages.

## 3. Slack-ready draft

Produce a Slack-formatted message (with proper markdown, mentions where known, ≤2000 chars) that the user can paste or that we hand to `draft_slack_message` (e.g. Slack `slack_send_message_draft`) (which creates a draft for human review, never auto-sends). Always show the draft inline first so the user can edit before approval.

**Use for**: build-net-new-pipeline outbound drafts, learn-from-similar-deals email follow-ups, start-the-day "share with manager" digests, spot-expansion-signals internal flags.

## Hard rules

- **Never auto-send** to Slack, email, or any external system. Drafts only.
- **Never write to Salesforce or any CRM** in v0.2. Out of scope, will be added with careful guardrails later.
- **Notion is optional — never a prerequisite.** If no workspace MCP is connected, persist to a portable Markdown artifact in `outputs/`; the skill must deliver full value with zero Notion setup. Only ask before writing to Notion if a workspace MCP IS connected and the target page doesn't already exist.
- **Persisted artifacts are dual-audience.** Structure coaching/deal/pipeline artifacts with a shared Summary + "— For the rep —" + "— For the manager —" + Evidence, so the same file serves the managee and the manager.
- **Always render the live brief first** even when also persisting an artifact or producing a Slack draft, so the user sees what's being saved.
