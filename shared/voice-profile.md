# Voice profile — the rep's writing voice as agent memory

A **voice profile** is a small, persisted, hand-correctable description of how one rep
writes email. It is the plugin's first piece of true "agent memory": built once from
the rep's real sent emails, reused across runs, and refreshed when stale.

The point is fidelity. A follow-up the rep has to rewrite isn't a follow-up — it's
homework. When the draft already sounds like them (their greeting, their sign-off,
their language, their length), the rep glances at it and ships it. The profile carries
**how** the rep writes; the specific thread carries **what** this exchange needs. The
draft is generated through the profile (style) but grounded in the fresh thread
(context and register).

This ref is the schema + build/refresh protocol. `write-the-follow-up` is the first
consumer; `build-net-new-pipeline`, `start-the-day`, and `score-this-call` can reuse it
for the emails they draft.

---

## Where it lives

- **Portable Markdown (default):** `outputs/voice-profiles/<rep-slug>.md`. One file per
  rep. Opens anywhere, the rep can edit it directly to correct a trait.
- **Notion (optional):** if a workspace MCP is connected and the rep wants it there,
  persist under the rep's coaching page. Same approval-gating as every other Notion
  write — ask before creating.

`<rep-slug>` is the kebab-cased rep name (e.g. `thomas-dhalluin`), resolved from the
running user's email via `get_users` — never assumed.

---

## What it captures

Every line is **evidence-backed** — derived from real sent emails, never invented. If a
trait can't be observed in the rep's sent mail, leave it blank; don't guess.

| Field | What it records | Example |
|---|---|---|
| `built_from` | ISO date the profile was last derived + how many sent emails it read | `2026-06-18 · 18 sent emails` |
| `languages` | Which languages the rep writes in, and when each is used | French to French-domain prospects; English otherwise |
| `greeting` | How they open | `Salut [prénom],` / `Bonjour [prénom],` / `Hi [first name],` |
| `sign_off` | How they close + how they sign | `Belle journée,` then first name only |
| `register` | Formality + tu/vous default (for French) | Warm-professional; tutoie French prospects after first call |
| `sentence_shape` | Typical sentence + paragraph length, density | Short sentences, 2–3 line paragraphs, lots of white space |
| `signature_moves` | Habitual phrasings — how they open a recap, how they ask for the next step | Opens with a one-line callback to the call; asks for next step as a yes/no question |
| `avoid` | What they conspicuously **don't** do | No emojis; never "I hope this finds you well"; no exclamation stacking |

Keep it tight — eight fields, a line or two each. This is a style fingerprint, not a
biography.

---

## How it's built

Build on the first run where source emails are available, then reuse.

1. **Resolve the rep** — `get_users` from the running user's email → `userId`, name →
   `<rep-slug>`.
2. **Read sent emails** (the source of voice — only emails the rep *wrote*):
   - **Gmail connected (best):** `search_threads` / `get_thread` for the rep's last
     ~15–20 *sent* messages. Real bodies → real voice.
   - **Modjo only:** `get_emails` filtered to the rep as sender, where bodies are
     available. Metadata-only emails (subject/sender, no body) can't teach voice — note
     that and lower confidence.
3. **Derive the traits** above from what you actually read. Quote nothing into the
   profile that isn't observable; an unobservable field stays blank.
4. **Write the profile** to `outputs/voice-profiles/<rep-slug>.md` (or Notion, gated).

### Thin-data honesty

If only a handful of sent emails are available, say so in `built_from` ("3 sent emails
— low confidence") and don't over-fit two emails into hard rules. A thin profile guides
gently; it never invents a "signature move" from a single data point.

### No source at all

If there's no Gmail and no usable Modjo bodies, **skip the profile**. The consuming
skill drafts in a neutral professional register and labels it: "no voice profile —
drafting in a neutral register; connect Gmail to match your tone." Never fabricate a
voice.

---

## How it's refreshed

- The profile carries a `built_from` date. If it's **older than ~30 days**, or the rep
  asks ("refresh my voice", "this doesn't sound like me"), **re-derive** from recent
  sent mail and overwrite.
- Otherwise **reuse** the persisted profile — don't spend tokens re-deriving voice every
  run.
- Never silently back-fill or invent trajectory. A refresh reads new sent mail; it
  doesn't imagine how the rep's style "probably" changed.

---

## How it's used by a drafting skill

1. Load the profile (build or refresh per above).
2. Read the **fresh thread** for this specific exchange (context + the register this
   conversation needs — a tense pricing thread wants more directness than a warm intro).
3. Generate the draft **through** the profile: their greeting, their sign-off, their
   language, their sentence shape, their habitual moves — applied to *this* thread's
   content.
4. If the profile is thin or absent, fall back to a neutral register and say so. Never
   present a neutral-register draft as voice-matched.

The profile styles the email; it never invents the email's facts. Commitments, quotes,
and recap lines still come from grounded call/deal evidence per
`using-modjo-mcp.md` — the voice profile changes *how it reads*, never *what it claims*.
