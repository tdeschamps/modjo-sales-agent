# Using the Modjo MCP — the agent playbook

How every skill in this plugin should talk to Modjo. This is the *how-to-use* companion to `data-sources.md` (which is the operation map — the table of which tool does what). Read this when a skill needs call content, deal/account data, or agent analysis.

The Modjo MCP is the plugin's primary data layer: calls, deals, accounts, contacts, emails, transcripts, and **AI agents** that read the underlying data server-side and answer questions about it.

---

## The one rule that matters most: get grounded answers from agents, not from raw transcripts

**`ask_anything_on_call` / `ask_anything_on_deal` / `ask_anything_on_account` are the PRIMARY way to get evidence.** These agents have already read the full call/deal/account server-side. Ask them a question and they return a grounded answer **with verbatim quotes and source citations** (e.g. `[Source](call:<uuid>:00:11:35)`). You get the exact words and the timestamp without ever pulling the raw transcript into your context.

This matters because it is **the** anti-fabrication safeguard for quoted evidence. When a skill pulls a raw transcript and tries to quote from it, two things go wrong:

1. Transcripts are large and **overflow the token limit** — they spill to a file (see "Large results" below), and a skill that doesn't handle the spill tends to fabricate quotes from the call summary.
2. Even reading the spilled file in chunks, a skill may not find a specific moment and **invents a plausible quote** to fill the gap.

`ask_anything_*` removes that surface entirely. Use it first, always.

### `get_transcript` is a LAST RESORT — never the primary path

**Do not call `get_transcript` to score, review, prep, coach, or summarize a call.** Get your quotes from `ask_anything_on_call`. Only reach for `get_transcript` when **all** of these hold:

- a single, specific, load-bearing quote is still missing, **and**
- `ask_anything_on_call` could not supply it (you asked and it returned empty or non-verbatim), **and**
- the observation genuinely cannot stand without that exact quote.

When you do call it, follow the file-spill protocol below, and obey the hard constraint:

> **If you cannot obtain a verbatim quote from either an agent citation or a transcript you actually read, DROP the observation. Never approximate, reconstruct, paraphrase-as-quote, or invent a quote or a timestamp.** A fabricated quote or timestamp (e.g. `00:03`, `14h51`) is an automatic fail regardless of how good the rest of the output looks. This is the single worst failure mode in this plugin.

> **Verbatim means original language.** Quote the words exactly as spoken — if the call was in French, the quoted string is in French. A translation is **not** a verbatim quote: never present a translated or paraphrased string as the quoted moment, even with a disclosure note. If a translation helps the reader, put it in parentheses *after* the original (e.g. *"on est en train d'accompagner Allianz"* — "we're currently working with Allianz"). The quoted string itself is always the speaker's actual words.

---

## Calling agents: discover first, ask single questions

1. **Discover the agent at runtime — never hard-code a UUID.** Modjo customers configure their own agents and UUIDs vary across tenants. Use `get_agents` with a search filter ("MEDDPICC", "deal challenger", "coaching", "next step", "scoring", "objection") and use the returned UUID. Cache the result for the run; don't re-discover per question.
2. **One question per call. Single-question framings only.** Multi-part questions return empty — a confirmed failure mode. To score multiple MEDDPICC pillars or assess multiple moments, make separate calls (the operation map caps agent calls per run per skill — respect it).
3. **Ask for the evidence explicitly.** When you want a quotable moment, ask for it: *"What was the strongest objection-handling moment? Quote the rep's exact words and give the timestamp."* The agent returns the quote + a source citation you can relay.
4. **Empty is normal, not a crash.** Thin deals and fresh calls often return empty. When that happens, score that dimension "not scored — agent returned empty" and move on. Never fill the gap from the summary or from imagination.

---

## Evidence scoping — keep claims tied to the right entity

When a skill is about a specific deal, account, or contact, **every objection, quote, commitment, and concern you report must come from THAT entity's own calls — not from thematically-similar moments elsewhere in the tenant.** Modjo holds calls across many accounts; it is easy to grab a similar-sounding objection from a different contact and present it as this one's. Don't.

- Scope your data pulls to the target: filter `get_calls` / `ask_anything_*` by the resolved `accountId` / `crmId` / `callIds` for the entity you're prepping, and attribute each point to the specific call + speaker it came from.
- **Never borrow another contact's objection.** "Samuel raised a Salesforce gap" is not evidence about Charlotte unless Charlotte's own calls show it. If you only have a thematically-related moment from a different account, either omit it or explicitly label it "(from a different account — not this buyer)".
- **Don't present inference as call fact.** Framings like "lost in Dec 2024", "they're the champion on a deal you lost", or "their pain is enablement" must be traceable to a call/CRM record. If it's your inference, label it as such; if you can't ground it, drop it.
- If the target entity genuinely has thin call history, say so ("only 1 prior call on this account") rather than padding with other accounts' evidence.

## Large results — the file-spill recovery protocol

Heavy Modjo calls — especially `get_transcript`, but also large `get_calls` / `ask_anything_*` results — frequently exceed the tool-output token limit. The tool does **not** fail and does **not** return data inline. It returns a message like:

> `Error: result (57,268 characters) exceeds maximum allowed tokens. Output has been saved to /…/tool-results/<tool>-<id>.txt … Use offset and limit parameters … read … in sequential chunks until 100% has been read.`

**This is not a failure — the full data is on disk and you are required to read it.** When you see "saved to … exceeds maximum allowed tokens":

1. **Read the spilled file** at the given path with the Read tool, in sequential `offset`/`limit` chunks, until you have covered the portion you need (for one load-bearing quote, read until you can copy the exact moment; for a full review, read 100%).
2. **Only then** quote — quotes and timestamps must come from text you actually read, not from the call summary.
3. **If you cannot read the spilled file** (path missing/unreadable), treat it as data-unavailable: say "summary-only — full transcript not read", emit **no** verbatim quotes and **no** timestamps, and score evidence-dependent dimensions Partial at best.

Never respond to a spill message by quietly using the summary while presenting summary-derived content as verbatim. (And remember: for call content you usually shouldn't be here at all — `ask_anything_on_call` avoids the spill entirely.)

---

## IDs, fallbacks, and approvals (quick reference)

- **`crmId` is verbatim.** Use the exact `crmId` from `get_deals` / `get_accounts`. Never reconstruct prefixes — Modjo exposes the underlying CRM's real id (Salesforce 18-char, HubSpot int, Pipedrive int, …) and tenants mix formats. A wrong id returns "not found" silently.
- **Resolve `userId` / `accountId` first** via `get_users` / `get_accounts` before filtering — never assume an id.
- **CSV / paste-in is always offered** when Modjo isn't connected or the rep doesn't want auto-pull (see `csv-schemas.md`).
- **External writes are approval-gated.** Notion writes ask first; Slack messages are drafts only; the plugin never writes to the customer's CRM.

See `data-sources.md` for the full operation map (every conceptual op → Modjo tool) and the hard rules.
