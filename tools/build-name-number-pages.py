#!/usr/bin/env python3
"""
Generate /name-number-N-meaning pages (1-9) for SEO.

Each page is unique, ~1000+ words, with BreadcrumbList + Article + FAQ
JSON-LD. Run:

    python3 tools/build-name-number-pages.py

Output: name-number-1-meaning.html ... name-number-9-meaning.html in
the repo root (matches the existing flat-URL structure).
"""
import json, os, re

BASE = 'https://www.namealigned.com'
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Per-number data (deliberately distinct per number) ──────────
NUMBERS = {
1:{'planet':'Sun','glyph':'☀','tagline':'Leadership · Authority · Visibility','color':'Gold · Orange · Red',
   'core':'Name number 1 places your daily expression under the influence of the Sun. Your name carries an authoritative, originating signature — people sense leadership, decisiveness and a willingness to start things from zero. The vibration tends to put you front-of-stage even in rooms where you didn\'t plan to lead.',
   'strengths':[
     'Pioneering instinct — you start things others only talk about','Unmistakable presence in a room','Decisive about direction once you\'ve thought it through','High agency in your own life — rarely a passenger','Originality of thought; you don\'t default to received wisdom'],
   'growth':[
     'Loneliness at the top — capable people often carry alone','Impatience with people who can\'t move at your pace','Tendency to over-extend before delegating'],
   'career':['CEO / Founder roles','Government & Public Office','Independent practice (law, medicine, consulting)','Entertainment & Media as a public figure','Gold, gemstone or luxury trade'],
   'compat_best':[1,2,4,9],'compat_good':[3,5,6],'compat_caution':[7,8],
   'famous':'Sun-ruled name vibrations are often found among monarchs, founders and people whose work bears their personal signature.',
   'how_known':'Your full name reduces (Chaldean letter values, summed and reduced to a single digit) to 1. The ruling planet of that single digit is the Sun.',
   'faq':[
     ('Is name number 1 lucky?','Name number 1 carries Sun energy — strongly visible, naturally leadership-oriented and generally considered fortunate for first-borns and entrepreneurs. Whether it works for *you* depends on whether your Moolank and Bhagyank harmonise with the Sun.'),
     ('What does name number 1 mean for marriage?','It tends to read as a partner who leads, decides and protects — best paired with name numbers 2, 4 and 9. Compatibility is more about planetary harmony than the single digit alone.'),
     ('Can I change my name to a name number 1?','Yes, but only if your Moolank and Bhagyank already harmonise with Sun energy. Otherwise the change adds friction rather than ease.'),
     ('What are the best careers for name number 1?','Roles where your judgement is the product — leadership, founder roles, government, top-of-firm professional services and visible public positions.'),
   ]},
2:{'planet':'Moon','glyph':'☾','tagline':'Sensitivity · Intuition · Harmony','color':'White · Silver · Cream',
   'core':'Name number 2 puts your daily expression under the Moon. The vibration is intuitive, emotionally perceptive and quietly diplomatic — you read rooms before others have finished speaking. Strength here is relational; people open up around your name without quite knowing why.',
   'strengths':[
     'Empathic radar — you sense moods before they\'re stated','Diplomatic by default; you bring people together','Imaginative inner world that fuels creative work','Patience with processes that need to ripen','Loyal to a depth most people miss until they\'ve earned it'],
   'growth':[
     'Absorbing other people\'s emotional states until you can\'t separate yours','Difficulty saying no when someone needs you','Decision fatigue when stakes feel too personal'],
   'career':['Counselling & Psychology','Hospitality & Food','Music, Poetry & the Arts','Nursing & Caregiving','Real Estate (homes, not commercial)'],
   'compat_best':[1,2,7],'compat_good':[4,6,8],'compat_caution':[3,5,9],
   'famous':'Moon-ruled name vibrations are common among artists, healers, hospitality founders and people whose work touches the emotional life of others.',
   'how_known':'Your full name\'s Chaldean letter values, summed and reduced, equal 2. The ruling planet of 2 is the Moon.',
   'faq':[
     ('Is name number 2 emotional?','Yes — it amplifies emotional sensitivity. That\'s a creative gift in art, hospitality and counselling, but asks for stronger boundaries in high-friction environments.'),
     ('Is name number 2 good for marriage?','Generally yes; Moon energy is naturally relational. Best harmony with name numbers 1, 2 and 7; Moon-ruled people often pair well with Sun-ruled (1) partners.'),
     ('What jobs suit name number 2?','Hospitality, food, the arts, counselling, nursing, residential real estate — anything where reading emotion is the value, not a side-effect.'),
     ('Why does name number 2 feel emotionally tiring?','The Moon\'s gift — emotional permeability — is also its cost. Daily decompression rituals (journaling, water, quiet) keep the gift sustainable.'),
   ]},
3:{'planet':'Jupiter','glyph':'♃','tagline':'Expression · Optimism · Joy','color':'Yellow · Cream · Violet',
   'core':'Name number 3 sits under Jupiter — the planet of expansion, teaching and celebration. The vibration is expressive, generous and naturally optimistic; people remember conversations with you. Strength here is the ability to make complex ideas land warmly with non-experts.',
   'strengths':[
     'Verbal charisma — you make hard topics feel easy','Natural teacher; ideas land when you explain them','Optimistic without being naive','Wide social range; you connect across worlds','Creative output flows in bursts you can\'t fully plan'],
   'growth':[
     'Scattering across too many projects','Sounding the most fine when you\'re the least fine','Saying yes more than the calendar can hold'],
   'career':['Education & Teaching','Law & Justice','Banking & Finance','Religion / Spirituality','Publishing & Media'],
   'compat_best':[3,6,9],'compat_good':[1,5],'compat_caution':[2,4,8],
   'famous':'Jupiter-ruled name vibrations are common among teachers, judges, religious leaders and influential writers.',
   'how_known':'Your full Chaldean name sum reduces to 3. Jupiter rules 3.',
   'faq':[
     ('Is name number 3 a creative number?','Yes — Jupiter gives expressive range. Name 3 people often write, teach, perform or run creative ventures.'),
     ('Is name number 3 lucky for money?','Jupiter is traditionally the planet of abundance, especially through teaching, publishing, finance and law. Direct cash speculation is less reliable than expansive long-term work.'),
     ('Why does name number 3 attract attention?','Jupiter expands. Whatever your name carries gets amplified outward, including the parts of yourself you didn\'t plan to put forward.'),
     ('What numbers harmonise best with name number 3?','3, 6 and 9 form a strong triangle — all expansion-oriented planets. 1 and 5 are also supportive.'),
   ]},
4:{'planet':'Rahu','glyph':'◈','tagline':'Innovation · Logic · Structure','color':'Blue · Electric · Grey',
   'core':'Name number 4 carries Rahu vibration — the unconventional, pattern-spotting, future-leaning energy. The signature reads as "different in a way you can\'t place" — a builder of systems, technologies and methods that don\'t exist yet. Strength here is seeing what others miss.',
   'strengths':[
     'Pattern vision — you spot what others overlook','Comfort with the unconventional and the not-yet-mainstream','Calm under disruption; chaos doesn\'t throw you','Quietly reliable for things that matter long-term','Original thinker; rarely defaults to consensus'],
   'growth':[
     'Misread as "difficult" by people who don\'t want to be questioned','Restlessness when systems become rigid','Abrupt shifts that test stability'],
   'career':['Engineering & Architecture','IT & Technology','Research & Analysis','Logistics & Supply Chain','Aviation, Foreign Trade, Anything cross-border'],
   'compat_best':[1,2,4,8],'compat_good':[6,7],'compat_caution':[3,5,9],
   'famous':'Rahu-ruled name vibrations are common in engineering, deep-tech founders, foreign-service careers and pioneers of unfamiliar fields.',
   'how_known':'Your full Chaldean name sum reduces to 4. Rahu (the north node) rules 4 in the Chaldean system.',
   'faq':[
     ('Is name number 4 unlucky?','No. The reputation comes from Rahu being misunderstood — but its gifts (innovation, foreign opportunity, technology) are genuine. Name 4 thrives in change-friendly environments.'),
     ('Should I avoid name number 4?','Only if your Moolank or Bhagyank carries strong Sun (1) or Saturn (8) friction with Rahu. Otherwise it\'s a powerful name vibration for unconventional careers.'),
     ('What careers suit name number 4?','Tech, engineering, research, foreign trade, aviation, anything that rewards original thinking over conformity.'),
     ('Why does name number 4 feel like an outsider?','Rahu gives an unusual angle of perception. Outsider status is often the source of the very insight that makes you valuable.'),
   ]},
5:{'planet':'Mercury','glyph':'☿','tagline':'Adaptability · Wit · Communication','color':'Green · Light Grey',
   'core':'Name number 5 puts you under Mercury — speed, adaptability, wit and the ability to learn anything quickly. The vibration is conversational, curious and commercially nimble; people enjoy your company before they realise they\'ve learned something.',
   'strengths':[
     'Quick mind — you absorb and synthesise at unusual speed','Conversational charisma; you make small-talk valuable','Versatile across very different worlds','Curiosity at scale — you keep learning past most people\'s threshold','Trade and negotiation come naturally'],
   'growth':[
     'Losing interest before things mature','Restlessness in slow-moving environments','Mental overstimulation — too many tabs open'],
   'career':['Media & Journalism','Sales & Marketing','Travel & Tourism','Stock Trading','Digital Startups'],
   'compat_best':[1,5,9],'compat_good':[3,6],'compat_caution':[2,4,8],
   'famous':'Mercury-ruled name vibrations are common in journalism, sales, broadcasting and high-velocity startup roles.',
   'how_known':'Your full Chaldean name sum reduces to 5. Mercury rules 5.',
   'faq':[
     ('Is name number 5 good for business?','Particularly for trade, media, marketing, agency work and any role that rewards speed of communication.'),
     ('Is name number 5 a stable number?','It\'s mobile by nature. Stability comes from rituals you choose, not from the vibration itself.'),
     ('What\'s the downside of name number 5?','Inability to slow down when slowing down would help — projects abandoned mid-maturation, decisions made before facts have settled.'),
     ('Which numbers pair well with name number 5?','1, 5 and 9 are strongest. 3 and 6 add expansion and harmony. 2, 4 and 8 ask for more conscious adjustment.'),
   ]},
6:{'planet':'Venus','glyph':'♀','tagline':'Harmony · Love · Aesthetics','color':'Pink · White · Pastel Blue',
   'core':'Name number 6 sits under Venus — beauty, harmony, relationship and aesthetic sense. The vibration is warm, devoted, and instinctively attuned to fairness in relationships. Strength here is making people and spaces feel held.',
   'strengths':[
     'Emotional fluency — you name what others can\'t articulate','Aesthetic instinct in design, dress, food, space','Devoted in relationships; loyalty runs deep','Caretaker presence that holds groups together','Strong sense of fair-play and reciprocity'],
   'growth':[
     'Holding everyone together while no-one asks who holds you','Difficulty saying no to people you love','Idealising partners until reality intrudes'],
   'career':['Fashion & Design','Entertainment & Film','Hospitality','Cosmetics & Beauty','Social Work / NGO'],
   'compat_best':[3,6,9],'compat_good':[1,4,5],'compat_caution':[2,7,8],
   'famous':'Venus-ruled name vibrations are common in design, hospitality, entertainment and any role where aesthetic taste is the product.',
   'how_known':'Your full Chaldean name sum reduces to 6. Venus rules 6.',
   'faq':[
     ('Is name number 6 the love number?','Often called that. Venus rules relationship and aesthetic harmony — name 6 people gravitate toward partnership and beauty in everything they do.'),
     ('Is name number 6 good for women?','It works regardless of gender; the cultural framing of Venus as feminine is incidental. The vibration is about harmony, not gender.'),
     ('What jobs suit name number 6?','Design, fashion, entertainment, hospitality, cosmetics, social work — fields where care and aesthetic taste are central, not decorative.'),
     ('Which numbers pair well with name number 6?','3, 6 and 9 are strongest. 1, 4 and 5 are supportive. 2, 7 and 8 ask for more boundary work.'),
   ]},
7:{'planet':'Ketu','glyph':'◉','tagline':'Wisdom · Introspection · Depth','color':'Violet · Purple · Grey',
   'core':'Name number 7 carries Ketu — the south-node energy of detachment, depth and inner inquiry. The vibration reads as a person who thinks before speaking and asks the question others were quietly avoiding. Strength here is depth where most people only have surface.',
   'strengths':[
     'Deep insight — you research thoroughly','Independent mind; you trust your own conclusions','Calm under pressure others find unbearable','Discernment — you see through performances','Spiritual or philosophical orientation that grounds you'],
   'growth':[
     'Over-thinking the final decision','Distance read as coldness when it\'s actually protection','Difficulty trusting people quickly'],
   'career':['Research & Science','Spirituality & Healing','Writing & Literature','Astrology & Mysticism','Philosophy & Academia'],
   'compat_best':[2,7],'compat_good':[1,4,6],'compat_caution':[3,5,8,9],
   'famous':'Ketu-ruled name vibrations are common in research, spirituality, monastic traditions, philosophy and contemplative writing.',
   'how_known':'Your full Chaldean name sum reduces to 7. Ketu (the south node) rules 7.',
   'faq':[
     ('Is name number 7 spiritual?','Strongly so. Ketu pulls toward inner inquiry — name 7 people often have a contemplative or research-driven thread running through their work.'),
     ('Is name number 7 lucky for marriage?','Best with name numbers 2 and 7. Otherwise marriage works when both partners respect the alone-time the vibration needs.'),
     ('What does name number 7 mean for career?','Research-heavy, depth-rewarding fields — science, spirituality, writing, academia. Surface-level commercial roles tend to feel hollow over time.'),
     ('Why does name number 7 prefer solitude?','Ketu rewards inner stillness. Solitude isn\'t avoidance — it\'s how the vibration regenerates.'),
   ]},
8:{'planet':'Saturn','glyph':'♄','tagline':'Discipline · Authority · Resilience','color':'Black · Dark Blue · Dark Grey',
   'core':'Name number 8 sits under Saturn — discipline, structure, long-game ambition and earned authority. The vibration is heavy in the best sense; people feel that you\'ve worked for what you have. Strength here is endurance — playing long games most people can\'t see.',
   'strengths':[
     'Strategic — you play long games','Resilient when others panic','Accountable; your word is your reputation','Endurance for projects that take years','Authority that\'s earned, not assumed'],
   'growth':[
     'Frustration before recognition arrives','Looking composed while carrying weight nobody sees','Slow trust — relationships take time to deepen'],
   'career':['Finance & Banking','Law & Courts','Mining & Heavy Industry','Import/Export','Real Estate Investment'],
   'compat_best':[2,4,6,8],'compat_good':[1,7],'compat_caution':[3,5,9],
   'famous':'Saturn-ruled name vibrations are common among judges, central bankers, long-game founders and people whose authority developed over decades.',
   'how_known':'Your full Chaldean name sum reduces to 8. Saturn rules 8.',
   'faq':[
     ('Is name number 8 unlucky?','No, but it\'s slow. Saturn rewards discipline and patience; quick-win approaches don\'t fit. Used well, name 8 builds enduring authority.'),
     ('Is name number 8 good for business?','Yes — particularly finance, law, real estate, heavy industry and import-export. Less suited to fast-moving consumer or media careers.'),
     ('Why does name number 8 feel heavy?','Saturn carries weight by design. The weight is what makes the eventual authority real, but it asks for endurance most people don\'t have.'),
     ('Which numbers pair well with name number 8?','2, 4, 6 and 8. Saturn-ruled pairings benefit from at least one Moon-ruled (2) partner who softens the structure.'),
   ]},
9:{'planet':'Mars','glyph':'♂','tagline':'Courage · Energy · Action','color':'Red · Crimson · Deep Orange',
   'core':'Name number 9 carries Mars — fire, courage, decisive action and protective force. The vibration moves first and explains later; people feel the heat in the room when you arrive. Strength here is the willingness to start and finish what others can\'t face.',
   'strengths':[
     'Bold — you move first while others wait','Protective of the people you love','Driven; your fire fuels everyone around you','Courage in action under pressure','Cuts through noise and gets to the point'],
   'growth':[
     'Felt at a volume the world keeps asking you to turn down','Crash-and-recovery rhythm in long projects','Impatience with slow-moving environments'],
   'career':['Military & Defense','Surgery & Medicine','Sports & Athletics','Politics','Social Activism / NGO'],
   'compat_best':[1,3,5,9],'compat_good':[6,7],'compat_caution':[2,4,8],
   'famous':'Mars-ruled name vibrations are common among soldiers, surgeons, athletes, activists and decisive political figures.',
   'how_known':'Your full Chaldean name sum reduces to 9. Mars rules 9.',
   'faq':[
     ('Is name number 9 aggressive?','Energetic, not aggressive. Mars is a fire planet — used well it\'s courage and protection; misused it tips into unnecessary conflict.'),
     ('Is name number 9 good for women?','It works regardless of gender. Mars is courage; the cultural framing as masculine is incidental.'),
     ('What jobs suit name number 9?','Defense, surgery, sports, activism, politics — roles requiring decisive action and the ability to handle physical or emotional intensity.'),
     ('Which numbers pair well with name number 9?','1, 3, 5 and 9. The fire-and-air combinations work; earth-and-water (2, 4, 8) ask for conscious effort.'),
   ]},
}


