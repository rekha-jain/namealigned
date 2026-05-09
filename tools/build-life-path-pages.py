#!/usr/bin/env python3
"""
Generate /life-path-number-N-meaning pages (1-9) for SEO.

Life Path Number = full date of birth reduced to a single digit
(Chaldean equivalent: Bhagyank). High-volume English-keyword target
("life path number" ~ 100-500K monthly searches globally).

Each page is ~1100+ words, unique, with Article + BreadcrumbList +
FAQPage JSON-LD. Same template/style as build-name-number-pages.py
so the visual is consistent.
"""
import json, os, re

BASE = 'https://www.namealigned.com'
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NUMBERS = {
1:{'planet':'Sun','glyph':'☀','tagline':'Pioneering · Independence · Originality','color':'Gold · Orange · Red',
   'core':'Life Path Number 1 puts your destiny under the Sun. The long arc of your life pulls you toward originating things — building from zero, leading from the front, and refusing to live a life designed by someone else. The Sun rewards initiative, visibility and the willingness to be wrong in public.',
   'destiny':'Your destiny is built around firsts. You\'re the one starting the company, leaving the safe job, founding the movement. The work that compounds for you is the work that has your fingerprints on it — not the work where you\'re executing someone else\'s blueprint.',
   'strengths':[
     'Originality — you don\'t default to received wisdom','Decisive momentum once you\'ve thought it through','Comfort being the visible face of an idea','Long-term ambition that survives short-term setbacks','Willingness to start things alone'],
   'growth':[
     'Loneliness at the top — capable people often carry alone','Difficulty receiving help even when you genuinely need it','Impatience with people who can\'t move at your pace'],
   'career':['Founder / CEO roles','Government & Public Office','Independent practice (law, medicine, design)','Creative direction in entertainment / media','Gold, gemstone or luxury trade'],
   'compat_best':[1,2,4,9],'compat_good':[3,5,6],'compat_caution':[7,8],
   'midlife':'The 28–34 window typically marks the first major rebirth — old identities fall away, the real one steps forward.',
   'how':'Add every digit of your date of birth and reduce to one digit. e.g. 14 March 1992 → 1+4+0+3+1+9+9+2 = 29 → 2+9 = 11 → 1+1 = 2 (Life Path 2). Your number is the planet that rules your destiny themes.',
   'faq':[
     ('What is Life Path Number 1?','It\'s the destiny vibration of the Sun — leadership, originality, building things from zero. People with Life Path 1 tend to be drawn toward founder, creator and authority roles regardless of the field.'),
     ('Is Life Path 1 a good number?','Strongly so for ambitious work. The Sun is traditionally the most fortunate planet for visibility, recognition and influence. The cost is loneliness at the top, which Life Path 1 people learn to navigate over time.'),
     ('Who is compatible with Life Path 1?','Best harmony with Life Paths 1, 2, 4 and 9. Supportive with 3, 5, 6. 7 and 8 ask for more conscious adjustment.'),
     ('Can my Life Path Number change?','No — it\'s derived from your date of birth, which is fixed. What changes over a lifetime is how skilfully you express the vibration.'),
   ]},
2:{'planet':'Moon','glyph':'☾','tagline':'Sensitivity · Partnership · Emotional Wisdom','color':'White · Silver · Cream',
   'core':'Life Path Number 2 places your destiny under the Moon. The long arc of your life is built around relationships, emotional perception and the slow work of bringing people together. The Moon rewards patience, empathy and the ability to read what people aren\'t saying.',
   'destiny':'Your destiny is rarely solo. The work that compounds for you happens in partnership — with a co-founder, a spouse, a creative collaborator, or a community you patiently build. Your gift is sensing what a group needs before it asks.',
   'strengths':[
     'Empathic radar — you read rooms before others have spoken','Diplomatic by default; you bring people together','Imaginative inner life that fuels creative work','Patience with long-ripening processes','Loyal to a depth most people miss'],
   'growth':[
     'Absorbing other people\'s emotional states','Difficulty saying no when someone needs you','Decision fatigue when stakes feel personal'],
   'career':['Counselling & Psychology','Hospitality & Food','Music, Poetry & the Arts','Nursing & Caregiving','Residential Real Estate'],
   'compat_best':[1,2,7],'compat_good':[4,6,8],'compat_caution':[3,5,9],
   'midlife':'A relational re-rooting often happens between 28–32 — the partnerships that started in your 20s are tested or transformed.',
   'how':'Add every digit of your full date of birth and reduce to one digit. The result is your Life Path Number; the planet ruling that digit shapes your destiny themes. (Chaldean numerology calls this Bhagyank.)',
   'faq':[
     ('Is Life Path 2 emotional?','Yes — Moon energy amplifies emotional sensitivity. It\'s a creative gift in art, hospitality and counselling, and it asks for stronger emotional boundaries in high-friction environments.'),
     ('Is Life Path 2 lucky for marriage?','Generally yes — Moon energy is naturally relational. Best harmony with Life Paths 1, 2 and 7.'),
     ('What jobs suit Life Path 2?','Hospitality, food, the arts, counselling, nursing, residential real estate — fields where reading emotion is the value, not a side-effect.'),
     ('Why does Life Path 2 feel emotionally tiring?','The Moon\'s gift — emotional permeability — is also its cost. Daily decompression rituals (journaling, water, quiet) make the gift sustainable.'),
   ]},
3:{'planet':'Jupiter','glyph':'♃','tagline':'Expression · Optimism · Teaching','color':'Yellow · Cream · Violet',
   'core':'Life Path Number 3 carries Jupiter — the planet of expansion, teaching and abundance. Your destiny pulls you toward expressing ideas to wide audiences. Jupiter rewards generosity, optimism and the willingness to make complex things land warmly.',
   'destiny':'Your destiny is built around expression. The work that compounds for you involves teaching, writing, performing, publishing, advising — anything where your voice carries the value. Money tends to flow through Jupiter-aligned channels (education, finance, law, religion) rather than direct speculation.',
   'strengths':[
     'Verbal charisma — you make hard topics feel easy','Natural teacher; ideas land when you explain them','Optimistic without being naive','Wide social range across worlds','Creative output flows in bursts you can\'t fully plan'],
   'growth':[
     'Scattering across too many projects','Sounding most fine when you\'re least fine','Saying yes more than the calendar can hold'],
   'career':['Education & Teaching','Law & Justice','Banking & Finance','Religion / Spirituality','Publishing & Media'],
   'compat_best':[3,6,9],'compat_good':[1,5],'compat_caution':[2,4,8],
   'midlife':'The 30s tend to consolidate the platforms started in your 20s — the audience grows or it doesn\'t, and Jupiter rewards the years of patience either way.',
   'how':'Sum every digit of your date of birth, reduce to one digit. (In Chaldean numerology this is your Bhagyank.) Jupiter rules 3.',
   'faq':[
     ('Is Life Path 3 creative?','Strongly so — Jupiter expands expression. Life Path 3 people often write, teach, perform or run creative ventures.'),
     ('Is Life Path 3 lucky for money?','Jupiter is the traditional abundance planet, especially via teaching, publishing, law and finance. Direct speculation is less reliable than expansive long-term work.'),
     ('Why does Life Path 3 attract attention?','Jupiter expands. Whatever your name and presence carry get amplified outward — including the parts of yourself you didn\'t plan to put forward.'),
     ('Which numbers harmonise with Life Path 3?','3, 6 and 9 form Jupiter\'s strongest triangle. 1 and 5 are supportive.'),
   ]},
4:{'planet':'Rahu','glyph':'◈','tagline':'Innovation · Foreign Reach · System Building','color':'Blue · Electric · Grey',
   'core':'Life Path Number 4 carries Rahu — the unconventional, future-leaning, pattern-spotting energy. Your destiny pulls you into territories most people consider too risky or too strange. Rahu rewards builders of systems, technologies and methods that don\'t yet exist.',
   'destiny':'Your destiny is built around the unfamiliar — foreign markets, emerging technologies, immigrant journeys, founders\' problems no playbook covers. The work that compounds for you is the work that requires a new mental model, not an optimised one.',
   'strengths':[
     'Pattern vision — you spot what others overlook','Comfort with the unconventional','Calm under disruption others find unbearable','Quietly reliable for things that matter long-term','Original thinker; you don\'t default to consensus'],
   'growth':[
     'Misread as "difficult" by people who don\'t want to be questioned','Restlessness when systems become rigid','Abrupt shifts that test stability'],
   'career':['Engineering & Architecture','IT & Technology','Research & Analysis','Logistics & Supply Chain','Foreign Trade / Aviation'],
   'compat_best':[1,2,4,8],'compat_good':[6,7],'compat_caution':[3,5,9],
   'midlife':'A foreign or industry pivot is common between 28–35 — Rahu rewards the move outward.',
   'how':'Sum every digit of your DOB, reduce to one. (Chaldean: Bhagyank.) Rahu (the north node) rules 4.',
   'faq':[
     ('Is Life Path 4 unlucky?','No — the reputation comes from Rahu being misunderstood. Used well, Life Path 4 thrives in tech, foreign trade and research-heavy fields.'),
     ('Should I avoid Life Path 4?','You can\'t — it\'s your DOB. The vibration is genuinely powerful in change-friendly environments.'),
     ('What careers suit Life Path 4?','Tech, engineering, research, foreign trade, aviation — anything that rewards original thinking over conformity.'),
     ('Why does Life Path 4 feel like an outsider?','Rahu gives an unusual angle of perception. Outsider status is often the source of the very insight that makes you valuable.'),
   ]},
5:{'planet':'Mercury','glyph':'☿','tagline':'Adaptability · Communication · Movement','color':'Green · Light Grey',
   'core':'Life Path Number 5 carries Mercury — speed, adaptability, wit and the ability to learn anything quickly. Your destiny is non-linear; the path twists, branches and changes shape, and the work that compounds is the work where speed of communication is the value.',
   'destiny':'Your destiny is built around movement — geographic, intellectual, professional. Mercury rewards the polymath, the trader, the journalist, the founder who pivots before others have noticed the shift.',
   'strengths':[
     'Quick mind — you absorb at unusual speed','Conversational charisma','Versatility across worlds','Curiosity at scale','Trade and negotiation come naturally'],
   'growth':[
     'Losing interest before things mature','Restlessness in slow-moving environments','Mental overstimulation — too many tabs open'],
   'career':['Media & Journalism','Sales & Marketing','Travel & Tourism','Stock Trading','Digital Startups'],
   'compat_best':[1,5,9],'compat_good':[3,6],'compat_caution':[2,4,8],
   'midlife':'A late-20s pivot is often dramatic — Mercury rewards the move that mattered, even when it looked rash from outside.',
   'how':'Sum every digit of your DOB, reduce to one. (Chaldean: Bhagyank.) Mercury rules 5.',
   'faq':[
     ('Is Life Path 5 good for business?','Particularly trade, media, marketing, agency work — anything that rewards speed of communication.'),
     ('Is Life Path 5 a stable number?','Mobile by nature. Stability comes from rituals you choose, not from the vibration itself.'),
     ('What\'s the downside of Life Path 5?','Inability to slow down when slowing down would help — projects abandoned mid-maturation.'),
     ('Which numbers pair well with Life Path 5?','1, 5 and 9 are strongest; 3 and 6 add expansion and harmony.'),
   ]},
6:{'planet':'Venus','glyph':'♀','tagline':'Harmony · Love · Aesthetic Wisdom','color':'Pink · White · Pastel Blue',
   'core':'Life Path Number 6 sits under Venus — beauty, harmony, relationship, aesthetic instinct. Your destiny is built around making people and spaces feel held; the work that compounds is the work where care and aesthetic taste are central, not decorative.',
   'destiny':'Venus rewards devotion, aesthetic mastery and relational fluency. Your destiny pulls you toward partnerships (romantic, creative, professional) and toward fields where beauty has commercial value — design, hospitality, entertainment, cosmetics, social work.',
   'strengths':[
     'Emotional fluency — you name what others can\'t articulate','Aesthetic instinct in design, dress, food, space','Devoted in relationships','Caretaker presence that holds groups','Strong sense of fairness'],
   'growth':[
     'Holding everyone together while no-one asks who holds you','Difficulty saying no to people you love','Idealising partners until reality intrudes'],
   'career':['Fashion & Design','Entertainment & Film','Hospitality','Cosmetics & Beauty','Social Work / NGO'],
   'compat_best':[3,6,9],'compat_good':[1,4,5],'compat_caution':[2,7,8],
   'midlife':'A relationship recalibration is typical in the late 20s — Venus rewards depth, not novelty.',
   'how':'Sum every digit of your DOB, reduce to one. (Chaldean: Bhagyank.) Venus rules 6.',
   'faq':[
     ('Is Life Path 6 the love number?','Often called that. Venus rules relationship and aesthetic harmony — Life Path 6 people gravitate toward partnership and beauty in everything they do.'),
     ('What jobs suit Life Path 6?','Design, fashion, entertainment, hospitality, cosmetics, social work — fields where care and aesthetic taste are central.'),
     ('Which numbers pair well with Life Path 6?','3, 6 and 9 are strongest. 1, 4 and 5 are supportive.'),
     ('Is Life Path 6 too people-pleasing?','It can tip there. The growth work is learning where care ends and self-erasure begins.'),
   ]},
7:{'planet':'Ketu','glyph':'◉','tagline':'Wisdom · Inquiry · Solitude','color':'Violet · Purple · Grey',
   'core':'Life Path Number 7 carries Ketu — the south-node energy of detachment, depth and inner inquiry. Your destiny is built around understanding; the work that compounds is research-heavy, depth-rewarding, and rarely glamorous in the moment.',
   'destiny':'Ketu rewards inner stillness over outer noise. Your destiny pulls you toward research, spirituality, philosophy, writing, academia — fields where solitude isn\'t a problem to fix but a tool to use.',
   'strengths':[
     'Deep insight — you research thoroughly','Independent mind; you trust your own conclusions','Calm under pressure','Discernment — you see through performances','Spiritual or philosophical orientation that grounds you'],
   'growth':[
     'Over-thinking the final decision','Distance read as coldness when it\'s actually protection','Difficulty trusting people quickly'],
   'career':['Research & Science','Spirituality & Healing','Writing & Literature','Astrology & Mysticism','Philosophy & Academia'],
   'compat_best':[2,7],'compat_good':[1,4,6],'compat_caution':[3,5,8,9],
   'midlife':'A retreat or sabbatical is common in the 30s — Ketu rewards the pause others find uncomfortable.',
   'how':'Sum every digit of your DOB, reduce to one. (Chaldean: Bhagyank.) Ketu (south node) rules 7.',
   'faq':[
     ('Is Life Path 7 spiritual?','Strongly so. Ketu pulls toward inner inquiry — Life Path 7 people often have a contemplative or research-driven thread running through their work.'),
     ('Is Life Path 7 lucky for marriage?','Best with Life Paths 2 and 7. Otherwise marriage works when both partners respect the alone-time the vibration needs.'),
     ('What career suits Life Path 7?','Research-heavy, depth-rewarding fields — science, spirituality, writing, academia.'),
     ('Why does Life Path 7 prefer solitude?','Ketu rewards inner stillness. Solitude is how the vibration regenerates.'),
   ]},
8:{'planet':'Saturn','glyph':'♄','tagline':'Discipline · Authority · Long Game','color':'Black · Dark Blue · Dark Grey',
   'core':'Life Path Number 8 sits under Saturn — discipline, structure, long-game ambition and earned authority. Your destiny is slow-cooked; the work that compounds takes years longer than your peers\' breakthroughs, but the authority it builds is more durable.',
   'destiny':'Saturn rewards endurance. Your destiny is built around playing long games — finance, law, real estate, heavy industry, infrastructure. Quick wins don\'t fit; the breakthrough usually arrives after the recognition you deserved years earlier.',
   'strengths':[
     'Strategic — you play long games','Resilient when others panic','Accountable; your word is your reputation','Endurance for projects that take years','Authority earned, not assumed'],
   'growth':[
     'Frustration before recognition arrives','Looking composed while carrying weight nobody sees','Slow trust — relationships take time to deepen'],
   'career':['Finance & Banking','Law & Courts','Mining & Heavy Industry','Import/Export','Real Estate Investment'],
   'compat_best':[2,4,6,8],'compat_good':[1,7],'compat_caution':[3,5,9],
   'midlife':'The first big Saturn return in the late 20s tests everything. Past the test, authority becomes real and earned.',
   'how':'Sum every digit of your DOB, reduce to one. (Chaldean: Bhagyank.) Saturn rules 8.',
   'faq':[
     ('Is Life Path 8 unlucky?','No, but it\'s slow. Saturn rewards discipline and patience; quick-win approaches don\'t fit. Used well, Life Path 8 builds enduring authority.'),
     ('Is Life Path 8 good for business?','Yes — particularly finance, law, real estate, heavy industry and import-export. Less suited to fast-moving consumer or media careers.'),
     ('Why does Life Path 8 feel heavy?','Saturn carries weight by design. The weight is what makes the eventual authority real, but it asks for endurance.'),
     ('Which numbers pair well with Life Path 8?','2, 4, 6 and 8. Saturn-ruled pairings benefit from at least one Moon-ruled (2) partner who softens the structure.'),
   ]},
9:{'planet':'Mars','glyph':'♂','tagline':'Courage · Service · Decisive Action','color':'Red · Crimson · Deep Orange',
   'core':'Life Path Number 9 carries Mars — fire, courage, decisive action and protective force. Your destiny is built around movement that requires nerve; the work that compounds is the work others were too cautious to attempt.',
   'destiny':'Mars rewards action under pressure. Your destiny pulls you toward defense, surgery, sports, activism, politics — roles where decisive movement and the ability to handle physical or emotional intensity are the value, not a side-effect.',
   'strengths':[
     'Bold — you move first while others wait','Protective of the people you love','Driven; your fire fuels everyone around you','Courage in action under pressure','Cuts through noise and gets to the point'],
   'growth':[
     'Felt at a volume the world keeps asking you to turn down','Crash-and-recovery rhythm in long projects','Impatience with slow-moving environments'],
   'career':['Military & Defense','Surgery & Medicine','Sports & Athletics','Politics','Social Activism / NGO'],
   'compat_best':[1,3,5,9],'compat_good':[6,7],'compat_caution':[2,4,8],
   'midlife':'The early 30s often involve a "fight worth fighting" — Mars rewards the cause you don\'t walk away from.',
   'how':'Sum every digit of your DOB, reduce to one. (Chaldean: Bhagyank.) Mars rules 9.',
   'faq':[
     ('Is Life Path 9 aggressive?','Energetic, not aggressive. Mars used well is courage and protection; misused it tips into unnecessary conflict.'),
     ('What jobs suit Life Path 9?','Defense, surgery, sports, activism, politics — roles requiring decisive action.'),
     ('Which numbers pair well with Life Path 9?','1, 3, 5 and 9. Fire-and-air combinations work; earth-and-water (2, 4, 8) ask for conscious effort.'),
     ('Why does Life Path 9 burn out?','Mars runs hot. Crash-and-recovery rhythms are healthy when planned; toxic when ignored.'),
   ]},
}

