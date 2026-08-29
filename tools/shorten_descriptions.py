"""Bring 21 over-long meta descriptions under the ~155 char SERP limit.

Two problems here, not one. The obvious one is length: these ran 160-231 chars
and were being cut mid-sentence. The less obvious one is that the nine
emotional-archetype pages ended with 130 characters of byte-identical
boilerplate, so the only distinguishing text sat in the part Google truncated.

Each rewrite keeps the page's own hook, which is good copy, and trims the shared
tail. og:description and twitter:description are only touched where they
currently match the meta description, so pages that intentionally diverge keep
their own social copy.
"""

import re
import sys

DESC_LIMIT = 155

ARCHETYPE_TAIL = "The emotional signature, relationship dynamic, and growth edge."

ARCHETYPES = {
    "the-inward-witness":      "The Inward Witness, comfortable with silence and allergic to performance.",
    "the-patient-builder":     "The Patient Builder, measures in years where others measure in weeks.",
    "the-quiet-disruptor":     "The Quiet Disruptor, sees what others will only see in three months.",
    "the-inner-sovereign":     "The Inner Sovereign, self-sufficient long before they feel it.",
    "the-devoted-beautifier":  "The Devoted Beautifier, finds the sacred in care and detail.",
    "the-protector":           "The Protector, fights for people who are not in the room.",
    "the-restless-mind":       "The Restless Mind, seventeen tabs open, all the time.",
    "the-mirror":              "The Mirror, reads the room before anyone has spoken.",
    "the-translator":          "The Translator, explains things to make them real.",
}

OTHERS = {
    "about.html":
        "We built NameAligned to make authentic Chaldean numerology accessible to "
        "every Indian: a strict system, transparent calculations, practical remedies.",
    "conflict-styles-in-emotional-relationships.html":
        "Some couples fight loud. Some go silent. The four conflict styles, which "
        "ones repair a relationship and which ones quietly erode it.",
    "emotional-communication-styles.html":
        "Some talk fast, some pause, some need to write it down first. The five "
        "emotional communication styles and how they collide in relationships.",
    "reassurance-needs-in-relationships.html":
        "Some need words, some need consistency, some need space. How different "
        "people receive reassurance, and why the wrong kind feels like nothing.",
    "the-emotionally-analytical-personality.html":
        "Some people process emotion through structure and analysis. What that "
        "costs, what it gives, and how to do it without numbing yourself.",
    "why-some-people-emotionally-withdraw.html":
        "Some people pull back exactly when closeness matters most. The patterns "
        "underneath emotional withdrawal, and what those around them can do.",
    "why-some-people-feel-too-much.html":
        "Some people register emotional information at a frequency most do not. "
        "What high-feeling people carry, and why it is often a strength.",
    "lucky-attributes.html":
        "Chaldean lucky attributes for Numbers 1 to 9: lucky days, dates, colours "
        "to wear and avoid, gemstones, metals and directions, side by side.",
    "methodology.html":
        "The full methodology behind NameAligned: the Chaldean letter-value table, "
        "how we calculate Moolank, Bhagyank and name number, and our limits.",
    "name-number-5-meaning.html":
        "Name Number 5 in Chaldean numerology carries Mercury energy: adaptability, "
        "communication and quick decisions, with career, love and shadow.",
    "numerology-love-styles.html":
        "How every Birth Number behaves in love: green flags, shadow patterns, who "
        "they reach for, and the full Chaldean compatibility matrix.",
    "sources.html":
        "Every interpretation on NameAligned is anchored in a documented source: "
        "Cheiro, Lal Kitab, Prashna Marga, Lilly, Hermetic and Jungian traditions.",
}


def build():
    plan = dict(OTHERS)
    for slug, hook in ARCHETYPES.items():
        plan[f"emotional-archetype-{slug}.html"] = f"{hook} {ARCHETYPE_TAIL}"
    return plan


def apply(path, new):
    src = open(path, encoding="utf-8").read()
    old = re.search(r'name="description" content="([^"]*)"', src).group(1)

    out = re.sub(r'(name="description" content=")[^"]*(")',
                 lambda m: m.group(1) + new + m.group(2), src, count=1)

    # Only follow on the social tags where they currently mirror the meta
    # description; some pages carry deliberately different social copy.
    synced = []
    for attr, key in (("property", "og:description"), ("name", "twitter:description")):
        m = re.search(rf'{attr}="{key}"\s+content="([^"]*)"', out)
        if m and m.group(1) == old:
            out = re.sub(rf'({attr}="{key}"\s+content=")[^"]*(")',
                         lambda mm: mm.group(1) + new + mm.group(2), out, count=1)
            synced.append(key)

    open(path, "w", encoding="utf-8").write(out)
    return old, synced


def main():
    plan = build()
    over = {f: d for f, d in plan.items() if len(d) > DESC_LIMIT}
    if over:
        for f, d in over.items():
            print(f"TOO LONG {len(d)}ch {f}")
        raise SystemExit(f"{len(over)} still over {DESC_LIMIT}")

    for path, new in sorted(plan.items()):
        old, synced = apply(path, new)
        print(f"{path}\n  - [{len(old)}] {old}\n  + [{len(new)}] {new}\n    social synced: {synced or 'none (left as-is)'}")
    print(f"\n{len(plan)} descriptions shortened")


if __name__ == "__main__":
    sys.exit(main())