HEAD_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-C1JMQTNHDE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-C1JMQTNHDE');
</script>

<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link rel="icon" type="image/svg+xml" href="/assets/namealigned-favicon.svg"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="keywords" content="name number {n}, name number {n} meaning, name number {n} {planet_lower}, chaldean name number {n}, name number {n} career, name number {n} compatibility"/>
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
<meta property="og:image" content="{base}/assets/og/moolank-{n}.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{og_desc}"/>
<meta name="twitter:image" content="{base}/assets/og/moolank-{n}.png"/>

<script type="application/ld+json">
{article_json}
</script>
<script type="application/ld+json">
{breadcrumb_json}
</script>
<script type="application/ld+json">
{faq_json}
</script>

<link rel="stylesheet" href="assets/style.css"/>
<link rel="stylesheet" href="assets/theme-cosmic-light.css"/>
<style>
.nn-hero{{padding:3.5rem 0 1.75rem;text-align:center;background:linear-gradient(160deg,#1a1340 0%,#2a1a5c 100%);color:#f0ece0;}}
.nn-hero .badge{{display:inline-block;font-family:sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f0b429;background:rgba(240,180,41,.12);padding:5px 14px;border-radius:20px;border:1px solid rgba(240,180,41,.35);margin-bottom:1rem;}}
.nn-hero h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4.2vw,44px);line-height:1.2;margin:0 auto .5rem;max-width:780px;}}
.nn-hero .glyph{{font-size:48px;color:#f0b429;line-height:1;margin-bottom:.75rem;}}
.nn-hero .tag{{font-family:sans-serif;font-size:14px;color:rgba(240,236,224,.78);letter-spacing:.06em;}}
.nn-body{{max-width:780px;margin:0 auto;padding:2rem 1.25rem;}}
.nn-body h2{{font-family:'Playfair Display',Georgia,serif;font-size:24px;color:var(--text);margin:2rem 0 .65rem;line-height:1.25;}}
.nn-body h3{{font-family:'Playfair Display',Georgia,serif;font-size:18px;color:var(--text);margin:1.5rem 0 .5rem;}}
.nn-body p{{font-family:sans-serif;font-size:14.5px;line-height:1.75;color:var(--text);margin-bottom:1rem;}}
.nn-body ul{{font-family:sans-serif;font-size:14px;line-height:1.85;color:var(--text);padding-left:1.25rem;margin-bottom:1.25rem;}}
.nn-body li{{margin-bottom:.35rem;}}
.nn-stat-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin:1.5rem 0;}}
.nn-stat{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem;text-align:center;}}
.nn-stat .lbl{{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;}}
.nn-stat .val{{font-family:Georgia,serif;font-size:16px;color:var(--text);margin-top:4px;}}
.nn-cta-band{{background:var(--gold-l);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.5rem;margin:2rem 0;text-align:center;}}
.nn-cta-band h3{{margin:0 0 .35rem;font-family:Georgia,serif;font-size:19px;color:var(--text);}}
.nn-cta-band p{{margin:0 0 1rem;font-size:13.5px;color:var(--text2);font-family:sans-serif;}}
.nn-cta-band .btn-pair{{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;}}
.nn-cta-band a{{display:inline-block;font-family:sans-serif;font-size:13.5px;font-weight:600;padding:9px 18px;border-radius:8px;text-decoration:none;}}
.nn-cta-band a.primary{{background:var(--gold);color:#0a0820;}}
.nn-cta-band a.primary:hover{{background:#f5c247;}}
.nn-cta-band a.outline{{background:transparent;color:var(--text);border:1.5px solid var(--gold-b);}}
.nn-faq{{margin:2rem 0;}}
.nn-faq details{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem 1.1rem;margin-bottom:.6rem;}}
.nn-faq summary{{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--text);cursor:pointer;line-height:1.4;}}
.nn-faq details[open] summary{{margin-bottom:.5rem;}}
.nn-faq details p{{font-family:sans-serif;font-size:13.5px;line-height:1.7;color:var(--text2);margin:0;}}
.nn-related{{margin:2rem 0;}}
.nn-related-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;}}
@media(max-width:640px){{.nn-related-grid{{grid-template-columns:1fr;}}}}
.nn-rel-card{{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.9rem 1rem;text-decoration:none;color:var(--text);transition:transform .15s ease,box-shadow .15s ease;}}
.nn-rel-card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(201,162,39,.12);}}
.nn-rel-card .eb{{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:.25rem;}}
.nn-rel-card .ti{{font-family:Georgia,serif;font-size:14.5px;font-weight:700;line-height:1.3;}}
nav.crumb{{font-family:sans-serif;font-size:12px;color:var(--text3);padding:1rem 1.25rem 0;max-width:780px;margin:0 auto;}}
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
      <div><div class="footer-brand">☽ NameAligned.com</div><p class="footer-tagline">Free Chaldean numerology for everyone.</p></div>
      <div><div class="footer-col-title">Free Tools</div><ul class="footer-links"><li><a href="/name-numerology-calculator">Name Calculator</a></li><li><a href="/name-correction-numerology">Name Correction</a></li><li><a href="/business-name-numerology">Business Name</a></li><li><a href="/baby-name-numerology">Baby Name</a></li><li><a href="/love-compatibility-numerology">Love Compatibility</a></li><li><a href="/report">Full Report INR 199/-</a></li></ul></div>
      <div><div class="footer-col-title">Guides</div><ul class="footer-links"><li><a href="/blog/chaldean-numerology-guide">Chaldean Guide</a></li><li><a href="/blog/moolank-meanings">Moolank Meanings</a></li><li><a href="/blog/personal-year-guide">Personal Year</a></li><li><a href="/blog/name-correction-guide">Name Correction</a></li><li><a href="/blog/compound-numbers-cheiro">Compound Numbers</a></li><li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid</a></li></ul></div>
      <div><div class="footer-col-title">More</div><ul class="footer-links"><li><a href="/blog">All Articles</a></li><li><a href="/about">About</a></li><li><a href="/sitemap-pages">Site Map</a></li><li><a href="/privacy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/refund">Refund</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 NameAligned.com</span><span>Made with <span style="color:#e8526b;">❤</span> in India</span></div>
  </div>
