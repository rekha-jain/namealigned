#!/usr/bin/env python3
"""
Generate the /number/{n}-personality cluster (1-9) for SEO.

Different angle from /name-number-{n}-meaning: this page treats Number N
as an archetype — anyone whose Birth, Life Path or Name reduces to N
shows these patterns — rather than focusing on the name reduction
specifically. That keeps unique content vs the existing name-number pages.

Run:
    python3 tools/build-number-cluster.py

Output: number/1-personality.html ... number/9-personality.html
URLs (with cleanUrls): /number/1-personality ... /number/9-personality
"""
import json, os, re, importlib.util, sys

BASE = 'https://www.namealigned.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'number')

# Pull the shared NUMBERS data dict from the existing builder so we don't
# duplicate truth. The existing module has rich per-number data already.
spec = importlib.util.spec_from_file_location(
    'name_number_pages',
    os.path.join(ROOT, 'tools', 'build-name-number-pages.py')
)
nnm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nnm)
BASE_NUMBERS = nnm.NUMBERS

# Personality-page extension data — content that's distinct from the
# name-number pages. Each entry is ADDITIONAL prose written specifically
# for the archetype/personality angle.
PERSONALITY = {
1:{'archetype':'The Originator',
   'tldr':'Number 1 in Chaldean numerology is the Sun-ruled archetype of the originator. People in this signature start things others only talk about, hold their own counsel, and lead by deciding before others have finished weighing options. Strengths cluster around agency and visibility; the shadow shows up as loneliness at the top.',
   'shadow':['Difficulty asking for help — receiving feels foreign','Dismissing slower thinkers as obstacles rather than collaborators','Confusing being right with being effective'],
   'love':'In love, Number 1 leads — the partner often discovers they\'ve agreed to a direction without quite meaning to. The match works when the other person is settled enough not to compete, and warm enough to soften the Sun\'s relentlessness. Best heat: with 2 (Moon — softens), 4 (Rahu — magnetic friction), 9 (Mars — fellow fire).',
   'lucky':{'days':'Sunday, Monday','stones':'Ruby, Yellow Sapphire','metals':'Gold','mantra':'Om Suryaya Namaha'},
   'famous_arch':'Founders, monarchs, signature artists — anyone whose work bears their personal stamp tends to carry Number 1 somewhere in their numerology.',
   'snippet':'In Chaldean numerology, Number 1 is the Sun-ruled archetype of leadership and origination. People with this signature in their birth, name or life path tend to be decisive, visible and naturally founder-shaped. Their lucky colours are gold and red, lucky day is Sunday, and they harmonise best with numbers 2, 4 and 9.',
   'extra_faq':[
     ('Is Number 1 a leader or a loner?','Both. The Sun puts you front-of-stage, but the same energy that draws people also keeps decisions on your shoulders alone.'),
     ('What does Number 1 mean for life path?','A life path 1 means the soul-curriculum is independence and originating. You\'re here to start things, not maintain them.'),
   ]},
2:{'archetype':'The Diplomat',
   'tldr':'Number 2 in Chaldean numerology is the Moon-ruled archetype of the diplomat. People in this signature read rooms before others have finished speaking, build trust through consistency, and carry an emotional permeability that\'s a creative gift in some rooms and a tax in others. Strengths cluster around empathy and harmony; the shadow shows up as boundary fatigue.',
   'shadow':['Saying yes when the body has already said no','Mistaking other people\'s emotions for your own','Indecision when stakes feel too personal'],
   'love':'In love, Number 2 attunes — your partner feels seen in ways they can\'t quite name. The match works when the other person can match your emotional depth without flooding you, and respects the quiet hours you need to regenerate. Best heat: with 1 (Sun — anchors), 2 (Moon — twin understanding), 7 (Ketu — both inner-facing).',
   'lucky':{'days':'Monday, Friday','stones':'Pearl, Moonstone','metals':'Silver','mantra':'Om Chandraya Namaha'},
   'famous_arch':'Therapists, hospitality founders, poets, hostesses, family-business stewards — Moon energy tends to gravitate to work that touches people\'s emotional life directly.',
   'snippet':'In Chaldean numerology, Number 2 is the Moon-ruled archetype of empathy and harmony. People with this signature in their birth, name or life path are intuitive, diplomatic and emotionally perceptive. Their lucky colours are white and silver, lucky day is Monday, and they harmonise best with numbers 1, 2 and 7.',
   'extra_faq':[
     ('Is Number 2 emotionally fragile?','Permeable, not fragile. The same sensitivity that makes Moon energy creative also asks for stronger boundary-keeping than other numbers need.'),
     ('Does Number 2 work for leaders?','Yes — quietly. Moon-ruled leaders pull through rapport and patience rather than command, which often outlasts louder leadership styles.'),
   ]},
3:{'archetype':'The Communicator',
   'tldr':'Number 3 in Chaldean numerology is the Jupiter-ruled archetype of the communicator. People in this signature make complex ideas land warmly, hold rooms with their voice, and turn social capital into opportunity without trying. Strengths cluster around expression and optimism; the shadow shows up as scattered output and sounding the most fine when you\'re the least fine.',
   'shadow':['Spreading thin across too many parallel projects','Performing okayness publicly while privately overwhelmed','Leaving the boring follow-through to whoever\'s nearby'],
   'love':'In love, Number 3 charms — your partner often falls for the way you make life feel bigger. The match works when the other person finds your social rhythm energising rather than draining, and can hold steadiness while you spark. Best heat: with 3 (Jupiter — twin breadth), 6 (Venus — beauty + warmth), 9 (Mars — fire-on-fire).',
   'lucky':{'days':'Thursday, Friday','stones':'Yellow Sapphire, Topaz','metals':'Gold, Brass','mantra':'Om Brihaspataye Namaha'},
   'famous_arch':'Teachers, judges, religious figures, broadcasters, popular writers — Jupiter rules the people who turn knowledge into accessible wisdom for others.',
   'snippet':'In Chaldean numerology, Number 3 is the Jupiter-ruled archetype of communication and joy. People with this signature in their birth, name or life path are expressive, optimistic and naturally teacher-shaped. Their lucky colours are yellow and violet, lucky day is Thursday, and they harmonise best with numbers 3, 6 and 9.',
   'extra_faq':[
     ('Is Number 3 the luckiest?','Often described that way because Jupiter is the planet of expansion, but luck still depends on whether your other numbers (Moolank, Bhagyank) harmonise.'),
     ('Why does Number 3 attract attention?','Jupiter amplifies whatever it touches. The vibration makes ideas — and the person delivering them — feel bigger than the room.'),
   ]},
4:{'archetype':'The Architect',
   'tldr':'Number 4 in Chaldean numerology is the Rahu-ruled archetype of the architect — restless, magnetic, drawn to systems and to disruption simultaneously. People in this signature build differently than they\'re told to, see patterns others miss, and carry an unmistakable intensity. Strengths cluster around lateral thinking and unconventional building; the shadow shows up as inner restlessness.',
   'shadow':['Resisting structure even when structure would help you','Burning bridges that took years to build','Confusing intensity with intimacy'],
   'love':'In love, Number 4 magnetises — there\'s a pull people can\'t fully explain. The match works when the partner is grounded enough not to be destabilised by your restlessness, and curious enough to keep up with the lateral angles your mind takes. Best heat: with 1 (Sun — anchoring), 5 (Mercury — fellow improviser), 8 (Saturn — stabilises Rahu).',
   'lucky':{'days':'Sunday, Saturday','stones':'Hessonite (Gomed)','metals':'Iron, Mixed alloys','mantra':'Om Rahave Namaha'},
   'famous_arch':'Inventors, contrarian founders, system-disruptors, unconventional artists — Rahu rules people who don\'t fit existing categories and end up creating new ones.',
   'snippet':'In Chaldean numerology, Number 4 is the Rahu-ruled archetype of the system-disruptor. People with this signature are restless, magnetic and naturally lateral thinkers. Their lucky day is Sunday, lucky stone is hessonite, and they harmonise best with numbers 1, 5 and 8.',
   'extra_faq':[
     ('Is Number 4 unlucky?','That\'s a common misconception. Rahu energy is intense and unconventional — it asks for awareness, not avoidance. Used well it builds entirely new categories.'),
     ('Why does Number 4 attract conflict?','Because Rahu sees the truth others avoid naming. The conflict isn\'t the energy — it\'s the willingness to surface what\'s being suppressed.'),
   ]},
5:{'archetype':'The Improviser',
   'tldr':'Number 5 in Chaldean numerology is the Mercury-ruled archetype of the improviser. People in this signature think fast, switch contexts faster, and turn information into leverage almost reflexively. Strengths cluster around adaptability and quick synthesis; the shadow shows up as restlessness, scattered focus and a fear of finishing.',
   'shadow':['Starting more than you can carry to the finish line','Mistaking novelty for progress','Restlessness that mistakes itself for boredom'],
   'love':'In love, Number 5 sparkles — your partner is rarely bored. The match works when the other person values mental match over emotional intensity, and gives you breathing space without taking it personally. Best heat: with 1 (Sun — gives direction), 5 (Mercury — twin pace), 9 (Mars — fire and movement).',
   'lucky':{'days':'Wednesday, Friday','stones':'Emerald','metals':'Bronze, Silver-mixed','mantra':'Om Budhaya Namaha'},
   'famous_arch':'Traders, journalists, multi-hyphenate creators, comedians, entrepreneurs who pivot well — Mercury rules everyone who works in fast-information environments.',
   'snippet':'In Chaldean numerology, Number 5 is the Mercury-ruled archetype of the improviser. People with this signature are quick-thinking, adaptable and naturally suited to information-rich, fast-moving fields. Their lucky day is Wednesday, lucky stone is emerald, and they harmonise best with numbers 1, 5 and 9.',
   'extra_faq':[
     ('Is Number 5 the most successful?','Often the most adaptable, which translates to success in fast-changing fields. Less suited to slow, deep, single-domain mastery — that\'s 7\'s territory.'),
     ('Why does Number 5 get bored?','Mercury\'s natural pace is fast. Boredom is a signal to pivot, not a flaw — but pivoting too often without finishing erodes long-term trust.'),
   ]},
6:{'archetype':'The Harmoniser',
   'tldr':'Number 6 in Chaldean numerology is the Venus-ruled archetype of the harmoniser. People in this signature draw beauty, ease and care into the rooms they enter, build relationships that last, and carry an aesthetic sensibility others quietly defer to. Strengths cluster around warmth and design; the shadow shows up as people-pleasing and inability to disappoint.',
   'shadow':['Saying yes to keep peace, then resenting it','Avoiding hard conversations until the friction is unsolvable','Mistaking aesthetics for substance'],
   'love':'In love, Number 6 envelops — the partner feels chosen and cared for. The match works when the other person can receive without losing themselves, and bring directness when your harmonising goes too far. Best heat: with 3 (Jupiter — warmth + warmth), 6 (Venus — twin softness), 9 (Mars — directness balances).',
   'lucky':{'days':'Friday, Tuesday','stones':'Diamond, White Sapphire','metals':'Silver, Platinum','mantra':'Om Shukraya Namaha'},
   'famous_arch':'Designers, hospitality leaders, family-business stewards, artists, peacemakers — Venus rules everyone whose work creates atmosphere others want to live inside.',
   'snippet':'In Chaldean numerology, Number 6 is the Venus-ruled archetype of harmony and beauty. People with this signature are nurturing, aesthetic and naturally relationship-builders. Their lucky day is Friday, lucky stone is diamond, and they harmonise best with numbers 3, 6 and 9.',
   'extra_faq':[
     ('Is Number 6 about love?','Partly — Venus rules love and aesthetics. But Number 6 is broader: it\'s about creating environments others want to be in, romantic or not.'),
     ('Does Number 6 mean family-oriented?','Often, yes. The vibration is naturally domestic and protective; many Number 6 people build careers around family, hospitality or care-giving even when they don\'t plan to.'),
   ]},
7:{'archetype':'The Mystic',
   'tldr':'Number 7 in Chaldean numerology is the Ketu-ruled archetype of the mystic — inward-facing, research-driven, comfortable in solitude that other numbers find unbearable. People in this signature go deep where others go wide. Strengths cluster around intuition and original thought; the shadow shows up as withdrawal, over-thinking and reading distance as coldness.',
   'shadow':['Disappearing for days inside your own head','Reading silence as rejection rather than space','Rejecting communities that would actually have you'],
   'love':'In love, Number 7 is quiet and exact — the partner is chosen carefully, and once chosen is held with rare loyalty. The match works when the other person doesn\'t mistake your alone-time for absence, and brings warmth without flooding. Best heat: with 2 (Moon — emotional fluency), 7 (Ketu — twin depth), 4 (Rahu — same axis, different angle).',
   'lucky':{'days':'Monday, Sunday','stones':'Cat\'s Eye (Lehsunia)','metals':'Mixed alloys','mantra':'Om Ketave Namaha'},
   'famous_arch':'Researchers, theologians, mystics, scientists, contemplative writers, monks — Ketu rules everyone whose work requires going inward to bring something out.',
   'snippet':'In Chaldean numerology, Number 7 is the Ketu-ruled archetype of the mystic. People with this signature are introspective, research-driven and deeply intuitive. Their lucky day is Monday, lucky stone is cat\'s eye, and they harmonise best with numbers 2, 7 and 4.',
   'extra_faq':[
     ('Is Number 7 anti-social?','Not anti-social — selectively social. The vibration regenerates in solitude rather than crowds, but loyalty to chosen people runs deep.'),
     ('Why does Number 7 feel different?','Ketu sits outside the usual planetary harmonies, so the vibration runs on a different frequency from the others. That difference is the gift — and the cost.'),
   ]},
8:{'archetype':'The Builder',
   'tldr':'Number 8 in Chaldean numerology is the Saturn-ruled archetype of the builder — patient, structured, ambitious in time-frames most numbers can\'t hold. People in this signature play long games, earn rather than borrow authority, and carry weight others sense before knowing why. Strengths cluster around resilience and discipline; the shadow shows up as carrying weight invisibly until it cracks.',
   'shadow':['Staying composed past the point where help would actually help','Confusing endurance with health','Slow trust read by others as coldness'],
   'love':'In love, Number 8 commits — slowly, but completely. The partner is chosen for substance, not surface, and once chosen is built around. The match works when the other person can match your time-horizon, and brings lightness without expecting you to perform it. Best heat: with 2 (Moon — softens Saturn), 4 (Rahu — same heaviness, different axis), 8 (Saturn — twin endurance).',
   'lucky':{'days':'Saturday, Friday','stones':'Blue Sapphire (Neelam)','metals':'Iron, Steel','mantra':'Om Shanicharaya Namaha'},
   'famous_arch':'Long-game founders, judges, central bankers, real-estate empires, infrastructure builders — Saturn rules everyone whose authority compounds over decades rather than years.',
   'snippet':'In Chaldean numerology, Number 8 is the Saturn-ruled archetype of the builder. People with this signature are disciplined, resilient and naturally suited to long-game endeavours. Their lucky day is Saturday, lucky stone is blue sapphire, and they harmonise best with numbers 2, 4 and 8.',
   'extra_faq':[
     ('Is Number 8 unlucky?','No, but it\'s slow. Saturn rewards endurance over speed. Used well, the eventual authority is rare and lasting; mismanaged, the same energy stalls and isolates.'),
     ('Why does Number 8 attract delays?','Saturn\'s curriculum is patience and structure. Delays aren\'t obstacles — they\'re the energy testing whether you\'ll stay disciplined long enough to deserve the result.'),
   ]},
9:{'archetype':'The Warrior',
   'tldr':'Number 9 in Chaldean numerology is the Mars-ruled archetype of the warrior — courage, decisiveness, protective force. People in this signature move first, finish what others can\'t face, and carry heat into rooms whether they mean to or not. Strengths cluster around bold action and protection; the shadow shows up as exhaustion, crash-and-recovery cycles and impatience with slow environments.',
   'shadow':['Finishing on willpower past the point of recovery','Reading slowness as weakness rather than caution','Going to war over things that didn\'t need a war'],
   'love':'In love, Number 9 protects — the partner feels safer than they did before. The match works when the other person doesn\'t need you to lower your volume to be loved, and can hold steadiness while you burn. Best heat: with 1 (Sun — twin authority), 3 (Jupiter — fire + breadth), 5 (Mercury — fire + speed).',
   'lucky':{'days':'Tuesday, Friday','stones':'Red Coral','metals':'Iron, Copper','mantra':'Om Mangalaya Namaha'},
   'famous_arch':'Soldiers, surgeons, athletes, activists, decisive political leaders, fire-fighters — Mars rules everyone whose work requires moving first under pressure.',
   'snippet':'In Chaldean numerology, Number 9 is the Mars-ruled archetype of courage and decisive action. People with this signature are bold, protective and naturally suited to high-pressure decisive roles. Their lucky day is Tuesday, lucky stone is red coral, and they harmonise best with numbers 1, 3 and 5.',
   'extra_faq':[
     ('Is Number 9 aggressive?','Energetic, not aggressive. Mars used well is courage and protection; misused it tips into unnecessary conflict. The vibration asks for a cause worth the heat.'),
     ('Why does Number 9 burn out?','Because the same fire that fuels action also depletes reserves faster than other numbers. Recovery rhythms aren\'t optional — they\'re the price of sustained Mars energy.'),
   ]},
}


