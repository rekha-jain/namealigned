#!/usr/bin/env python3
"""
Cross-link the six emotional-pattern pages from the archetype hub, the nine
archetype pages, and each other. These pages had only 1-2 internal inbound
links, which left them in "Crawled - currently not indexed".

Idempotent: the block lives between markers and is replaced on rerun.
Rerun after build-emotional-cluster.py or build-archetype-pages.py.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = '<!-- NA_EMOTIONAL_PATTERNS_START -->'
END = '<!-- NA_EMOTIONAL_PATTERNS_END -->'

PATTERNS = [
    ('why-some-people-emotionally-withdraw', 'Why some people emotionally withdraw when they care most'),
    ('reassurance-needs-in-relationships', 'Reassurance needs in relationships'),
    ('emotional-communication-styles', 'Emotional communication styles'),
    ('why-some-people-feel-too-much', 'Why some people feel too much'),
    ('the-emotionally-analytical-personality', 'The emotionally analytical personality'),
    ('conflict-styles-in-emotional-relationships', 'Conflict styles in emotional relationships'),
]


def block(self_slug):
    cards = '\n'.join(
        f'        <a href="/{slug}" class="seo-rel-card" data-na-event="related_insight_clicked" '
        f'data-na-params=\'{{"to_page":"{slug}","from_page":"{self_slug}"}}\'>'
        f'<span class="eb">Emotional Pattern</span><span class="ti">{title}</span></a>'
        for slug, title in PATTERNS if slug != self_slug
    )
    return f'''{START}
    <section class="seo-related">
      <h2>Emotional patterns</h2>
      <div class="seo-related-grid">
{cards}
      </div>
    </section>
{END}
'''


def main():
    files = ['emotional-archetypes.html']
    files += sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'emotional-archetype-*.html')))
    files += [f'{slug}.html' for slug, _ in PATTERNS]
    pat = re.compile(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', re.S)
    for name in files:
        path = os.path.join(ROOT, name)
        html = open(path, encoding='utf-8').read()
        html = pat.sub('', html)
        if html.count('</main>') != 1:
            print(f'skip {name}: expected one </main>')
            continue
        html = html.replace('  </main>', block(name[:-5]) + '  </main>', 1) if '  </main>' in html \
            else html.replace('</main>', block(name[:-5]) + '</main>', 1)
        open(path, 'w', encoding='utf-8').write(html)
        print(f'linked {name}')


if __name__ == '__main__':
    main()
