# The slop catalog

Each tell is listed with the reason it reads as machine-made and what a person would write instead. Patterns marked **(scanned)** are caught by `unslop.py scan`. Patterns marked **(eyes only)** are too fuzzy for a regex, so look for them yourself.

## Contents
1. Fake contrast and drumrolls
2. AI vocabulary
3. Openers and closers
4. Empty analysis
5. Hedging and intensifiers
6. Rhythm and structure
7. Formatting
8. Tells only a human eye catches

---

## 1. Fake contrast and drumrolls

The strongest tell of all. The model invents a position nobody held so that it can knock it down.

| Tell | Example | Human version |
|---|---|---|
| It's not X, it's Y **(scanned)** | "This isn't just a job. It's a calling." | "I love this job." Or skip it entirely. |
| Not only... but also **(scanned)** | "not only faster but also cheaper" | "faster and cheaper" |
| Less about X, more about Y **(scanned)** | "Leadership is less about authority and more about trust." | Say the thing about trust, with an example. |
| Self-answered question **(scanned)** | "The result? A 40% lift." | "Conversions went up 40%." |
| Here's the thing / Let that sink in **(scanned)** | "Here's the thing: nobody reads docs." | "Nobody reads docs." |
| The answer is simple: **(scanned)** | "The secret is simple: consistency." | "Show up every week." |

**Why:** a person who has a point makes it. The setup and reveal is a rhetorical move from ad copy, and models use it in every paragraph.

## 2. AI vocabulary **(scanned)**

The words: delve, tapestry, testament, realm, landscape, navigate the complexities, intricate, multifaceted, nuanced, pivotal, paramount, crucial, leverage, utilize, harness, seamless, robust, cutting-edge, game-changer, foster, empower, elevate, unlock, embark, showcase, underscore, boast, meticulous, vibrant, bustling, journey (when nobody is traveling), synergy, holistic, plays a crucial role, in today's fast-paced world, Moreover, Furthermore, Additionally.

**Why:** none of these is wrong on its own. They are just far more common in model output than in human writing, so a reader's pattern-matcher fires on them. Two in one paragraph and the reader stops trusting the text.

**Fix:** usually delete, sometimes replace with the plain word (use, help, important, shows, has, start). The best fix is often a concrete detail. "A robust solution" becomes "it hasn't gone down since March".

## 3. Openers and closers **(scanned)**

Openers: "I hope this email finds you well", "Great question!", "Certainly!", "Absolutely!", "Let's dive in", "I'm thrilled to announce", "I am writing to express", "When it comes to".

Closers: "I hope this helps", "Don't hesitate to reach out", "Let me know if you have any questions", "In conclusion,", "Ultimately,", "At the end of the day,", "Happy to help!", "The future looks bright", "Thoughts?" / "Agree?" (LinkedIn bait).

**Why:** these are the packaging around the content. Humans skip packaging when writing to someone they know, and keep it to a word or two ("Hi Sarah,", "Thanks,") otherwise.

**Fix:** start with the reason you're writing. End with the specific ask, or end when the content ends.

## 4. Empty analysis **(scanned)**

| Tell | Example | Fix |
|---|---|---|
| Participle tail | "The city opened a library, highlighting its commitment to education." | "The city opened a library." |
| serves as / stands as | "The park serves as a hub for the community." | "The park is where everyone ends up on Sundays." |
| Vague authority | "Experts say..." / "Studies show..." | Name the study, or drop it. |
| False range | "from startups to enterprises, from students to CEOs" | Name who actually uses it. |
| Significance inflation **(eyes only)** | "marking a pivotal moment in the evolution of..." | Say what happened. Let the reader decide if it's pivotal. |

## 5. Hedging and intensifiers **(scanned)**

Hedges: "It's worth noting that", "It's important to remember", "generally speaking", "to some extent", "arguably", "can help improve".
Intensifiers: truly, genuinely, incredibly, deeply, profoundly, remarkably, "passionate about".

**Why:** hedges are a model protecting itself. Intensifiers are a model trying to sound sincere. Both make it sound less sincere.

**Fix:** delete the hedge and state the claim. If the claim really is uncertain, say what it depends on. Delete the intensifier: "I'm grateful" is stronger than "I'm truly grateful".

## 6. Rhythm and structure **(scanned)**

- **Flat sentence lengths.** Models write sentence after sentence of 15–20 words. People write a 3-word sentence, then a 30-word one. The scanner reports this as "rhythm variation" (the coefficient of variation of sentence lengths): under ~0.35 is flat, and 0.5–0.8 is typical for people.
- **Rule of three.** "fast, reliable, and secure"; "innovation, collaboration, and trust". One triplet is fine. Three in one post is a signature.
- **Em-dash pileups.** A single em-dash is fine. Several per paragraph is the most-memed AI tell there is. Use a period, a comma or parentheses instead, and don't just turn them all into semicolons or colons.
- **LinkedIn staircase.** Every sentence its own paragraph. One or two for punch is fine; a whole post of them reads like a template.

## 7. Formatting **(scanned)**

- `**Bold label:**` bullets in an email or post. Fine in docs, robotic in a message to a person.
- Emoji used as bullets (🚀 ✅ 💡 👉 🔥).
- Markdown headers in emails, DMs and social posts.
- **(eyes only)** Title Case Headings Everywhere, and a bulleted list where two sentences would do.

## 8. Tells only a human eye catches **(eyes only)**

- **Symmetry.** Every paragraph is the same length, and every bullet starts with a verb and has the same shape.
- **Summary restatement.** The last paragraph repeats the first in different words.
- **Elegant variation.** The same thing called "the company", "the organization", "the firm" and "the business" in four sentences, to avoid repeating a word. People just repeat the word.
- **Generic specifics.** "a leading company in the industry", "various stakeholders", "a wide range of features". These look like detail and contain none.
- **Over-politeness and sycophancy.** "You're absolutely right!", "What a great question", and thanking someone three times.
- **No opinion.** Every side gets equal weight, and nothing is ever bad. People have takes.
- **Perfect parallel lists of benefits** with nothing negative, no tradeoffs and no "but".
- **Over-explaining the obvious** to a reader who clearly knows it.
