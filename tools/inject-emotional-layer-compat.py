#!/usr/bin/env python3
"""
Inject the emotional layer into all 29 compatibility pair pages:
  - emotional-insights.css link in head
  - emotional-insights.js + share-helpers.js scripts at body end
  - Pair-insight strip after first paragraph in main body
  - Share strip after the inline CTA-band, with pair-specific copy
  - "You may also relate to" archetype cross-links for BOTH numbers
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLANETS = {1:'Sun',2:'Moon',3:'Jupiter',4:'Rahu',5:'Mercury',6:'Venus',7:'Ketu',8:'Saturn',9:'Mars'}

N_TO_ARCHETYPE = {
    1: ('the-inner-sovereign', 'The Inner Sovereign'),
    2: ('the-mirror', 'The Mirror'),
    3: ('the-translator', 'The Translator'),
    4: ('the-quiet-disruptor', 'The Quiet Disruptor'),
    5: ('the-restless-mind', 'The Restless Mind'),
    6: ('the-devoted-beautifier', 'The Devoted Beautifier'),
    7: ('the-inward-witness', 'The Inward Witness'),
    8: ('the-patient-builder', 'The Patient Builder'),
    9: ('the-protector', 'The Protector'),
}


def add_assets_links(html):
    changed = False
    if 'emotional-insights.css' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="/assets/style.css"/>',
            '<link rel="stylesheet" href="/assets/style.css"/>\n<link rel="stylesheet" href="/assets/emotional-insights.css"/>',
            1
        )
        changed = True
    needed = []
    if 'emotional-insights.js' not in html: needed.append('emotional-insights.js')
    if 'share-helpers.js' not in html:      needed.append('share-helpers.js')
    if needed:
        tags = '\n'.join(f'<script src="/assets/{f}" defer></script>' for f in needed)
        html = html.replace('</body>', tags + '\n</body>', 1)
        changed = True
    return html, changed


def inject_pair_insight_strip(html, a, b):
    """Insert a pair-insight strip after first <p> in main body."""
    if 'emotional-pair-insights' in html:
        return html, False
    strip = f'\n  <div class="emotional-pair-insights emotional-insights-strip" data-pair="{a}-{b}"></div>\n'
    m = re.search(r'(<main class="seo-body">\s*<p>.*?</p>)', html, re.S)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + strip, 1), True


def inject_pair_share_strip(html, a, b, pa, pb):
    """Insert a share strip after the inline CTA-band, with pair-specific copy."""
    if 'data-share-source="compat-pair"' in html:
        return html, False
    headline = f'Send this to the person you are wondering about.'
    prompt   = f'Ask them which lines hit. The conversation that follows is usually more useful than the reading.'
    share_text = f'Number {a} ({pa}) and Number {b} ({pb}) compatibility, read it and tell me which parts you recognise:'
    block = (
        '\n<div class="share-strip"\n'
        f'     data-share-source="compat-pair"\n'
        f'     data-emotion-headline="{headline}"\n'
        f'     data-emotion-prompt="{prompt}"\n'
        f'     data-share-text="{share_text}"></div>\n'
    )
    m = re.search(r'(<div class="seo-cta-band">.*?</div>\s*</div>)', html, re.S)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + block, 1), True


def inject_archetype_links(html, a, b):
    """Add 'archetype' cross-links for BOTH numbers inside related-grid."""
    if 'emotional-archetype-' in html:
        return html, False
    slug_a, name_a = N_TO_ARCHETYPE[a]
    slug_b, name_b = N_TO_ARCHETYPE[b] if b != a else (None, None)
    cards = (
        f'\n      <a href="/emotional-archetype-{slug_a}" class="seo-rel-card" data-na-event="archetype_viewed" data-na-params=\'{{"archetype":"{slug_a}","number":{a},"from":"compat-{a}-{b}"}}\'>'
        f'<span class="eb">Their archetype</span><span class="ti">{name_a}, the deeper read for Number {a}</span></a>'
    )
    if slug_b and slug_b != slug_a:
        cards += (
            f'\n      <a href="/emotional-archetype-{slug_b}" class="seo-rel-card" data-na-event="archetype_viewed" data-na-params=\'{{"archetype":"{slug_b}","number":{b},"from":"compat-{a}-{b}"}}\'>'
            f'<span class="eb">Their archetype</span><span class="ti">{name_b}, the deeper read for Number {b}</span></a>'
        )
    m = re.search(r'(<div class="seo-related-grid">)', html)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + cards, 1), True


def process_file(filepath, a, b):
    with open(filepath) as fh: html = fh.read()
    orig = html
    html, _ = add_assets_links(html)
    html, _ = inject_pair_insight_strip(html, a, b)
    html, _ = inject_pair_share_strip(html, a, b, PLANETS[a], PLANETS[b])
    html, _ = inject_archetype_links(html, a, b)
    if html != orig:
        with open(filepath, 'w') as fh: fh.write(html)
        return True
    return False


def main():
    files = sorted(glob.glob(os.path.join(ROOT, 'number-*-and-*-compatibility.html')))
    total = 0
    for fp in files:
        name = os.path.basename(fp)
        m = re.match(r'number-(\d+)-and-(\d+)-compatibility\.html', name)
        if not m: continue
        a, b = int(m.group(1)), int(m.group(2))
        if process_file(fp, a, b):
            total += 1
            print(f'  injected {name}')
    print(f'\nInjected emotional layer into {total} compatibility pages.')


if __name__ == '__main__':
    main()
