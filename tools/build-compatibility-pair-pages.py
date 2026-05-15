#!/usr/bin/env python3
"""
Build the "Number A and B Compatibility" SEO cluster.

Target: high-intent comparison queries:
  - "number 4 and 8 compatibility"
  - "moolank 2 and 7 marriage"
  - "is number 3 and 9 a good match"
  - "5 and 7 compatibility numerology"

URL pattern: /number-{a}-and-{b}-compatibility   (a < b for canonical order)

First batch: 10 highest-volume / most-evocative pairings drawn from
Cheiro's planetary-triangle compatibility logic.
"""
import os
import json
from _seo_template import HEAD, NAV, FOOTER, PLANETS, BASE, make_article, make_breadcrumb, make_faq, jsonld

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each pair, with both numbers' planets and a unique long-form interpretation.
# Authored fresh, not copied; rooted in Cheiro's planetary-triangle logic.
PAIRS = [
  # (a, b, rating, summary, body, faqs)
  (1, 2, 'Strong', 'Sun and Moon', dict(
    one_liner='Sun meets Moon: a classic complementary pairing where action and feeling balance each other.',
    para1='Number 1 (Sun) and Number 2 (Moon) form one of the most celebrated pairings in Chaldean numerology. The Sun provides direction, ambition and visibility; the Moon provides emotional depth, intuition, and the steady inner world that holds the relationship together. Together they cover both halves of a full life, public momentum and private sanctuary.',
    para2='The friction point: Number 1 can be impatient with Number 2\'s emotional pace; Number 2 can feel unseen by Number 1\'s outward-facing focus. The fix is rhythm. Couples who plan deliberate inner time, weekly evenings without external commitments, dinners with no phones, walks where no problem-solving happens, last longest. The Moon needs to feel met; the Sun needs to feel home is steady.',
    para3='Marriage outlook: traditionally one of the strongest pairings for marriage and long-term partnership. Cheiro notes the natural attraction between these vibrations; the Sun and the Moon are the two great lights of the chart, and partners under each tend to recognise each other quickly.',
    bullets=[
      'Communication style: 1 speaks plainly, 2 speaks through tone. Both need patience.',
      'Conflict pattern: 2 absorbs and withdraws, 1 wants to resolve and move on. Slow down.',
      'Friendship depth: very high once the trust is built. Often lifelong friendships.',
      'Best moments: travel, family events, shared rituals.',
    ],
  ), [
    ('Is 1 and 2 a good match for marriage?', 'Generally yes, traditionally one of the strongest Chaldean pairings. The Sun and Moon balance each other naturally, with 1 providing direction and 2 providing emotional depth.'),
    ('What is the main challenge between 1 and 2?', 'Pace. Number 1 wants to move; Number 2 wants to feel. The fix is rhythm, building inner time deliberately into the relationship.'),
    ('Are 1 and 2 compatible in business?', 'Yes, especially when 1 leads the outward strategy and 2 handles internal culture and relationships.'),
    ('Does 1 and 2 work in friendship?', 'Strongly. Often lifelong, with deep mutual trust once both feel met.'),
  ]),

  (1, 9, 'Strong', 'Sun and Mars', dict(
    one_liner='Sun meets Mars: fire and fire. Two leaders, two strong wills, one shared cause or perpetual friction.',
    para1='Number 1 (Sun) and Number 9 (Mars) are both fire-based vibrations, ambitious, decisive, and unwilling to be told what to do. When they share a common cause, they are unstoppable; when they compete with each other, the same fire that fuels them burns the relationship.',
    para2='The signature of a thriving 1-9 pair: they are not in each other\'s way. They have separate domains they each lead in, and they bring those wins back to the shared life. The signature of a struggling 1-9 pair: they keep crossing into each other\'s territory and treating disagreement as betrayal.',
    para3='Marriage outlook: high-intensity, deeply loyal, and rarely boring. The relationship lives at temperature, both partners feel it, both partners use it. Couples who learn to fight clean (issues, not personalities) tend to last; couples who let the heat compost into resentment burn out fast.',
    bullets=[
      'Communication style: both speak directly. The room knows what is being discussed.',
      'Conflict pattern: heated and fast. Resolution must be just as fast.',
      'Friendship depth: intense; often a "ride or die" energy.',
      'Watch for: ego clashes around recognition, family politics, public decisions.',
    ],
  ), [
    ('Is 1 and 9 compatible in marriage?', 'Yes, when both partners have separate leadership domains. Trouble arises when they compete for the same territory.'),
    ('Do 1 and 9 fight a lot?', 'They can. Both are direct, decisive, and unwilling to be wrong. The relationship thrives when both partners learn to fight clean and resolve fast.'),
    ('What makes a 1-9 partnership work long-term?', 'Shared mission. When 1 and 9 align around a cause larger than the relationship itself, the fire becomes productive rather than competitive.'),
    ('Are 1 and 9 emotionally compatible?', 'Yes in passion and loyalty, harder in vulnerability. Both numbers can struggle to admit weakness; couples who normalise that grow deeper.'),
  ]),

  (2, 7, 'Strong', 'Moon and Ketu', dict(
    one_liner='Moon meets Ketu: a deeply spiritual, often unspoken pairing. The most introverted of the classic harmonies.',
    para1='Number 2 (Moon) and Number 7 (Ketu) are traditionally considered one of the most spiritually attuned pairings in Chaldean numerology. Both vibrations are receptive, contemplative, and uninterested in social performance. When they find each other, the relationship often feels recognised rather than built.',
    para2='Strength: both partners need quiet, private depth, and unhurried emotional connection. They can sit in silence and feel met. They communicate as much through atmosphere as through words.',
    para3='Friction: both can withdraw inward when stressed, and neither naturally pulls the other back out. A 2-7 couple must consciously practise the small daily acts that re-attach them, the touch, the meal eaten together, the evening question that says "I am still here".',
    bullets=[
      'Communication style: layered, intuitive, often non-verbal.',
      'Conflict pattern: quiet withdrawal rather than open fighting. Bring it forward.',
      'Friendship depth: rare, profound, and life-altering when it lands.',
      'Watch for: both partners going internal at once and losing each other for weeks.',
    ],
  ), [
    ('Is 2 and 7 a good match?', 'Traditionally one of the strongest spiritual pairings. Both partners share an introverted, contemplative depth that few other combinations reach.'),
    ('What is the main risk in 2 and 7 relationship?', 'Mutual withdrawal. Both numbers retreat inward under stress, so the relationship needs deliberate practices to keep both partners engaged.'),
    ('Are 2 and 7 compatible spiritually?', 'Yes, very. Many lifelong friendships and marriages under this pairing share a meditative, philosophical or creative practice.'),
    ('Do 2 and 7 work in friendship?', 'Beautifully. Often quiet, depth-first friendships that survive long absences without weakening.'),
  ]),

  (3, 6, 'Strong', 'Jupiter and Venus', dict(
    one_liner='Jupiter meets Venus: the most aesthetically harmonious pairing in Chaldean numerology. Warmth meets beauty.',
    para1='Number 3 (Jupiter) and Number 6 (Venus) form what Cheiro called the "natural triangle". Jupiter expands; Venus refines. Together the relationship feels generous, beautiful, well-fed, and well-spoken-of.',
    para2='Strength: both partners value warmth, social connection, beauty, food, conversation, and the slow art of building a life that feels good to live. The relationship tends to have an unmistakable atmosphere, friends want to be around the couple.',
    para3='Friction: both can avoid hard truths to keep the harmony. The relationship can develop a smooth surface and an unspoken depth that has not been addressed. The fix is deliberate honesty practised gently, often, and early.',
    bullets=[
      'Communication style: warm, expressive, often public.',
      'Conflict pattern: tends to be avoided. Conscious work needed to surface tension.',
      'Friendship depth: high warmth, social ease, lots of shared rituals.',
      'Watch for: maintaining the aesthetic at the cost of the truth.',
    ],
  ), [
    ('Is 3 and 6 a good match for marriage?', 'Yes, one of the most aesthetically and socially harmonious pairings in Chaldean numerology. Jupiter and Venus form a natural triangle.'),
    ('What is the main challenge for 3 and 6 couples?', 'Avoidance of hard truths. The desire to keep harmony can suppress conversations that the relationship actually needs.'),
    ('Are 3 and 6 compatible in business?', 'Strongly. Both are people-facing, warm, and creative. Hospitality, fashion, education and creative ventures fit naturally.'),
    ('Do 3 and 6 stay friends if the romance ends?', 'Often yes. The underlying warmth tends to survive the romantic phase.'),
  ]),

  (3, 9, 'Strong', 'Jupiter and Mars', dict(
    one_liner='Jupiter meets Mars: expansion meets action. A pairing built for visible work in the world.',
    para1='Number 3 (Jupiter) and Number 9 (Mars) form the second leg of Cheiro\'s fire triangle (along with 1-Sun). The relationship has natural drive, public energy, and a shared appetite for taking on big projects together.',
    para2='Strength: both partners are confident, expressive, ambitious, and willing to commit. The relationship typically has visible ambition, a business built together, a cause supported, children raised with intention.',
    para3='Friction: both can be the one who needs to be right. Mars is forceful, Jupiter is expansive in opinion; in conflict, both want the floor. Couples who learn to speak in turn, who let one partner be fully heard before responding, find the relationship steadies.',
    bullets=[
      'Communication style: assertive, expressive, animated.',
      'Conflict pattern: both raise volume. Lower it deliberately.',
      'Friendship depth: high; often built around shared work or cause.',
      'Watch for: competing for "the right answer" instead of building together.',
    ],
  ), [
    ('Is 3 and 9 compatible for marriage?', 'Yes, particularly when both partners share a cause or mission. Fire triangle pairings (1, 3, 9) thrive when channelled outward.'),
    ('What jobs work for a 3-9 couple?', 'Building something together: a business, a creative venture, a non-profit, an educational project. Both vibrations love visible work.'),
    ('Do 3 and 9 argue often?', 'They can. Both want to be heard. The fix is structural: take turns, slow down, let one partner finish.'),
    ('Are 3 and 9 emotionally compatible?', 'Yes in passion and loyalty; both need practice in softness and vulnerability.'),
  ]),

  (4, 8, 'Heavy', 'Rahu and Saturn', dict(
    one_liner='Rahu meets Saturn: the most controversial pairing in Chaldean numerology. Powerful, karmic, and traditionally cautioned against.',
    para1='Number 4 (Rahu) and Number 8 (Saturn) is the pairing Cheiro warned about most strongly. Both vibrations carry weight, both are slow-moving, both attract difficulty as a teacher rather than as an enemy. When they pair, the relationship intensifies both, the gains feel earned and the costs feel real.',
    para2='Why traditional sources caution against it: the pairing tends to amplify each partner\'s shadow rather than soften it. Both numbers can take on too much, hold burdens silently, and turn shared life into shared burden.',
    para3='Why modern couples sometimes choose it anyway: when both partners are conscious of the pattern, the same intensity produces unusual depth. A 4-8 marriage that survives is often the most loyal, structured, and quietly powerful relationship either partner has ever known. The catch is that both must work, deliberately and continuously, on not collapsing inward.',
    bullets=[
      'Communication style: brief, weighted, important.',
      'Conflict pattern: heavy and slow. Decisions take time. Avoid hasty conclusions.',
      'Friendship depth: rare, but loyal and structural when it lands.',
      'Watch for: heaviness becoming the relationship\'s default state.',
    ],
  ), [
    ('Is 4 and 8 bad for marriage?', 'Traditionally cautioned against in Chaldean numerology because the pairing amplifies both numbers\' weight. With awareness it can still work, but the relationship is real work.'),
    ('Why do some 4-8 couples thrive?', 'When both partners deliberately bring lightness into the relationship and refuse to let the karmic intensity become the default mood, the depth becomes a strength.'),
    ('Are 4 and 8 spiritually compatible?', 'Yes, both have a serious, karmic vibration. Spiritual practice often anchors the relationship.'),
    ('Should I avoid 4-8 compatibility?', 'You cannot choose your number; you can choose your awareness. A conscious 4-8 partnership is often more durable than many "easier" pairings.'),
  ]),

  (5, 7, 'Supportive', 'Mercury and Ketu', dict(
    one_liner='Mercury meets Ketu: speed meets stillness. A mind-rich, often surprising pairing.',
    para1='Number 5 (Mercury) and Number 7 (Ketu) is an under-discussed pairing that often produces genuinely interesting relationships. Mercury is fast, social, communicative; Ketu is slow, depth-oriented, and quiet. Each is what the other does not have.',
    para2='Strength: the conversation is excellent. Mercury brings ideas, news, social texture; Ketu brings meaning, depth, contemplation. A long evening with this couple feels surprising, neither of them runs out of things to say.',
    para3='Friction: pace. Mercury moves faster than Ketu can. Ketu disappears inward faster than Mercury notices. The fix is calendar discipline, structured time together that respects both rhythms.',
    bullets=[
      'Communication style: idea-rich, often philosophical.',
      'Conflict pattern: Mercury wants to talk it through immediately; Ketu wants time. Both need patience.',
      'Friendship depth: intellectual and meaningful; often built on shared curiosity.',
      'Watch for: pace mismatch becoming a permanent gap.',
    ],
  ), [
    ('Is 5 and 7 a good match?', 'Surprisingly yes, when both partners respect each other\'s pace. Mercury and Ketu complement each other intellectually.'),
    ('What is the friction between 5 and 7?', 'Speed. 5 wants instant connection, 7 needs space and time. Calendar discipline helps.'),
    ('Are 5 and 7 compatible for business?', 'Best in roles where 5 handles communication and 7 handles depth work (research, strategy, writing).'),
    ('Do 5 and 7 stay friends?', 'Yes, often. The friendship survives time apart well, both partners are comfortable with long pauses.'),
  ]),

  (6, 9, 'Strong', 'Venus and Mars', dict(
    one_liner='Venus meets Mars: the classical pairing of love and passion. Romantic, intense, sensorial.',
    para1='Number 6 (Venus) and Number 9 (Mars) is one of the most romantically charged pairings in Chaldean numerology. Venus is beauty, comfort, the body, aesthetic care; Mars is fire, drive, passion, action. Together the relationship is alive on every register: emotional, physical, creative.',
    para2='Strength: both partners value the relationship visibly. The home is beautiful and warm; the physical connection stays alive; the relationship is not allowed to fade into "comfortable".',
    para3='Friction: temperature. Mars runs hot, Venus runs aesthetic. When 9 brings conflict to the table, 6 wants to restore harmony before the issue is resolved. The fix is committing to the hard conversation even when it threatens the beautiful surface.',
    bullets=[
      'Communication style: physical and verbal, expressive on both sides.',
      'Conflict pattern: 9 escalates, 6 smooths. Resist smoothing too early.',
      'Friendship depth: warm, physical (hugs, food, shared experiences), enduring.',
      'Watch for: 6 enabling avoidance to keep the harmony.',
    ],
  ), [
    ('Is 6 and 9 compatible for marriage?', 'Yes, one of the most romantically charged pairings. Venus and Mars are the classical love-passion combination.'),
    ('What is the main risk between 6 and 9?', 'Avoiding hard conversations to keep the beautiful surface. Both partners must commit to resolution, not just restoration.'),
    ('Are 6 and 9 compatible in business?', 'Yes, especially in creative, hospitality, design, or any field where aesthetic and energy matter.'),
    ('Do 6 and 9 fade in long marriage?', 'Rarely. Both partners actively keep the relationship sensorial, food, touch, beauty, conversation. Couples who tend to this daily last.'),
  ]),

  (7, 8, 'Caution', 'Ketu and Saturn', dict(
    one_liner='Ketu meets Saturn: the karmic pairing. Deep, serious, often heavy. Lifelong if conscious.',
    para1='Number 7 (Ketu) and Number 8 (Saturn) is a pairing of weight. Both partners are introspective, responsibility-aware, and uninterested in superficial relationships. When they pair, the connection is genuinely deep, often described as "feeling known immediately".',
    para2='Strength: very high mutual respect. Both partners take the relationship seriously; neither plays games. The depth of conversation, intention, and commitment is rare.',
    para3='Friction: both can default to seriousness. The relationship can lose its lightness, its play, its everyday warmth. Couples who deliberately build small joys into the week, small humour, small adventures, save the marriage from becoming a shared meditation.',
    bullets=[
      'Communication style: spare, deliberate, weighted.',
      'Conflict pattern: cold and structural rather than hot. Bring warmth back fast.',
      'Friendship depth: rare and lifelong; survives long absences.',
      'Watch for: the relationship becoming purely about responsibility and forgetting joy.',
    ],
  ), [
    ('Is 7 and 8 good for marriage?', 'It can be, but the pairing requires deliberate work on lightness. The natural seriousness of both numbers can overweigh the relationship.'),
    ('What do 7 and 8 share?', 'Both take responsibility seriously, both are introspective, both prefer depth over performance. Mutual respect comes naturally.'),
    ('Are 7 and 8 spiritually compatible?', 'Yes, very. Many of these marriages are anchored in shared spiritual practice or philosophical alignment.'),
    ('What should a 7-8 couple watch for?', 'Joylessness. The relationship can drift toward shared burden. Small daily lightness, humour, play, shared meals, protects it.'),
  ]),

  (8, 9, 'Caution', 'Saturn and Mars', dict(
    one_liner='Saturn meets Mars: structure meets fire. A pairing that produces real friction or real partnership, never neutrality.',
    para1='Number 8 (Saturn) and Number 9 (Mars) is a pairing of strong, immovable forces. Saturn wants to plan, structure, persist; Mars wants to act, fight, move now. Without conscious work the relationship oscillates between feeling stuck and feeling on fire.',
    para2='When it works: Saturn provides the structure within which Mars\' energy compounds. The 9 fights the right battles; the 8 builds the lasting platform. Together the couple often produces something significant in the world.',
    para3='When it struggles: 8 feels burdened by 9\'s urgency; 9 feels suffocated by 8\'s pace. The fix is role clarity. Each partner needs a domain where they unambiguously lead.',
    bullets=[
      'Communication style: direct from 9, considered from 8. Both must adapt.',
      'Conflict pattern: 9 erupts, 8 withdraws and waits. Both feel unheard.',
      'Friendship depth: builds slowly but holds firmly once established.',
      'Watch for: power struggles around timing, decision pace, and money.',
    ],
  ), [
    ('Is 8 and 9 good for marriage?', 'It works when both partners have clear separate domains. Without that, the structural-vs-impulsive tension wears the relationship down.'),
    ('What do 8 and 9 share?', 'Both are immovable when committed. Both bring intensity to whatever they enter. Both respect strength in the other.'),
    ('Are 8 and 9 compatible in business?', 'Yes if the 8 handles long-term structure and 9 handles execution and disruption. The pair can produce significant ventures.'),
    ('What is the main 8-9 friction?', 'Pace. 9 wants now, 8 wants when-it-is-right. Couples who agree on a shared time-horizon for big decisions reduce most of the conflict.'),
  ]),
]


