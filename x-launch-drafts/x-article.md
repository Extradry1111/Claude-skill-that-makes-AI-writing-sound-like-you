# SPACEXAI NOW PAYS YOU FOR GROK BOTS. HERE'S THE FULL SETUP, COPY IT IN THIS ORDER

Grok Bot Creator Rewards went live 10 days ago. Most people saw the headline and scrolled past. I read the terms, built a template around the one metric that gets paid, and open-sourced all of it.

---

## What happened

Aug 28: Grok Bot shipped Templates. You set up a bot once, hit "Share as template", and anyone with the link gets their own copy. That includes skills, routines and memories.

Sep 26: SpaceXAI opened the Grok Bot Template Rewards pilot. Creators get paid every two weeks, in USD, straight to X Money, based on how many people use their templates.

Most posts stopped at that sentence. The terms say a bit more.

The rewards look at how many people use your bot **and how consistently they keep using it.**

That second part changes what you should build. A logo generator gets copied once and forgotten. A bot that sends something useful every morning without being asked keeps counting.

So I built one around that, and since SpaceXAI is now literally part of SpaceX, I gave it a SpaceX theme.

## Meet Liftoff

Liftoff is a SpaceX launch desk that runs inside Grok Bot.

→ 08:00 every day: the next 72h of launches in your timezone, one line on why each matters
→ T-60 min: a final time check, the stream link and a ready-to-post draft
→ T+30 min: what happened, confirmed vs. unconfirmed, with a recap draft
→ Sunday: the week in launches

It's built on three skills:

1. `launch-desk` finds launches and cross-checks every time against SpaceX, NASA and the FAA
2. `starship-explainer` explains any flight in under 60 seconds of reading
3. `launch-post` drafts pre-launch, live and recap posts in your voice

Starship flights are some of the biggest live events on X. People who follow them come back for every one.

## The setup (copy it in this order)

**1. Grab the repo**

github.com/Extradry1111/liftoff

**2. Create the bot**

Open Grok Bot → new bot → paste `template/BOT.md` into the instructions.

**3. Add the skills**

Add each folder under `template/skills/` as a skill. Keep `SKILL.md` inside its folder, because the folder name is the slug you call it with (`/launch-desk`).

**4. Add the routines**

`template/ROUTINES.md` has 4 copy-paste prompts. Start with the morning brief:

```
Run /launch-desk for the next 72 hours. Send me a brief:
max 5 launches, each with vehicle, mission, time in my
timezone + UTC, and one line on why it matters. If nothing
launches, say so in one line and tell me the next launch date.
```

**5. Make it yours**

Don't share my exact bot. Change the angle: Starship only, Starlink coverage, a Starbase local feed. There's no point in 500 identical copies.

**6. Scrub it**

This is the step people will skip and regret. Templates copy your description, skills and routines **as written**. If an API key or your email is in there, it ships with the link.

```
python3 scripts/validate.py
```

It checks every skill and flags anything that looks like a key, token, email, phone number or private address. The `/template-scrub` skill does the same check inside Grok Bot.

**7. Share it**

Settings → Share as template → create a public link.

**8. Post it the right way**

The program has two posting rules:

→ a public X post with the template's share link
→ X's **paid partnership label** turned on

The `/template-launch` skill writes the post and 3 follow-up quote-posts, and it reminds you about the label.

**9. Log every payout**

Every two weeks, run `/rewards-log`. It keeps a table of each payout next to what you changed, then suggests one experiment for the next period.

## Not into space? Build your own

The repo includes `/template-forge`. Give it an idea and it scores it on 6 tests before writing anything:

| Test | Question |
|---|---|
| Recurring job | Needed weekly or more? |
| Routine-able | Can a schedule run it with nobody typing? |
| Live data | Does the output change every day? |
| Personal memory | Does it get better the more it knows you? |
| 30-second win | Is the first message useful? |
| Shareable | Would someone post the output? |

Under 18/30, it tells you to sharpen the idea before building.

There's also a ranked list of 30 template ideas in `docs/template-ideas.md`. The pattern at the top: **a routine sends something without being asked, it pulls live data, and it remembers the user.** The bottom of the list is one-shot generators.

## The catch (read this before you get excited)

→ **It's invite-only.** It's a pilot. You need an invite, US residency, 18+, Grok Bot, a clean X account and an eligible Premium plan.
→ **Payouts are discretionary.** X says it in plain words: not a revenue share, no guaranteed income.
→ **The formula isn't public.** Anyone posting "exact payout per user" numbers is guessing.
→ **Launch times move.** Liftoff searches live and marks when it last checked, but check an official source before you post a time as fact.
→ **[NEED: your own honest minus. Example: "my first version spammed every Starlink launch and I muted my own bot in 2 days"]**

## Numbers

| | |
|---|---|
| Cost to build | $0 beyond the Grok/X plan you already have |
| Time to set up from the repo | [NEED: your real setup time] |
| Skills | 3 in the template, 4 in the creator kit |
| Routines | 4 |
| Payout cadence | every 2 weeks |
| My payouts so far | [NEED: real number or "first window closes Oct XX, I'll post it"] |

## Steal this today

- [ ] Fork the repo
- [ ] Pick a template with a daily routine (Liftoff or one from the list)
- [ ] Use it yourself for 24 hours and fix what annoys you
- [ ] Run the validator
- [ ] Share as template, then post with the link and the paid partnership label
- [ ] Bookmark this and come back when your first payout lands

## Links

→ Repo (free, MIT): github.com/Extradry1111/liftoff
→ Rewards pilot rules: help.x.com/en/using-x/grok-bot-template-rewards-pilot
→ Program terms: legal.x.com/en/grok-bot-template-rewards-terms.html
→ Templates guide: x.ai/bot/guides/templates-for-grok-bot

No ref links in this article. Not affiliated with SpaceX, SpaceXAI or X.
