#!/usr/bin/env python3
"""
Second-pass anti-template SEO sweep across long-tail pages.

After yesterday's intro variation (5 voices per cluster), the next layer of
"AI-template" signal lives in:
  1. Identical H2 headings across cluster siblings
  2. Repeated CTA-block headings and copy
  3. Template phrases that repeat across hundreds of pages
     ("in plain English", "the natural slope", "the seeker")

This script applies deterministic variation by page-number for cluster pages
(so the same page always gets the same variant on re-crawls) and rotating
copy for shared blocks like the inline CTA.

Same 600-800 word substantive body content stays intact; only the recurring
labels and tics change.

Run:
  python3 tools/destemplate-seo.py
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------- H2 heading pools per cluster ----------
# Five variants each, indexed by (n - 1) % 5.

OVERTHINK_H2_VARIANTS = {
    'pattern_h2': [
        'Where {planet}-driven minds get stuck',
        'How the loop actually shows up',
        'The shape this kind of thinking takes',
        'What overthinking looks like under {planet}',
        'The {planet} mental signature',
    ],
    'quiet_h2': [
        'What actually settles the loop',
        'Ways to soften the mental tightness',
        'How {planet} minds find relief',
        'Working with the pattern instead of against it',
        'When the loop loosens',
    ],
    'final_h2': [
        'When the same trait becomes useful',
        'The other side of Number {n} thinking',
        'Why Number {n} should not try to switch this off',
        'The hidden gift inside the overthinking',
        'How this mind serves you',
    ],
}

LOVE_H2_VARIANTS = {
    'how_h2': [
        'The shape of {planet}-led love',
        'Inside the love style of Number {n}',
        'How a Number {n} actually shows up',
        'The signature of Number {n} in a relationship',
        'How love works for a {planet} person',
    ],
    'attract_h2': [
        'Who Number {n} reaches for',
        'The kind of partner Number {n} chooses',
        'What pulls Number {n} in',
        'Who Number {n} cannot quite walk past',
        'The pull behind their attractions',
    ],
    'shadow_h2': [
        'Where this love style trips up',
        'The version that does not work',
        'How this love hurts when it hurts',
        'The hard part of being with a Number {n}',
        'When this love goes sideways',
    ],
    'longterm_h2': [
        'How this pairing ages over years',
        'The long arc of Number {n} love',
        'Number {n} in marriage and beyond',
        'What the years do to this kind of love',
        'Number {n} love after the early years',
    ],
    'compat_h2': [
        'Who fits well with Number {n}',
        'Numbers that pair naturally with {n}',
        'The Number {n} compatibility picture',
        'How Number {n} pairs with each other number',
        'The pairings that work and the ones that test you',
    ],
}

SPIRIT_H2_VARIANTS = {
    'essence_h2': [
        'What this soul came here to do',
        'The shape of the Number {n} journey',
        'The work behind the surface personality',
        'What {planet} asks of Number {n}',
        'The deeper assignment of Number {n}',
    ],
    'lesson_h2': [
        'The work that sits underneath',
        'What this lifetime keeps returning to',
        'The recurring growth edge',
        'The piece Number {n} keeps being shown',
        'What the path is teaching',
    ],
    'practice_h2': [
        'The practices that actually work',
        'What strengthens the path',
        'Where Number {n} should put the daily time',
        'Disciplines that fit this soul shape',
        'How to feed this kind of inner life',
    ],
    'shadow_h2': [
        'How the path goes sideways',
        'When the gift becomes the trap',
        'The version of this that does not heal',
        'The shadow side of the {planet} path',
        'Where Number {n} loses the thread',
    ],
}

LUCKY_H2_VARIANTS = {
    'days_h2': [
        'Days of the week that favour Number {n}',
        'When Number {n} runs best',
        'Weekdays aligned with {planet}',
        'When to do important things if you are Number {n}',
        'The {planet} days',
    ],
    'colors_h2': [
        'Colors {planet} responds to',
        'What to wear, what to avoid',
        'Colors that lift Number {n}',
        'The color palette {planet} prefers',
        'Color choices that help and ones that work against you',
    ],
    'stones_h2': [
        'Stones traditionally worn by Number {n}',
        'Gems for {planet} energy',
        'What gemstones suit this number',
        'The {planet} stones, with practitioner cautions',
        'Traditional gemstone choices',
    ],
}


# ---------- phrase replacements ----------
# Map of recurring phrases to a small pool of alternatives. Chosen
# deterministically per-page by hashing the filename so the same page
# always picks the same alternative on re-runs.

PHRASE_POOLS = {
    'in plain English': [
        'in everyday language',
        'without the jargon',
        'in language that does not need a glossary',
        'in words anyone can use',
        'put simply',
    ],
    'the natural slope': [
        'the natural inclination',
        'the default tilt',
        'the way it tends to lean',
        'the underlying current',
        'the path of least resistance',
    ],
}


# ---------- inline CTA-band variants ----------
# Each entry is (heading_html, paragraph_html). The CTA block sits in
# .seo-cta-band. Five variants rotated by file-hash.

CTA_BAND_VARIANTS = [
    (
        'See your full Chaldean pattern in ten seconds',
        'Free analysis, no signup. Or open the complete destiny report for <strong>INR 499 &middot; $5 USD</strong>.',
    ),
    (
        'Want this read against your own chart?',
        'Plug in your name and date of birth, no signup. Full report (5-year forecast, name corrections, compatibility) is <strong>INR 499 &middot; $5 USD</strong>.',
    ),
    (
        'Curious how this lands for your own number?',
        'Run a free Chaldean check, takes a few seconds. The full personalised destiny report is <strong>INR 499 &middot; $5 USD</strong>.',
    ),
    (
        'Read your own number the same way',
        'Free pattern check in seconds. The deeper personalised report, with name corrections and 5-year forecast, is <strong>INR 499 &middot; $5 USD</strong>.',
    ),
    (
        'Take this further with your own details',
        'Quick free analysis on your name and birth date. Full destiny report (compatibility, remedies, forecast) is <strong>INR 499 &middot; $5 USD</strong>.',
    ),
]


# ---------- cluster definitions ----------
def replace_overthinking_h2s(html, n, planet):
    i = (n - 1) % 5
    return (
        html
        .replace(
            'The ' + planet + '-led overthinking pattern',
            OVERTHINK_H2_VARIANTS['pattern_h2'][i].format(planet=planet),
        )
        .replace(
            'How to quiet it (without trying to think less)',
            OVERTHINK_H2_VARIANTS['quiet_h2'][i].format(planet=planet),
        )
        .replace(
            f'Is overthinking always bad for Number {n}?',
            OVERTHINK_H2_VARIANTS['final_h2'][i].format(n=n),
        )
    )


def replace_love_h2s(html, n, planet):
    i = (n - 1) % 5
    return (
        html
        .replace(f'How Number {n} loves', LOVE_H2_VARIANTS['how_h2'][i].format(n=n, planet=planet))
        .replace(f'What attracts Number {n}', LOVE_H2_VARIANTS['attract_h2'][i].format(n=n))
        .replace('The shadow side', LOVE_H2_VARIANTS['shadow_h2'][i].format(n=n))
        .replace(f'What Number {n} long-term love looks like', LOVE_H2_VARIANTS['longterm_h2'][i].format(n=n))
        .replace(f'Compatibility map for Number {n}', LOVE_H2_VARIANTS['compat_h2'][i].format(n=n))
    )


def replace_spiritual_h2s(html, n, planet):
    i = (n - 1) % 5
    return (
        html
        .replace('The essence of the ' + planet + '-led path', SPIRIT_H2_VARIANTS['essence_h2'][i].format(n=n, planet=planet))
        .replace('The spiritual lesson', SPIRIT_H2_VARIANTS['lesson_h2'][i].format(n=n))
        .replace(f'How Number {n} grows spiritually', SPIRIT_H2_VARIANTS['practice_h2'][i].format(n=n, planet=planet))
        .replace(f'The spiritual shadow of Number {n}', SPIRIT_H2_VARIANTS['shadow_h2'][i].format(n=n, planet=planet))
    )


def replace_lucky_h2s(html, n, planet):
    i = (n - 1) % 5
    return (
        html
        .replace(f'Lucky days for Number {n}', LUCKY_H2_VARIANTS['days_h2'][i].format(n=n, planet=planet))
        .replace('Lucky colors', LUCKY_H2_VARIANTS['colors_h2'][i].format(n=n, planet=planet))
        .replace('Lucky gemstones', LUCKY_H2_VARIANTS['stones_h2'][i].format(n=n, planet=planet))
    )


# ---------- phrase replacements per-file ----------
def hash_index(filename, pool_size):
    """Deterministic small int from filename hash."""
    return sum(ord(c) for c in filename) % pool_size


def replace_phrases(html, filename):
    for original, pool in PHRASE_POOLS.items():
        if original in html:
            idx = hash_index(filename + original, len(pool))
            html = html.replace(original, pool[idx])
    return html


# ---------- CTA band variation ----------
CTA_BAND_RE = re.compile(
    r'<div class="seo-cta-band">\s*'
    r'<h3>[^<]*</h3>\s*'
    r'<p>[^<]*(?:<strong>[^<]*</strong>[^<]*)*</p>',
    re.S,
)


def replace_cta_band(html, filename):
    idx = hash_index(filename + 'cta', len(CTA_BAND_VARIANTS))
    heading, paragraph = CTA_BAND_VARIANTS[idx]
    new_block = (
        '<div class="seo-cta-band">\n'
        f'  <h3>{heading}</h3>\n'
        f'  <p>{paragraph}</p>'
    )
    return CTA_BAND_RE.sub(new_block, html, count=1)


# ---------- planet lookup ----------
PLANETS = {1:'Sun',2:'Moon',3:'Jupiter',4:'Rahu',5:'Mercury',6:'Venus',7:'Ketu',8:'Saturn',9:'Mars'}


# ---------- main ----------
def process_file(path, n, planet, h2_replacer=None):
    with open(path) as fh: c = fh.read()
    orig = c
    if h2_replacer:
        c = h2_replacer(c, n, planet)
    c = replace_phrases(c, os.path.basename(path))
    c = replace_cta_band(c, os.path.basename(path))
    if c != orig:
        with open(path, 'w') as fh: fh.write(c)
        return True
    return False


def main():
    total = 0
    clusters = [
        ('why-number-{n}-overthinks.html',       replace_overthinking_h2s),
        ('number-{n}-in-love.html',              replace_love_h2s),
        ('number-{n}-spiritual-meaning.html',    replace_spiritual_h2s),
        ('lucky-attributes-number-{n}.html',     replace_lucky_h2s),
    ]
    for tpl, h2_fn in clusters:
        for n in range(1, 10):
            fp = os.path.join(ROOT, tpl.format(n=n))
            if not os.path.exists(fp): continue
            if process_file(fp, n, PLANETS[n], h2_fn):
                total += 1
                print(f'  updated {os.path.basename(fp)}')

    # Compatibility pages: no per-page h2 swap (their h2s are already
    # pair-specific), just phrase + CTA variation.
    compat_files = sorted(glob.glob(os.path.join(ROOT, 'number-*-and-*-compatibility.html')))
    for fp in compat_files:
        name = os.path.basename(fp)
        m = re.match(r'number-(\d+)-and-(\d+)-compatibility\.html', name)
        if not m: continue
        a = int(m.group(1))
        if process_file(fp, a, PLANETS[a], None):
            total += 1
            print(f'  updated {name}')

    # Life-path + name-number + number/N-personality/career pages: built
    # from older templates with their own H2s + CTA blocks. Their hardest
    # template signal is the "the natural slope" closer line on the career
    # section, repeated word-for-word across 36 pages. Phrase replacement
    # reaches it.
    older_glob = (
        glob.glob(os.path.join(ROOT, 'life-path-number-*-meaning.html')) +
        glob.glob(os.path.join(ROOT, 'name-number-*-meaning.html')) +
        glob.glob(os.path.join(ROOT, 'number', '*-personality.html')) +
        glob.glob(os.path.join(ROOT, 'number', '*-career.html'))
    )
    for fp in sorted(older_glob):
        name = os.path.basename(fp)
        # Match a single digit anywhere in the filename: 5-personality.html,
        # life-path-number-3-meaning.html, name-number-8-meaning.html.
        m = re.search(r'(\d)', name)
        if not m: continue
        n = int(m.group(1))
        with open(fp) as fh: orig = fh.read()
        c = replace_phrases(orig, name)
        if c != orig:
            with open(fp, 'w') as fh: fh.write(c)
            total += 1
            print(f'  updated {name}')

    print(f'\nDe-templated {total} pages.')


if __name__ == '__main__':
    main()
