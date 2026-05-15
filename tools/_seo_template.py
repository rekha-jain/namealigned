#!/usr/bin/env python3
"""
Shared template helpers for programmatic SEO pages.

Used by tools/build-overthinking-pages.py, build-in-love-pages.py, etc.
Centralises:
  - Google Analytics tag
  - Cosmic theme + styling
  - Navigation + breadcrumbs + footer
  - JSON-LD generation for Article / BreadcrumbList / FAQPage

Each builder script supplies a content dict keyed by number 1..9 plus
some category-level metadata, calls render_page() per number, writes
HTML to the repo root.
"""
import json

BASE = 'https://www.namealigned.com'

PLANETS = {
    1: ('Sun',     '☀'),
    2: ('Moon',    '☾'),
    3: ('Jupiter', '♃'),
    4: ('Rahu',    '◈'),
    5: ('Mercury', '☿'),
    6: ('Venus',   '♀'),
    7: ('Ketu',    '☋'),
    8: ('Saturn',  '♄'),
    9: ('Mars',    '♂'),
}

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-70GFTN27M6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-70GFTN27M6');
</script>

<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link rel="icon" type="image/svg+xml" href="/assets/namealigned-favicon.svg"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="keywords" content="{keywords}"/>
<meta name="author" content="NameAligned.com"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<link rel="canonical" href="{canon}"/>
<link rel="alternate" hreflang="en-IN" href="{canon}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{og_desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:site_name" content="NameAligned.com"/>
<meta property="og:locale" content="en_IN"/>
<meta property="og:image" content="{base}/assets/og/moolank-{n}.jpg"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{og_desc}"/>
<meta name="twitter:image" content="{base}/assets/og/moolank-{n}.jpg"/>

<script type="application/ld+json">
{article_json}
</script>
<script type="application/ld+json">
{breadcrumb_json}
</script>
<script type="application/ld+json">
{faq_json}
</script>

