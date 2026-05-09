#!/usr/bin/env python3
"""
Generate the /number/ hub index page.

This is the landing page for the entire /number/ cluster. It:
- Educates: what a number means in Chaldean numerology, the four
  kinds (Birth, Name, Destiny, Life Path) and how they differ.
- Lists all 9 numbers with every aspect page that currently exists
  for them (personality, career, plus the existing root-level
  /name-number-N-meaning and /life-path-N-meaning pages).
- Auto-grows: when /number/{n}-love and /number/{n}-compatibility
  ship, just add them to ASPECTS and re-run.

Run:
    python3 tools/build-number-index.py

Output: number/index.html (served at /number/ via Vercel cleanUrls)
"""
import json, os, re, importlib.util

BASE = 'https://www.namealigned.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'number', 'index.html')

# Reuse data: planet, glyph, tagline + archetype
spec = importlib.util.spec_from_file_location('nnp', os.path.join(ROOT, 'tools', 'build-name-number-pages.py'))
nnp = importlib.util.module_from_spec(spec); spec.loader.exec_module(nnp)
NUMBERS = nnp.NUMBERS

spec2 = importlib.util.spec_from_file_location('ncl', os.path.join(ROOT, 'tools', 'build-number-cluster.py'))
ncl = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(ncl)
ARCH = {n: ncl.PERSONALITY[n]['archetype'] for n in range(1, 10)}
TLDR_LINE = {n: ncl.PERSONALITY[n]['tldr'].split('. ')[0] + '.' for n in range(1, 10)}

# Aspect pages currently shipped per number. Add love/compatibility here
# once those slices ship, the hub will auto-list them.
ASPECTS = [
    ('personality', '/number/{n}-personality',   'Personality'),
    ('career',      '/number/{n}-career',        'Career'),
    ('name',        '/name-number-{n}-meaning',  'Name Number'),
    ('lifepath',    '/life-path-number-{n}-meaning','Life Path'),
]

TITLE = 'Numbers 1-9 in Chaldean Numerology, Personality, Career, Name & Life Path Guides'
DESC  = 'Every Chaldean numerology number 1-9 explained, personality archetype, best careers, name number meaning and life path. Free, no signup.'
OGTITLE = 'Numbers 1-9 in Chaldean Numerology · The complete guide'
OGDESC  = 'Personality, career, name and life-path readings for each Chaldean number 1-9. Free.'
CANON = f'{BASE}/number'

ARTICLE = {
  '@context':'https://schema.org','@type':'CollectionPage','name':TITLE,'description':DESC,'url':CANON,
  'inLanguage':'en-IN','isPartOf':{'@type':'WebSite','name':'NameAligned.com','url':BASE+'/'},
  'about':{'@type':'DefinedTerm','name':'Chaldean Numerology','inDefinedTermSet':'Numerology Systems'}
}

ITEMLIST = {
  '@context':'https://schema.org','@type':'ItemList','name':'Numbers 1 to 9',
  'itemListElement':[
    {'@type':'ListItem','position':n,'url':f'{BASE}/number/{n}-personality',
     'name':f'Number {n}, {ARCH[n]} ({NUMBERS[n]["planet"]})'} for n in range(1,10)
  ]
}

BREADCRUMB = {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
  {'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},
  {'@type':'ListItem','position':2,'name':'Numbers','item':CANON}
]}


HEAD = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-70GFTN27M6"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-70GFTN27M6');</script>

<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link rel="icon" type="image/svg+xml" href="/assets/namealigned-favicon.svg"/>
<title>{TITLE}</title>
<meta name="description" content="{DESC}"/>
<meta name="keywords" content="numerology numbers, chaldean numerology numbers, number 1 to 9 meaning, numerology hub, chaldean number guide"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<link rel="canonical" href="{CANON}"/>
<link rel="alternate" hreflang="en-IN" href="{CANON}"/>
<meta property="og:title" content="{OGTITLE}"/>
<meta property="og:description" content="{OGDESC}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{CANON}"/>
<meta property="og:site_name" content="NameAligned.com"/>
<meta property="og:locale" content="en_IN"/>
<meta property="og:image" content="{BASE}/assets/namealigned-logo-full.svg"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{OGTITLE}"/>
<meta name="twitter:description" content="{OGDESC}"/>

