#!/usr/bin/env python3
"""
Inject the new emotional engagement layer into existing long-tail and
number pages:

  - <link rel="stylesheet" href="/assets/emotional-insights.css">
  - <script src="/assets/emotional-insights.js" defer></script>
  - <script src="/assets/share-helpers.js" defer></script>
  - Insight strip after first <p> in main body
  - Share strip after the inline CTA band
  - "You may also relate to" emotional-archetype block before related-links
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLANETS = {1:'Sun',2:'Moon',3:'Jupiter',4:'Rahu',5:'Mercury',6:'Venus',7:'Ketu',8:'Saturn',9:'Mars'}

# Map birth number to emotional archetype slug.
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
    """Add emotional-insights.css + helpers JS if not present."""
    changed = False
    if 'emotional-insights.css' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="/assets/style.css"/>',
            '<link rel="stylesheet" href="/assets/style.css"/>\n<link rel="stylesheet" href="/assets/emotional-insights.css"/>',
            1
        )
        changed = True
    # Add script tags right before </body>.
    needed = []
    if 'emotional-insights.js' not in html: needed.append('emotional-insights.js')
    if 'share-helpers.js' not in html:      needed.append('share-helpers.js')
    if needed:
        tags = '\n'.join(f'<script src="/assets/{f}" defer></script>' for f in needed)
        html = html.replace('</body>', tags + '\n</body>', 1)
        changed = True
    return html, changed


def inject_insight_strip(html, n):
    """Insert an insight strip after first <p> in <main class="seo-body">."""
    if 'emotional-insights" data-number' in html:
        return html, False  # already injected
    strip = f'\n  <div class="emotional-insights emotional-insights-strip" data-number="{n}" data-count="2"></div>\n'
    # Find the first <p>...</p> inside the seo-body and append the strip after it.
    m = re.search(r'(<main class="seo-body">\s*<p>.*?</p>)', html, re.S)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + strip, 1), True


def inject_share_strip(html, n, planet, slug_or_title):
    """Insert a share strip after the inline .seo-cta-band block."""
    if 'data-share-source="long-tail"' in html:
        return html, False
    archetype_slug, archetype_name = N_TO_ARCHETYPE[n]
    headline = 'Send this to someone who is a Number ' + str(n).strip()
    prompt   = 'Ask them which lines feel like home, and which felt called out.'
    share_text = 'A Number ' + str(n) + ' reading that hit, read it and tell me which parts you recognise:'
    block = (
        '\n<div class="share-strip"\n'
        f'     data-share-source="long-tail"\n'
        f'     data-emotion-headline="{headline}"\n'
        f'     data-emotion-prompt="{prompt}"\n'
        f'     data-share-text="{share_text}"></div>\n'
    )
    # Place it AFTER the inline CTA-band.
    m = re.search(r'(<div class="seo-cta-band">.*?</div>\s*</div>)', html, re.S)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + block, 1), True


def inject_archetype_link(html, n):
    """Add an 'You may also relate to' archetype link inside the related-grid."""
    if 'emotional-archetype-' in html:
        return html, False
    slug, name = N_TO_ARCHETYPE[n]
    card = (
        f'\n      <a href="/emotional-archetype-{slug}" class="seo-rel-card" data-na-event="archetype_viewed" data-na-params=\'{{"archetype":"{slug}","number":{n}}}\'>'
        f'<span class="eb">Emotional Archetype</span><span class="ti">{name}, the deeper read for Number {n}</span></a>'
    )
    # Inject right after the opening of <div class="seo-related-grid">.
    m = re.search(r'(<div class="seo-related-grid">)', html)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + card, 1), True


def process_file(filepath, n):
    with open(filepath) as fh: html = fh.read()
    original = html
    html, _ = add_assets_links(html)
    html, _ = inject_insight_strip(html, n)
    html, _ = inject_share_strip(html, n, PLANETS[n], None)
    html, _ = inject_archetype_link(html, n)
    if html != original:
        with open(filepath, 'w') as fh: fh.write(html)
        return True
    return False


def main():
    targets = []
    # All long-tail single-number clusters.
    for n in range(1, 10):
        for tmpl in (
            'why-number-{n}-overthinks.html',
            'number-{n}-in-love.html',
            'number-{n}-spiritual-meaning.html',
            'lucky-attributes-number-{n}.html',
            'life-path-number-{n}-meaning.html',
            'name-number-{n}-meaning.html',
        ):
            f = os.path.join(ROOT, tmpl.format(n=n))
            if os.path.exists(f):
                targets.append((f, n))

    total = 0
    for fp, n in targets:
        if process_file(fp, n):
            total += 1
            print(f'  injected {os.path.basename(fp)}')
    print(f'\nInjected emotional layer into {total} pages.')


if __name__ == '__main__':
    main()
