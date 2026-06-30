# Output modes — delivery channels for artifacts

This file covers **how** an artifact reaches the user (the channels) and the **hard rules** that
govern every external write. **What** an artifact is — the four classes, the component vocabulary,
the rendered↔markdown parity — lives in `content-model.md`. **How** to author the headline
interactive artifact lives in `native-artifact.md`. Read those for structure; read this for
delivery and guardrails.

Every artifact belongs to one of four classes (`content-model.md` §1): **A — ephemeral brief ·
B — persisted record · C — customer-facing sendable · D — internal draft/nudge**. The channels
below are how each class is delivered. Never invent a channel that auto-sends.

---

## Channel 1 — Native interactive artifact (the headline)

The primary rendered output for Class A/B is a **native interactive Claude Artifact** — a
self-contained, clickable view (expandable scorecard, collapsible stakeholder map, live trend
chart), styled with the **evolved-Munro** design system in `artifact-design.md`. It **bakes in a
snapshot** of the data the skill pulled — it does not call MCP at open time; "refresh" = re-run the
skill (`native-artifact.md`).

This supersedes the old hand-rolled `show_widget` HTML as the headline. `show_widget` survives only
as a **fallback rung** (below). The full recipe, honesty rules, and authoring checklist are in
`native-artifact.md`.

**The fallback chain — never emit a broken artifact:**
1. Native interactive artifact (when the host can render it).
2. Static Munro widget (interactive unsupported → same components, no JS).
3. **Portable Markdown — always written to `outputs/`, regardless.**

Detect, don't assume: if unsure the host can render, write the Markdown and *offer* the artifact.

**Use for**: audit-this-deal, coach-this-rep, review-the-pipeline, start-the-day, prep-this-meeting,
win-loss readouts — any Class A/B skill.

## Channel 2 — Persisted artifact (Notion OPTIONAL, portable Markdown is the default)

Class B skills produce something worth keeping (a coaching log, a 1:1 agenda, a close plan, a
win-loss readout, a CSM handover). They persist it. **Notion is optional, never required.** Decide
the target at runtime:

- **If a Notion (or equivalent workspace) MCP is connected** and the user wants it persisted there:
  write a structured page via `workspace_create_page` / `workspace_update_page`, following
  `notion-structure.md`. Always search before creating to avoid duplicates, and always ask before
  creating a new structural page.
- **If no workspace MCP is connected** (the common case): write a **portable Markdown artifact** to
  `outputs/<skill>-<entity>-<YYYY-MM-DD>.md`. No external dependency, opens anywhere, paste-able
  into Notion/email/Slack later. This is the default — never block a skill's value on Notion.

Detect, don't assume: if unsure a workspace MCP is available, default to the Markdown artifact and
mention Notion is available if they connect it.

The portable artifact uses the **markdown component forms** in `content-model.md` §2 and **may**
carry the optional YAML front-matter (`content-model.md` §4) so future runs parse structure rather
than prose. The body is organized by substance, with one **Manager-lens callout** carrying the
manager's takeaway — see "Dual-audience" below.

**Use for**: coach-this-rep logs, prep-the-1on1 agendas, lock-the-close-plan (internal MAP),
win-loss findings, hand-off-to-csm packages.

## Channel 3 — Slack-ready draft

Produce a Slack-formatted message (proper markdown, mentions where known, ≤2000 chars) that the
user can paste or that we hand to `slack_send_message_draft` (creates a draft for human review,
never auto-sends). Always show the draft inline first so the user can edit before approval.

**Use for**: build-net-new-pipeline outbound drafts, learn-from-similar-deals follow-ups,
start-the-day "share with manager" digests, spot-expansion-signals internal flags.

## Channel 4 — Gmail draft handoff (optional — `write-the-follow-up`)

A variant of the draft contract for email, available only when Gmail is connected. After the email
is rendered inline and the user approves it, the skill places it as a **draft in the user's
mailbox** via `create_draft` — threaded to the conversation, correct recipient and subject — for
the user to review and send from their own inbox.

This is still "drafts only, never auto-send": there is no send path. It removes the copy-paste step,
not the human's hand on the send button.

- **Always render the email inline first**, so the user sees exactly what would be created.
- **Ask before creating the draft** ("Want me to drop this in your Gmail drafts, threaded to the
  [X] thread?"). Only create on an explicit yes.
- **Thread it.** Pass the `threadId`; don't start a new thread.
- **Also persist the portable copy** (`outputs/`) so the email is recoverable without Gmail.

**Use for**: write-the-follow-up. (Reusable by other email-drafting skills under the same draft-only
guarantee.)

---

## Dual-audience — the Manager-lens callout (replaces the old role-split template)

Class B artifacts serve the rep **and** the manager. **Do not** use a rigid
`— For the rep — / — For the manager —` split — it fights how reps organize content and had no
adoption. Instead:

- The **body stays substance-organized** (the default reader is the rep).
- One **Manager-lens callout** carries the manager's takeaway — the risk/health call, the one thing
  to raise in the 1:1, where to intervene. A pointer *into* the body, not a duplicate section.
- The shared **verdict line** is read by both.

This serves the manager without needing to know *who asked*, so it's robust to identity ambiguity.
Component forms for the callout: `content-model.md` §2. The full rationale: `content-model.md` §5.

**Customer-facing artifacts (Class C) carry zero internal content** — no Manager-lens, no MEDDPICC,
no Source column. B and C are *separate artifacts* so the wall is enforced by construction
(`content-model.md` §5).

---

## Hard rules

- **Never auto-send** to Slack, email, or any external system. Drafts only. The Gmail draft handoff
  (channel 4) creates a draft in the user's mailbox — it never sends; the user sends from their
  inbox. No artifact has a send affordance — a drafted action ships with **Copy, never Send**.
- **Never write to Salesforce or any CRM** in v0.2. Out of scope, will be added with careful
  guardrails later.
- **Notion is optional — never a prerequisite.** If no workspace MCP is connected, persist to a
  portable Markdown artifact in `outputs/`; the skill must deliver full value with zero Notion
  setup. Only ask before writing to Notion if a workspace MCP IS connected and the target page
  doesn't already exist.
- **Persisted artifacts are dual-audience.** Use the substance-organized body + a Manager-lens
  callout (above) so the same artifact serves the managee and the manager.
- **Always render the live brief first** even when also persisting an artifact or producing a Slack
  draft, so the user sees what's being saved.
- **Anti-fabrication carries into every channel.** No invented quotes, themes, deltas, or
  precedents — in the artifact, the Markdown, or the draft. A 0-scored pillar shows "scored 0", not
  a fabricated quote; baseline weeks are labelled; missing evidence is named (`native-artifact.md`).
