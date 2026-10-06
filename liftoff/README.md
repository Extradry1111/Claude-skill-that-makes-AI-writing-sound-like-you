# liftoff 🚀

**A Grok Bot template + a creator skill pack, built for Grok Bot Creator Rewards.**

SpaceXAI now pays people whose Grok Bot templates other people actually use. This repo gives you two things:

1. **Liftoff**: a ready-to-copy Grok Bot that runs a SpaceX launch desk. It watches Starship, Falcon and Starlink launches, explains them in plain English, and drafts X posts before and after every launch.
2. **The creator kit**: four skills that help you build, clean, launch and track your *own* templates, so you aren't stuck guessing what gets paid.

Fork it, copy it, ship your own version. MIT licensed.

---

## Why now

| Date (2026) | What happened |
|---|---|
| Feb | SpaceX acquires xAI |
| Jul | xAI rebrands as **SpaceXAI** |
| Aug 28 | Grok Bot ships **Templates**: package a configured bot, share it as a link, anyone can copy it |
| Sep 26 | **Grok Bot Template Rewards** pilot opens: creators get paid every two weeks based on template usage |
| Sep 30 | Reports say SpaceXAI is planning a $100/mo "Ultra" tier that includes Grok Bot |
| Oct 4 | Musk says SpaceXAI will be renamed **SpaceXSI** |

Templates are brand new and the rewards program is in a pilot, so not many people are building yet.

## How the rewards actually work

Short version (full notes with sources in [`docs/creator-rewards.md`](docs/creator-rewards.md)):

- **Invite-only pilot.** You need an invite. Requirements: 18+, US-based (where X Money works), a Grok Bot account, an X account in good standing, and an eligible X Premium subscription or Premium Business affiliation.
- **Paid every two weeks** in USD to your **X Money** balance.
- **Paid on usage**, meaning how many people use your template and **how consistently they keep using it**.
- **Discretionary.** It isn't a revenue share and there's no guaranteed income.
- You must **post each template publicly on X with its share link** and use the **paid partnership label**.

The thing that matters most is retention. A template people try once and forget won't earn much, while one that runs a useful job every day keeps counting. Everything in this repo is built around that.

## What's inside

```
template/                      ← the Liftoff bot, ready to load into Grok Bot
  BOT.md                       identity + standing instructions (paste into the bot)
  ROUTINES.md                  the schedules that bring users back daily
  skills/space/launch-desk/        what's launching, when, where to watch
  skills/space/starship-explainer/ any Starship flight explained in 60 seconds
  skills/space/launch-post/        pre-launch / live / post-launch X drafts

creator-kit/skills/creator/    ← skills for building your OWN money templates
  template-forge/   turn an idea into a template people come back to
  template-scrub/   strip keys, emails and private stuff before sharing
  template-launch/  write the X post: share link + paid partnership label
  rewards-log/      log each two-week payout and learn what moved it

docs/
  creator-rewards.md   the program, rules, sources
  template-ideas.md    30 template ideas ranked by retention
  playbook.md          the 7-day launch plan

scripts/validate.py    checks every SKILL.md and scans for leaked secrets
```

## Quick start

### Run Liftoff as your own bot

1. Open Grok Bot and create a new bot.
2. Paste [`template/BOT.md`](template/BOT.md) into its instructions.
3. Add the three folders under `template/skills/` as skills, keeping each `SKILL.md` inside its folder.
4. Set up the routines from [`template/ROUTINES.md`](template/ROUTINES.md).
5. Say: `what's launching this week?`

### Ship it as *your* template and get into rewards

1. Make it yours: change the voice, add your angle (Starlink coverage, a Starbase local feed, Starship only).
2. Load the creator kit skills and run `/template-scrub` so nothing private ships.
3. In bot settings, pick **Share as template** and create a public link.
4. Run `/template-launch` to draft the X post. Post it with the link and the **paid partnership label**.
5. Every payout, run `/rewards-log` to see what worked.

### Build a different template

Run `/template-forge` with an idea, or start from [`docs/template-ideas.md`](docs/template-ideas.md).

## Validate before you share

```bash
python3 scripts/validate.py
```

It checks that every skill has `name` + `description` frontmatter, the folder name matches the slug, and nothing that looks like an API key, token, email or phone number is shipping inside it. In templates, secrets **do** travel with the share link unless you remove them.

## Honest notes

- None of this guarantees you'll be paid. The pilot is invite-only and payouts are at X's discretion.
- Launch data comes from Grok's own web and X search. Always check the final time against an official source before you post it as fact.
- This project isn't affiliated with SpaceX, SpaceXAI or X.

## License

MIT
