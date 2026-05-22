#!/usr/bin/env python3
"""
Build the 9 Emotional Archetype pages + the /emotional-archetypes hub.

Each archetype maps to a Chaldean birth number but the page is written
in PSYCHOLOGICAL language, not numerology language. The page deliberately
avoids "ruling planet", "moolank", "Chaldean" in the body. Numerology is
in the cross-link footer, not the spine.

URL pattern:
  /emotional-archetypes               hub
  /emotional-archetype-{slug}         9 pages
"""
import os
from _seo_template import HEAD, NAV, FOOTER, BASE, make_article, make_breadcrumb, make_faq, jsonld

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each archetype, written deliberately in plain psychological language.
# Numerology mapping kept in `linked_number` but never named in the body.
ARCHETYPES = [
    dict(
        slug='the-inner-sovereign',
        n=1,
        name='The Inner Sovereign',
        tagline='Self-sufficient long before they feel it',
        hero_subtitle='You appear ready before you feel ready. You decide in silence and announce later. The world reads it as confidence, and you let them.',
        signature='You carry leadership even into rooms that did not ask you to lead. You move faster than the people who love you, and you feel that gap. Compliments land as confirmation, not surprise. Loneliness for you is not the absence of people, it is the absence of equals.',
        relationships='You appear independent in love, and most partners take a long time to see how much you actually want to be met. You do not ask twice. Once you have shown your hand and not been met, you quietly redirect your warmth somewhere else. With the right partner, you build something visible and steady. With the wrong one, you outpace them and feel cold inside it.',
        misread='Often mistaken for arrogant when really you are just unwilling to perform humility you do not feel. Often called intense when really you are at the temperature you have always run at.',
        growth='Your edge is asking for help before you are at the end of yourself. The strength you have already demonstrated does not get re-earned by suffering alone now.',
        question_tag='When did you last let someone in before they had to figure out a way through?',
        emoji='',
        siblings=[
          ('the-restless-mind', 'The Restless Mind', 'A different kind of solo energy'),
          ('the-protector',    'The Protector',     'For partnerships where both lead'),
          ('the-patient-builder', 'The Patient Builder', 'Where slow steadiness anchors you'),
        ],
    ),
    dict(
        slug='the-mirror',
        n=2,
        name='The Mirror',
        tagline='Reads the room before anyone has spoken',
        hero_subtitle='You feel the temperature of a room before anyone has used a word. You absorb tone, atmosphere, the unsaid parts. Most people do not know how much you carry on the way home.',
        signature='You read tone before you read words. You forgive faster than your body does, your mind moves on and your shoulders remember. The smallest tone shift in a message you love can sit with you all evening. You apologise for being emotional, then quietly notice no one else apologises for being cold.',
        relationships='You hold space for people without them realising they were held. You take their mood home with you, even when you tried not to. Love for you is felt through small consistencies: how someone says good night, whether they remember your favourite mug, the daily small evidence that you are seen. With the right person you bloom in private. With the wrong one you slowly disappear into their weather.',
        misread='Often called too sensitive by people who do not carry as much. Often called quiet when really you are listening for what matters before you speak.',
        growth='Your edge is naming a need before it has hardened into resentment. Saying it out loud, even before it feels reasonable, before the body has been carrying it for months.',
        question_tag='What did you feel today that you decided was easier not to mention?',
        emoji='',
        siblings=[
          ('the-inward-witness',     'The Inward Witness',     'A different shape of inner life'),
          ('the-devoted-beautifier', 'The Devoted Beautifier', 'For caregivers who give too well'),
          ('the-patient-builder',    'The Patient Builder',    'A grounded counterweight'),
        ],
    ),
    dict(
        slug='the-translator',
        n=3,
        name='The Translator',
        tagline='Explains things to make them real',
        hero_subtitle='You turn felt experience into words other people can use. You teach by accident in conversations you forgot, and you sometimes forget which insights belong to you and which you shared away.',
        signature='You are warmest in public and quietest at home. Both versions are you. You are good company; sometimes you need to remember you are also good alone. Your honesty arrives wrapped in humour and people miss the honest part. You light up other people\'s rooms and forget to light your own.',
        relationships='You love through expression: long conversations, shared meals, an evening where you both make each other laugh and then say something real. You are openly affectionate, often visibly so. The risk is staying in the warm public layer too long, where the hard private conversations never quite happen. The partner who matches you sees the inner you, not the version that performs warmth.',
        misread='Sometimes read as scattered when you are actually carrying many threads on purpose. Sometimes read as superficial when the depth is just held back for the people who actually want it.',
        growth='Your edge is committing to one thing long enough for it to mature. Jupiter\'s warmth without Saturn\'s discipline is a dilution. Both are available to you.',
        question_tag='What have you been almost-saying for months that wants to be fully said?',
        emoji='',
        siblings=[
          ('the-quiet-disruptor', 'The Quiet Disruptor', 'A different kind of insight-carrier'),
          ('the-restless-mind',   'The Restless Mind',   'When language is your medium'),
          ('the-protector',       'The Protector',       'For the cause-driven version of you'),
        ],
    ),
    dict(
        slug='the-quiet-disruptor',
        n=4,
        name='The Quiet Disruptor',
        tagline='Sees what others will only see in three months',
        hero_subtitle='You notice things other people will only spot in three months. You hold back the obvious thing in meetings because no one wants to hear it yet. Your unusual angle is the value, and also the reason you sometimes feel like the outsider.',
        signature='Being called paranoid by people you were right about is exhausting in a specific way. You build the thing first and explain it after. Words come late for you. You change your mind in public, which other people find threatening; it is just how you think.',
        relationships='You attach intensely once you trust, and you trust slowly. Your love is unconventional in shape and deeply loyal in substance. You need a partner who does not require you to be normal for the social comfort of others. The wrong partner asks you to dim. The right one asks what you saw and listens before responding.',
        misread='Often labelled difficult when you are early. Often called rebellious when you are just unwilling to pretend the obvious problem is not a problem.',
        growth='Your edge is shipping the prototype before perfecting the explanation. Built evidence convinces people that words cannot.',
        question_tag='What have you been seeing that no one else has named yet?',
        emoji='',
        siblings=[
          ('the-inward-witness',  'The Inward Witness',  'For your contemplative twin'),
          ('the-patient-builder', 'The Patient Builder', 'Where slow structure helps you land'),
          ('the-translator',      'The Translator',      'To get the unspoken outward'),
        ],
    ),
    dict(
        slug='the-restless-mind',
        n=5,
        name='The Restless Mind',
        tagline='Seventeen tabs open, all the time',
        hero_subtitle='You have seventeen tabs open in your mind right now, and that is on a calm day. You enjoy your own conversations, including the ones in your head. You think while moving, stillness is harder for you than action.',
        signature='You start things quickly. You finish them when something matches the original spark. You can talk to almost anyone; you are picky about who you stay quiet with. You absorb information at a rate that exhausts you and you keep doing it anyway. You leave conversations early sometimes because your mind already left.',
        relationships='You love through ideas, conversation, shared movement. You need a partner who can keep up intellectually and not require constant emotional translation. Stillness feels like trap to you; choose someone who shares your appetite for the world. The risk is novelty: every new direction looks better than the one you committed to last month. The fix is depth practised on purpose.',
        misread='Sometimes called flaky when you are actually pruning. Sometimes called distant when you are just thinking three topics ahead.',
        growth='Your edge is choosing one direction long enough for the compounding to start. Mercury rewards depth as much as breadth.',
        question_tag='Which of your half-finished projects has been waiting for you to come back to it?',
        emoji='',
        siblings=[
          ('the-translator',      'The Translator',      'When mind goes outward'),
          ('the-inner-sovereign', 'The Inner Sovereign', 'For the solo-led version of you'),
          ('the-quiet-disruptor', 'The Quiet Disruptor', 'For your pattern-spotting side'),
        ],
    ),
    dict(
        slug='the-devoted-beautifier',
        n=6,
        name='The Devoted Beautifier',
        tagline='Finds the sacred in care and detail',
        hero_subtitle='You confuse care with self-care more than you realise. You smooth other people\'s rough edges and quietly carry your own. You make beautiful spaces because beauty steadies you, not because it is decoration.',
        signature='You can tell when a room is uncomfortable and you usually rearrange it before anyone notices. You say yes to comfort over honesty in small ways, until the honesty has nowhere to go. You apologise for needs you have not even named yet. You love through routine, the Tuesday meal, the morning text, the small habits.',
        relationships='You love sensorially: through food, touch, the daily texture of life. Your home is a held space. You give devotion that most partners take time to recognise; some never do. The relationship needs honesty practised early, before harmony becomes a place where the hard truth has nowhere to go. The right partner sees your tending and tends back.',
        misread='Often called controlling when you are actually trying to keep the felt atmosphere good for everyone. Often called superficial when the aesthetic care is genuine devotion.',
        growth='Your edge is letting the truth disrupt the harmony for a few hours, instead of letting the harmony slowly bleach the truth.',
        question_tag='What are you tending for someone that they have stopped noticing?',
        emoji='',
        siblings=[
          ('the-mirror',          'The Mirror',          'For your emotional-attunement twin'),
          ('the-protector',       'The Protector',       'For the fierce-care version'),
          ('the-patient-builder', 'The Patient Builder', 'Where care meets structure'),
        ],
    ),
    dict(
        slug='the-inward-witness',
        n=7,
        name='The Inward Witness',
        tagline='Comfortable with silence, allergic to performance',
        hero_subtitle='You can sit in silence with the right person and feel more met than after an hour of words. You stand slightly outside groups by design, not because you were not invited. Your inner life has more rooms than most people\'s outer life does.',
        signature='You ask questions other people consider rude; you consider them honest. You meet someone once and either feel everything or feel nothing, rarely a middle. Your most useful work happens when no one is looking. You will dissolve a relationship before you will dilute it. The lonely parts of your life are not failures, they are how you metabolise the world.',
        relationships='You attach quietly and stay deeply. Your love is rarely demonstrative; it is woven into how you defend their solitude, remember the small thing they said in passing, choose to be there in private. You need a partner who does not require constant proof, and who is comfortable with rooms that have no agenda. With the right one you go very deep. With the wrong one you retreat all the way back.',
        misread='Often called cold when you are just not performing. Often called antisocial when you simply do not pretend conversations are happening when they are not.',
        growth='Your edge is reaching toward another person on a difficult day, instead of retreating into your inner world for the third week in a row.',
        question_tag='Who have you been silent with for a little too long?',
        emoji='',
        siblings=[
          ('the-mirror',          'The Mirror',          'For your attuned partner-archetype'),
          ('the-quiet-disruptor', 'The Quiet Disruptor', 'For your pattern-spotting twin'),
          ('the-patient-builder', 'The Patient Builder', 'For the structured-depth version'),
        ],
    ),
    dict(
        slug='the-patient-builder',
        n=8,
        name='The Patient Builder',
        tagline='Measures in years where others measure in weeks',
        hero_subtitle='You measure things in years where other people measure in weeks. You carry responsibilities other people would have set down by now. You appear emotionally steady while internally carrying real pressure.',
        signature='You wait. You wait longer than other people would wait. Then you move, and it sticks. You can hold a hard truth without flinching, but the soft ones move you more than people realise. You take a long time to build trust and a longer time to take it back once given. You sometimes mistake endurance for love, other times you are simply right.',
        relationships='You build relationships the way you build everything: slowly, structurally, with the assumption that it will last. You do not flirt; if you are putting time into someone, you have decided this matters. The risk is staying inside a structure long after the love has cooled, because the structure is so well built. The right partner respects your pace and also keeps reminding you to play.',
        misread='Often called cold or distant when you are taking the long-arc view. Often called harsh when you are actually steady, and steady is rarer than people realise.',
        growth='Your edge is letting joy happen on a Tuesday, not only as a reward for finished work. The Saturn path matures into joy as well as endurance.',
        question_tag='What have you been enduring lately that wants to be set down?',
        emoji='',
        siblings=[
          ('the-inward-witness',     'The Inward Witness',     'For your contemplative depth twin'),
          ('the-inner-sovereign',    'The Inner Sovereign',    'For the solo-leader version'),
          ('the-devoted-beautifier', 'The Devoted Beautifier', 'Where structure meets aesthetic'),
        ],
    ),
    dict(
        slug='the-protector',
        n=9,
        name='The Protector',
        tagline='Fights for people who are not in the room',
        hero_subtitle='You fight for people who are not yet in the room. Your anger is rarely about the present moment, the present is just where it landed. You will lose sleep over an injustice that did not happen to you.',
        signature='You love at temperature. Lukewarm is not a setting your heart has. You replay arguments in your head, winning the version you did not get to say out loud. You burn out because you cannot stand watching wrong things continue. You are not aggressive; you are alive in a culture that is uncomfortable with aliveness.',
        relationships='You love openly and protectively. Your partner is your cause. You will defend them to everyone, including themselves on the bad days. The risk is mistaking heat for connection: passion and conflict are not the same thing. The right partner can hold your intensity and also ask you to slow down, and you respect the asking.',
        misread='Often called aggressive when you are passionate. Often called dramatic when you are at the only temperature your heart runs at.',
        growth='Your edge is channelling the fire into the work, not into the people closest to the work. Mars used well is the protector; misused it tips into unnecessary fight.',
        question_tag='Whose battle are you fighting right now that is not actually yours?',
        emoji='',
        siblings=[
          ('the-inner-sovereign', 'The Inner Sovereign', 'For your solo-leader twin'),
          ('the-translator',      'The Translator',      'For when expression channels fire'),
          ('the-devoted-beautifier', 'The Devoted Beautifier', 'For care meeting courage'),
        ],
    ),
]


