#!/usr/bin/env python3
"""
Rewrite the opening paragraph of programmatic-SEO pages so that pages
within a cluster don't all start with identical phrasing. Reduces the
"scaled content" pattern signal Google's spam classifiers look for.

Five intro variants per cluster, assigned deterministically by number
(n % 5) so same number always gets same variant (consistency for
re-crawls) but the cluster as a whole reads as five distinct voices.

Also fixes "1th" / "11th, 21th" ordinal typos that the original
overthinking builder produced.

Run:
  python3 tools/vary-seo-intros.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLANETS = {
    1: 'Sun', 2: 'Moon', 3: 'Jupiter', 4: 'Rahu', 5: 'Mercury',
    6: 'Venus', 7: 'Ketu', 8: 'Saturn', 9: 'Mars',
}


# ---------- helpers ----------
def ordinal(n):
    """Proper English ordinal: 1st, 2nd, 3rd, 4th, 11th, 21st, etc."""
    if 10 <= n % 100 <= 20:
        return f'{n}th'
    return f"{n}{ {1:'st', 2:'nd', 3:'rd'}.get(n % 10, 'th') }"


def date_phrase(n):
    """Build 'Nth, 1Nth, or 2Nth' with correct ordinals."""
    primary = ordinal(n)
    if n < 10:
        secondary = ordinal(10 + n)
        tertiary = ordinal(20 + n)
        return f'{primary}, {secondary} or {tertiary}'
    return primary


# ---------- intro variant pools ----------
# Each variant takes (n, planet) and returns the intro paragraph.
# Aim for 5 distinct voices: declarative, question-led, observational,
# personal-direct, contemplative.

def overthinking_intros():
    return [
        lambda n, p, dates: (
            f'Some minds chase clarity outward, some chase it in circles. If you were born on the '
            f'{dates} of any month (or your Life Path Number reduces to {n}), yours runs on '
            f'<strong>{p}</strong> energy, and the loop has a signature that is genuinely worth '
            f'understanding before you try to silence it.'
        ),
        lambda n, p, dates: (
            f'Why does your mind keep going back to the same thought when you have already decided? '
            f'For people born on the {dates}, the answer sits inside the way <strong>{p}</strong> '
            f'energy moves. Naming the pattern is half of releasing it.'
        ),
        lambda n, p, dates: (
            f'There is a specific kind of mental loop that belongs to <strong>{p}</strong>-led people, '
            f'meaning anyone born on the {dates} of any month, or with Life Path Number {n}. '
            f'It is not a flaw. It is information about what your mind is for.'
        ),
        lambda n, p, dates: (
            f'If you found this page on a tired night, you are not the first. The '
            f'<strong>{p}</strong>-led mind, common to people born on the {dates}, goes looking '
            f'for itself in language. Reading the pattern back to you is often the first thing '
            f'that quiets the loop.'
        ),
        lambda n, p, dates: (
            f'Number {n} thinks in a particular shape. If you were born on the {dates}, the '
            f'overthinking is not random anxiety, it is <strong>{p}</strong> energy running its '
            f'usual route. The route is worth knowing before you try to redirect it.'
        ),
    ]


def in_love_intros():
    return [
        lambda n, p, dates: (
            f'How a person loves is rarely random. For those born on the {dates} of any month '
            f'(or with Life Path {n}), the love style runs on <strong>{p}</strong> energy, with '
            f'its own warmth, its own friction, and its own kind of devotion.'
        ),
        lambda n, p, dates: (
            f'If you are dating, married to, or quietly wondering about a Number {n}, this page '
            f'describes how <strong>{p}</strong>-led people show up in love. Born on the {dates}, '
            f'or with Life Path {n}, the pattern below tends to feel recognisable on first read.'
        ),
        lambda n, p, dates: (
            f'Every number loves differently. Number {n} loves under <strong>{p}</strong>, which '
            f'shapes everything from what attracts them to how they handle conflict. Whether you '
            f'are the Number {n} or in a relationship with one, the felt signature below is real.'
        ),
        lambda n, p, dates: (
            f'<strong>{p}</strong>-led love has a temperature and a tempo of its own. People '
            f'born on the {dates} (or with Life Path {n}) tend to love with the same signature, '
            f'and the partners who thrive with them learn to read it early.'
        ),
        lambda n, p, dates: (
            f'There is a way that Number {n} people fall, stay, fight, and forgive that is '
            f'unmistakable once you see it named. The pattern below describes <strong>{p}</strong>-led '
            f'love, born from the {dates} of any month or Life Path {n}, plain English, no jargon.'
        ),
    ]


def spiritual_intros():
    return [
        lambda n, p, dates: (
            f'Numerology is often read as a personality system. Look one layer down and every '
            f'number is also a soul path, the felt direction your spirit is travelling in this '
            f'lifetime. Number {n} walks the <strong>{p}</strong>-led path.'
        ),
        lambda n, p, dates: (
            f'Beyond the surface personality reading, your number carries a deeper assignment. '
            f'For Number {n}, that assignment is shaped by <strong>{p}</strong>, with its own '
            f'lesson, its own daily practice, and its own shadow to integrate.'
        ),
        lambda n, p, dates: (
            f'What does it mean that you were born under Number {n}? The everyday reading talks '
            f'about strengths and traits. The deeper reading talks about <strong>{p}</strong>, '
            f'and the specific work your soul came here to do.'
        ),
        lambda n, p, dates: (
            f'If your number-reading has always felt slightly thin, this is the part most '
            f'pop-numerology skips. Number {n} carries a soul path under <strong>{p}</strong>, '
            f'and the path has texture, lesson, practice, and shadow.'
        ),
        lambda n, p, dates: (
            f'A soul path is not a destiny, it is a slope. Number {n} slopes toward the work '
            f'that <strong>{p}</strong> rewards, with the specific lesson, practice, and shadow '
            f'described below.'
        ),
    ]


def lucky_attr_intros():
    return [
        lambda n, p, dates: (
            f'Lucky attributes are not magic, they are tilt. For people born on the {dates}, '
            f'<strong>{p}</strong> rewards certain days, colours, stones and directions more '
            f'than others. Cheiro\'s table has been used by practitioners for over a century.'
        ),
        lambda n, p, dates: (
            f'Which day of the week is luckiest for you? Which gemstone? Which colour to wear '
            f'on important days? For Number {n} people, <strong>{p}</strong> answers each of '
            f'these questions specifically, and the answers have remained consistent across '
            f'Chaldean tradition.'
        ),
        lambda n, p, dates: (
            f'Most of what people call "luck" is really alignment, the small daily choices '
            f'that pull energy in your direction instead of against it. For Number {n}, '
            f'<strong>{p}</strong>-aligned attributes are listed below. Use them where the tilt '
            f'matters; ignore them where it does not.'
        ),
        lambda n, p, dates: (
            f'If you were born on the {dates}, the traditional Chaldean attributes for your '
            f'number all derive from one source, <strong>{p}</strong>. The days, colours, '
            f'gemstones and directions below come from Cheiro\'s framework, unmodified.'
        ),
        lambda n, p, dates: (
            f'Think of these less as superstitions and more as defaults. <strong>{p}</strong> '
            f'rewards Number {n} most on certain weekdays, in certain colours, through certain '
            f'stones. The full list below is honest about which ones matter and which are tilt-only.'
        ),
    ]


# ---------- cluster definitions ----------
CLUSTERS = [
    dict(
        glob='why-number-{n}-overthinks.html',
        intros=overthinking_intros(),
        date_pattern='multi',  # 'Nth, 1Nth, 2Nth'
    ),
    dict(
        glob='number-{n}-in-love.html',
        intros=in_love_intros(),
        date_pattern='single',  # 'Nth'
    ),
    dict(
        glob='number-{n}-spiritual-meaning.html',
        intros=spiritual_intros(),
        date_pattern='none',
    ),
    dict(
        glob='lucky-attributes-number-{n}.html',
        intros=lucky_attr_intros(),
        date_pattern='multi',
    ),
]


# ---------- compatibility pages (29 files) ----------
# Different shape: pair-based. We vary the opening line only.
COMPAT_OPENERS = [
    'Number {a} ({pa}) and Number {b} ({pb}) form what Cheiro called {kind}. This is what that actually feels like in a real relationship.',
    'When a Number {a} meets a Number {b}, two specific planetary signatures, {pa} and {pb}, come into the room. The pattern below describes how the pairing actually behaves.',
    'The {pa}-{pb} pairing (Number {a} with Number {b}) is one of the more {kind_adj} matches in Cheiro\'s system. Strengths, frictions, and long-term arcs are real and worth naming.',
    'How does Number {a} pair with Number {b}? In Chaldean numerology, {pa} meeting {pb} produces a {kind_adj} signature, which is decoded below.',
    'A relationship between a Number {a} and a Number {b} is a meeting of {pa} and {pb}. The way these two planetary energies interact follows a pattern that practitioners have observed for a long time.',
]

KIND_ADJECTIVES = {
    'Strong': 'naturally harmonious',
    'Supportive': 'supportive',
    'Mirror': 'mirror-effect',
    'Heavy': 'karmically weighted',
    'Caution': 'friction-prone',
}


# ---------- the actual rewriter ----------
def rewrite_cluster_page(filepath, n, intros, date_pattern):
    """Replace the first <p>...</p> in <main class="seo-body"> with a varied intro."""
    with open(filepath) as fh:
        c = fh.read()
    planet = PLANETS[n]

    if date_pattern == 'multi':
        dates = date_phrase(n)
    elif date_pattern == 'single':
        dates = ordinal(n)
    else:
        dates = ''

    new_intro = intros[(n - 1) % len(intros)](n, planet, dates)

    # Find the first <p> inside <main class="seo-body"> and replace it.
    m = re.search(r'(<main class="seo-body">\s*)<p>(.*?)</p>', c, re.S)
    if not m:
        return False
    before = m.group(0)
    after = m.group(1) + f'<p>{new_intro}</p>'
    new_c = c.replace(before, after, 1)
    if new_c == c:
        return False
    with open(filepath, 'w') as fh:
        fh.write(new_c)
    return True


def rewrite_compatibility_page(filepath, a, b, opener_template):
    """Replace the first <p><strong>...</strong></p> opener with a varied line."""
    with open(filepath) as fh:
        c = fh.read()
    pa = PLANETS[a]
    pb = PLANETS[b]

    # Read the current rating from the existing badge if possible.
    rating_m = re.search(r'Compatibility verdict: ([A-Za-z]+)', c)
    rating = rating_m.group(1) if rating_m else 'Strong'
    kind_adj = KIND_ADJECTIVES.get(rating, 'a notable')
    kind = {
        'Strong': 'one of the natural triangles',
        'Supportive': 'a supportive harmonic',
        'Mirror': 'the mirror-pair',
        'Heavy': 'one of the heavier karmic combinations',
        'Caution': 'a friction-prone pairing',
    }.get(rating, 'a pairing worth understanding')

    new_intro = opener_template.format(
        a=a, b=b, pa=pa, pb=pb, kind=kind, kind_adj=kind_adj,
    )

    # First paragraph is the <strong>one-liner</strong> wrapped in <p>.
    # We replace it with a plain <p> opener (no <strong>), so the page
    # no longer all-look-the-same with bold first lines.
    m = re.search(r'(<main class="seo-body">\s*)<p><strong>(.*?)</strong></p>', c, re.S)
    if not m:
        return False
    before = m.group(0)
    after = m.group(1) + f'<p>{new_intro}</p>'
    new_c = c.replace(before, after, 1)
    if new_c == c:
        return False
    with open(filepath, 'w') as fh:
        fh.write(new_c)
    return True


# ---------- main ----------
def main():
    total = 0
    for cluster in CLUSTERS:
        for n in range(1, 10):
            filename = cluster['glob'].format(n=n)
            filepath = os.path.join(ROOT, filename)
            if not os.path.exists(filepath):
                continue
            ok = rewrite_cluster_page(filepath, n, cluster['intros'], cluster['date_pattern'])
            if ok:
                total += 1
                print(f'  varied {filename}')

    # Compatibility pages: discover by glob.
    import glob
    compat_files = sorted(glob.glob(os.path.join(ROOT, 'number-*-and-*-compatibility.html')))
    for i, filepath in enumerate(compat_files):
        name = os.path.basename(filepath)
        m = re.match(r'number-(\d+)-and-(\d+)-compatibility\.html', name)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        opener = COMPAT_OPENERS[i % len(COMPAT_OPENERS)]
        ok = rewrite_compatibility_page(filepath, a, b, opener)
        if ok:
            total += 1
            print(f'  varied {name}')

    print(f'\nTotal pages varied: {total}')


if __name__ == '__main__':
    main()