HEAD_TEMPLATE = '''<!DOCTYPE html>
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
<meta name="keywords" content="life path number {n}, life path {n} meaning, life path {n} {planet_lower}, destiny number {n}, bhagyank {n}, life path number {n} career, life path {n} compatibility"/>
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
      <div><div class="footer-col-title">Guides</div><ul class="footer-links"><li><a href="/blog/chaldean-numerology-guide">Chaldean Guide</a></li><li><a href="/blog/moolank-meanings">Birth Number Meanings</a></li><li><a href="/blog/personal-year-guide">Personal Year</a></li><li><a href="/blog/name-correction-guide">Name Correction</a></li><li><a href="/blog/compound-numbers-cheiro">Compound Numbers</a></li><li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid</a></li></ul></div>
      <div><div class="footer-col-title">More</div><ul class="footer-links"><li><a href="/blog">All Articles</a></li><li><a href="/about">About</a></li><li><a href="/sitemap-pages">Site Map</a></li><li><a href="/privacy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/refund">Refund</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 NameAligned.com</span><span>Made with <span style="color:#e8526b;">❤</span> in India</span></div>
  </div>
</footer>
</body>
</html>
'''

def render(n, data):
    title = f'Life Path Number {n} Meaning · Destiny, Career & Compatibility ({data["planet"]})'
    desc = f'Life Path Number {n} carries {data["planet"]} energy — {data["tagline"].lower()}. The destiny themes, career paths, compatibility and growth lessons of Life Path {n}, in plain English. Free Chaldean check at the bottom.'
    og_desc = f'Life Path Number {n} ({data["planet"]}) decoded — destiny themes, career, compatibility and growth.'
    canon = f'{BASE}/life-path-number-{n}-meaning'

    article = {
        "@context":"https://schema.org","@type":"Article","headline":title,
        "description":desc,"url":canon,"datePublished":"2026-02-15","dateModified":"2026-05-06",
        "author":{"@type":"Organization","name":"NameAligned.com","url":BASE+"/"},
        "publisher":{"@type":"Organization","name":"NameAligned.com","url":BASE+"/","logo":{"@type":"ImageObject","url":BASE+"/assets/namealigned-logo-full.svg"}},
        "inLanguage":"en-IN","mainEntityOfPage":{"@type":"WebPage","@id":canon}
    }
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Numerology Guides","item":BASE+"/sitemap-pages"},
        {"@type":"ListItem","position":3,"name":f"Life Path Number {n} Meaning","item":canon}
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

    strengths_html = '\n'.join(f'    <li>{s}</li>' for s in data['strengths'])
    growth_html    = '\n'.join(f'    <li>{s}</li>' for s in data['growth'])
    career_html    = '\n'.join(f'    <li>{s}</li>' for s in data['career'])
    faq_html       = '\n'.join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q,a in data['faq'])

    related = [m for m in [1,2,3,4,5,6,7,8,9] if m != n][:6]
    related_html = '\n'.join(
        f'    <a href="/life-path-number-{m}-meaning" class="nn-rel-card"><span class="eb">Life Path {m}</span><span class="ti">{NUMBERS[m]["planet"]} · {NUMBERS[m]["tagline"].split(" · ")[0]}</span></a>'
        for m in related
    )

    body = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/sitemap-pages">Numerology Guides</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">Life Path Number {n} Meaning</span>
