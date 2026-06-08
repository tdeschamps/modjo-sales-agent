# Notion Structure for Sales Coaching

All three skills assume the following Notion structure. If pages don't exist yet, the skill should create them via `workspace_create_page` (e.g. Notion `notion-create-pages`) on first run.

## Top-level workspace page

**Page title**: `Sales Coaching` (search with `notion-search` query="Sales Coaching")

Under it, one sub-page per IC:

```
Sales Coaching/
├── [IC Name] — Coaching
│   ├── Objectives (current quarter)
│   ├── Coaching Log
│   │   ├── 2026-W21 — Weekly review
│   │   ├── 2026-W20 — Weekly review
│   │   └── ...
│   ├── 1-on-1 Notes
│   │   ├── 2026-05-21 — 1:1 with [Manager]
│   │   └── ...
│   └── Development Themes (rolling)
```

## Objectives page — expected structure

The skill reads this as plain markdown / blocks. It expects (loosely):

```markdown
## Quarterly objectives — Q2 2026

- **Quota**: €450k ARR — Currently: €212k (47%)
- **Activity**: 60 quality discos / quarter — Currently: 28
- **Win rate**: 25% on qualified pipeline — Currently: 18%

## Development focus this quarter

1. Objection handling — pricing pushback specifically
2. Multi-threading — at least 3 contacts per active deal
3. Champion testing — never skip the "what would block this?" question
```

If the format differs, the skill should parse what it can and surface a flag: "Objectives page format unclear — pulled best-effort interpretation." Never invent missing objectives.

## Coaching Log entries — write format

When the **coach-this-rep** skill writes a new entry, use this exact template so future runs can parse the prior week:

```markdown
# [YYYY-Www] — Weekly review — [IC Name]

**Reviewed by**: [Manager]
**Calls reviewed**: [N calls, list crmLinks]
**Period**: [YYYY-MM-DD] → [YYYY-MM-DD]

## Headline
[One-sentence framing of the week.]

## Wins (reinforce)
- [theme: ...] [Specific moment + evidence]

## Gaps (work on)
- [theme: ...] [Specific moment + evidence + suggested fix]

## MEDDPICC snapshot — active deals
- [Deal name]: M:_ E:_ D-crit:_ D-proc:_ P:_ I:_ C-hamp:_ C-omp:_ | Total: __/16
- ...

## Trend vs last week
- [theme]: ↑ improving / ↓ regressing / → flat
- ...

## Focus for next week
1. [Specific behavior + measurable]
2. ...
```

## 1-on-1 Notes — write format

When **prep-the-1on1** generates an agenda, use:

```markdown
# [YYYY-MM-DD] — 1:1 with [Manager] — [IC Name]

## Anchors
- Objective progress: [Quota X%, Activity Y%, Win rate Z%]
- Last week's coaching focus: [theme + status]

## Topics
### 1. [Topic title] — [type: win | blocker | development | strategic ask]
**Why this matters**: [one line]
**Evidence**: [call/deal/email reference]
**What I need from you**: [specific ask]

### 2. ...

## Questions for [Manager]
- ...
```

## Tool reference cheatsheet (Notion MCP)

| Action | Tool | Key params |
|---|---|---|
| Find a page by title/text | `notion-search` | `query: "Sales Coaching"` |
| Read page content | `notion-fetch` | `urls: [page_url]` |
| Create a new page | `notion-create-pages` | `pages: [{ parent: {...}, properties: { title }, content }]` |
| Update existing page | `notion-update-page` | `page_id`, `command: "replace_content" \| "append_content"` |

**Always search before creating.** Notion has a flat search — if a page named "[IC Name] — Coaching" exists, find it; don't create a duplicate.
