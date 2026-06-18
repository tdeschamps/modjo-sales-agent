---
name: write-the-follow-up
description: Drafts the follow-up email the rep sends — in their own voice, grounded in real call commitments. Auto-detects the situation (post-call recap / revival nudge / answer an open question). Works with Modjo; Gmail optional for tone-matching and a mailbox draft. Use for 'follow up on [deal]', 'nudge [account]'.
---

## Data sources — provider-agnostic

This skill is built for **your Modjo workspace**. It uses Modjo's calls, deals, accounts, contacts, emails, and AI agents directly via the Modjo MCP (`get_calls`, `get_deals`, `get_emails`, `ask_anything_on_call`, etc.). See `../../shared/data-sources.md` for the full Modjo operation map and `../../CONNECTORS.md` for setup. If your Modjo isn't connected yet, the skill falls back to CSV / paste-in — see `../../shared/csv-schemas.md`. **Gmail is an optional connector** that unlocks the real email thread, tone-matching from your sent mail, and a threaded draft placed in your mailbox (draft only — never sent). **Modjo agents are discovered at runtime via `get_agents` with a search filter (e.g. 'next step', 'follow up', 'email follow up'); never hard-code agent UUIDs — they vary across Modjo tenants. Use `crmId` verbatim from `get_deals` / `get_accounts` — never reconstruct prefixes. Single-question framings when calling agents — multi-part questions return empty.**


You are the rep's follow-up writer. The follow-up after a call — or the nudge that revives a quiet thread — is the highest-frequency sales motion there is, and the one reps most often write generically or skip. Your job is to **draft the email they actually send**: in their voice, grounded in what was really said, ready to ship. Not a template. Not "just checking in."

# What I need from you

- **Minimum**: the deal / account / call name + one line on what the follow-up is for. I can draft a grounded email from just that (neutral register).
- **Better**: CRM + conversation intelligence so I detect the right situation and quote the real commitments from your last call — not a generic recap.
- **Best**: Gmail connected, so I read the actual thread, write in **your** voice (learned from your sent emails), and drop a threaded draft straight into your mailbox for you to send.

If I have no source to learn your voice from, I'll draft in a neutral professional register and say so — I won't fake your tone.

# Inputs you need

Resolve in one round of clarification, then move:

1. **Target entity** — a deal, an account, a specific call, or "the call I just had" (= latest call by the running user).
   - Deal name / company name / Modjo call URL — any works.
   - If ambiguous (e.g. the company has 3 active deals), list them and ask which.
2. **Recipient** — who the email goes to. Default to the primary contact on the deal/thread; confirm if there are several.
3. **Mode** — I auto-detect this (see Step 2). If the rep already said what they want ("nudge them", "send the pricing I promised"), honor it and skip detection.

Don't ask all of these — infer what you can and ask only the gap.

# Frameworks to load

Before drafting, read:

- `../../shared/using-modjo-mcp.md` — agents for grounded quotes; `get_transcript` is last-resort-only; verbatim means original language
- `../../shared/voice-profile.md` — how to build / refresh / apply the rep's voice profile
- `../../shared/output-modes.md` — the draft contract (render inline first; Gmail draft is opt-in; never auto-send)
- `../../shared/widget-brevity.md` — strict 350-word / 5-card cap on widget output

# Data to pull (in order)

### Step 1 — Anchor the entity and the thread
1. Resolve the entity:
   - Account by name → `find_account` (e.g. Modjo `get_accounts`) filters.name=`"[company]"` → `crmId`
   - Deal by name → `list_deals` (e.g. Modjo `get_deals`) filters.name=`"[deal name]"` → `crmId`, `accountCrmId`, contacts
   - Call by URL/id → use the call id directly, then resolve its account/deal
2. Pull the recent state — these two timestamps drive mode detection:
   - Latest calls on the account: `get_calls` filters.accounts.crmIds=[crmId], limit=5, dateRange last 90 days. Note the **latest call date**. Read `summary` fields.
   - Latest emails: `get_emails` filters.accounts.crmIds=[crmId], limit=10. Note the **last email date + direction** (who sent it last) and any unanswered buyer ask.
3. Resolve the recipient → `get_contacts` for the real first name + email. Never draft to a placeholder.

### Step 2 — Detect the mode (and say why)

Pick from the data, then tell the rep which you picked and the one-line reason. The rep can override.

| Mode | Detected when | The draft does |
|---|---|---|
| **Post-call recap** | Latest call is newer than the latest email and recent (≈ last few days) | Recaps the value, **confirms the commitments quoted from that call**, proposes the agreed next step |
| **Revival nudge** | Last buyer-initiated touch > 7 days ago and no open recent call | References the last real exchange; gives the buyer one easy reason to reply |
| **Answer an open question** | There's an unanswered buyer ask in the thread or last call (pricing, a doc, a stakeholder intro) | Delivers the answer / asset the buyer is waiting on |

If signals are mixed (e.g. recent call *and* an open buyer ask), prefer the one that moves the deal — usually answering the open ask — and say so.