def render_archetype(arch):
    slug = arch['slug']
    n    = arch['n']
    title = arch['name'] + ', An Emotional Archetype Reading'
    desc  = arch['name'] + ', ' + arch['tagline'] + '. Read the emotional signature, relationship dynamic, common misreadings, and growth edge. A psychologically grounded read, no jargon.'
    og_desc = arch['name'] + ', ' + arch['tagline'] + '. Read the psychology.'
    canon = f'{BASE}/emotional-archetype-{slug}'

    article = make_article(title, desc, canon)
    breadcrumb = make_breadcrumb(arch['name'], canon)
    faqs = [
        ('Is this the same as my birth number?',
         f'It is closely linked. The {arch["name"].lower()} archetype maps to people whose Chaldean birth number is {n}, but the page is written in psychological language, not numerology language. You can read it whether you are into numerology or not.'),
        ('How accurate is an emotional archetype reading?',
         'It is not deterministic. Think of it as a felt-experience description that many people in this archetype recognise. The bits that ring true tell you more than the bits that do not.'),
        ('Can my archetype change over time?',
         'The signature usually stays. The way you express it does change with age, life experience, and the people you choose to be close to. The page is a starting reflection, not a fixed identity.'),
        ('What should I do with this reading?',
         'Send it to one person who knows you well. Ask which parts they recognise. The conversation that follows is usually more useful than the reading itself.'),
    ]
    aj, bj, fj = jsonld(article, breadcrumb, faqs and {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})

    siblings_html = '\n'.join(
        f'        <a class="emotion-path-link" href="/emotional-archetype-{s_slug}" data-na-event="related_insight_clicked" data-na-params=\'{{"from_page":"emotional-archetype-{slug}","to_page":"emotional-archetype-{s_slug}","link_text":"{s_name}"}}\'><span class="ep-eyebrow">Adjacent archetype</span><span class="ep-title">{s_name}</span><span style="font-size:12.5px;color:#9d7fff;margin-top:.25rem">{s_tag}</span></a>'
        for (s_slug, s_name, s_tag) in arch['siblings']
    )

    head = HEAD.format(
        n=n, title=title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        keywords=f'emotional archetype, {arch["name"].lower()}, emotional pattern, psychological archetype, {arch["tagline"].lower()}, namealigned emotional reading',
        article_json=aj, breadcrumb_json=bj, faq_json=fj,
    )

    faq_html = '\n'.join(
        f'        <details><summary>{q}</summary><p>{a}</p></details>'
        for q, a in faqs
    )

    body = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">&rsaquo;</span>
  <a href="/emotional-archetypes">Emotional Archetypes</a> <span style="margin:0 8px;">&rsaquo;</span>
  <span style="color:var(--text2);">{arch['name']}</span>
