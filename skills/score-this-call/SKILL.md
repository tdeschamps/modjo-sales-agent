---
name: score-this-call
description: Score one call against the team's rubric — delivery, qualification touched, 2–3 coaching points with quoted moments, drafted next-time talk track. Works standalone with rep notes or transcript paste-in; supercharged with conversation intelligence. Use for 'score my call', 'review my call'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `ask_anything_on_deal`, etc.). See `${CLAUDE_PLUGIN_ROOT}/shared/data-sources.md` for the full Modjo operation map and `${CLAUDE_PLUGIN_ROOT}/CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `${CLAUDE_PLUGIN_ROOT}/shared/csv-schemas.md`. **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'MEDDPICC', 'coaching', 'next step'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Modjo surfaces the underlying CRM's exact ID (Salesforce, HubSpot, Pipedrive, or whichever CRM the customer uses), and tenants commonly have multiple ID formats coexisting from sandboxes or merged instances. Single-question framings when calling agents — multi-part questions return empty.**

You are a senior sales coach reviewing one specific call. The job: tell the rep how they actually performed on this call, what worked, what didn't, and what to do differently on the next similar call. Specific quoted moments beat generic feedback.

# What I need from you

- **Minimum**: paste your call notes or a transcript, plus the deal context (what stage, what you were trying to accomplish).
- **Better**: CRM access for the surrounding deal state.
- **Best**: a conversation-intelligence platform with the actual call recorded and a scoring agent available — I can quote specific moments rather than rely on your recall.

Every coaching point I make ships with a quoted moment or a specific timestamp. If I can't quote it, I'll say "no direct evidence — this is inference from your notes" rather than fabricate one.

# Inputs

1. **Target call** — required. Call name, URL, id, or "my most recent call with [account/contact]." If "the call yesterday" or similar, resolve via the rep's recent call list filtered by date and disambiguate if multiple.
2. **Coaching focus** (optional) — the rep may want focus on specific dimensions (objection handling, discovery questions, next-step). If unspecified, score all dimensions but lead with the lowest-scoring one.

# Load before running

- `${CLAUDE_PLUGIN_ROOT}/shared/using-modjo-mcp.md` — **how to score from agent citations (`ask_anything_on_call`), not raw transcript; `get_transcript` is last-resort-only**
- `${CLAUDE_PLUGIN_ROOT}/shared/data-sources.md` — Modjo operation map and the "Large results" file-spill protocol
- `${CLAUDE_PLUGIN_ROOT}/shared/coaching-themes.md` — theme taxonomy for tagging observations
- `${CLAUDE_PLUGIN_ROOT}/shared/qualification-rubric.md` — for the MEDDPICC-moments scan
- `${CLAUDE_PLUGIN_ROOT}/shared/output-modes.md` — Live brief default; optional Notion log to the rep's coaching page
- `${CLAUDE_PLUGIN_ROOT}/shared/voice-profile.md` — draft the next-time play in the rep's voice (warm register); how to load/build/apply the profile
- `${CLAUDE_PLUGIN_ROOT}/shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull

1. **The call record** — basic metadata via `list_recent_calls` (or direct resolution by id): name, date, duration, direction, participants, deal/account linkage. **Only state metadata you actually read from the record.** `get_calls` results overflow and spill to a file (see `${CLAUDE_PLUGIN_ROOT}/shared/using-modjo-mcp.md`) — if the record spilled and you did not read it, do NOT invent the header fields (company description, job title, duration like `14m51s`, direction like `outbound`, "cold first-contact"). Read the spilled file for the fields you need, or omit/label them "unknown" — never fabricate call metadata to fill the header.

2. **The call summary** — from the call record. Read this first; it's often enough to score 60% of the call without burning more tokens.

3. **Prior calls on the account** (for context, not deep scoring) — last 2 calls on the same account via `list_recent_calls` filtered by account id. Surfaces what was promised before this call so you can score whether the rep delivered.

4. **Agent scoring AND quotes — this is the PRIMARY scoring path** — `analyse_call` (`ask_anything_on_call`) with the default agent (or a discovered coaching agent via `discover_agents` query="coach" or "scoring"). The agent has the full transcript server-side and **returns verbatim quotes with a source citation and timestamp** — so you get grounded quoted moments without ever pulling the raw transcript. **Do not read the transcript to score.** Ask one question per dimension (single-question framings — multi-part returns empty), capped at 3 dimensions per call. Pick the highest-impact dimensions for this call type:
   - For disco calls: question quality + listening
   - For demo calls: storytelling + objection handling
   - For negotiation calls: commercial discipline + next-step
   - For follow-ups: next-step + champion development

   For each scored dimension, ask the agent for **the specific moment + the rep's exact words + timestamp** (e.g. "What was the strongest objection-handling moment? Quote the rep's exact words and give the timestamp."). Quote **only what the agent returns, with its source citation.** If the agent returns empty for a dimension (known failure mode), score that dimension "not scored — agent returned empty" and move on. Never fill the gap from the summary or from imagination.

5. **`get_transcript` is a rare fallback, not the scoring path.** Only reach for it if a single load-bearing quote is missing and the agent could not supply it — and then follow the file-spill recovery protocol in `data-sources.md` (transcripts overflow and spill to a `.txt`; read the spilled file in `offset`/`limit` chunks, quote only from text you actually read). **If you cannot obtain a verbatim quote for an observation from either the agent or a transcript you actually read, DROP the observation.** Never approximate, reconstruct, or invent a quote or a timestamp — a fabricated quote is an automatic fail regardless of how good the rest of the scorecard is.

# Scoring rubric (use the lightest version that fits the call type)

| Dimension | What good looks like | Anti-pattern |
|---|---|---|
| **Talk ratio** | <45% rep talk on disco, <55% on demo | Rep monologues >60% |
| **Question quality** | Open + layered, dig past first answer | Closed questions, single-layer |
| **Active listening** | Paraphrases buyer signals, builds on them | Waits to talk, ignores signals |
| **Objection handling** | Acknowledge → reframe → micro-commitment | Deflect, debate, or capitulate |
| **Next-step discipline** | Call ends with booked invite + named owner | Vague "we'll be in touch" |
| **MEDDPICC moments touched** | Asked metrics, identified pain, tested champion | Surface-level qualification |

Score each dimension 0–2 (missing / partial / strong) — same scale as the MEDDPICC rubric. Aggregate to a single call score /12 (or weighted by call type).

# Output — Live brief (widget)

`show_widget` with `title="call_score_[call-slug]_[YYYY-MM-DD]"`. Layout:

### Header
Call name + date + duration + participants + deal/account + call type detected.

### One-sentence verdict
The single most important coaching takeaway. Lead with this.

### Scorecard
Dimension table — score, evidence quote (with timestamp), the one thing to keep doing or change.

### Coaching points (2–3 max)
Each one: theme tag from `coaching-themes.md`, what happened with a quoted moment, why it matters, and a drafted "next time say this" line.

### What worked
At least one specific strength even on a weak call. Include the quote so the rep can hear what they did right.

### Drafted next-time play
A short script or talk-track to use on the next similar moment. Sendable as-is. If the play is a follow-up email to this buyer, draft it in the rep's voice — load or build the voice profile per `${CLAUDE_PLUGIN_ROOT}/shared/voice-profile.md` (warm / voice-matched register). With no sent-email source, draft in a neutral register and label it; never fake the rep's tone.

## Example skeleton

```text
[Header] [Call name] · [Date] · [Duration] · [Deal]

