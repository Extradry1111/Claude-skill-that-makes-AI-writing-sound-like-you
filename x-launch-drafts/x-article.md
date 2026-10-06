# SPACEXAI PAYS FOR GROK BOTS PEOPLE KEEP USING. I BUILT THE TOOL THAT CHECKS YOURS BEFORE YOU SHIP

Grok Bot Creator Rewards went live 10 days ago. I read the terms, found the one line that decides who gets paid, and built a free skill that scores your bot against it, catches leaked keys and writes the launch post.

---

## The line most people skipped

Aug 28: Grok Bot shipped Templates. You set up a bot once, hit "Share as template", and anyone with the link gets their own copy.

Sep 26: SpaceXAI opened the Grok Bot Template Rewards pilot. It pays every two weeks, in USD, straight to X Money.

Most posts stopped there. The terms go on to say what the payouts are based on:

→ how many people use your template
→ **how consistently they keep using it**

That second part kills most template ideas. A logo generator gets copied, used once and forgotten. A bot that sends you something useful every morning keeps counting.

So I stopped guessing and built a scorer.

## Meet liftoff

liftoff is a skill. It runs in Grok Bot and Claude, since both use the same SKILL.md format, and it ships with a small Python script that measures three things.

**1. Stickiness Score (0-100)**

Will people come back tomorrow? It checks 8 habits of bots people reuse:

| Check | Points |
|---|---|
| Comes back on its own (daily routine) | 25 |
| Fresh every day (live web/X data) | 15 |
| Remembers the user | 15 |
| 30-second first win | 15 |
| Does one job well (1-3 skills) | 10 |
| Skills trigger reliably | 10 |
| Easy to turn down | 5 |
| Short instructions | 5 |

It costs you 10 points for each thing that won't travel to the people who copy it, like logins, custom code or private MCP servers.

I ran a plain "logo generator" bot through it and it scored **5/100**. Then the skill rebuilt it as "Brand Radar", a daily design brief plus a logo critic. Same niche, **100/100**.

**2. Leak Scan**

This is the step people will skip and regret. Templates copy your instructions, skills and routines **exactly as written**. Grok Bot doesn't strip secrets for you.

I planted 4 leaks in a test bot: a teammate's email, a phone number, a Slack webhook and an API key. The scan caught all 4, plus a step that depended on a login. It never prints the full secret, only the first 4 characters.

**3. Launch Check**

The program has two posting rules: a public X post that includes the share link, and the paid partnership label turned on.

liftoff checks your post for the link, a hook under 110 characters, em dashes, hype words and money claims with no proof. It reminds you about the label, because that can't be checked from text.

## The SpaceX part

SpaceXAI is literally part of SpaceX now, so the flagship template is a **SpaceX launch desk**:

→ 08:00 daily: next 72h of launches in your timezone, and why each one matters
→ T-60 min: confirmed time, official stream link, a ready-to-post draft
→ T+30 min: what happened, confirmed vs. rumor, a recap draft
→ Sunday: the week in launches

Score: 100/100. Leak Scan: safe to share.

Starship flights are some of the biggest live moments on X, and people who follow them come back for every launch.

## Copy it in this order

**1.** Grab it: github.com/Extradry1111/liftoff

**2.** Install the skill. In Claude, add `dist/liftoff.skill`. In Grok Bot, add the `liftoff/` folder as a skill.

**3.** Say one of these:

```
build me a grok bot template for [your niche]
here's my bot: [paste]. is it ready to share?
set up the spacex launch-desk bot for me
```

**4.** Let it run the loop: score the idea, build, `score` until 80+, `scan` until safe, `pack`.

**5.** Paste `TEMPLATE_CARD.md` into Grok Bot. Every block is there in order.

**6.** Use it yourself for a day. Fix whatever annoys you.

**7.** Settings → Share as template → public link.

**8.** Ask the skill for the launch post. Paste in the link, turn on **Paid partnership** and attach a screen recording.

**9.** Every two weeks, tell it what you got paid. It logs each payout next to what you changed and suggests one experiment.

## The catch

→ **Invite-only pilot.** US-based, 18+, with a Grok Bot account, a clean X account and an eligible Premium plan.
→ **Discretionary payouts.** X's own words: not a revenue share, no guaranteed income.
→ **The score is mine, not X's.** It's built on the factors X named publicly. A high score means you avoided the usual ways templates fail, not that a payout is coming.
→ [NEED: your own honest minus, e.g. "first version of my launch bot pinged me 11 times in one day, I muted my own bot"]

## Steal this today

- [ ] Run your bot idea through the 6 questions. Under 18/30? Add a daily routine.
- [ ] Never share a template without a leak scan
- [ ] One job, 1-3 skills, a first message that asks one question
- [ ] Post with the link, the label and real proof
- [ ] Bookmark this and come back when the first payout window closes

## Links

→ liftoff (free, MIT): github.com/Extradry1111/liftoff
→ Rewards pilot rules: help.x.com/en/using-x/grok-bot-template-rewards-pilot
→ Program terms: legal.x.com/en/grok-bot-template-rewards-terms.html

No ref links. Not affiliated with SpaceX, SpaceXAI or X.