</nav>

<link rel="stylesheet" href="/assets/emotional-insights.css"/>

<header class="seo-hero">
  <div class="container">
    <div class="badge">Emotional Archetype</div>
    <h1>{arch['name']}</h1>
    <div class="tag">{arch['tagline']}</div>
  </div>
</header>

<div class="seo-wrap">
  <main class="seo-body">

    <p style="font-size:16px;line-height:1.7;font-style:italic;color:var(--text2);margin:1rem 0 1.75rem;">{arch['hero_subtitle']}</p>

    <h2>The signature, in their own words</h2>
    <p>{arch['signature']}</p>

    <div class="emotional-insights-strip emotional-insights" data-number="{n}" data-count="3"></div>

    <h2>In relationships</h2>
    <p>{arch['relationships']}</p>

    <h2>Often misread as</h2>
    <p>{arch['misread']}</p>

    <h2>The growth edge</h2>
    <p>{arch['growth']}</p>

    <div class="share-strip"
         data-share-source="archetype-{slug}"
         data-emotion-headline="Send this to someone who needs to see themselves here."
         data-emotion-prompt="Ask them which lines feel like home, and which felt called out."
         data-share-text="Read this archetype, see if you recognise yourself or someone you know:"
         data-share-url="{canon}"></div>

    <div class="emotion-paths">
      <h2>{arch['question_tag']}</h2>
      <p>Adjacent archetypes you may also relate to. Most people see themselves partly in two or three.</p>
      <div class="emotion-paths-grid">
{siblings_html}
      </div>
    </div>

    <h2>Frequently asked</h2>
    <div class="seo-faq">
{faq_html}
    </div>

    <section class="seo-related">
      <h2>Continue exploring</h2>
      <div class="seo-related-grid">
        <a href="/love-compatibility-numerology" class="seo-rel-card" data-na-event="related_insight_clicked" data-na-params='{{"to_page":"compatibility","from_page":"archetype-{slug}"}}'><span class="eb">Compatibility</span><span class="ti">How this archetype loves and clashes</span></a>
        <a href="/analyzer" class="seo-rel-card" data-na-event="analyzer_started" data-na-params='{{"source":"archetype-{slug}"}}'><span class="eb">Free Analysis</span><span class="ti">Get your full chart in 10 seconds</span></a>
        <a href="/why-number-{n}-overthinks" class="seo-rel-card" data-na-event="related_insight_clicked"><span class="eb">Emotional Pattern</span><span class="ti">The overthinking signature of this archetype</span></a>
        <a href="/number-{n}-in-love" class="seo-rel-card" data-na-event="related_insight_clicked"><span class="eb">Love Style</span><span class="ti">How this archetype shows up in love</span></a>
        <a href="/emotional-archetypes" class="seo-rel-card" data-na-event="related_insight_clicked"><span class="eb">Hub</span><span class="ti">All 9 emotional archetypes</span></a>
        <a href="/ask-aura" class="seo-rel-card" data-na-event="related_insight_clicked"><span class="eb">Ask Aura</span><span class="ti">Talk to a reflective companion</span></a>
      </div>
    </section>

  </main>

  <aside class="seo-aside">
    <div class="article-sidebar">
      <div class="eyebrow">Free Analysis</div>
      <h3>Find your own archetype</h3>
      <p>Enter your name + birth date, see which of the nine emotional archetypes you carry.</p>
      <a href="/analyzer" class="cta" data-na-event="analyzer_started" data-na-params='{{"source":"archetype-sidebar"}}'>Start free &rarr;</a>
      <a href="/love-compatibility-numerology" class="cta outline" data-na-event="compatibility_started" data-na-params='{{"source":"archetype-sidebar"}}'>Check a relationship</a>
      <div class="sep"></div>
      <div class="eyebrow">Full Destiny Report</div>
      <h3>Personalised PDF</h3>
      <div class="price-row"><span class="price-inr">INR 499</span><span class="price-usd">or $5 USD</span></div>
      <p>Complete chart, name corrections, compatibility map, 5-year forecast.</p>
      <a href="/report" class="cta" data-na-event="report_clicked" data-na-params='{{"source":"archetype-sidebar"}}'>Get the report &rarr;</a>
    </div>
  </aside>