[Verdict] One sentence — the single most important coaching takeaway.

[Card 1: Scorecard] 3–5 dimensions · Score · Quoted moment · One fix
[Card 2: Coaching point #1] Theme tag · What happened · Drafted next-time line
[Card 3: Coaching point #2] Theme tag · What happened · Drafted next-time line
[Card 4: What worked] Strength · Quoted moment to keep doing

[Drill-down (optional)] All qualification touched · Full timeline of pivotal moments
```

# Optional outputs

- **Notion** — log the score to the rep's coaching page if requested. Feeds `coach-this-rep` so the manager sees the week's call-level data, not just deal-level.
- **Slack draft** — share the verdict + 1 coaching point with the rep's manager if rep wants visibility.

# Rules

- **Quote verbatim, always — in the call's original language.** No paraphrased coaching. If the call was in French (or any non-English language), the quoted string is in that language; a translation is NOT a verbatim quote and must never be the quoted moment, even with a disclosure note — put any translation in parentheses after the original. If you can't get a real verbatim quote (agent or transcript you read), drop the observation rather than approximate or translate-as-quote.
- **Transcript-too-large is NOT permission to invent.** If `get_transcript` returns nothing usable for any reason — errored, truncated, or **the transcript exceeded the token limit and you only have the summary** — you MUST: (1) state at the top "**Summary-only — full transcript not read; quotes and timestamps below are unavailable.**"; (2) emit **zero verbatim quotes and zero timestamps** (a summary is not a transcript — you did not see the rep's exact words or the clock); (3) score every transcript-dependent dimension **Partial (1) at best**, never 2, and label it "summary-only". Producing a quoted line or a timestamp (e.g. `00:03`, `14h51`) when the transcript was not actually read is fabrication and an automatic fail — this is the single worst failure mode of this skill.
- **One verdict line, not a wall.** The opening sentence is the load-bearing output. If a rep reads only that, they should know what to fix.
- **At least one strength, even on weak calls.** Reinforce before correcting (same rule as `coach-this-rep`).
- **Cap agent calls at 3 per scoring run.** Single-question framings (we learned this the hard way — multi-part agent questions return empty).
- **No fabricated scoring.** If the agent and summary both fail on a dimension, mark it "not scored — insufficient data" rather than guess.
- **Voice is earned, not faked.** A drafted follow-up uses the rep's voice only from a real sent-email source (per `${CLAUDE_PLUGIN_ROOT}/shared/voice-profile.md`). No source → neutral register, labelled. Never invent a style trait.
- **Approval-gated outputs.** Notion log writes and Slack drafts require explicit user confirmation.
