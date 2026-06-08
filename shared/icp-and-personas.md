# ICP and personas

Reference for build-net-new-pipeline, learn-from-similar-deals, and account targeting skills. The team should fill in the specifics; this file is the structural template.

## ICP definition

Each ICP segment captures:

- **Segment name** — short label (e.g. "Mid-market SaaS EU")
- **Firmographics** — company size (employees / ARR), industry, geography, growth stage
- **Tech stack signals** — tools that suggest fit (CRM, dialler, recording platform)
- **Trigger events** — recent funding, leadership changes, hiring patterns, expansion to new markets, public RFPs
- **Disqualifiers** — what makes an account *not* worth pursuing (e.g. air-gapped industries, single-rep teams below threshold)
- **Average deal size** and **typical sales cycle**

## Personas

For each role we sell to, document:

- **Title patterns** — exact strings to look for in LinkedIn / CRM
- **Top 3 pains** — in their own words, not ours
- **What they care about** — outcomes, metrics, organisational pressure
- **What they fear** — risk, change management, what gets them fired
- **Best opening hook** — proven first line or question that lands

## How skills use this

- **build-net-new-pipeline** reads ICP segments to score net-new accounts; reads personas to draft personalized outbound.
- **learn-from-similar-deals** uses segment + persona to find truly comparable historical deals.
- **prep-this-meeting** uses persona pain language to suggest opening questions.
- **spot-expansion-signals** uses persona + buying group to identify untapped stakeholders in existing accounts.

## First-run behaviour

If this file is empty (no ICP/persona content yet), the skill that needs it should:

1. State the gap once: "No ICP or persona defined yet — running on inferred patterns from your last 20 won deals."
2. Run a best-effort inference from `list_closed_deals` (any connected CRM or CI provider) filtered by won status, grouped by deal size / source / contact role.
3. Offer to draft a starter ICP/persona file the user can review and edit.

Never silently fabricate ICP fit signals. If the data isn't there, say so.
