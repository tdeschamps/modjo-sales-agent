# CSV schemas — standalone path for sales-execution

This file documents the exact column shapes each skill expects when you're running standalone (no CRM or CI connector). Copy the schemas you need into your own spreadsheet, populate, and paste the CSV into your message to Claude.

**Rules across every schema:**

- Column headers must match exactly (case-insensitive). Underscores or spaces are both fine — Claude normalises.
- Dates use ISO 8601 (`YYYY-MM-DD`). Other formats are accepted but slower to parse and ambiguous.
- Amounts are numeric; include the currency in the `currency` column (`EUR`, `USD`, `GBP`). Avoid mixed currencies in one paste — split into separate runs.
- Empty cells are fine for optional columns; for required columns, Claude will flag the gap rather than guess.

## Schema 1: open pipeline

**Used by**: `audit-the-forecast`, `review-the-pipeline`, `forecast` *(v0.1 placeholder)*

The standard open-pipeline export. One row per open opportunity.

| Column | Required? | Type | Example | Notes |
|---|---|---|---|---|
| `deal_name` | required | text | Acme Q4 expansion | Internal name |
| `account` | required | text | Acme Corp | Customer name |
| `amount` | required | number | 84000 | Annual contract value |
| `currency` | required | text | EUR | ISO currency code |
| `stage` | required | text | Proposal | Your CRM stage name |
| `close_date` | required | date | 2026-09-30 | Expected close |
| `owner` | required | text | catalin@modjo.ai | Rep email or name |
| `probability` | recommended | number | 60 | % win likelihood |
| `days_in_stage` | recommended | number | 47 | Days since stage entered |
| `last_activity_date` | recommended | date | 2026-05-18 | Last buyer touch |
| `next_step` | recommended | text | Demo with VP Eng 6/9 | CRM next-step field |
| `primary_contact` | optional | text | Marie Dupont (CTO) | Champion or buyer |
| `competitor` | optional | text | Competitor X | Known competition |
| `source` | optional | text | Inbound — webinar | How the deal originated |
| `notes` | optional | text | Procurement starts next week | Free text |

**Skill-specific use**:

- `audit-the-forecast` reads everything; `days_in_stage` and `last_activity_date` drive the stage-stagnation flags. Without them, those flags can't fire and Claude will say so.
- `review-the-pipeline` reads everything; without `last_activity_date`, the "no buyer touch in N days" flag is unavailable.
- `forecast` reads everything; without `probability`, the weighted scenario math degrades to stage-band defaults and Claude flags the lower-confidence band.

## Schema 2: target accounts

**Used by**: `build-net-new-pipeline`

One row per net-new target account.

| Column | Required? | Type | Example | Notes |
|---|---|---|---|---|
| `account_name` | required | text | Acme Corp | Target company |
| `industry` | recommended | text | SaaS | For ICP scoring |
| `employee_count` | recommended | number | 350 | Or band like `100-500` |
| `country` | recommended | text | FR | ISO country code preferred |
| `primary_contact_title` | recommended | text | VP Sales | Title or persona |
| `primary_contact_name` | optional | text | Pierre Martin | If known |
| `primary_contact_email` | optional | text | pierre@acme.com | If known |
| `trigger_event` | optional | text | Series B raised May 2026 | Recent firmographic event |
| `our_relationship` | optional | text | cold | cold / warm / lapsed / existing-customer |
| `notes` | optional | text | LinkedIn-engaged with our content twice | Free text |

**Without an ICP file** (`shared/icp-and-personas.md` empty): Claude flags the gap once and runs scoring on inferred patterns from your closed-won corpus — explicitly labelling the inference as such.

## Schema 3: customer book (post-sale)

**Used by**: `spot-expansion-signals`

One row per active customer account.

