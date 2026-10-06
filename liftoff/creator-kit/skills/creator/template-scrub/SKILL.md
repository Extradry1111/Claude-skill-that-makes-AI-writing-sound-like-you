---
name: template-scrub
description: Audit a Grok Bot before it is shared as a template and remove secrets, personal data and anything that won't travel (API keys, tokens, emails, phone numbers, private URLs, private MCP servers, custom code). Use before "Share as template", or when the user asks if their bot is safe to share.
when-to-use: "scrub", "safe to share", "before I share", "check for secrets"
---

# Template scrub

Templates copy the bot's description, skills, routines, relevant memories and first-party plugins. **Anything in those ships with the link unless you remove it.** Conversation history, logins, custom code and private MCP servers don't travel.

## Steps

1. Ask the user to paste (or open) the bot's description, every skill and every routine.
2. Scan for these and list every hit with its location:

| Type | Look for |
|---|---|
| Keys / tokens | `sk-`, `xai-`, `ghp_`, `AKIA`, `Bearer `, long random strings, `api_key=` |
| Personal data | emails, phone numbers, home address, real names of other people |
| Private links | internal docs, Notion/Drive links, local or private-network addresses, webhook URLs |
| Won't travel | references to private MCP servers, custom scripts, "my computer", logged-in accounts |
| Memories | personal facts in memories that would copy over (finances, health, family) |

3. For each hit, propose a fix: delete it, replace it with a placeholder (`[YOUR_TIMEZONE]`) or turn it into a first-message question.
4. For anything that won't travel, propose a fallback that works with built-in tools, such as web search instead of a private API.
5. End with a verdict: **SAFE TO SHARE** or **FIX FIRST: N issues**.

## Rules

- When unsure, flag it. A false positive costs 5 seconds, while a leaked key can cost real money.
- Never repeat a full secret back. Show only the first 4 characters and `…`.
