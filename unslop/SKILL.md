---
name: unslop
description: >-
  Makes writing sound like a real person wrote it, in that person's own voice. It strips AI tells
  ("delve", "It's not X, it's Y", groups of three, em-dash pileups, "I hope this email finds you
  well", "The result?", LinkedIn staircase posts), measures before/after with a 0-100 Slop Score,
  checks that no numbers, names or dates got lost, and can clone someone's style from a few samples of
  their real writing. Use this whenever someone wants text to sound human, natural, less robotic, less
  like ChatGPT/AI, or "like me", and whenever they ask whether something sounds AI-written. Also use
  it when writing an email, LinkedIn post, cover letter, Slack message, bio, essay, tweet or blog post
  that they will send or publish under their own name, even if they never say "AI". Trigger words:
  humanize, de-AI, unslop, make it sound natural, rewrite in my voice, too robotic, too corporate, too
  ChatGPT, does this sound AI.
---

# unslop

People can smell AI text in one sentence. What gives it away is a stack of habits: the fake contrast, the drumroll question, three adjectives where one would do, every sentence the same length, the "hope this helps" at the end. This skill removes those habits **without** changing what the writer meant, and makes the result sound like *them*, not like a generic "human" voice.

Three tools make this better than "rewrite it more casually":

| Tool | Command | Why it matters |
|---|---|---|
| **Slop Score** | `unslop.py scan` | Measures instead of guessing. Points to each problem line with a suggested fix. |
| **Voiceprint** | `unslop.py voice` / `voicecheck` | Measures how the person really writes (sentence length, rhythm, contractions, punctuation, lowercase habits) so the rewrite matches them. |
| **Fact Lock** | `unslop.py lock` (built into `compare`) | Rewriting is where numbers, names and dates quietly go missing. This catches it. |

All commands live in `scripts/unslop.py` (Python 3, no dependencies). Paths below are relative to this skill's folder. Use `-` to read from stdin, and `--json` for machine-readable output.

## Workflow

### 1. Work out the job

- **Rewrite** (the default): they gave you text and want it to sound human.
- **Roast / check**: "does this sound AI?" Scan it, give a verdict and the 3–6 biggest tells, then offer to rewrite. Don't rewrite unless they ask.
- **Write from scratch, human-sounding**: draft it, then run steps 4–6 on your own draft before showing it. Your first draft *will* have tells. Everyone's does.
- **Clone my voice**: build a voiceprint (step 3) and save it so later rewrites can use it.

Then work out the **mode** (email, Slack/DM, LinkedIn, cover letter, essay/blog, tweet/thread, docs/README, bio, academic). Each mode has different human norms: a Slack message with a greeting and a sign-off is as fake as a cover letter written in lowercase. Read `references/modes.md` for the mode you're in. It's short.

### 2. Scan the original

Save the text to a temp file and run:

```bash
python3 scripts/unslop.py scan /tmp/unslop_before.txt
```

This gives you the score (0 human ... 100 robotic), every flagged line with the matched phrase and a fix, plus rhythm problems no single phrase shows (flat sentence lengths, em-dash overuse, rule-of-three lists, one-line-paragraph staircases). Treat these as your to-do list.

If Python can't run here, scan by hand with `references/slop-patterns.md`, which has the same catalog in readable form.

### 3. Get the voice

In order of preference:

1. **They gave you samples of their own writing** (old emails, posts, messages, anything they wrote *without* AI). Save them and run:
   ```bash
   python3 scripts/unslop.py voice sample1.txt sample2.txt -o voice.json
   ```
   Read the description it prints. It says things like "starts 96% of sentences lowercase", "contracts a lot", "never uses semicolons". Those are your style rules. 150+ words makes a usable print. 500+ is great.
2. **A saved voiceprint exists** (look for `voice.json` in the working directory or one they mention). Reuse it.
3. **Neither**: if they're likely to come back to this skill (job hunting, regular posting), offer to clone their voice once: "Paste 2–3 things you wrote yourself and I'll match your style from now on." Then go ahead with a plain-spoken default instead of blocking: a clear, direct person who uses contractions and talks to one reader.

The text being rewritten is **not** a voice sample. It's the AI's voice. That's the problem you're fixing.

### 4. Rewrite

Read `references/rewrite-playbook.md` before your first rewrite in a session. The short version:

- **Meaning is locked.** Every fact, number, name, date, link, commitment and ask in the original survives. You're changing how it sounds, not what it says. If the original is vague, don't invent specifics to fill it in. Mark the gap instead (see below).
- **Delete before you replace.** Most slop is padding. "It's worth noting that X" becomes "X", not "Notably, X". Swapping a tell for its synonym (crucial → critical, delve → dig deep) doesn't fix it.
- **Concrete beats adjectives.** "A vibrant, collaborative team" says nothing. "Priya rewrote the onboarding flow in a weekend" says something. Only use details that are in the source or that the user gives you.
- **Break the rhythm.** Mix a 4-word sentence with a 25-word one. Merge some short ones. Let a paragraph be one sentence when it earns it, but not every paragraph.
- **Say the thing first.** Cut the opener, cut the drumroll, put the point or the ask in sentence one or two.
- **Don't overcorrect.** No fake typos, no forced slang, no "lol" unless their voiceprint has it, no swapping every em-dash for a semicolon. A human-sounding text is plain and specific, not quirky.
- **Match the voiceprint.** If they write short, lowercase, no exclamation marks, then so does the rewrite.

**Missing specifics.** AI drafts are often vague because nobody gave the AI the specifics. When the honest fix is a detail only the user knows, put a visible placeholder like `[which client?]` or `[real number?]` and list them after the text. Inventing a convincing detail is worse than the slop.

### 5. Verify

Save the rewrite and run the full report:

```bash
python3 scripts/unslop.py compare /tmp/unslop_before.txt /tmp/unslop_after.txt
python3 scripts/unslop.py voicecheck /tmp/unslop_after.txt --profile voice.json   # if you have a voiceprint
```

Done means:

- Slop Score **≤ 15** (HUMAN). For long formal documents ≤ 25 is fine, because those legitimately use words like "crucial".
- Fact Lock clean, or every flag is explained (for example "Sarah" became "you" in a reply to Sarah).
- Voice match **≥ 80%** if there's a voiceprint.

If you're not there, fix what the report names and run it again. Up to 3 passes. The score is a tool, not the goal. Don't game it with synonyms the scanner doesn't know yet. The final test is whether a sharp friend reading it would think "a person wrote this". Read it aloud in your head. If any sentence sounds like an ad, a press release or a motivational poster, rewrite it.

### 6. Deliver

Lead with the rewritten text in a clean block they can copy. Then a short report, no longer than this:

```
Slop Score 96 → 8 (ROBOTIC → HUMAN) · facts locked ✓ · voice match 88%
Cut: "hope this finds you well", fake contrast, 3 rule-of-three lists, "Ultimately,", "don't hesitate to reach out"
Needs you: [real number?] in paragraph 2
```

Keep the report short. The text is the product. If they asked for a roast, flip it: verdict and tells first, with the offending lines quoted.

## A note on honesty

This skill is about writing that reads well to people. It doesn't promise to fool AI-detection software, and it shouldn't be pitched as that. If someone wants to pass off generated text where AI use isn't allowed (graded coursework, for example), say so plainly. Rewriting your *own* drafts, emails and posts to sound like you is exactly what this is for.

## Extending

Users and teams can add their own banned phrases (company buzzwords, a pet peeve) without editing the skill. They write a JSON file in the same shape as `scripts/slop_patterns.json` and pass `--extra their_patterns.json`. For a docs repo, `scan --fail-above 30` exits non-zero, so it can block PRs in CI.

## Files

- `scripts/unslop.py`: scanner, voiceprint, fact lock, compare report
- `scripts/slop_patterns.json`: the pattern library (regex, weight, fix) plus rhythm thresholds
- `references/slop-patterns.md`: readable catalog with before/after examples, including tells too subtle for a regex
- `references/rewrite-playbook.md`: how to rewrite well, with worked examples
- `references/modes.md`: norms per format (email, LinkedIn, Slack, cover letter, and more)