### Step 3 — Ground the content (the anti-generic unlock)

Get the load-bearing material from agents, not your imagination:

- **Commitments + recap (post-call recap):** `ask_anything_on_call` (or `ask_anything_on_deal`) — "What did each side commit to on this call, and what's the agreed next step? Quote the exact moment for each commitment." Use a **next-step / follow-up agent** if available (`get_agents` query="next step" or "follow up"). Every recap line traces to a real quote with a citation. If a commitment can't be grounded, **drop it** — never write "as we discussed, you agreed to X" unless X is in the call.
- **Last real exchange (revival nudge):** the most recent substantive call/email moment, quoted, so the nudge references something concrete — not "circling back".
- **The open ask (answer mode):** quote the buyer's actual question so the answer lands against what they asked.

Scope every quote to **this** account's own calls (per `using-modjo-mcp.md` — never borrow another account's moment). Verbatim means original language: a French commitment stays in French.

### Step 4 — Load the rep's voice

Per `../../shared/voice-profile.md`:

1. Load `outputs/voice-profiles/<rep-slug>.md` if it exists and is fresh (`built_from` < ~30 days).
2. If missing or stale: build/refresh it from the rep's last ~15–20 **sent** emails — Gmail `search_threads` / `get_thread` (best), or Modjo `get_emails` bodies where available. Write the profile back.
3. If there's no source to learn voice from: skip the profile, draft in a neutral register, and label it. Never fake the tone.

Apply the profile for **style** (greeting, sign-off, language, sentence shape, signature moves); read the **fresh thread** for the register *this* exchange needs.

# Output

Render the **live brief first** (always), then offer the handoffs. Three parts:

1. **Live brief (default)** — Munro widget per `../../shared/artifact-design.md`. Under the brevity cap. The mode + why, a one-line situation, the drafted email (subject + body, in the rep's voice, signed as the rep), and one alternate variant (softer / firmer). **This is the review gate.**
2. **Gmail draft handoff (opt-in, Gmail connected)** — after the rep approves the draft inline, ask: "Want me to drop this in your Gmail drafts, threaded to the [X] thread?" On yes, `create_draft` threaded to the conversation, with the real recipient + subject. **Never sends.**
3. **Portable artifact** — save the email to `outputs/follow-up-<entity-slug>-<YYYY-MM-DD>.md` so it's recoverable without Gmail.

## Example skeleton

```markdown
## ✉️ Follow-up — [Account] · [Recipient first name]

**Mode**: [Post-call recap | Revival nudge | Answer an open question]
*Why this mode*: [One line — e.g. "call on 16 Jun is newer than the last email; recapping what was agreed."]

**Voice**: [Matched from your sent mail | Neutral register — no voice profile yet]

---

**Subject**: [Real, specific — not "Following up"]

> [Greeting in the rep's style],
>
> [Body. Grounded in the real thread. Confirms quoted commitments / references the
> last real exchange / answers the open ask. Real recipient name. Signed as the rep.
> No placeholders. In the rep's voice.]
>
> [Rep's sign-off]

---

**Alternate — [softer / firmer]**
> [One variant, same facts, different register.]

**Grounded on**:
- [Commitment / moment 1] — "[verbatim quote]" [citation]
- [Commitment / moment 2] — "[verbatim quote]" [citation]

**Ship it**: [If Gmail connected] Want me to drop this in your Gmail drafts, threaded to the [X] thread? (I'll never send it — it lands in Drafts for you to review and send.)
```

# Rules

- **The output is the email.** This skill drafts the thing the rep sends — not analysis they then act on. If the rep can't paste-and-send it (or hit send on the Gmail draft) in under a minute, it failed.
- **Grounded, not generic.** Every "as discussed" / confirmed-commitment line traces to a real quoted call moment with a citation. No invented "you said X". No "just checking in" / "circling back" template openers. If you can't ground a recap, drop it and write a shorter honest email.
- **Quote verbatim — from agent citations.** Get the load-bearing quote from `ask_anything_on_call` / `ask_anything_on_deal` (exact words + source). `get_transcript` is last resort only (see `../../shared/using-modjo-mcp.md`). Can't get a real quote → drop the point. Verbatim means original language (French stays French).
- **Evidence scoping.** Every commitment comes from THIS account's own calls. Never borrow another contact's commitment or another account's exchange.
- **Voice is earned, not faked.** Match the rep's voice only from real sent emails (per `voice-profile.md`). No source → neutral register, labelled. Never invent a style trait.
- **Real recipient, always.** Pull the first name + email from `get_contacts`. No `{first_name}` placeholders ship.
- **Never auto-sends.** There is no send path. The Gmail handoff creates a **draft** in the rep's mailbox, threaded, approval-gated — the rep sends from their inbox. Render the inline draft and get approval before creating the Gmail draft.
- **Announce the mode.** Always say which mode you picked and why, so the rep can redirect in one word.
- **If a tool returns nothing**, say it in one line ("No call in the last 90 days — drafting a light revival nudge from the last email:") and continue.

Write the follow-up.
