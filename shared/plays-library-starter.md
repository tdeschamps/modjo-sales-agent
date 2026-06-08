# Plays Library — starter set

Eight widely-applicable sales plays drawn from MEDDPICC + Winning by Design + Force Management practice. **The plugin ships with these so `learn-from-similar-deals`, `unstick-this-deal`, and `lock-the-close-plan` have evidence to cite from day one** — without waiting for `learn-from-closed-deals` to populate a team-specific library from your own deals.

These are baseline. As `learn-from-closed-deals` runs on real closed deals, the team's actual plays (with verified evidence) accumulate alongside or replace these. After 8–12 weeks of normal use, the team library should dominate; these starter plays remain as fallbacks for situations the team hasn't yet faced.

Each play follows the same structure: name, when to use, the move, why it works, anti-pattern.

---

## 1. The Champion test

**When to use**: A contact is acting friendly but you don't know if they'd actually fight for you internally.

**The move**: Ask directly — *"If you were in my shoes, what would you be worried about? What's most likely to kill this internally?"* Their answer reveals whether they've thought about internal opposition (real champion) or whether they're just being nice (coach).

**Why it works**: A real champion has already mapped the internal politics. A coach hasn't. The question is uncomfortable, so an evasive answer is itself a data point.

**Anti-pattern**: Assuming friendly = champion. The most-engaged contact often isn't the one who'll push the deal through procurement.

---

## 2. Multi-thread to power before legal

**When to use**: You're working with a mid-level champion on an enterprise deal and the deal is approaching paper process.

**The move**: Before legal/procurement engages, ask the champion: *"For a business case at your VP/CRO level, what would they need to see? Could we get 20 minutes with them to test the value framing before we commit to the procurement timeline?"*

**Why it works**: Legal/procurement defaults to friction. An economic-buyer touchpoint upstream gives the deal political momentum that survives procurement.

**Anti-pattern**: Letting the champion be the only carrier of the value story into the exec layer. The exec hears it second-hand.

---

## 3. Stalled-deal "I assume this is dead" email

**When to use**: A previously-engaged buyer has gone silent for 14+ days and isn't responding to follow-ups.

**The move**: Send a short, no-pressure email: *"[Name], hadn't heard back so I'm assuming this isn't a priority right now. No worries — if anything changes, I'm here. Otherwise I'll close out the file."*

**Why it works**: Most reps escalate when ghosted (more follow-ups, more pressure), which pushes the buyer further away. The "assume dead" move is counterintuitive — it removes pressure and creates urgency from the buyer's side. Response rates on this template are typically 30–40% on previously-engaged contacts.

**Anti-pattern**: The fifth "just checking in" email. By move 4, you've already lost; move 5 is noise.

---

## 4. Quantified pain — turn qualitative complaints into a dollar number

**When to use**: The prospect describes pain qualitatively ("our team wastes a lot of time on this") but no number has been put to it.

**The move**: Turn the complaint into a calculation in their own words. *"You said your reps spend ~4 hours a week on this. With 30 reps, that's 120 rep-hours. At a loaded cost of around €60/hour, that's €7,200/week — about €375k/year. Does that math feel right to you?"*

**Why it works**: A number the buyer agreed to becomes the M (Metrics) pillar. Without quantification, value claims are negotiable; with it, ROI becomes self-evident.

**Anti-pattern**: Citing reference customers' numbers ("Acme saved 30%") without anchoring on the buyer's own baseline. Their math will always discount yours.

---

## 5. Critical event creation — the "what changes on date X" question

**When to use**: The deal has interest but no urgency.

**The move**: Ask: *"If we don't have this in place by [specific date], what changes for you?"* The buyer either names a real critical event (creates urgency) or admits there isn't one (creates clarity).

**Why it works**: SPICED methodology calls this the C — Critical Event. Without one, even validated deals slip indefinitely. With one, the close plan has a real anchor.

**Anti-pattern**: Manufacturing urgency from your side ("our pricing changes next quarter"). Buyers see through this and it damages trust.

---

## 6. Procurement parallel-track

**When to use**: An enterprise deal is in late-stage commercial discussion and procurement is the next gate.

**The move**: Don't wait for procurement to start. Send the standard DPA, SOC 2, and MSA template to the champion now, framed as: *"To save us time on the back-end, can your legal/procurement team start their review while we finalize the commercials?"*

**Why it works**: Procurement timelines are largely a fixed cost (weeks of review regardless of when started). Running them in parallel with commercial close compresses the total cycle by the procurement duration. Common pattern: an enterprise deal loses 4–8 weeks to sequential procurement that could have started in parallel with commercial close.

**Anti-pattern**: Treating procurement as a post-close step. It IS the close in enterprise.

---

## 7. Competitive judo — reframe their strength as your differentiator

**When to use**: The buyer is leaning toward a competitor based on a feature/strength the competitor has.

**The move**: Acknowledge the competitor's strength explicitly, then reframe what that strength implies as a tradeoff. *"Yes, [competitor] has [feature]. That's because they're built for [their target segment]. The trade-off is [tradeoff that matters to this buyer]. For your specific situation, here's what we do that they don't."*

**Why it works**: Denying or minimizing a competitor's strength loses credibility. Acknowledging it and reframing positions you as a serious analyst, not just a salesperson.

**Anti-pattern**: Trash-talking the competitor or claiming feature parity when you don't have it. Buyers do their own research and will catch this.

---

## 8. Mutual action plan — make the close the customer's project, not yours

**When to use**: Any late-stage deal where you need predictable close timing.

**The move**: Co-build a written, dated plan from today to signature. Each step has an owner (us or them) and a date. Share it with the champion as a Google Doc they can edit. Reference it on every call.

**Why it works**: Without a written plan, the buyer's internal momentum slips and your forecast wobbles. With a written, co-owned plan, slip becomes visible (and discussable) immediately. See `lock-the-close-plan` skill + `mutual-action-plan-template.md`.

**Anti-pattern**: Keeping the close plan in your CRM as a one-sided thing. If the customer hasn't seen the plan, it's not mutual.

---

## How the consuming skills should use these

- **`learn-from-similar-deals`** — when no team-specific won-deal comparable exists, cite the matching starter play with an explicit "(starter play — no team-specific precedent yet)" tag.
- **`unstick-this-deal`** — when a rep is stuck on a situation that matches a starter play, propose the play with a quote from this file. Same "starter" tag.
- **`lock-the-close-plan`** — reference play #8 directly when building the plan.

**Starter plays are clearly labelled as such in any output. They're never presented as the team's verified evidence — that distinction matters for the rep's trust.**

---

## How `learn-from-closed-deals` should populate the team library

When `learn-from-closed-deals` runs and identifies a real team play (≥2 supporting won deals), it should write to a separate `shared/plays-library-team.md` file (or a Notion database). Skills read both files — team plays take precedence over starter plays where overlap exists. Over time the team library becomes the primary; starter remains as fallback.