</div>

<script src="/assets/emotional-insights.js" defer></script>
<script src="/assets/share-helpers.js" defer></script>
<script src="/assets/analytics.js" defer></script>

{FOOTER}
'''
    return head + body


HUB_BODY = '''
<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">&rsaquo;</span>
  <span style="color:var(--text2);">Emotional Archetypes</span>
</nav>

<link rel="stylesheet" href="/assets/emotional-insights.css"/>

<header class="seo-hero">
  <div class="container">
    <div class="badge">Hub</div>
    <h1>The Nine Emotional Archetypes</h1>
    <div class="tag">Nine ways of being a person, read in plain psychological language. Find yours.</div>
  </div>
</header>

<div class="seo-wrap">
  <main class="seo-body">
    <p>Most people sit primarily in one archetype, with one or two adjacent ones bleeding into the picture. None of these are diagnoses. They are felt-experience descriptions of how a person shows up in their inner life, their relationships, and their work.</p>
    <p>Click into any archetype you suspect is yours. Better, click into the one you suspect belongs to someone you are trying to understand. The reading will tell you more about the gap between you than about either of you alone.</p>

    <div class="archetype-hub-grid" style="display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin:2rem 0 2.5rem;">
      {cards}
    </div>

    <div class="share-strip"
         data-share-source="archetype-hub"
         data-emotion-headline="Send this to a friend who would over-identify with one of these."
         data-emotion-prompt="See which archetype they pick. See if you agree."
         data-share-text="Nine emotional archetypes, find yours, find the one that explains the people you love:"
         data-share-url="{canon}"></div>

    <section class="seo-related" style="margin-top:2.5rem;">
      <h2>Continue exploring</h2>
      <div class="seo-related-grid">
        <a href="/analyzer" class="seo-rel-card" data-na-event="analyzer_started" data-na-params='{{"source":"archetype-hub"}}'><span class="eb">Free Analysis</span><span class="ti">Match your full chart to an archetype</span></a>
        <a href="/love-compatibility-numerology" class="seo-rel-card" data-na-event="compatibility_started" data-na-params='{{"source":"archetype-hub"}}'><span class="eb">Compatibility</span><span class="ti">How two archetypes interact</span></a>
        <a href="/ask-aura" class="seo-rel-card" data-na-event="related_insight_clicked"><span class="eb">Aura</span><span class="ti">Talk to a reflective companion</span></a>
        <a href="/report" class="seo-rel-card" data-na-event="report_clicked"><span class="eb">Full Report</span><span class="ti">All of this, deeper, in a PDF</span></a>
      </div>
    </section>
  </main>

  <aside class="seo-aside">
    <div class="article-sidebar">
      <div class="eyebrow">Free Analysis</div>
      <h3>Find your archetype</h3>
      <p>Enter your name + birth date and get your archetype mapped in 10 seconds.</p>
      <a href="/analyzer" class="cta" data-na-event="analyzer_started" data-na-params='{{"source":"hub-sidebar"}}'>Start free &rarr;</a>
      <a href="/ask-aura" class="cta outline">Ask Aura</a>
      <div class="sep"></div>
      <div class="eyebrow">Full Destiny Report</div>
      <h3>Personalised PDF</h3>
      <div class="price-row"><span class="price-inr">INR 499</span><span class="price-usd">or $5 USD</span></div>
      <p>Archetype, compatibility, 5-year forecast, name corrections.</p>
      <a href="/report" class="cta" data-na-event="report_clicked" data-na-params='{{"source":"hub-sidebar"}}'>Get the report &rarr;</a>
    </div>
  </aside>
