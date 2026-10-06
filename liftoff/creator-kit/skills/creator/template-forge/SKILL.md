---
name: template-forge
description: Turn a rough idea into a Grok Bot template built for repeat use (bot instructions, 1-3 focused skills, routines, first message). Use when the user wants to design a new Grok Bot template, improve one nobody keeps using, or pick which idea to build for Creator Rewards.
when-to-use: "build a template", "template idea", "make a bot people use daily", "why is nobody using my template"
---

# Template forge

Creator Rewards counts **how many people use a template and how consistently they keep using it**. Design for the second day, not the first.

## Step 1: Score the idea (be blunt)

Score each one from 1 to 5 and show the table:

| Test | Question |
|---|---|
| Recurring job | Does the user need this weekly or more? |
| Routine-able | Can a schedule run it with no user typing? |
| Live data | Does it use fresh web/X data, so the output changes every day? |
| Personal memory | Does it get better the more it knows the user? |
| 30-second win | Does the first message show value fast? |
| Shareable | Would someone post the output on X? |

Below 18 out of 30, suggest a sharper version or a different idea before building anything.

## Step 2: Build the files

Output these, ready to paste:

1. **BOT.md**: identity, who it serves, what it does, rules, first message. Under 400 words.
2. **Skills**: 1-3 of them, each one job, at `skills/<category>/<slug>/SKILL.md` with `name` + `description` frontmatter. The description says *when* to use it, because that's what the bot matches against.
3. **ROUTINES.md**: at least one daily or weekly routine with a copy-paste prompt.
4. **First message**: ask for 1-2 preferences, then give one example prompt to try.

## Step 3: The retention checklist

- [ ] Something useful arrives without the user asking (a routine)
- [ ] It remembers preferences and uses them next time
- [ ] There's an easy "off switch" per alert type, so nobody gets spammed into quitting
- [ ] Outputs are short by default
- [ ] It has no private keys, private MCP servers or custom code it depends on, because those don't travel with templates

## Anti-patterns

- One-shot generators ("make me a logo"). Used once, then forgotten.
- Bots that need a login or private server to work. Those parts won't copy.
- Ten skills doing everything. Nobody knows what it's for.
