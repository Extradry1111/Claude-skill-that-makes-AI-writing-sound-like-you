#!/usr/bin/env python3
"""unslop - measure and remove the tells that make writing sound machine-made.

Zero dependencies. Python 3.8+.

Commands
  scan FILE            Slop Score (0 = human, 100 = pure AI) + every flagged line
  compare BEFORE AFTER Score delta, what was fixed, what's left, and a fact-lock check
  voice SAMPLE...      Build a voiceprint (rhythm + habits) from someone's real writing
  voicecheck DRAFT     Compare a draft against a saved voiceprint
  lock ORIGINAL NEW    Make sure numbers, names, dates, links survived a rewrite

Use "-" as FILE to read stdin. Add --json to any command for machine output.
"""

import argparse
import signal
import json
import math
import os
import re
import statistics
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERNS_PATH = os.path.join(HERE, "slop_patterns.json")

# ---------------------------------------------------------------- terminal ---

USE_COLOR = (sys.stdout.isatty() or os.environ.get("FORCE_COLOR")) and os.environ.get("NO_COLOR") is None


def c(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def bold(t): return c(t, "1")
def dim(t): return c(t, "2")
def red(t): return c(t, "31")
def green(t): return c(t, "32")
def yellow(t): return c(t, "33")
def cyan(t): return c(t, "36")
def magenta(t): return c(t, "35")
def hl(t): return c(t, "1;30;43")


CROSS, CHECK, WAVE, ARROW, DOWN, UP = "\u2717", "\u2713", "\u223f", "\u2192", "\u2193", "\u2191"


# ------------------------------------------------------------------- text ---

def read_input(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


WORD_RE = re.compile(r"[A-Za-z0-9À-ɏ']+")
EM_DASH_RE = re.compile(r"—|\s–\s|\s--\s")
TRIPLET_RE = re.compile(
    r"\b[\w'-]+(?: [\w'-]+){0,2}, [\w'-]+(?: [\w'-]+){0,2},? (?:and|or) [\w'-]+", re.I)
CONTRACTION_RE = re.compile(
    r"\b\w+'(s|t|re|ve|ll|d|m)\b|\b(gonna|wanna|gotta|kinda|y'all)\b", re.I)
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF☀-➿⭐⭕✅❌✨]")
BULLET_RE = re.compile(r"^\s*([-*•]|\d+[.)])\s+")


def words(text):
    return WORD_RE.findall(text)


def strip_markdown(line):
    line = BULLET_RE.sub("", line)
    return line.replace("**", "").replace("__", "")


def sentences(text):
    out = []
    for para in paragraphs(text):
        para = " ".join(strip_markdown(l) for l in para.splitlines())
        for s in re.split(r"(?<=[.!?])\s+(?=[\"'(\[]?[A-Za-z0-9])", para):
            s = s.strip()
            if len(words(s)) >= 1:
                out.append(s)
    return out


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def per100(count, n_words):
    return 100.0 * count / max(n_words, 1)


# ------------------------------------------------------------------- scan ---

def load_patterns(extra=None):
    with open(PATTERNS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    pats = data["patterns"]
    if extra:
        with open(extra, encoding="utf-8") as f:
            more = json.load(f)
        pats = pats + (more["patterns"] if isinstance(more, dict) else more)
    for p in pats:
        p["_re"] = re.compile(p["regex"], re.I | re.M)
    return pats, data["rhythm"]


def grade(score):
    if score <= 15:
        return "HUMAN", green
    if score <= 35:
        return "LIGHT TOUCH", cyan
    if score <= 60:
        return "NOTICEABLY AI", yellow
    return "ROBOTIC", red


def mask_code(text):
    """Blank out fenced code blocks (keeping line numbers) so `# comments` and
    sample code don't count as prose."""
    return re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*$",
                  lambda m: "\n" * m.group(0).count("\n"), text)


def scan_text(text, extra=None):
    pats, rhythm = load_patterns(extra)
    text = mask_code(text)
    n_words = len(words(text))
    hits = []
    for p in pats:
        for m in p["_re"].finditer(text):
            raw = m.group(0)
            start = m.start() + len(raw) - len(raw.lstrip(" \t\n.!?"))
            hits.append({
                "id": p["id"], "category": p["category"], "label": p["label"],
                "fix": p["fix"], "weight": p["weight"],
                "line": line_of(text, start), "match": raw.strip(" \t\n.!?") or raw.strip(),
                "start": start, "end": m.end(),
            })

    # Rhythm signals: things no single regex catches.
    sents = sentences(text)
    lens = [len(words(s)) for s in sents]
    em = len(EM_DASH_RE.findall(text))
    trip = len(TRIPLET_RE.findall(text))
    paras = paragraphs(text)
    # Greetings and sign-offs ("Hi Sarah,", "- j") are one-liners by nature; skip them.
    paras = [p for p in paras if len(words(p)) > 4]
    one_liners = sum(1 for p in paras if len(sentences(p)) <= 1 and "\n" not in p)
    cv = (statistics.pstdev(lens) / statistics.mean(lens)) if len(lens) >= 5 else None
    burst_cv = cv if len(lens) >= rhythm.get("burstiness_min_sentences", 8) else None

    rh = {
        "words": n_words, "sentences": len(sents),
        "avg_sentence_words": round(statistics.mean(lens), 1) if lens else 0,
        "burstiness_cv": round(cv, 2) if cv is not None else None,
        "em_dashes": em, "em_dash_per_100": round(per100(em, n_words), 2),
        "triplets": trip, "triplet_per_100": round(per100(trip, n_words), 2),
        "one_line_paragraph_ratio": round(one_liners / len(paras), 2) if paras else 0,
    }
    rhythm_pen = {}
    x = rh["em_dash_per_100"] - rhythm["em_dash_per_100_words_ok"]
    if x > 0 and em >= rhythm.get("em_dash_min_count", 2):
        rhythm_pen["em-dash overuse"] = x * rhythm["em_dash_weight"]
    x = rh["triplet_per_100"] - rhythm["triplet_per_100_words_ok"]
    if x > 0 and trip >= rhythm.get("triplet_min_count", 2):
        rhythm_pen["rule-of-three lists"] = x * rhythm["triplet_weight"]
    if burst_cv is not None and burst_cv < rhythm["burstiness_cv_ok"]:
        rhythm_pen["flat sentence rhythm"] = (
            (rhythm["burstiness_cv_ok"] - burst_cv) / rhythm["burstiness_cv_ok"]
            * rhythm["burstiness_weight"])
    if len(paras) >= 5 and rh["one_line_paragraph_ratio"] > rhythm["one_line_paragraph_ratio_ok"]:
        ok = rhythm["one_line_paragraph_ratio_ok"]
        rhythm_pen["one-line-paragraph staircase"] = (
            (rh["one_line_paragraph_ratio"] - ok) / (1 - ok) * rhythm["one_line_paragraph_weight"])

    lexical = per100(sum(h["weight"] for h in hits), n_words)
    density = lexical + sum(rhythm_pen.values())
    # Saturating curve: one tell in a long piece barely moves it,
    # a tell every sentence pins it near 100.
    score = round(100 * (1 - math.exp(-density / 7.0)))
    g, _ = grade(score)

    cats = Counter()
    for h in hits:
        cats[h["category"]] += 1
    for k in rhythm_pen:
        cats["rhythm"] += 1

    return {
        "score": score, "grade": g, "density": round(density, 2),
        "hits": sorted(hits, key=lambda h: (h["line"], h["start"])),
        "rhythm": rh, "rhythm_penalties": {k: round(v, 2) for k, v in rhythm_pen.items()},
        "categories": dict(cats),
    }


def bar(score, width=30):
    filled = round(score / 100 * width)
    _, col = grade(score)
    return col("█" * filled) + dim("░" * (width - filled))


def print_scan(text, r, title="SLOP SCAN", max_hits=40):
    g, col = grade(r["score"])
    print()
    print(bold(f"  {title}"))
    print(f"  {bar(r['score'])}  {bold(col(str(r['score'])))}{dim('/100')}  {col(g)}")
    rh = r["rhythm"]
    print(dim(f"  {rh['words']} words · {rh['sentences']} sentences · "
              f"avg {rh['avg_sentence_words']} words/sentence · "
              f"rhythm variation {rh['burstiness_cv'] if rh['burstiness_cv'] is not None else 'n/a'}"))
    print()
    if not r["hits"] and not r["rhythm_penalties"]:
        print(green("  No tells found. This reads like a person wrote it."))
        print()
        return
    lines = text.splitlines()
    shown = 0
    by_line = {}
    for h in r["hits"]:
        by_line.setdefault(h["line"], []).append(h)
    for ln in sorted(by_line):
        if shown >= max_hits:
            print(dim(f"  ... {len(r['hits']) - shown} more (use --json for all)"))
            break
        src = lines[ln - 1] if ln - 1 < len(lines) else ""
        snippet = src
        for h in sorted(by_line[ln], key=lambda h: -len(h["match"])):
            if h["match"] and h["match"] in snippet:
                snippet = snippet.replace(h["match"], hl(h["match"]), 1)
        if len(src) > 140:
            snippet = snippet[:220] + dim("…")
        print(f"  {dim(f'L{ln:<4}')}{snippet.strip()}")
        for h in by_line[ln]:
            shown += 1
            print(f"        {red('✗')} {bold(h['label'])} {dim('→')} {h['fix']}")
    if r["rhythm_penalties"]:
        print()
        print(bold("  Rhythm"))
        msgs = {
            "em-dash overuse": f"{rh['em_dashes']} em-dashes ({rh['em_dash_per_100']}/100 words). Humans use commas, periods, parentheses.",
            "rule-of-three lists": f"{rh['triplets']} 'A, B, and C' lists. AI loves threes. Use two, or one.",
            "flat sentence rhythm": f"sentence lengths barely vary (variation {rh['burstiness_cv']}). Mix a 4-word sentence with a 25-word one.",
            "one-line-paragraph staircase": f"{round(rh['one_line_paragraph_ratio']*100)}% one-line paragraphs. That's the LinkedIn staircase.",
        }
        for k in r["rhythm_penalties"]:
            print(f"   {yellow('∿')} {msgs[k]}")
    print()
    print(dim("  by category: " + ", ".join(f"{k} {v}" for k, v in
                                           sorted(r["categories"].items(), key=lambda kv: -kv[1]))))
    print()


# ------------------------------------------------------------------- lock ---

MONTHS = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
NUM_RE = re.compile(r"(?<![A-Za-z0-9])[$€£]?\d[\d,]*(?:\.\d+)?\s?(?:%|k|K|M|B|x)?(?![A-Za-z0-9])")
DATE_RE = re.compile(MONTHS + r"\.? \d{1,2}(?:st|nd|rd|th)?(?:,? \d{4})?")
URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
HANDLE_RE = re.compile(r"(?<![\w@])@\w{2,}")
QUOTE_RE = re.compile(r"\"([^\"\n]{3,80})\"|“([^”\n]{3,80})”")
COMMON_CAPS = set("""I I'm I've I'll I'd A An The This That These Those It Its We Our You Your He She They Their
My Me Hi Hey Hello Dear Thanks Thank Best Regards Cheers Sincerely Also And But So Or If When While As At In On For
To Of With From By Just Here There What Why How Who Where Which Let Please Yes No Ok Okay Monday Tuesday Wednesday
Thursday Friday Saturday Sunday Mr Mrs Ms Dr""".split())


NUM_WORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()


def norm_num(s):
    return re.sub(r"[,\s]", "", s).rstrip(".").lower()


def facts(text):
    f = {"numbers": set(), "dates": set(), "links": set(), "emails": set(),
         "handles": set(), "quotes": set(), "names": set()}
    for m in NUM_RE.finditer(text):
        v = norm_num(m.group(0))
        if re.search(r"\d", v):
            f["numbers"].add(v)
    f["dates"] = {m.group(0) for m in DATE_RE.finditer(text)}
    f["links"] = {m.group(0).rstrip(".,)") for m in URL_RE.finditer(text)}
    f["emails"] = set(EMAIL_RE.findall(text))
    f["handles"] = set(HANDLE_RE.findall(text)) - {"@" + e.split("@")[1] for e in f["emails"]}
    f["quotes"] = {(a or b) for a, b in QUOTE_RE.findall(text)}
    # Proper nouns: capitalized words that are not just sentence-initial.
    for s in sentences(text):
        if re.match(r"(subject|re|fwd?):", s, re.I):
            s = s.split(":", 1)[1]
        toks = re.findall(r"[A-Za-z][\w'&.-]*", s)
        if len(toks) >= 3 and sum(t[0].isupper() for t in toks) / len(toks) > 0.6:
            continue  # Title Case Headline, not a run of names
        for i, t in enumerate(toks):
            t = t.rstrip(".'")
            if i == 0 or not t or not t[0].isupper() or t in COMMON_CAPS:
                continue
            if t.isupper() and len(t) == 1:
                continue
            f["names"].add(t)
    return f


def lock_check(orig, new):
    a, b = facts(orig), facts(new)
    new_nums = {norm_num(m.group(0)) for m in NUM_RE.finditer(new)}
    missing = {}
    for k, vals in a.items():
        miss = []
        for v in sorted(vals):
            if k == "numbers":
                ok = v in new_nums or v in norm_num(new)
                if not ok and v.isdigit() and int(v) <= 20:  # "6" -> "six" is fine
                    ok = re.search(r"\b" + NUM_WORDS[int(v)] + r"\b", new, re.I) is not None
            elif k == "names":
                ok = re.search(r"\b" + re.escape(v) + r"\b", new) is not None
            else:
                ok = v in new
            if not ok:
                miss.append(v)
        if miss:
            missing[k] = miss
    added_nums = sorted(new_nums - {norm_num(m.group(0)) for m in NUM_RE.finditer(orig)})
    added_nums = [n for n in added_nums if re.search(r"\d", n)]
    return {"ok": not missing and not added_nums, "missing": missing, "invented_numbers": added_nums,
            "checked": {k: len(v) for k, v in a.items()}}


def print_lock(r):
    total = sum(r["checked"].values())
    print(bold("  FACT LOCK"))
    if r["ok"]:
        print(f"  {green('✓')} all {total} facts survived (numbers, names, dates, links, quotes)")
    else:
        for k, vals in r["missing"].items():
            print(f"  {red('✗')} missing {k}: {', '.join(vals)}")
        if r["invented_numbers"]:
            print(f"  {red('✗')} numbers in the rewrite that weren't in the original: "
                  f"{', '.join(r['invented_numbers'])}")
        if "names" in r["missing"]:
            print(dim("    (a missing name is sometimes a fine pronoun swap - check before shipping)"))
    print()


# ------------------------------------------------------------------ voice ---

STOP = set("""the a an and or but so of to in on for with at by from up about into over after is are was were be
been being have has had do does did i you he she it we they me him her us them my your his its our their this
that these those there here what which who whom when where why how all any both each few more most other some
such no nor not only own same than too very can will just should now if then as because until while also get got
im ive dont cant its thats youre theyre were id ill would could one like really""".split())


def voice_metrics(text):
    w = words(text)
    n = len(w)
    sents = sentences(text)
    lens = [len(words(s)) for s in sents] or [0]
    paras = paragraphs(text)
    firsts = [words(s)[0] for s in sents if words(s)]
    m = {
        "words": n,
        "avg_sentence_words": round(statistics.mean(lens), 1),
        "sentence_variation": round(statistics.pstdev(lens) / statistics.mean(lens), 2) if statistics.mean(lens) else 0,
        "short_sentence_pct": round(100 * sum(1 for l in lens if l <= 6) / len(lens)),
        "long_sentence_pct": round(100 * sum(1 for l in lens if l >= 25) / len(lens)),
        "sentences_per_paragraph": round(len(sents) / max(len(paras), 1), 1),
        "contractions_per_100": round(per100(len(CONTRACTION_RE.findall(text)), n), 1),
        "em_dash_per_100": round(per100(len(EM_DASH_RE.findall(text)), n), 2),
        "exclamations_per_100": round(per100(text.count("!"), n), 2),
        "questions_per_100": round(per100(text.count("?"), n), 2),
        "semicolons_per_100": round(per100(text.count(";"), n), 2),
        "parens_per_100": round(per100(text.count("("), n), 2),
        "ellipses_per_100": round(per100(len(re.findall(r"\.\.\.|…", text)), n), 2),
        "emoji_per_100": round(per100(len(EMOJI_RE.findall(text)), n), 2),
        "first_person_per_100": round(per100(sum(1 for x in w if x.lower() in ("i", "i'm", "i've", "i'll", "i'd", "me", "my")), n), 1),
        "lowercase_start_pct": round(100 * sum(1 for s in sents if s[:1].islower()) / max(len(sents), 1)),
        "conjunction_start_pct": round(100 * sum(1 for f in firsts if f.lower() in ("and", "but", "so", "or")) / max(len(firsts), 1)),
    }
    return m


def voice_profile(texts):
    joined = "\n\n".join(texts)
    m = voice_metrics(joined)
    w = [x.lower() for x in words(joined)]
    sents = sentences(joined)
    firsts = Counter(words(s)[0].lower() for s in sents if len(words(s)) > 2)
    content = Counter(x for x in w if x not in STOP and len(x) > 2 and not x.isdigit())
    greetings, signoffs = Counter(), Counter()
    for t in texts:
        ls = [l.strip() for l in t.strip().splitlines() if l.strip()]
        if ls and len(words(ls[0])) <= 4:
            greetings[ls[0]] += 1
        if len(ls) > 1 and len(words(ls[-1])) <= 4:
            signoffs[ls[-1]] += 1
    return {
        "metrics": m,
        "favorite_openers": [k for k, v in firsts.most_common(6) if v > 1],
        "signature_words": [k for k, v in content.most_common(15) if v > 1],
        "greetings": [k for k, _ in greetings.most_common(3)],
        "signoffs": [k for k, _ in signoffs.most_common(3)],
        "samples": len(texts),
    }


def describe_voice(p):
    m = p["metrics"]
    out = []
    a = m["avg_sentence_words"]
    out.append(f"Sentences average {a} words "
               f"({'short and punchy' if a < 12 else 'medium' if a < 20 else 'long and flowing'}), "
               f"{m['short_sentence_pct']}% are 6 words or fewer, {m['long_sentence_pct']}% run 25+.")
    v = m["sentence_variation"]
    out.append(f"Rhythm variation {v} "
               f"({'very uneven, lots of short/long mixing' if v > 0.7 else 'natural variation' if v > 0.45 else 'fairly even'}).")
    k = m["contractions_per_100"]
    out.append(f"Contractions: {k}/100 words ({'casual' if k > 2.5 else 'some' if k > 0.8 else 'formal, rarely contracts'}).")
    punct = []
    for key, name in [("em_dash_per_100", "em-dashes"), ("exclamations_per_100", "exclamation marks"),
                      ("semicolons_per_100", "semicolons"), ("parens_per_100", "parentheses"),
                      ("ellipses_per_100", "ellipses"), ("emoji_per_100", "emoji"), ("questions_per_100", "questions")]:
        punct.append(f"{name} {m[key]}")
    out.append("Punctuation per 100 words: " + ", ".join(punct) + ".")
    if m["lowercase_start_pct"] > 20:
        out.append(f"Starts {m['lowercase_start_pct']}% of sentences lowercase - keep that.")
    if m["conjunction_start_pct"] > 8:
        out.append(f"Starts {m['conjunction_start_pct']}% of sentences with And/But/So.")
    if p["favorite_openers"]:
        out.append("Favorite sentence openers: " + ", ".join(p["favorite_openers"]) + ".")
    if p["signature_words"]:
        out.append("Words they reach for: " + ", ".join(p["signature_words"]) + ".")
    if p["greetings"]:
        out.append("Greetings: " + " | ".join(p["greetings"]))
    if p["signoffs"]:
        out.append("Sign-offs: " + " | ".join(p["signoffs"]))
    return out


TOL = {  # metric: (absolute tolerance, relative tolerance)
    "avg_sentence_words": (3, 0.25), "sentence_variation": (0.12, 0.25),
    "short_sentence_pct": (12, 0.5), "long_sentence_pct": (12, 0.5),
    "sentences_per_paragraph": (1.5, 0.4), "contractions_per_100": (1.0, 0.4),
    "em_dash_per_100": (0.3, 0.5), "exclamations_per_100": (0.4, 0.5),
    "questions_per_100": (0.5, 0.5), "semicolons_per_100": (0.3, 0.5),
    "parens_per_100": (0.4, 0.5), "ellipses_per_100": (0.3, 0.5),
    "emoji_per_100": (0.3, 0.5), "first_person_per_100": (2.0, 0.4),
    "lowercase_start_pct": (15, 0.5), "conjunction_start_pct": (8, 0.6),
}


def voice_check(profile, draft):
    want = profile["metrics"]
    got = voice_metrics(draft)
    rows, off = [], 0
    for k, (at, rt) in TOL.items():
        tol = max(at, rt * abs(want[k]))
        diff = got[k] - want[k]
        bad = abs(diff) > tol
        off += bad
        rows.append({"metric": k, "voice": want[k], "draft": got[k], "off": bad,
                     "direction": "too high" if diff > 0 else "too low"})
    match = round(100 * (1 - off / len(TOL)))
    return {"match": match, "rows": rows}


# -------------------------------------------------------------------- cli ---

def cmd_scan(a):
    text = read_input(a.file)
    r = scan_text(text, a.extra)
    if a.json:
        for h in r["hits"]:
            h.pop("start"); h.pop("end")
        print(json.dumps(r, indent=2))
    else:
        print_scan(text, r)
    if a.fail_above is not None and r["score"] > a.fail_above:
        sys.exit(1)


def cmd_compare(a):
    before, after = read_input(a.before), read_input(a.after)
    rb, ra = scan_text(before, a.extra), scan_text(after, a.extra)
    lk = lock_check(before, after)
    fixed = Counter(h["label"] for h in rb["hits"]) - Counter(h["label"] for h in ra["hits"])
    left = ra["hits"]
    if a.json:
        print(json.dumps({"before": rb["score"], "after": ra["score"],
                          "before_grade": rb["grade"], "after_grade": ra["grade"],
                          "fixed": dict(fixed), "remaining": [
                              {k: h[k] for k in ("line", "label", "match", "fix")} for h in left],
                          "remaining_rhythm": ra["rhythm_penalties"], "fact_lock": lk}, indent=2))
        return
    gb, cb = grade(rb["score"])
    ga, ca = grade(ra["score"])
    print()
    print(bold("  UNSLOP REPORT"))
    print(f"  before  {bar(rb['score'])}  {cb(str(rb['score']).rjust(3))}  {cb(gb)}")
    print(f"  after   {bar(ra['score'])}  {ca(str(ra['score']).rjust(3))}  {ca(ga)}")
    d = rb["score"] - ra["score"]
    print(f"          {green(f'↓ {d} points') if d > 0 else red(f'↑ {-d} points') if d < 0 else dim('no change')}")
    print()
    if fixed:
        print(bold("  Removed"))
        for lbl, n in fixed.most_common():
            print(f"  {green('✓')} {lbl}" + (dim(f" ×{n}") if n > 1 else ""))
        for k in rb["rhythm_penalties"]:
            if k not in ra["rhythm_penalties"]:
                print(f"  {green('✓')} {k}")
        print()
    if left or ra["rhythm_penalties"]:
        print(bold("  Still there"))
        for h in left:
            print(f"  {red('✗')} L{h['line']} {h['label']}: \"{h['match']}\"")
        for k in ra["rhythm_penalties"]:
            print(f"  {yellow('∿')} {k}")
        print()
    print_lock(lk)


def cmd_voice(a):
    texts = [read_input(f) for f in a.samples]
    p = voice_profile(texts)
    p["description"] = describe_voice(p)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
    if a.json:
        print(json.dumps(p, indent=2))
        return
    print()
    print(bold(f"  VOICEPRINT") + dim(f"  ({p['metrics']['words']} words from {p['samples']} sample(s))"))
    if p["metrics"]["words"] < 150:
        print(yellow("  ! under 150 words - the profile will be rough. More samples = better clone."))
    for line in p["description"]:
        print(f"  • {line}")
    if a.out:
        print(dim(f"\n  saved → {a.out}"))
    print()


def cmd_voicecheck(a):
    with open(a.profile, encoding="utf-8") as f:
        prof = json.load(f)
    r = voice_check(prof, read_input(a.draft))
    if a.json:
        print(json.dumps(r, indent=2))
        return
    col = green if r["match"] >= 80 else yellow if r["match"] >= 60 else red
    print()
    print(bold("  VOICE MATCH ") + col(f"{r['match']}%"))
    for row in r["rows"]:
        mark = red("✗") if row["off"] else green("✓")
        note = red(f"  {row['direction']}") if row["off"] else ""
        print(f"  {mark} {row['metric']:<26} you {str(row['voice']):>6}   draft {str(row['draft']):>6}{note}")
    print()


def cmd_lock(a):
    r = lock_check(read_input(a.original), read_input(a.rewrite))
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print()
        print_lock(r)
    if not r["ok"]:
        sys.exit(2)


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet exit when piped to head
    ap = argparse.ArgumentParser(prog="unslop", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="score a text and flag every AI tell")
    s.add_argument("file")
    s.add_argument("--json", action="store_true")
    s.add_argument("--extra", help="extra patterns JSON to merge in")
    s.add_argument("--fail-above", type=int, help="exit 1 if score is above this (for CI)")
    s.set_defaults(fn=cmd_scan)

    s = sub.add_parser("compare", help="before/after report + fact lock")
    s.add_argument("before")
    s.add_argument("after")
    s.add_argument("--json", action="store_true")
    s.add_argument("--extra")
    s.set_defaults(fn=cmd_compare)

    s = sub.add_parser("voice", help="build a voiceprint from writing samples")
    s.add_argument("samples", nargs="+")
    s.add_argument("-o", "--out", help="save profile JSON here")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_voice)

    s = sub.add_parser("voicecheck", help="check a draft against a voiceprint")
    s.add_argument("draft")
    s.add_argument("--profile", required=True)
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_voicecheck)

    s = sub.add_parser("lock", help="verify facts survived a rewrite")
    s.add_argument("original")
    s.add_argument("rewrite")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_lock)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