HEAD = '''<!DOCTYPE html>
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
<meta name="keywords" content="number {n} personality, number {n} traits, number {n} {planet_lower}, number {n} chaldean numerology, number {n} archetype, number {n} strengths, number {n} love, number {n} career"/>
<meta name="author" content="NameAligned.com"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<link rel="canonical" href="{canon}"/>
<link rel="alternate" hreflang="en-IN" href="{canon}"/>
<meta property="og:title" content="{og_title}"/>
<meta property="og:description" content="{og_desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:site_name" content="NameAligned.com"/>
<meta property="og:locale" content="en_IN"/>
<meta property="og:image" content="{base}/assets/og/moolank-{n}.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{og_title}"/>
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

<link rel="stylesheet" href="/assets/style.css"/>
<link rel="stylesheet" href="/assets/theme-cosmic-light.css"/>
<style>
.np-hero{{padding:3.5rem 0 1.75rem;text-align:center;background:linear-gradient(160deg,#1a1340 0%,#2a1a5c 100%);color:#f0ece0;}}
.np-hero .badge{{display:inline-block;font-family:sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f0b429;background:rgba(240,180,41,.12);padding:5px 14px;border-radius:20px;border:1px solid rgba(240,180,41,.35);margin-bottom:1rem;}}
.np-hero h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4.2vw,44px);line-height:1.2;margin:0 auto .5rem;max-width:780px;color:#f0ece0!important;}}
.np-hero h2{{color:#f0ece0!important;}}
.np-hero .glyph{{font-size:48px;color:#f0b429;line-height:1;margin-bottom:.75rem;}}
.np-hero .tag{{font-family:sans-serif;font-size:14px;color:rgba(240,236,224,.78);letter-spacing:.06em;}}
.np-tldr{{max-width:780px;margin:1.5rem auto 0;padding:1.25rem 1.5rem;background:rgba(0,0,0,.28);border:1px solid rgba(240,180,41,.45);border-radius:12px;font-family:sans-serif;font-size:14.5px;line-height:1.7;color:#f0ece0;backdrop-filter:blur(6px);}}
.np-tldr strong{{color:#f0b429;}}
.np-body{{max-width:780px;margin:0 auto;padding:2rem 1.25rem;}}
.np-body h2{{font-family:'Playfair Display',Georgia,serif;font-size:24px;color:var(--text);margin:2rem 0 .65rem;line-height:1.25;}}
.np-body h3{{font-family:'Playfair Display',Georgia,serif;font-size:18px;color:var(--text);margin:1.5rem 0 .5rem;}}
.np-body p{{font-family:sans-serif;font-size:14.5px;line-height:1.75;color:var(--text);margin-bottom:1rem;}}
.np-body ul{{font-family:sans-serif;font-size:14px;line-height:1.85;color:var(--text);padding-left:1.25rem;margin-bottom:1.25rem;}}
.np-body li{{margin-bottom:.35rem;}}
.np-stat-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin:1.5rem 0;}}
@media(max-width:540px){{.np-stat-row{{grid-template-columns:1fr 1fr;}}}}
.np-stat{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem;text-align:center;}}
.np-stat .lbl{{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;}}
.np-stat .val{{font-family:Georgia,serif;font-size:15px;color:var(--text);margin-top:4px;}}
.np-compat-tbl{{width:100%;border-collapse:collapse;font-family:sans-serif;font-size:13.5px;margin:1rem 0 1.25rem;}}
.np-compat-tbl th,.np-compat-tbl td{{padding:.55rem .7rem;border-bottom:1px solid var(--gold-b);text-align:left;}}
.np-compat-tbl th{{background:rgba(240,180,41,.08);color:var(--gold-d);text-transform:uppercase;letter-spacing:.06em;font-size:11px;}}
.np-compat-tbl a{{color:var(--text);text-decoration:underline;text-decoration-color:rgba(157,127,255,.4);}}
.np-cta-band{{background:var(--gold-l);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.5rem;margin:2rem 0;text-align:center;}}
.np-cta-band h3{{margin:0 0 .35rem;font-family:Georgia,serif;font-size:19px;color:var(--text);}}
.np-cta-band p{{margin:0 0 1rem;font-size:13.5px;color:var(--text2);font-family:sans-serif;}}
.np-cta-band .btn-pair{{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;}}
.np-cta-band a{{display:inline-block;font-family:sans-serif;font-size:13.5px;font-weight:600;padding:9px 18px;border-radius:8px;text-decoration:none;}}
.np-cta-band a.primary{{background:var(--gold);color:#0a0820;}}
.np-cta-band a.primary:hover{{background:#f5c247;}}
.np-cta-band a.outline{{background:transparent;color:var(--text);border:1.5px solid var(--gold-b);}}
.np-faq{{margin:2rem 0;}}
.np-faq details{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem 1.1rem;margin-bottom:.6rem;}}
.np-faq summary{{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--text);cursor:pointer;line-height:1.4;}}
.np-faq details[open] summary{{margin-bottom:.5rem;}}
.np-faq details p{{font-family:sans-serif;font-size:13.5px;line-height:1.7;color:var(--text2);margin:0;}}
.np-related{{margin:2rem 0;}}
.np-related-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;}}
@media(max-width:640px){{.np-related-grid{{grid-template-columns:1fr;}}}}
.np-rel-card{{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.9rem 1rem;text-decoration:none;color:var(--text);transition:transform .15s ease,box-shadow .15s ease;}}
.np-rel-card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(201,162,39,.12);}}
.np-rel-card .eb{{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:.25rem;}}
.np-rel-card .ti{{font-family:Georgia,serif;font-size:14.5px;font-weight:700;line-height:1.3;}}
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
      <div>
        <div class="footer-brand"><span class="logo-moon">☽</span> NameAligned.com</div>
        <p class="footer-tagline">Free Chaldean numerology analysis for everyone. Based on Cheiro\'s Book of Numbers, the oldest and most accurate system.</p>
        <div style="margin-top:1.5rem;display:flex;gap:10px">
          <a href="/analyzer" style="font-size:12px;font-family:sans-serif;color:var(--gold);border:1px solid rgba(240,180,41,.35);border-radius:20px;padding:5px 14px;text-decoration:none;transition:all .2s" onmouseover="this.style.background='rgba(240,180,41,.12)'" onmouseout="this.style.background='transparent'">Try free →</a>
          <a href="/report" style="font-size:12px;font-family:sans-serif;color:rgba(157,127,255,.8);border:1px solid rgba(157,127,255,.3);border-radius:20px;padding:5px 14px;text-decoration:none;transition:all .2s" onmouseover="this.style.background='rgba(157,127,255,.10)'" onmouseout="this.style.background='transparent'">Full report · ₹199 / $2.99</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Free Tools</div>
        <ul class="footer-links">
          <li><a href="/name-numerology-calculator">Name Numerology Calculator</a></li>
          <li><a href="/name-correction-numerology">Name Correction Check</a></li>
          <li><a href="/business-name-numerology">Business Name Check</a></li>
          <li><a href="/love-compatibility-numerology">Love Compatibility</a></li>
          <li><a href="/report">Full Destiny Report · ₹199 / $2.99</a></li>
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


def render(n):
    base = BASE_NUMBERS[n]
    extra = PERSONALITY[n]
    planet = base['planet']
    glyph = base['glyph']
    archetype = extra['archetype']

    title = f'Number {n} Personality — Traits, Strengths, Career & Love'
    og_title = f'Number {n}: {archetype} — the Chaldean numerology personality'
    desc = f'Number {n} in Chaldean numerology is the {planet}-ruled archetype of "{archetype.lower()}" — read the personality traits, strengths, shadow side, career fits, love patterns and lucky elements.'
    og_desc = f'Number {n} ({planet}) personality archetype — strengths, shadow side, career and love patterns.'
    canon = f'{BASE}/number/{n}-personality'

    article = {
        '@context':'https://schema.org','@type':'Article','headline':title,
        'description':desc,'url':canon,'datePublished':'2026-05-08','dateModified':'2026-05-08',
        'author':{'@type':'Organization','name':'NameAligned.com','url':BASE+'/'},
        'publisher':{'@type':'Organization','name':'NameAligned.com','url':BASE+'/','logo':{'@type':'ImageObject','url':BASE+'/assets/namealigned-logo-full.svg'}},
        'inLanguage':'en-IN','mainEntityOfPage':{'@type':'WebPage','@id':canon},
        'about':[
            {'@type':'DefinedTerm','name':f'Number {n}','inDefinedTermSet':'Chaldean Numerology'},
            {'@type':'DefinedTerm','name':planet,'inDefinedTermSet':'Ruling Planets'}
        ]
    }
    breadcrumb = {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},
        {'@type':'ListItem','position':2,'name':'Numbers','item':BASE+'/sitemap-pages'},
        {'@type':'ListItem','position':3,'name':f'Number {n} Personality','item':canon}
    ]}
    # Combine the personality-specific FAQ with 2 reused from name-number page for depth
    combined_faq = list(extra['extra_faq']) + list(base['faq'][:3])
    faq = {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[
        {'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in combined_faq
    ]}

    head = HEAD.format(
        n=n, title=title, og_title=og_title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        planet_lower=planet.lower(),
        article_json=json.dumps(article, ensure_ascii=False),
        breadcrumb_json=json.dumps(breadcrumb, ensure_ascii=False),
        faq_json=json.dumps(faq, ensure_ascii=False),
    )

    strengths_html = '\n'.join(f'    <li>{s}</li>' for s in base['strengths'])
    shadow_html = '\n'.join(f'    <li>{s}</li>' for s in extra['shadow'])
    career_html = '\n'.join(f'    <li>{s}</li>' for s in base['career'])
    faq_html = '\n'.join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q,a in combined_faq)

    # Compatibility table — links to the existing name-number pages as the
    # closest-shipping target. Once /compatibility/number-{a}-and-{b} exists
    # these can switch.
    def num_link(m):
        return f'<a href="/name-number-{m}-meaning">Number {m}</a> ({BASE_NUMBERS[m]["planet"]})'
    compat_rows = ''
    compat_rows += f'      <tr><td>Strongest harmony</td><td>{", ".join(num_link(m) for m in base["compat_best"])}</td></tr>\n'
    compat_rows += f'      <tr><td>Supportive</td><td>{", ".join(num_link(m) for m in base["compat_good"])}</td></tr>\n'
    compat_rows += f'      <tr><td>Asks for awareness</td><td>{", ".join(num_link(m) for m in base["compat_caution"])}</td></tr>'

    related = [m for m in [1,2,3,4,5,6,7,8,9] if m != n][:6]
    related_html = '\n'.join(
        f'    <a href="/number/{m}-personality" class="np-rel-card"><span class="eb">Number {m} · {BASE_NUMBERS[m]["planet"]}</span><span class="ti">{PERSONALITY[m]["archetype"]}</span></a>'
        for m in related
    )

    body = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/sitemap-pages">Numbers</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">Number {n} Personality</span>
</nav>

<header class="np-hero">
  <div class="container">
    <div class="badge">Chaldean Numerology · Number {n}</div>
    <div class="glyph">{glyph}</div>
    <h1>Number {n} Personality — {archetype}</h1>
    <div class="tag">{base["tagline"]}</div>
  </div>
  <div class="np-tldr"><strong>In short.</strong> {extra["tldr"]}</div>
</header>

<main class="np-body">

  <h2>Ruling planet & symbolism of Number {n}</h2>
  <p>{extra["snippet"]}</p>
  <p>In Chaldean numerology, every single digit is governed by a planet — and {planet} is the planet that shapes the temperament, the timing and the natural arc of Number {n} people. {base["famous"]}</p>

  <div class="np-stat-row">
    <div class="np-stat"><div class="lbl">Ruling Planet</div><div class="val">{glyph} {planet}</div></div>
    <div class="np-stat"><div class="lbl">Lucky Day</div><div class="val">{extra["lucky"]["days"]}</div></div>
    <div class="np-stat"><div class="lbl">Lucky Stone</div><div class="val">{extra["lucky"]["stones"]}</div></div>
  </div>

  <h2>Core personality traits of Number {n}</h2>
  <p>{base["core"]}</p>

  <h2>Strengths Number {n} carries</h2>
  <ul>
{strengths_html}
  </ul>

  <h2>Shadow side / blind spots of Number {n}</h2>
  <p>Every archetype has a shadow — not a flaw to fix, but a recurring pattern that shows up when the strengths over-rotate. For Number {n}, the most common patterns are:</p>
  <ul>
{shadow_html}
  </ul>

  <h2>Career paths Number {n} thrives in</h2>
  <p>Career fields that traditionally favour {planet} energy — and reward the natural rhythm of Number {n} — include:</p>
  <ul>
{career_html}
  </ul>
  <p>This isn't a checklist; many Number {n} people thrive outside these fields. The list captures the natural slope. Working against the slope isn't a problem — it just asks for more conscious calibration.</p>
  <p style="font-family:sans-serif;font-size:13.5px;"><a href="/number/{n}-career" style="color:var(--gold-d);font-weight:600;">→ Read the full career guide for Number {n}</a> — top 10 ranked roles, industries to avoid, self-employment shapes and launch timing.</p>

  <h2>Love & relationship patterns of Number {n}</h2>
  <p>{extra["love"]}</p>

  <h2>Compatible numbers for Number {n}</h2>
  <table class="np-compat-tbl">
    <thead><tr><th>Match strength</th><th>Numbers</th></tr></thead>
    <tbody>
{compat_rows}
    </tbody>
  </table>
  <p>Compatibility in Chaldean numerology comes from how the ruling planets interact, not from the numbers in isolation. The pairings above describe the natural rhythm — committed couples can outperform any chart with awareness and effort.</p>

  <h2>Lucky elements for Number {n}</h2>
  <ul>
    <li><strong>Days:</strong> {extra["lucky"]["days"]}</li>
    <li><strong>Stones:</strong> {extra["lucky"]["stones"]}</li>
    <li><strong>Metals:</strong> {extra["lucky"]["metals"]}</li>
    <li><strong>Colours:</strong> {base["color"]}</li>
    <li><strong>Mantra:</strong> <em>{extra["lucky"]["mantra"]}</em></li>
  </ul>

  <h2>Famous Number {n} archetypes</h2>
  <p>{extra["famous_arch"]}</p>

  <div class="np-cta-band">
    <h3>Find your exact numbers in 15 seconds</h3>
    <p>Free Chaldean calculator — Birth Number, Life Path Number and Name Number, side by side.</p>
    <div class="btn-pair">
      <a class="primary" href="/name-numerology-calculator">Calculate my numbers →</a>
      <a class="outline" href="/analyzer">Full free analysis</a>
    </div>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="np-faq">
{faq_html}
  </div>

  <div class="np-cta-band">
    <h3>Want the full personalised picture?</h3>
    <p>The Full Destiny Report covers Number {n} in your chart specifically — Birth, Life Path and Name — plus a 5-year forecast, lucky elements, name correction options and remedies, all in one PDF.</p>
    <div class="btn-pair">
      <a class="primary" href="/report">Full Destiny Report · ₹199 / $2.99 USD</a>
      <a class="outline" href="/name-number-{n}-meaning">Name Number {n} meaning</a>
    </div>
  </div>

  <h2>Related: Number {n} on every chart</h2>
  <p>Number {n} can show up as your <strong>Birth Number</strong> (born on the {n}th, 1{n}th, 2{n}th — sums to {n}), your <strong>Life Path Number</strong> (full birth-date sum) or your <strong>Name Number</strong> (Chaldean letter values of your name). Each angle has its own page:</p>
  <ul>
    <li><a href="/name-number-{n}-meaning">Name Number {n} meaning</a> — what your name does</li>
    <li><a href="/life-path-number-{n}-meaning">Life Path Number {n} meaning</a> — your soul curriculum</li>
    <li><a href="/blog/moolank-meanings">Moolank guide</a> — Birth Numbers 1–9 explained</li>
  </ul>

  <h2>Other number archetypes</h2>
  <div class="np-related">
    <div class="np-related-grid">
{related_html}
    </div>
  </div>

</main>

{FOOTER}
'''
    return head + body


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for n in range(1, 10):
        out = os.path.join(OUT_DIR, f'{n}-personality.html')
        html = render(n)
        with open(out, 'w') as f:
            f.write(html)
        words = len(re.findall(r'\b\w+\b', html))
        print(f'wrote number/{n}-personality.html (~{words} words including markup)')


if __name__ == '__main__':
    main()
