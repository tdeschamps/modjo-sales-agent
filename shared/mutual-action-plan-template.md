# Mutual action plan (MAP) template

The MAP is a co-owned, dated path from today to signed contract. It is the single highest-leverage artifact in enterprise sales. Used by `lock-the-close-plan` skill; referenced by `audit-this-deal` when a deal needs one.

## Header

- **Deal**: [Account name + opportunity name]
- **Target close date**: [ISO date]
- **Total contract value**: [€ ARR]
- **Last updated**: [ISO date]
- **Sales lead**: [AE name + email]
- **Customer lead**: [Champion name + role]

## Why we're doing this together

One short paragraph — the business outcome the customer is buying, in the customer's own words. This is the "why" everyone keeps coming back to when steps slip.

## The plan

A table, not prose. Each row = one concrete step.

| # | Date | Step | Owner | Status | Notes |
|---|------|------|-------|--------|-------|
| 1 | YYYY-MM-DD | [Specific action] | Customer / Sales / Joint | ✅ done / 🟡 in progress / 🔴 blocked / ⏳ upcoming | [Any context] |

Steps should cover: discovery validation, business case build, security review, legal / paper process, internal sponsor reviews, executive sign-off, signature, kick-off. Both sides have rows.

## Signers and approvers

Named list. Title + name + signing role + status (engaged / aware / unknown).

## Open risks

Bulleted. Each risk gets an owner and a date by which we'll know more.

## How we'll update this

A cadence — typically weekly. Who shares the updated MAP with whom and when.

---

## How the skill builds it

When `lock-the-close-plan` runs:

1. Pull the deal's calls and emails from the last 90 days.
2. Identify steps already agreed (anything with a date and an owner already exists).
3. Identify gaps — typical steps missing for a deal of this stage and size (e.g. no security review row on an enterprise deal).
4. Draft a complete MAP, marking which rows are **derived from real call/email evidence** vs **suggested based on stage**. Never blur the two.
5. Output as a Notion page (under the deal's account) OR a markdown file the user can paste into a shared doc with the customer.

The MAP is **co-owned** — the skill drafts it from our side, but the rep then shares it with the champion and the champion edits. The output should make that handoff easy (clean formatting, customer-readable language, no internal jargon).