</div>

<script src="/assets/emotional-insights.js" defer></script>
<script src="/assets/share-helpers.js" defer></script>
<script src="/assets/analytics.js" defer></script>
'''


def render_hub(archetypes):
    title = 'The Nine Emotional Archetypes, Read Yourself and the People You Love'
    desc  = 'Nine psychologically grounded archetypes that describe how people show up in their inner life and relationships. Find yours, find theirs, understand the gap.'
    og_desc = 'Nine emotional archetypes, plain psychological language. Find yours.'
    canon = f'{BASE}/emotional-archetypes'

    article = make_article(title, desc, canon)
    breadcrumb = make_breadcrumb('Emotional Archetypes', canon)
    aj, bj, fj = jsonld(article, breadcrumb, {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[]})

    head = HEAD.format(
        n=1, title=title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        keywords='emotional archetypes, personality archetypes, psychological archetype, emotional pattern, namealigned',
        article_json=aj, breadcrumb_json=bj, faq_json=fj,
    )

    cards = []
    for a in archetypes:
        cards.append(
            f'<a class="seo-rel-card" href="/emotional-archetype-{a["slug"]}" data-na-event="archetype_viewed" data-na-params=\'{{"archetype":"{a["slug"]}","number":{a["n"]}}}\'>'
            f'<span class="eb">{a["tagline"]}</span>'
            f'<span class="ti">{a["name"]}</span>'
            f'<span style="font-size:12px;color:#cbb8e8;margin-top:.4rem;line-height:1.45">{a["hero_subtitle"][:140]}{"..." if len(a["hero_subtitle"])>140 else ""}</span>'
            '</a>'
        )

    body = NAV + HUB_BODY.format(cards='\n      '.join(cards), canon=canon) + FOOTER
    return head + body


def build():
    # Hub
    hub_html = render_hub(ARCHETYPES)
    with open(os.path.join(OUT, 'emotional-archetypes.html'), 'w') as fh:
        fh.write(hub_html)
    print('  wrote emotional-archetypes.html')

    # 9 archetype pages
    for arch in ARCHETYPES:
        html = render_archetype(arch)
        path = os.path.join(OUT, f'emotional-archetype-{arch["slug"]}.html')
        with open(path, 'w') as fh: fh.write(html)
        print(f'  wrote emotional-archetype-{arch["slug"]}.html')

    print(f'\nBuilt 1 hub + {len(ARCHETYPES)} archetype pages.')


if __name__ == '__main__':
    build()