def render_pair(a, b, rating, planet_summary, content, faqs):
    pa, ga = PLANETS[a]
    pb, gb = PLANETS[b]
    title = f'Number {a} and {b} Compatibility ({pa} & {pb}) · Chaldean Numerology'
    desc  = f'Number {a} ({pa}) and Number {b} ({pb}) compatibility, in marriage, friendship and business. {rating} match. The strengths, frictions, and what makes it last, plain English.'
    og_desc = f'{pa} and {pb} compatibility decoded, marriage, friendship, business, strengths and frictions.'
    canon = f'{BASE}/number-{a}-and-{b}-compatibility'

    article = make_article(title, desc, canon)
    breadcrumb = make_breadcrumb(f'Number {a} & {b} Compatibility', canon)
    faq_dict = make_faq(faqs)
    aj, bj, fj = jsonld(article, breadcrumb, faq_dict)

    keywords = (
        f'number {a} and {b} compatibility, {a} {b} compatibility, '
        f'moolank {a} {b} compatibility, life path {a} and {b}, '
        f'{pa.lower()} {pb.lower()} compatibility, chaldean numerology compatibility, '
        f'number {a} number {b} marriage'
    )

    head = HEAD.format(
        n=a, title=title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        keywords=keywords,
        article_json=aj, breadcrumb_json=bj, faq_json=fj,
    )

    bullets_html = '\n'.join(f'      <li>{b_}</li>' for b_ in content['bullets'])
    faq_html = '\n'.join(f'    <details><summary>{q}</summary><p>{a_}</p></details>' for q, a_ in faqs)

    body_html = f'''
  <p><strong>{content["one_liner"]}</strong></p>

  <p>{content["para1"]}</p>

  <h2>What works between Number {a} and Number {b}</h2>
  <p>{content["para2"]}</p>

  <h2>What to watch for</h2>
  <p>{content["para3"]}</p>

  <div class="seo-tells">
    <h3>Quick read: how this pairing actually plays out</h3>
    <ul>
{bullets_html}
    </ul>
  </div>

  <h2>Compatibility verdict: {rating}</h2>
  <p>In Cheiro\'s planetary triangles, Number {a} ({pa}) and Number {b} ({pb}) sit as a <strong>{rating.lower()}</strong> pairing. This describes the natural slope, not destiny. Many lifelong marriages exist in pairings traditionally cautioned against; the variable is awareness.</p>
'''

    cta = f'''
<div class="seo-cta-band">
  <h3>See your full compatibility map in 10 seconds</h3>
  <p>Beyond a single-number match, check both birth dates against the full Chaldean compatibility model. Free, no signup. Or unlock the full report for <strong>INR 499 &middot; $5 USD</strong>.</p>
  <div class="btn-pair">
    <a href="/love-compatibility-numerology" class="primary">Compatibility check →</a>
    <a href="/report" class="outline">Full Report INR 499 &middot; $5</a>
    <a href="/ask-aura" class="outline">Ask Aura</a>
  </div>
</div>
'''

    sidebar = f'''
  <aside class="seo-aside">
    <div class="article-sidebar">
      <div class="eyebrow">Free Analysis</div>
      <h3>Check your own compatibility</h3>
      <p>Get a full Chaldean compatibility read for any two birth dates. Marriage, business, friendship, family. 10 seconds.</p>
      <a href="/love-compatibility-numerology" class="cta">Free check →</a>
      <a href="/ask-aura" class="cta outline">✦ Ask Aura</a>
      <div class="sep"></div>
      <div class="eyebrow">Full Destiny Report</div>
      <h3>Your personalised PDF</h3>
      <div class="price-row">
        <span class="price-inr">INR 499</span>
        <span class="price-usd">or $5 USD</span>
      </div>
      <p>5-year forecast, name corrections, remedies, compatibility map, mobile-number check.</p>
      <a href="/report" class="cta">Get the report →</a>
    </div>
  </aside>
'''

    related_links = [
        (f'Number {a}', f'Number {a} in Love · How {pa}-led people show up', f'/number-{a}-in-love'),
        (f'Number {b}', f'Number {b} in Love · How {pb}-led people show up', f'/number-{b}-in-love'),
        (f'Life Path {a}', f'Life Path Number {a} · {pa}', f'/life-path-number-{a}-meaning'),
        (f'Life Path {b}', f'Life Path Number {b} · {pb}', f'/life-path-number-{b}-meaning'),
        ('Compatibility', 'Free Chaldean compatibility check', '/love-compatibility-numerology'),
        ('Ask Aura', 'Ask Aura about your relationship', '/ask-aura'),
    ]
    related_html = '\n'.join(
        f'      <a href="{href}" class="seo-rel-card"><span class="eb">{eb}</span><span class="ti">{ti}</span></a>'
        for (eb, ti, href) in related_links
    )

    page = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/sitemap-pages">Numerology Guides</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">Number {a} & {b} Compatibility</span>
</nav>

<header class="seo-hero">
  <div class="container">
    <div class="badge">Compatibility · {pa} &amp; {pb}</div>
    <div class="glyph">{ga}{gb}</div>
    <h1>Number {a} and {b} Compatibility</h1>
    <div class="tag">{planet_summary} pairing. The strengths, frictions and long-arc dynamics, decoded.</div>
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


def build():
    for (a, b, rating, planet_summary, content, faqs) in PAIRS:
        html = render_pair(a, b, rating, planet_summary, content, faqs)
        out_path = os.path.join(OUT, f'number-{a}-and-{b}-compatibility.html')
        with open(out_path, 'w') as fh: fh.write(html)
        print(f'  wrote {out_path}')


if __name__ == '__main__':
    build()
    print(f'\n{len(PAIRS)} compatibility pair pages built.')
