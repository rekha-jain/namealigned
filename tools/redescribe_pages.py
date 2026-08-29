"""Mirror the Moolank / Bhagyank vocabulary into meta descriptions.

Descriptions do not affect ranking, but Google bolds terms that match the query,
which lifts CTR on impressions we already earn. Same doctrinal rule as the
titles: Bhagyank on life-path, Moolank on personality/career, and nothing added
to the name-number pages because "Namank" is absent from the body copy.

The spiritual pages get a different fix. Their descriptions never contained the
phrase "spiritual meaning", so there was nothing for Google to bold on the exact
query the page targets.

Per-number trait phrases are lifted from the descriptions already on disk rather
than retyped, so the copy stays consistent with the page.
"""

import re
import sys

PLANET = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury",
          6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}

# Google truncates around 155-160 chars; keep headroom.
DESC_LIMIT = 158


def read(path):
    return open(path, encoding="utf-8").read()


def traits():
    """Pull the '<planet> energy: <traits>, with' fragment from each life-path page."""
    out = {}
    for n in PLANET:
        s = read(f"life-path-number-{n}-meaning.html")
        d = re.search(r'name="description" content="([^"]*)"', s).group(1)
        out[n] = re.search(r"energy:\s*(.+?),\s*with\b", d).group(1).strip()
    return out


def set_desc(path, new, also_social=True):
    """Rewrite meta description, optionally keeping og/twitter in lockstep.

    The spiritual pages intentionally carry a different og:description from their
    meta description, so those are left alone (also_social=False).
    """
    src = read(path)
    out = src
    old = re.search(r'name="description" content="([^"]*)"', out).group(1)

    out = re.sub(r'(name="description" content=")[^"]*(")',
                 lambda m: m.group(1) + new + m.group(2), out, count=1)

    if also_social:
        for attr, key in (("property", "og:description"), ("name", "twitter:description")):
            pat = rf'({attr}="{key}"\s+content=")[^"]*(")'
            if re.search(pat, out):
                out = re.sub(pat, lambda m: m.group(1) + new + m.group(2), out, count=1)
            else:
                print(f"  ! {path}: missing {key}")

    open(path, "w", encoding="utf-8").write(out)
    return old


def main():
    T = traits()
    plan = []

    for n, p in PLANET.items():
        t = T[n]
        plan.append((f"life-path-number-{n}-meaning.html", True,
                     f"Life Path Number {n} (Bhagyank {n}) carries {p} energy: {t}, "
                     f"with Chaldean destiny themes, love, and growth."))
        plan.append((f"number/{n}-personality.html", True,
                     f"Moolank {n} personality in Chaldean numerology: {t}, "
                     f"with love style, career rhythm, and emotional shadows."))
        plan.append((f"number/{n}-career.html", True,
                     f"Best careers for Moolank {n} in Chaldean numerology: work strengths, "
                     f"pressure patterns, industries to avoid, and role matches."))
        plan.append((f"number-{n}-spiritual-meaning.html", False,
                     f"Number {n} spiritual meaning in Chaldean numerology: the {p}-led "
                     f"soul path, the essence, the lesson, the practice, and the shadow."))

    over = [(f, len(d), d) for f, _, d in plan if len(d) > DESC_LIMIT]
    if over:
        for f, L, d in over:
            print(f"TOO LONG {L}ch {f}: {d}")
        raise SystemExit(f"{len(over)} descriptions exceed {DESC_LIMIT} chars")

    for path, social, new in plan:
        old = set_desc(path, new, social)
        print(f"{path}\n  - [{len(old)}] {old}\n  + [{len(new)}] {new}")
    print(f"\n{len(plan)} descriptions rewritten")


if __name__ == "__main__":
    sys.exit(main())