<link rel="stylesheet" href="/assets/style.css"/>
<link rel="stylesheet" href="/assets/theme-cosmic-light.css"/>
<style>
.seo-hero{{padding:3.5rem 0 1.75rem;text-align:center;background:linear-gradient(160deg,#1a1340 0%,#2a1a5c 100%);color:#f0ece0;}}
.seo-hero .badge{{display:inline-block;font-family:sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f0b429 !important;background:rgba(240,180,41,.12);padding:5px 14px;border-radius:20px;border:1px solid rgba(240,180,41,.35);margin-bottom:1rem;}}
.seo-hero h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4.2vw,42px);line-height:1.2;margin:0 auto .5rem;max-width:780px;color:#f0ece0 !important;text-shadow:0 2px 24px rgba(124,92,255,.35);}}
.seo-hero .glyph{{font-size:42px;color:#f0b429 !important;line-height:1;margin-bottom:.75rem;}}
.seo-hero .tag{{font-family:sans-serif;font-size:14px;color:rgba(240,236,224,.85) !important;letter-spacing:.04em;max-width:680px;margin:0 auto;line-height:1.5;}}
/* Two-column layout: article + sticky CTA sidebar (matches /blog) */
.seo-wrap{{max-width:1080px;margin:0 auto;padding:0 1.25rem;display:grid;grid-template-columns:1fr 280px;gap:2.5rem;align-items:start;}}
@media(max-width:880px){{.seo-wrap{{grid-template-columns:1fr;gap:0;}}}}
.seo-body{{padding:2rem 0;}}
.seo-aside{{padding-top:2rem;}}
@media(max-width:880px){{.seo-aside{{padding-top:0;margin-bottom:2rem;}}}}
.article-sidebar{{position:sticky;top:90px;background:linear-gradient(135deg,#03090f,#060d18);border-radius:14px;padding:1.5rem;color:#f0ece0;border:1px solid rgba(157,127,255,.18);}}
.article-sidebar .eyebrow{{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#f0b429;font-family:sans-serif;margin-bottom:.6rem;font-weight:600;}}
.article-sidebar h3{{font-family:Georgia,serif;font-size:18px;color:#f0ece0;margin:0 0 .55rem;line-height:1.3;}}
.article-sidebar p{{font-size:13px;color:#b0a898;font-family:sans-serif;line-height:1.6;margin:0 0 1rem;}}
.article-sidebar .price-row{{display:flex;gap:.5rem;align-items:baseline;margin-bottom:1rem;}}
.article-sidebar .price-inr{{font-size:18px;color:#f0b429;font-weight:700;font-family:sans-serif;}}
.article-sidebar .price-usd{{font-size:13px;color:#9d7fff;font-family:sans-serif;}}
.article-sidebar a.cta{{display:block;text-align:center;background:#f0b429;color:#0a0820;font-family:sans-serif;font-size:13.5px;font-weight:700;padding:10px 14px;border-radius:8px;text-decoration:none;transition:background .2s;}}
.article-sidebar a.cta:hover{{background:#f5c247;}}
.article-sidebar a.cta.outline{{background:transparent;color:#cbb8e8;border:1px solid rgba(157,127,255,.35);margin-top:.55rem;}}
.article-sidebar .sep{{height:1px;background:rgba(157,127,255,.15);margin:1.1rem 0;}}
.seo-body h2{{font-family:'Playfair Display',Georgia,serif;font-size:24px;color:var(--text);margin:2rem 0 .65rem;line-height:1.25;}}
.seo-body h3{{font-family:'Playfair Display',Georgia,serif;font-size:18px;color:var(--text);margin:1.5rem 0 .5rem;}}
.seo-body p{{font-family:sans-serif;font-size:14.5px;line-height:1.75;color:var(--text);margin-bottom:1rem;}}
.seo-body ul{{font-family:sans-serif;font-size:14px;line-height:1.85;color:var(--text);padding-left:1.25rem;margin-bottom:1.25rem;}}
.seo-body li{{margin-bottom:.35rem;}}
.seo-body em{{color:var(--gold-d);font-style:italic;}}
.seo-cta-band{{background:var(--gold-l);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.5rem;margin:2rem 0;text-align:center;}}
.seo-cta-band h3{{margin:0 0 .35rem;font-family:Georgia,serif;font-size:19px;color:var(--text);}}
.seo-cta-band p{{margin:0 0 1rem;font-size:13.5px;color:var(--text2);font-family:sans-serif;}}
.seo-cta-band .btn-pair{{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;}}
.seo-cta-band a{{display:inline-block;font-family:sans-serif;font-size:13.5px;font-weight:600;padding:9px 18px;border-radius:8px;text-decoration:none;}}
.seo-cta-band a.primary{{background:var(--gold);color:#0a0820;}}
.seo-cta-band a.primary:hover{{background:#f5c247;}}
.seo-cta-band a.outline{{background:transparent;color:var(--text);border:1.5px solid var(--gold-b);}}
.seo-faq{{margin:2rem 0;}}
.seo-faq details{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem 1.1rem;margin-bottom:.6rem;}}
.seo-faq summary{{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--text);cursor:pointer;line-height:1.4;}}
.seo-faq details[open] summary{{margin-bottom:.5rem;}}
.seo-faq details p{{font-family:sans-serif;font-size:13.5px;line-height:1.7;color:var(--text2);margin:0;}}
.seo-related{{margin:2.5rem 0 1rem;}}
.seo-related-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;}}
@media(max-width:640px){{.seo-related-grid{{grid-template-columns:1fr;}}}}
.seo-rel-card{{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.9rem 1rem;text-decoration:none;color:var(--text);transition:transform .15s ease,box-shadow .15s ease;}}
.seo-rel-card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(201,162,39,.12);}}
.seo-rel-card .eb{{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:.25rem;}}
.seo-rel-card .ti{{font-family:Georgia,serif;font-size:14.5px;font-weight:700;line-height:1.3;}}
nav.crumb{{font-family:sans-serif;font-size:12px;color:var(--text3);padding:1rem 1.25rem 0;max-width:1080px;margin:0 auto;}}
nav.crumb a{{color:var(--text3);text-decoration:none;}}
.seo-tells{{background:rgba(157,127,255,.05);border:1px solid rgba(157,127,255,.18);border-radius:12px;padding:1.25rem 1.5rem;margin:1.5rem 0;}}
.seo-tells h3{{margin:0 0 .65rem;font-family:Georgia,serif;font-size:17px;color:var(--gold-d);}}
.seo-tells ul{{margin:0;padding-left:1.25rem;}}
</style>
</head>
<body>'''

NAV = '''
<nav class="nav">
  <div class="container nav-inner">
    <a href="/" class="nav-logo" aria-label="NameAligned.com" style="font-family:'Playfair Display',Georgia,serif;text-decoration:none;display:inline-flex;flex-direction:column;align-items:stretch;gap:0;line-height:1;">
      <span style="font-size:26px;font-weight:700;color:#0a0820;letter-spacing:-.01em;line-height:1;white-space:nowrap;">Name<span style="color:#6d4ed1;">Aligned</span><span style="color:#6d4ed1;font-weight:600;">.com</span></span>
      <span style="font-family:'Inter','Helvetica Neue',Arial,sans-serif;font-size:9.5px;font-weight:600;color:#8a7ba8;text-transform:uppercase;margin-top:5px;display:flex;justify-content:space-between;width:100%;"><span>C</span><span>H</span><span>A</span><span>L</span><span>D</span><span>E</span><span>A</span><span>N</span><span>&nbsp;</span><span>N</span><span>U</span><span>M</span><span>E</span><span>R</span><span>O</span><span>L</span><span>O</span><span>G</span><span>Y</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="/analyzer">Free Analysis</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/analyzer" class="nav-cta">Try Free →</a></li>
    </ul>
  </div>
</nav>
'''

FOOTER = '''
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div><div class="footer-brand">☽ NameAligned.com</div><p class="footer-tagline">Free Chaldean numerology for everyone.</p></div>
      <div><div class="footer-col-title">Free Tools</div><ul class="footer-links"><li><a href="/name-numerology-calculator">Name Calculator</a></li><li><a href="/name-correction-numerology">Name Correction</a></li><li><a href="/business-name-numerology">Business Name</a></li><li><a href="/love-compatibility-numerology">Love Compatibility</a></li><li><a href="/ask-aura">Ask Aura</a></li><li><a href="/report">Full Report INR 499 · $5 USD</a></li></ul></div>
      <div><div class="footer-col-title">Guides</div><ul class="footer-links"><li><a href="/blog/chaldean-numerology-guide">Chaldean Guide</a></li><li><a href="/blog/moolank-meanings">Birth Number Meanings</a></li><li><a href="/blog/personal-year-guide">Personal Year</a></li><li><a href="/blog/name-correction-guide">Name Correction</a></li><li><a href="/blog/compound-numbers-cheiro">Compound Numbers</a></li><li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid</a></li></ul></div>
      <div><div class="footer-col-title">More</div><ul class="footer-links"><li><a href="/blog">All Articles</a></li><li><a href="/about">About</a></li><li><a href="/sitemap-pages">Site Map</a></li><li><a href="/privacy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/refund">Refund</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 NameAligned.com</span><span>Made with <span style="color:#e8526b;">❤</span> in India</span></div>
  </div>
</footer>
</body>
</html>
'''


def jsonld(article_dict, breadcrumb_dict, faq_dict):
    return (
        json.dumps(article_dict, ensure_ascii=False),
        json.dumps(breadcrumb_dict, ensure_ascii=False),
        json.dumps(faq_dict, ensure_ascii=False),
    )


def make_article(title, desc, canon, date_pub='2026-05-15', date_mod='2026-05-15'):
    return {
        "@context": "https://schema.org", "@type": "Article", "headline": title,
        "description": desc, "url": canon, "datePublished": date_pub, "dateModified": date_mod,
        "author": {"@type": "Organization", "name": "NameAligned.com", "url": BASE + "/"},
        "publisher": {"@type": "Organization", "name": "NameAligned.com", "url": BASE + "/",
                      "logo": {"@type": "ImageObject", "url": BASE + "/assets/namealigned-logo-full.svg"}},
        "inLanguage": "en-IN",
        "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
    }


def make_breadcrumb(crumb_label, canon):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Numerology Guides", "item": BASE + "/sitemap-pages"},
        {"@type": "ListItem", "position": 3, "name": crumb_label, "item": canon},
    ]}


def make_faq(qa_pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in qa_pairs
    ]}


def render_page(
    *,
    n,
    title,
    desc,
    og_desc,
    canon,
    crumb_label,
    keywords,
    hero_badge,
    hero_h1,
    hero_tag,
    body_html,
    faqs,
    related_links,
    cta_block_html=None,
):
    """
    Generic page renderer. Keys are explicit so callers can't accidentally
    mix arguments. `body_html` is fully-rendered HTML for the main article
    body (between the hero and the FAQ).
    `related_links` is a list of (eyebrow, title, href) tuples.
    """
    planet, glyph = PLANETS[n]
    article = make_article(title, desc, canon)
    breadcrumb = make_breadcrumb(crumb_label, canon)
    faq_dict = make_faq(faqs)
    aj, bj, fj = jsonld(article, breadcrumb, faq_dict)

    head = HEAD.format(
        n=n, title=title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        keywords=keywords,
        article_json=aj, breadcrumb_json=bj, faq_json=fj,
    )

    faq_html = '\n'.join(
        f'    <details><summary>{q}</summary><p>{a}</p></details>'
        for q, a in faqs
    )

    related_html = '\n'.join(
        f'    <a href="{href}" class="seo-rel-card"><span class="eb">{eyebrow}</span><span class="ti">{ti}</span></a>'
        for (eyebrow, ti, href) in related_links
    )

    cta = cta_block_html or f'''
<div class="seo-cta-band">
  <h3>See your own full Chaldean pattern in 10 seconds</h3>
  <p>Free analysis · No signup. Or unlock the full destiny report for <strong>INR 499 · $5 USD</strong>.</p>
  <div class="btn-pair">
    <a href="/analyzer" class="primary">Free Analysis →</a>
    <a href="/report" class="outline">Full Report INR 499 · $5</a>
    <a href="/ask-aura" class="outline">Ask Aura</a>
  </div>
</div>
'''

    # Sticky right-rail CTA, matches /blog style. Sits next to the article on
    # desktop, stacks above the article on mobile.
    sidebar = f'''
  <aside class="seo-aside">
    <div class="article-sidebar">
      <div class="eyebrow">Free Analysis</div>
      <h3>Decode your full chart</h3>
      <p>Moolank, Bhagyank, name number, lucky stones, compatibility map. 10 seconds, no signup.</p>
      <a href="/analyzer" class="cta">Start free →</a>
      <a href="/ask-aura" class="cta outline">✦ Ask Aura</a>
      <div class="sep"></div>
      <div class="eyebrow">Full Destiny Report</div>
      <h3>Your personalised PDF</h3>
      <div class="price-row">
        <span class="price-inr">INR 499</span>
        <span class="price-usd">or $5 USD</span>
      </div>
      <p>5-year forecast, name corrections, remedies, compatibility, mobile-number check.</p>
      <a href="/report" class="cta">Get the report →</a>
    </div>
  </aside>
'''

    page = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/sitemap-pages">Numerology Guides</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">{crumb_label}</span>
</nav>

<header class="seo-hero">
  <div class="container">
    <div class="badge">{hero_badge}</div>
    <div class="glyph">{glyph}</div>
    <h1>{hero_h1}</h1>
    <div class="tag">{hero_tag}</div>
  </div>
</header>

<div class="seo-wrap">

  <main class="seo-body">

{body_html}

{cta}

    <h2>Frequently asked</h2>
    <div class="seo-faq">
{faq_html}
    </div>

    <section class="seo-related">
      <h2>Continue exploring</h2>
      <div class="seo-related-grid">
{related_html}
      </div>
    </section>

  </main>

{sidebar}

</div>

{FOOTER}
'''

    return head + page