</footer>
</body>
</html>
'''

def render(n, data):
    title = f'Name Number {n} Meaning · {data["planet"]} Energy in Chaldean Numerology'
    desc = f'Name number {n} carries {data["planet"]} energy — {data["tagline"].lower()}. Read what name number {n} means for personality, career, marriage and compatibility, with a free Chaldean check.'
    og_desc = f'Name number {n} ({data["planet"]}) decoded — strengths, growth themes, career fields and compatibility.'
    canon = f'{BASE}/name-number-{n}-meaning'

    article = {
        "@context":"https://schema.org","@type":"Article","headline":title,
        "description":desc,"url":canon,"datePublished":"2026-02-01","dateModified":"2026-05-06",
        "author":{"@type":"Organization","name":"NameAligned.com","url":BASE+"/"},
        "publisher":{"@type":"Organization","name":"NameAligned.com","url":BASE+"/","logo":{"@type":"ImageObject","url":BASE+"/assets/namealigned-logo-full.svg"}},
        "inLanguage":"en-IN","mainEntityOfPage":{"@type":"WebPage","@id":canon}
    }
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Numerology Guides","item":BASE+"/sitemap-pages"},
        {"@type":"ListItem","position":3,"name":f"Name Number {n} Meaning","item":canon}
    ]}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in data["faq"]
    ]}

    head = HEAD_TEMPLATE.format(
        n=n, title=title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        planet_lower=data["planet"].lower(),
        article_json=json.dumps(article, ensure_ascii=False),
        breadcrumb_json=json.dumps(breadcrumb, ensure_ascii=False),
        faq_json=json.dumps(faq, ensure_ascii=False),
    )

    # Body content
    strengths_html = '\n'.join(f'    <li>{s}</li>' for s in data['strengths'])
    growth_html = '\n'.join(f'    <li>{s}</li>' for s in data['growth'])
    career_html = '\n'.join(f'    <li>{s}</li>' for s in data['career'])
    faq_html = '\n'.join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q,a in data['faq'])

    related = [m for m in [1,2,3,4,5,6,7,8,9] if m != n][:6]
    related_html = '\n'.join(
        f'    <a href="/name-number-{m}-meaning" class="nn-rel-card"><span class="eb">Name Number {m}</span><span class="ti">{NUMBERS[m]["planet"]} · {NUMBERS[m]["tagline"].split(" · ")[0]}</span></a>'
        for m in related
    )

    body = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/sitemap-pages">Numerology Guides</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">Name Number {n} Meaning</span>
</nav>

<header class="nn-hero">
  <div class="container">
    <div class="badge">Chaldean Numerology · Name Number {n}</div>
    <div class="glyph">{data["glyph"]}</div>
    <h1>Name Number {n} Meaning · The {data["planet"]} Vibration</h1>
    <div class="tag">{data["tagline"]}</div>
  </div>
</header>

<main class="nn-body">

  <p>{data["core"]}</p>

  <div class="nn-stat-row">
    <div class="nn-stat"><div class="lbl">Ruling Planet</div><div class="val">{data["glyph"]} {data["planet"]}</div></div>
    <div class="nn-stat"><div class="lbl">Lucky Colours</div><div class="val">{data["color"]}</div></div>
    <div class="nn-stat"><div class="lbl">Element</div><div class="val">{data["tagline"].split(" · ")[0]}</div></div>
  </div>

  <h2>What does name number {n} mean?</h2>
  <p>In Chaldean numerology, your <strong>name number</strong> is the single digit that your name's letters reduce to using the Chaldean letter-value table (A=1, B=2, C=3, D=4, E=5, F=8, G=3, H=5, I=1, J=1, K=2, L=3, M=4, N=5, O=7, P=8, Q=1, R=2, S=3, T=4, U=6, V=6, W=6, X=5, Y=1, Z=7). Sum every letter, reduce the total to one digit, and the planet that rules that digit is the planet that rules your daily expression.</p>

  <p>For name number {n}, that planet is <strong>{data["planet"]}</strong>. The vibration of {data["planet"]} carries themes of <em>{data["tagline"].lower()}</em>. Where your <em>Moolank</em> (day-of-birth number) describes how you naturally operate from within, your <em>Name Number</em> describes the vibration the world meets when they encounter you.</p>

  <h2>Core strengths of name number {n}</h2>
  <ul>
{strengths_html}
  </ul>

  <h2>Growth themes for name number {n}</h2>
  <p>Every name number has a recurring growth theme — not a problem to solve, but a pattern to notice with awareness. For name number {n}, the most common themes are:</p>
  <ul>
{growth_html}
  </ul>

  <h2>Best careers for name number {n}</h2>
  <p>Career fields that traditionally favour {data["planet"]} energy and reward the natural strengths of name number {n} include:</p>
  <ul>
{career_html}
  </ul>
  <p>This isn\'t a checklist — many name {n} people thrive outside these fields. The list captures the natural slope; working against it isn\'t a problem, but takes more conscious adjustment.</p>

  <h2>Compatibility for name number {n}</h2>
  <p>Compatibility in Chaldean numerology comes from how the ruling planets of two numbers interact. For name number {n}:</p>
  <ul>
    <li><strong>Strongest harmony:</strong> {", ".join(str(x) for x in data["compat_best"])}</li>
    <li><strong>Supportive:</strong> {", ".join(str(x) for x in data["compat_good"])}</li>
    <li><strong>Asks for awareness:</strong> {", ".join(str(x) for x in data["compat_caution"])}</li>
  </ul>
  <p>{data["famous"]}</p>

  <h2>How do I know if I\'m a name number {n}?</h2>
  <p>{data["how_known"]} If you don\'t want to do the math by hand, run the <a href="/name-numerology-calculator">free Chaldean Name Calculator</a> — it shows your letter-by-letter breakdown, the unreduced compound, the final reduced digit and the planet that rules it. The whole thing takes 15 seconds.</p>

  <div class="nn-cta-band">
    <h3>Find your exact name number in 15 seconds</h3>
    <p>Free Chaldean letter-by-letter calculation. No signup, no email required.</p>
    <div class="btn-pair">
      <a class="primary" href="/name-numerology-calculator">Calculate my name number →</a>
      <a class="outline" href="/analyzer">Full free analysis</a>
    </div>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="nn-faq">
{faq_html}
  </div>

  <div class="nn-cta-band">
    <h3>Want the complete picture?</h3>
    <p>The personalised destiny report covers your name number, Moolank, Bhagyank, name correction options, 5-year forecast, career and compatibility — all in one PDF.</p>
    <div class="btn-pair">
      <a class="primary" href="/report">Full Destiny Report · INR 199/-</a>
      <a class="outline" href="/blog/moolank-meanings">Read Moolank meanings</a>
    </div>
  </div>

  <h2>Related: name numbers 1–9</h2>
  <div class="nn-related">
    <div class="nn-related-grid">
{related_html}
    </div>
  </div>

</main>

{FOOTER}
'''
    return head + body


def main():
    for n, data in NUMBERS.items():
        out = os.path.join(OUT_DIR, f'name-number-{n}-meaning.html')
        with open(out, 'w') as f:
            f.write(render(n, data))
        words = len(re.findall(r'\b\w+\b', render(n, data)))
        print(f'wrote name-number-{n}-meaning.html (~{words} words including markup)')

if __name__ == '__main__':
    main()
