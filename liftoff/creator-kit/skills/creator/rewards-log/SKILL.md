---
name: rewards-log
description: Keep a two-week log of Grok Bot Creator Rewards payouts per template alongside what changed (posts, edits, new routines), and suggest the next experiment. Use when a payout lands, when the user asks how their templates are doing, or what to change next.
when-to-use: "log payout", "rewards update", "how are my templates doing", "what should I change"
---

# Rewards log

Rewards are decided every two weeks from usage: how many people use a template and how consistently. Payouts are discretionary and the formula isn't public, so treat this as a lab notebook, not a dashboard.

## Each period, ask for

- Period dates
- Payout amount (from X Money)
- Per template: anything the user can see about usage, plus what they changed (edits, new routine, launch post, quote-posts)

Store it in memory as a table:

| Period | Template | Payout | Changes this period | Posts |
|---|---|---|---|---|

## Then answer

1. **What moved?** Compare with the last period, and only claim a cause if the timing clearly lines up. Otherwise write "unclear".
2. **One experiment for next period.** Change one thing per template so the result can be read. Examples: add a daily routine, shorten the first message, post a real output.
3. **Kill or keep.** If a template has been flat for 3 periods with changes tried, suggest retiring it and building a new idea with `/template-forge`.

## Rules

- Never invent numbers. If the user doesn't have one, leave it blank.
- Keep the log private. Don't put payout figures in drafted posts unless the user asks.
