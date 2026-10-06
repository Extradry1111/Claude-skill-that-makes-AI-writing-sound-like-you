#!/usr/bin/env python3
"""Validate every SKILL.md and scan template files for secrets before sharing.

Usage: python3 scripts/validate.py [root]
Exits 1 if any check fails.
"""
import re
import sys
from pathlib import Path

SECRET_PATTERNS = {
    "api key (sk-/xai-)": re.compile(r"\b(?:sk|xai)-[A-Za-z0-9_-]{16,}"),
    "github token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    "aws key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer token": re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"),
    "key assignment": re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9._-]{12,}"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"(?<!\d)\+?\d{1,3}[ .-]?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}(?!\d)"),
    "private host": re.compile(r"\b(?:localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)\b"),
}
SCAN_DIRS = ("template", "creator-kit")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def main(root):
    errors = []
    skills = sorted(root.glob("**/skills/*/*/SKILL.md"))
    if not skills:
        errors.append("no skills found at skills/<category>/<slug>/SKILL.md")
    for path in skills:
        rel = path.relative_to(root)
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        slug = path.parent.name
        if not SLUG.match(slug):
            errors.append(f"{rel}: folder '{slug}' is not kebab-case")
        if fm.get("name") != slug:
            errors.append(f"{rel}: name '{fm.get('name')}' should match folder '{slug}'")
        if len(fm.get("description", "")) < 40:
            errors.append(f"{rel}: description missing or too short to trigger reliably")

    for d in SCAN_DIRS:
        for path in sorted((root / d).glob("**/*")):
            if not path.is_file():
                continue
            rel = path.relative_to(root)
            for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                for label, pattern in SECRET_PATTERNS.items():
                    if pattern.search(line):
                        errors.append(f"{rel}:{n}: possible {label}")

    for e in errors:
        print(f"FAIL {e}")
    print(f"{len(skills)} skills checked, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)))
