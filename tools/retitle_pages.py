"""Rewrite <title>/og:title/twitter:title on the 45 doctrinal number pages.

Two goals:
  1. Surface the India-market vocabulary (Moolank / Bhagyank) on the pages whose
     body copy already teaches those terms, so the title matches how the query is
     actually typed.
  2. Put the real query in the spiritual titles. "The Soul Path of Number N" is a
     phrase nobody searches; the H1 and schema headline already say
     "Number N Spiritual Meaning".

Moolank = birth number (day of birth) -> personality, career.
Bhagyank = life path (full DOB)       -> life-path-number-N-meaning.
Name number pages are left on Chaldean vocabulary: the body copy never uses
"Namank", so the title must not claim it.
"""

import re
import sys

PLANET = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury",
          6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}

SERP_LIMIT = 60


def targets():
    for n, p in PLANET.items():
        yield (f"life-path-number-{n}-meaning.html",
               f"Life Path Number {n} Meaning: Bhagyank {n}, {p} Destiny")
        yield (f"name-number-{n}-meaning.html",
               f"Name Number {n} Meaning: Chaldean {p} Vibration")
        yield (f"number/{n}-personality.html",
               f"Moolank {n} Personality: Number {n} Traits Under {p}")
        yield (f"number/{n}-career.html",
               f"Best Careers for Moolank {n}: Number {n} {p} Work Style")
        yield (f"number-{n}-spiritual-meaning.html",
               f"Number {n} Spiritual Meaning: The {p}-Led Soul Path")


def esc(s):
    """Titles here are plain ASCII words, digits, commas and hyphens, but keep
    attribute values safe regardless."""
    return s.replace("&", "&amp;").replace('"', "&quot;")


def retitle(path, new):
    src = open(path, encoding="utf-8").read()
    out = src

    old = re.search(r"<title>(.*?)</title>", out, re.S)
    if not old:
        raise SystemExit(f"{path}: no <title>")
    old = old.group(1).strip()

    out = re.sub(r"<title>.*?</title>", f"<title>{new}</title>", out, count=1, flags=re.S)

    for attr, key in (("property", "og:title"), ("name", "twitter:title")):
        pat = rf'({attr}="{key}"\s+content=")[^"]*(")'
        if not re.search(pat, out):
            print(f"  ! {path}: missing {key}")
            continue
        out = re.sub(pat, lambda m: m.group(1) + esc(new) + m.group(2), out, count=1)

    if out == src:
        return old, False
    open(path, "w", encoding="utf-8").write(out)
    return old, True


def main():
    changed = 0
    for path, new in targets():
        if len(new) > SERP_LIMIT:
            raise SystemExit(f"{path}: title {len(new)}ch exceeds {SERP_LIMIT}: {new}")
        old, did = retitle(path, new)
        if did:
            changed += 1
            print(f"{path}\n  - {old}\n  + {new}  [{len(new)}ch]")
    print(f"\n{changed} pages retitled")


if __name__ == "__main__":
    sys.exit(main())