<script type="application/ld+json">{json.dumps(ARTICLE, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(BREADCRUMB, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ITEMLIST, ensure_ascii=False)}</script>

<link rel="stylesheet" href="/assets/style.css"/>
<link rel="stylesheet" href="/assets/theme-cosmic-light.css"/>
<style>
.nh-hero{{padding:3.25rem 1.25rem 2.25rem;text-align:center;background:linear-gradient(160deg,#1a1340 0%,#2a1a5c 60%,#1a0e52 100%);color:#f0ece0;position:relative;overflow:hidden;}}
.nh-hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 50% 5%,rgba(240,180,41,.16) 0%,transparent 65%);}}
.nh-hero .badge{{display:inline-block;font-family:sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f0b429;background:rgba(240,180,41,.12);padding:5px 14px;border-radius:20px;border:1px solid rgba(240,180,41,.32);margin-bottom:1rem;position:relative;}}
.nh-hero h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4.5vw,44px);line-height:1.2;margin:0 auto .65rem;max-width:780px;color:#f0ece0!important;position:relative;}}
.nh-hero p{{font-family:sans-serif;font-size:14.5px;line-height:1.65;color:#cbb8e8;max-width:600px;margin:0 auto;position:relative;}}
.nh-body{{max-width:980px;margin:0 auto;padding:2.5rem 1.25rem;}}
.nh-body h2{{font-family:'Playfair Display',Georgia,serif;font-size:24px;color:var(--text);margin:1.75rem 0 .65rem;line-height:1.25;}}
.nh-body p{{font-family:sans-serif;font-size:14.5px;line-height:1.75;color:var(--text);margin-bottom:1rem;}}
.nh-kinds{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;margin:1rem 0 1.5rem;}}
@media(max-width:640px){{.nh-kinds{{grid-template-columns:1fr;}}}}
.nh-kind{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:1rem 1.1rem;}}
.nh-kind .lbl{{font-family:sans-serif;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:.3rem;}}
.nh-kind h3{{font-family:'Playfair Display',Georgia,serif;font-size:17px;color:var(--text);margin:0 0 .35rem;}}
.nh-kind p{{font-family:sans-serif;font-size:13px;color:var(--text2);line-height:1.55;margin:0;}}
.nh-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1.25rem;}}
@media(max-width:900px){{.nh-grid{{grid-template-columns:repeat(2,1fr);}}}}
@media(max-width:560px){{.nh-grid{{grid-template-columns:1fr;}}}}
.nh-card{{background:var(--card);border:1px solid var(--gold-b);border-radius:14px;padding:1.25rem 1.25rem 1.1rem;display:flex;flex-direction:column;transition:transform .15s ease,box-shadow .15s ease;position:relative;overflow:hidden;}}
.nh-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#9d7fff,#f0b429,#9d7fff);opacity:.7;}}
.nh-card:hover{{transform:translateY(-2px);box-shadow:0 10px 28px rgba(109,78,209,.12);}}
.nh-card .nh-num{{display:flex;align-items:center;gap:.65rem;margin-bottom:.5rem;}}
.nh-card .nh-glyph{{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#9d7fff,#f0b429);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',Georgia,serif;font-size:18px;font-weight:700;}}
.nh-card .nh-n{{font-family:'Playfair Display',Georgia,serif;font-size:22px;color:var(--text);font-weight:700;line-height:1;}}
.nh-card .nh-arch{{font-family:'Playfair Display',Georgia,serif;font-size:18px;color:var(--text);font-weight:700;margin-bottom:.2rem;}}
.nh-card .nh-tag{{font-family:sans-serif;font-size:11.5px;letter-spacing:.06em;color:var(--gold-d);font-weight:700;text-transform:uppercase;margin-bottom:.6rem;}}
.nh-card .nh-blurb{{font-family:sans-serif;font-size:13px;color:var(--text2);line-height:1.6;margin-bottom:.85rem;flex:1;}}
.nh-card .nh-links{{display:flex;flex-wrap:wrap;gap:.4rem;}}
.nh-card .nh-links a{{font-family:sans-serif;font-size:11.5px;font-weight:600;color:#7c3aed;background:rgba(157,127,255,.08);border:1px solid rgba(157,127,255,.2);padding:4px 10px;border-radius:6px;text-decoration:none;transition:background .15s ease;}}
.nh-card .nh-links a:hover{{background:rgba(157,127,255,.16);}}
.nh-cta-band{{background:var(--gold-l);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.5rem;margin:2rem 0;text-align:center;}}
.nh-cta-band h3{{margin:0 0 .35rem;font-family:Georgia,serif;font-size:19px;color:var(--text);}}
.nh-cta-band p{{margin:0 0 1rem;font-size:13.5px;color:var(--text2);font-family:sans-serif;}}
.nh-cta-band .btn-pair{{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;}}
.nh-cta-band a{{display:inline-block;font-family:sans-serif;font-size:13.5px;font-weight:600;padding:9px 18px;border-radius:8px;text-decoration:none;}}
.nh-cta-band a.primary{{background:var(--gold);color:#0a0820;}}
.nh-cta-band a.primary:hover{{background:#f5c247;}}
.nh-cta-band a.outline{{background:transparent;color:var(--text);border:1.5px solid var(--gold-b);}}
nav.crumb{{font-family:sans-serif;font-size:12px;color:var(--text3);padding:1rem 1.25rem 0;max-width:980px;margin:0 auto;}}
nav.crumb a{{color:var(--text3);text-decoration:none;}}
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
      <div>
        <div class="footer-brand"><span class="logo-moon">☽</span> NameAligned.com</div>
        <p class="footer-tagline">Free Chaldean numerology analysis for everyone. Based on Cheiro\'s Book of Numbers, the oldest and most accurate system.</p>
        <div style="margin-top:1.5rem;display:flex;gap:10px">
          <a href="/analyzer" style="font-size:12px;font-family:sans-serif;color:var(--gold);border:1px solid rgba(240,180,41,.35);border-radius:20px;padding:5px 14px;text-decoration:none;transition:all .2s" onmouseover="this.style.background='rgba(240,180,41,.12)'" onmouseout="this.style.background='transparent'">Try free →</a>
          <a href="/report" style="font-size:12px;font-family:sans-serif;color:rgba(157,127,255,.8);border:1px solid rgba(157,127,255,.3);border-radius:20px;padding:5px 14px;text-decoration:none;transition:all .2s" onmouseover="this.style.background='rgba(157,127,255,.10)'" onmouseout="this.style.background='transparent'">Full report · ₹499 / $5</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Free Tools</div>
        <ul class="footer-links">
          <li><a href="/name-numerology-calculator">Name Numerology Calculator</a></li>
          <li><a href="/name-correction-numerology">Name Correction Check</a></li>
          <li><a href="/business-name-numerology">Business Name Check</a></li>
          <li><a href="/love-compatibility-numerology">Love Compatibility</a></li>
          <li><a href="/report">Full Destiny Report · ₹499 / $5</a></li>
          <li><a href="/ask-aura">✦ Ask Aura · Conversational</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Guides</div>
        <ul class="footer-links">
          <li><a href="/blog/chaldean-numerology-guide">Chaldean Guide</a></li>
          <li><a href="/blog/moolank-meanings">Birth Number Meanings</a></li>
          <li><a href="/blog/personal-year-guide">Personal Year Guide</a></li>
          <li><a href="/blog/name-correction-guide">Name Correction Guide</a></li>
          <li><a href="/blog/compound-numbers-cheiro">Compound Numbers</a></li>
          <li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">More</div>
        <ul class="footer-links">
          <li><a href="/blog">All Articles</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/sitemap-pages">Site Map</a></li>
          <li><a href="/privacy">Privacy</a></li>
          <li><a href="/terms">Terms</a></li>
          <li><a href="/refund">Refund</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 NameAligned.com · For entertainment &amp; self-reflection purposes</span>
      <span>Made with <span style="color:#e8526b;">❤</span> in India · 🔒 Secured by <strong style="color:#9d7fff;">Razorpay</strong></span>
    </div>
  </div>
</footer>
</body>
</html>
'''


def render():
    cards = []
    for n in range(1, 10):
        d = NUMBERS[n]
        arch = ARCH[n]
        # Short blurb pulled from the personality TLDR, first sentence
        blurb = TLDR_LINE[n]
        # Build aspect links, only include if the page exists
        link_html = ''
        for key, tmpl, label in ASPECTS:
            link_html += f'<a href="{tmpl.format(n=n)}">{label}</a>'
        cards.append(f'''      <div class="nh-card">
        <div class="nh-num"><div class="nh-glyph">{d["glyph"]}</div><div class="nh-n">Number {n}</div></div>
        <div class="nh-arch">{arch}</div>
        <div class="nh-tag">{d["planet"]} · {d["tagline"].split(" · ")[0]}</div>
        <p class="nh-blurb">{blurb}</p>
        <div class="nh-links">{link_html}</div>
      </div>''')
    cards_html = '\n'.join(cards)

    body = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">Numbers</span>
</nav>

<header class="nh-hero">
  <div class="badge">Chaldean Numerology · Numbers 1-9</div>
  <h1>Every number in Chaldean numerology, in one place</h1>
  <p>Each number 1-9 carries a planetary signature that shapes personality, career fit and the kind of relationships that thrive around you. Pick a number to read it from every angle.</p>
</header>

<main class="nh-body">

  <h2>What is a number in Chaldean numerology?</h2>
  <p>In Chaldean numerology, the system Cheiro popularised and the one most Indian numerologists still use, every single digit (1 through 9) is governed by a planet. The planet sets the temperament, the rhythm, and the natural arc of life events for anyone whose chart carries that number.</p>
  <p>Your chart carries multiple numbers. The four most important are:</p>

  <div class="nh-kinds">
    <div class="nh-kind">
      <div class="lbl">Birth Number (Moolank)</div>
      <h3>The day you were born</h3>
      <p>Reduce your day-of-birth to a single digit (e.g. 23 → 2+3 → 5). This is the energy you operate from internally.</p>
    </div>
    <div class="nh-kind">
      <div class="lbl">Life Path Number (Bhagyank / Destiny)</div>
      <h3>Your full birth-date sum</h3>
      <p>Sum the entire birth date and reduce. This is the soul-curriculum, the long-arc lesson your life is shaped around.</p>
    </div>
    <div class="nh-kind">
      <div class="lbl">Name Number</div>
      <h3>The Chaldean letter values of your name</h3>
      <p>Each letter has a number value (different from Pythagorean). Sum your full daily-use name and reduce. This is the vibration the world meets.</p>
    </div>
    <div class="nh-kind">
      <div class="lbl">Personal Year Number</div>
      <h3>Your day + month + current year</h3>
      <p>Reduce day + month + the current year. This shifts annually and tells you what energy is most active in any given year.</p>
    </div>
  </div>

  <p>The same single digit (say, Number 8) can show up in any of those four positions, and the meaning shifts subtly depending on where it lives in your chart. The pages below cover Number N as an archetype across the whole chart, plus the specific aspect pages where they exist.</p>

  <h2>Pick a number</h2>
  <div class="nh-grid">
{cards_html}
  </div>

  <div class="nh-cta-band">
    <h3>Don't know your numbers yet?</h3>
    <p>The free Chaldean calculator gives you Birth Number, Life Path Number and Name Number, side by side, in 15 seconds.</p>
    <div class="btn-pair">
      <a class="primary" href="/name-numerology-calculator">Calculate my numbers →</a>
      <a class="outline" href="/analyzer">Full free analysis</a>
    </div>
  </div>

  <h2>Going deeper</h2>
  <p>For the complete picture, your specific Birth, Name and Life Path numbers in your own chart, plus a 5-year personal-year forecast, name-correction options and remedies, the <a href="/report">Full Destiny Report (₹499 / $5 USD)</a> generates a personalised PDF in 60 seconds.</p>

</main>

{FOOTER}
'''
    return HEAD + body


def main():
    html = render()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        f.write(html)
    words = len(re.findall(r'\b\w+\b', html))
    print(f'wrote number/index.html (~{words} words including markup)')


if __name__ == '__main__':
    main()
