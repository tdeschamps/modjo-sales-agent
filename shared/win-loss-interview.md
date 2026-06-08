# Win-loss interview structure

Used by `learn-from-closed-deals` skill. Defines the questions and the synthesis pattern so findings are comparable across deals and feed the Plays library cleanly.

## Source data, in order

1. The deal's `lossReason` (or won status) from Modjo `get_deals`.
2. The full call history (`get_calls` filtered by deal CRM id) — read summaries, pull transcripts for the 1–2 most consequential moments.
3. Email history (`get_emails`) — note who initiated key threads.
4. The internal `ask_anything_on_deal` with **Deal Challenger** agent for a structured MEDDPICC retro.
5. **(Optional but ideal)** an actual customer interview — the skill drafts the outreach if the rep wants to do one.

## Questions to answer per deal

**For both wins and losses:**

1. **Why us / why not us?** What was the single biggest reason the buyer picked or rejected us?
2. **Who actually decided?** Was the named decision maker the real decider, or did the call get made elsewhere?
3. **When was the deal really won or lost?** The pivotal moment is usually weeks before close — find it.
4. **What did we do that worked / hurt?** A specific moment, quote, or action — not "we built rapport."
5. **What did the competitor do?** If known. Includes "status quo" as a competitor for losses.
6. **What signal did we miss?** Was there a flag in the data that, in hindsight, predicted the outcome?

## Synthesis — feeding the Plays library

Each finding gets tagged with one or more coaching themes from `coaching-themes.md` and one or more **plays**. A play is a specific move that worked (for wins) or that should have happened (for losses).

Output structure:

```
Deal: [name]
Outcome: Won / Lost
Pivotal moment: [date + one-line description]
Themes: [from taxonomy]
Plays surfaced:
  - [Specific move, e.g. "Champion → Decision Maker intro via business case before pricing"]
  - [...]
Anti-pattern (losses only):
  - [What we should have done differently]
Signal we missed (if any):
  - [Data point or quote that predicted the outcome]
```

## The Plays library

`learn-from-closed-deals` writes to a shared Notion database `Plays Library` (created on first run). Each play has:

- Name
- Theme(s)
- "When to use" trigger
- Evidence: 1–3 won deals where it worked
- Anti-pattern: 1+ lost deals where its absence hurt
- Last updated date

Other skills (`learn-from-similar-deals`, `unstick-this-deal`, `lock-the-close-plan`) read this library to anchor their recommendations in real, retroactively-verified team plays.

## Cadence

Run `learn-from-closed-deals` weekly on deals closed in the prior 7 days, plus monthly on the prior 30-day window for pattern detection. Never run it on a single deal without context — always include the comparable wins/losses from the same period.
