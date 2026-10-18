#!/usr/bin/env python3
"""
Build the on-brand SEO pages (birthday numbers, personal year, master
numbers, karmic debt, house numbers) from JSON content files.

    python3 tools/build-onbrand-pages.py

Content lives in tools/content/onbrand/<slug>.json. Shared chrome (styles,
nav, footer) is copied from life-path-number-3-meaning.html into
tools/content/onbrand/_*.html so generated pages match the site.

JSON fields:
  slug, title, description, keywords, badge, glyph, h1, tag, crumb,
  intro (html string), stats [{lbl,val}] (3), sections [{h2, html}],
  faq [{q,a}], related_title, related [{href, eb, ti}],
  calculator (optional html, inserted after intro), og_image (optional)
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'content', 'onbrand')
SITE = 'https://www.namealigned.com'
V = '20261018'


def part(name):
    return open(os.path.join(SRC, name), encoding='utf-8').read()


STYLE, NAV, FOOTER = part('_style.html'), part('_nav.html'), part('_footer.html')
DASHES = re.compile('[–—]')


def esc(s):
    return html.escape(s, quote=True)


def page(d):
    url = f"{SITE}/{d['slug']}"
    og = d.get("og_image") or f"{SITE}/assets/og/moolank-1.jpg"
    article = {
        '@context': 'https://schema.org', '@type': 'Article',
        'headline': d['h1'], 'description': d['description'],
        'author': {'@type': 'Organization', 'name': 'NameAligned.com'},
        'publisher': {'@type': 'Organization', 'name': 'NameAligned.com'},
        'mainEntityOfPage': url, 'datePublished': '2026-10-18', 'dateModified': '2026-10-18',
    }
    crumbs = {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE}/'},
            *([{'@type': 'ListItem', 'position': 2, 'name': d['crumb_parent']['name'],
                'item': f"{SITE}{d['crumb_parent']['href']}"}] if d.get('crumb_parent') else []),
            {'@type': 'ListItem', 'position': 3 if d.get('crumb_parent') else 2,
             'name': d['crumb'], 'item': url},
        ],
    }
    faq = {
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': f['q'],
                        'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in d['faq']],
    }
    stats = ''.join(f'<div class="nn-stat"><div class="lbl">{esc(s["lbl"])}</div><div class="val">{esc(s["val"])}</div></div>'
                    for s in d['stats'])
    sections = '\n'.join(f'  <h2>{esc(s["h2"])}</h2>\n  {s["html"]}' for s in d['sections'])
    faqs = '\n'.join(f'    <details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for f in d['faq'])
    related = '\n'.join(f'    <a href="{r["href"]}" class="nn-rel-card"><span class="eb">{esc(r["eb"])}</span><span class="ti">{esc(r["ti"])}</span></a>'
                        for r in d['related'])
    parent = (f'<a href="{d["crumb_parent"]["href"]}">{esc(d["crumb_parent"]["name"])}</a> <span style="margin:0 8px;">›</span>\n  '
              if d.get('crumb_parent') else '')
    calc = d.get('calculator', '')
    extra_js = d.get('script', '')

    return f'''<!DOCTYPE html><html lang="en"><head>
<!-- Google tag (gtag.js) -->
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-70GFTN27M6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-70GFTN27M6');
</script>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="icon" type="image/svg+xml" href="/assets/namealigned-favicon.svg">
<title>{esc(d['title'])}</title>
<meta name="description" content="{esc(d['description'])}">
<meta name="keywords" content="{esc(d['keywords'])}">
<meta name="author" content="NameAligned.com">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(d['title'])}">
<meta property="og:description" content="{esc(d['description'])}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="NameAligned.com">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(d['title'])}">
<meta name="twitter:description" content="{esc(d['description'])}">
<meta name="twitter:image" content="{og}">

<script type="application/ld+json">
{json.dumps(article, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(crumbs, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq, ensure_ascii=False)}
</script>

<link rel="stylesheet" href="/assets/style.css?v={V}">
<link rel="stylesheet" href="/assets/theme-cosmic-light.css?v={V}">
{STYLE}
<style>
.nn-calc{{background:var(--card);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.25rem;margin:1.5rem 0;font-family:sans-serif}}
.nn-calc label{{display:block;font-size:13px;color:var(--text2);margin-bottom:.35rem}}
.nn-calc .row{{display:flex;gap:.5rem;flex-wrap:wrap}}
.nn-calc input{{flex:1 1 180px;padding:.65rem .8rem;border-radius:10px;border:1px solid var(--gold-b);font-size:15px}}
.nn-calc button{{padding:.65rem 1.2rem;border:0;border-radius:999px;background:var(--gold);color:#0a0820;font-weight:700;cursor:pointer}}
.nn-calc .out{{margin-top:.9rem;font-size:15px;line-height:1.6;color:var(--text)}}
.nn-hub-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.6rem;margin:1rem 0 1.5rem}}
.nn-hub-grid a{{display:block;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.7rem .8rem;text-decoration:none;color:var(--text);font-family:sans-serif;font-size:13.5px}}
.nn-hub-grid a strong{{display:block;font-family:Georgia,serif;font-size:16px}}
</style>
</head>
<body>

{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  {parent}<span style="color:var(--text2);">{esc(d['crumb'])}</span>
</nav>

<header class="nn-hero">
  <div class="container">
    <div class="badge">{esc(d['badge'])}</div>
    <div class="glyph">{esc(d['glyph'])}</div>
    <h1>{esc(d['h1'])}</h1>
    <div class="tag">{esc(d['tag'])}</div>
  </div>
</header>

<main class="nn-body">

  {d['intro']}

  <div class="nn-stat-row">
    {stats}
  </div>
{calc}
{sections}

  <div class="nn-cta-band">
    <h3>See all your numbers in 15 seconds</h3>
    <p>Free Chaldean analysis: Birth Number, Life Path Number, Name Number and an alignment score. No signup.</p>
    <div class="btn-pair">
      <a class="primary" href="/analyzer">Run my free analysis →</a>
      <a class="outline" href="/name-numerology-calculator">Just calculate my name number</a>
    </div>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="nn-faq">
{faqs}
  </div>

  <div class="nn-cta-band">
    <h3>Want the complete picture?</h3>
    <p>The personalised destiny report covers your Birth Number, Life Path Number, Name Number, name correction options, 5-year forecast and compatibility, in one PDF.</p>
    <div class="btn-pair">
      <a class="primary" href="/report">Full Destiny Report · 50% off</a>
      <a class="outline" href="/blog/chaldean-numerology-guide">Read the Chaldean guide</a>
    </div>
  </div>

  <h2>{esc(d.get('related_title', 'Related reading'))}</h2>
  <div class="nn-related">
    <div class="nn-related-grid">
{related}
    </div>
  </div>

</main>

{FOOTER}
<script src="/assets/numerology.js?v={V}"></script>
{extra_js}
<script src="/assets/aura-fab.js?v={V}" defer></script>
<script src="/assets/sticky-ad.js?v={V}" defer></script>
<script src="/assets/nav-mobile.js?v={V}" defer></script>
</body></html>
'''


def main():
    files = sorted(f for f in glob.glob(os.path.join(SRC, '*.json')))
    if not files:
        sys.exit('no content files')
    bad = 0
    for f in files:
        d = json.load(open(f, encoding='utf-8'))
        out = page(d)
        if DASHES.search(out):
            print(f'!! en/em dash in {os.path.basename(f)}'); bad += 1
        words = len(re.sub(r'<[^>]+>', ' ', d['intro'] + ' '.join(s['html'] for s in d['sections'])).split())
        open(os.path.join(ROOT, d['slug'] + '.html'), 'w', encoding='utf-8').write(out)
        print(f"{d['slug']:45s} {words:5d} words")
    print(f'{len(files)} pages built' + (f', {bad} with dashes' if bad else ''))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