| Column | Required? | Type | Example | Notes |
|---|---|---|---|---|
| `account_name` | required | text | Acme Corp | Customer |
| `current_arr` | required | number | 120000 | Annual recurring revenue |
| `currency` | required | text | EUR | ISO currency code |
| `renewal_date` | required | date | 2027-03-15 | Next renewal |
| `products_purchased` | recommended | text | Platform; Coaching add-on | Semicolon-separated |
| `csm_owner` | recommended | text | jean@modjo.ai | Account owner |
| `primary_contact` | recommended | text | Marie Dupont (CTO) | Champion |
| `last_activity_date` | recommended | date | 2026-05-22 | Last engaged touchpoint |
| `health_score` | optional | text | green | green / yellow / red, or your team's scale |
| `expansion_history` | optional | text | Upsold +30 seats Feb 2026 | Past expansions |
| `notes` | optional | text | New CTO arrived in Q2 | Free text |

Without `last_activity_date`, freshness signals aren't available and Claude flags this.

## Schema 4: today's meetings (paste-in)

**Used by**: `start-the-day`, `prep-this-meeting`

Lightweight — a list of today's external meetings if no calendar is connected. CSV or freeform list both work.

CSV form:

| Column | Required? | Type | Example | Notes |
|---|---|---|---|---|
| `time` | required | text | 09:30 | Local time |
| `account` | required | text | Acme Corp | Customer |
| `meeting_type` | recommended | text | Discovery | Discovery / Demo / Negotiation / Close / Internal |
| `attendees` | recommended | text | Marie Dupont (CTO); Pierre Martin (CFO) | Semicolon-separated |
| `deal_name` | optional | text | Acme Q4 expansion | If multiple deals on the account |
| `goal` | optional | text | Get to MEDDPICC pillar I (pain) | What success looks like |

Freeform form (also accepted):

```
09:30 — Acme Corp discovery with Marie Dupont (CTO)
11:00 — Globex demo, deal Globex Q3, Pierre Martin attending
14:00 — Initech negotiation, Sara Lee CFO
```

## Schema 5: deal context paste-in (per-deal skills)

**Used by**: `audit-this-deal`, `prep-this-meeting`, `lock-the-close-plan`, `unstick-this-deal`, `learn-from-similar-deals`, `hand-off-to-csm`, `score-this-call`

These skills don't take a CSV — they take a free-text paste-in. The recommended structure when going purely standalone:

```
DEAL: <name>
ACCOUNT: <customer>
STAGE: <current stage>
AMOUNT: <€X annual>
CLOSE DATE: <YYYY-MM-DD>
OWNER: <rep email>

STAKEHOLDERS:
- <Name, title, role on deal (champion / EB / influencer / unknown), last touch date>
- <...>

CURRENT STATE (2–4 sentences):
<What's the deal status in your own words?>

WHAT'S STUCK / WHAT YOU NEED (1–2 sentences):
<Free text — the skill uses this to focus its output.>

KEY MOMENTS (optional, if you remember specifics):
- <Call/meeting date — what happened — quoted moment if you remember any>
```

Claude doesn't require every block — it uses what you give and explicitly flags what's missing.

## Schema 6: closed deals (read by `learn-from-similar-deals`)

**Used by**: `learn-from-similar-deals` when reasoning from a CSV instead of CRM history.

Same shape as `sales-coaching`'s schema for `learn-from-closed-deals` — one row per recently closed deal:

| Column | Required? | Type | Example | Notes |
|---|---|---|---|---|
| `deal_name` | required | text | Acme Q2 expansion | |
| `account` | required | text | Acme Corp | |
| `outcome` | required | text | won | `won` or `lost` |
| `close_date` | required | date | 2026-04-12 | |
| `amount` | required | number | 84000 | Final contract value |
| `currency` | required | text | EUR | |
| `segment` | recommended | text | Mid-market SaaS EU | For comparable matching |
| `deal_size_band` | recommended | text | €50k–€150k | Or your team's bands |
| `primary_competitor` | recommended | text | Competitor X | Especially for losses |
| `win_loss_reason` | recommended | text | Champion left mid-cycle | 1–2 sentences |
| `key_stakeholders` | optional | text | CTO; CFO; Procurement Lead | Semicolon-separated |
| `notes` | optional | text | Free text | |

## When to skip CSV

If you're working with a single deal or a single account, just paste a free-form description — Claude is good with messy prose. The CSV schemas matter when you're feeding portfolio-shaped data (multiple deals, accounts, or contacts) and want the skill to triage at scale.