</nav>

<header class="nn-hero">
  <div class="container">
    <div class="badge">Chaldean Numerology · Life Path {n}</div>
    <div class="glyph">{data["glyph"]}</div>
    <h1>Life Path Number {n} Meaning · Destiny Under {data["planet"]}</h1>
    <div class="tag">{data["tagline"]}</div>
  </div>
</header>

<main class="nn-body">

  <p>{data["core"]}</p>

  <div class="nn-stat-row">
    <div class="nn-stat"><div class="lbl">Ruling Planet</div><div class="val">{data["glyph"]} {data["planet"]}</div></div>
    <div class="nn-stat"><div class="lbl">Lucky Colours</div><div class="val">{data["color"]}</div></div>
    <div class="nn-stat"><div class="lbl">Vibration</div><div class="val">{data["tagline"].split(" · ")[0]}</div></div>
  </div>

  <h2>What does Life Path Number {n} mean?</h2>
  <p>Your <strong>Life Path Number</strong> is the single digit your full date of birth reduces to. In Indian Chaldean numerology this is also called <em>Bhagyank</em> — same number, different name. Where your <em>Birth Number</em> (day of birth, also called Moolank) shapes your daily expression, your <em>Life Path Number</em> shapes the long-arc themes of your life.</p>

  <p>For Life Path {n}, the ruling planet is <strong>{data["planet"]}</strong>. The vibration carries themes of <em>{data["tagline"].lower()}</em>. {data["destiny"]}</p>

  <h2>Strengths of Life Path Number {n}</h2>
  <ul>
{strengths_html}
  </ul>

  <h2>Growth themes for Life Path {n}</h2>
  <p>Every Life Path Number carries a recurring growth theme — not a problem to solve, but a pattern to notice with awareness. For Life Path {n}, the most common are:</p>
  <ul>
{growth_html}
  </ul>

  <h2>Best careers for Life Path {n}</h2>
  <p>Career fields traditionally favoured by {data["planet"]} energy and rewarding the natural strengths of Life Path {n}:</p>
  <ul>
{career_html}
  </ul>
  <p>This isn\'t a checklist — many Life Path {n} people thrive outside these fields. The list captures the natural slope; working against it isn\'t a problem, but takes more conscious adjustment.</p>

  <h2>Compatibility for Life Path {n}</h2>
  <p>Compatibility in Chaldean numerology comes from how the ruling planets of two numbers interact:</p>
  <ul>
    <li><strong>Strongest harmony:</strong> {", ".join(str(x) for x in data["compat_best"])}</li>
    <li><strong>Supportive:</strong> {", ".join(str(x) for x in data["compat_good"])}</li>
    <li><strong>Asks for awareness:</strong> {", ".join(str(x) for x in data["compat_caution"])}</li>
  </ul>

  <h2>Mid-life turning points</h2>
  <p>{data["midlife"]}</p>

  <h2>How to calculate your Life Path Number</h2>
  <p>{data["how"]}</p>
  <p>If you\'d rather skip the math, the <a href="/analyzer">free Chaldean analyser</a> calculates your Birth Number, Life Path Number and Name Number in 15 seconds, plus an alignment score that tells you how well your name supports your destiny.</p>

  <div class="nn-cta-band">
    <h3>Calculate yours in 15 seconds</h3>
    <p>Free Chaldean analysis — Birth Number, Life Path Number, Name Number and alignment score. No signup.</p>
    <div class="btn-pair">
      <a class="primary" href="/analyzer">Run my free analysis →</a>
      <a class="outline" href="/name-numerology-calculator">Just calculate name number</a>
    </div>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="nn-faq">
{faq_html}
  </div>

  <div class="nn-cta-band">
    <h3>Want the complete picture?</h3>
    <p>The personalised destiny report covers your Birth Number, Life Path Number, Name Number, name correction options, 5-year forecast and compatibility — all in one PDF.</p>
    <div class="btn-pair">
      <a class="primary" href="/report">Full Destiny Report · INR 199/-</a>
      <a class="outline" href="/blog/chaldean-numerology-guide">Read Chaldean guide</a>
    </div>
  </div>

  <h2>Related: Life Path Numbers 1–9</h2>
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
        out = os.path.join(OUT_DIR, f'life-path-number-{n}-meaning.html')
        with open(out, 'w') as f:
            f.write(render(n, data))
    print(f'wrote 9 life-path-number-N-meaning pages')

if __name__ == '__main__':
    main()
