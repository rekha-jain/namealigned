#!/usr/bin/env python3
"""
Build the "Number N in love" SEO cluster (9 pages).

Target: long-tail relationship-intent queries:
  - number 6 in love
  - how does number 7 love
  - dating a number 1 person
  - moolank N relationship style
  - life path N love compatibility

URL pattern: /number-{n}-in-love
"""
import os
from _seo_template import render_page, PLANETS, BASE

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA = {
1: dict(
  planet='Sun',
  love_style='Number 1 in love is steady, protective, and slow to commit but immovable once committed. The Sun does not flirt. When Number 1 chooses you, they usually do not change their mind, even when life makes the choice harder.',
  attraction='Number 1 is drawn to people who already have a centre, your own work, your own people, your own opinions. They do not want to be your only world; they want a partner with their own gravity.',
  green_flags=[
    'Plans and follows through on plans',
    'Shows up for the unglamorous days, not just the celebrations',
    'Tells you the hard truth gently',
    'Treats your career ambition as a shared project, not competition',
  ],
  shadow='Number 1 can confuse leadership with control. The shadow shows up when they start "improving" you, your habits, your friends, your work, instead of trusting your judgement.',
  longterm='With a settled Number 1, long-term love feels like a fortress. The cost is that warmth has to be deliberately practised, the Sun is not naturally tender, but it is loyal at a depth most people underestimate.',
  best_with=[1, 2, 4, 9],
  good_with=[3, 5, 6],
  caution_with=[7, 8],
),
2: dict(
  planet='Moon',
  love_style='Number 2 in love is emotionally porous, intuitive about your mood before you have named it, and almost embarrassingly devoted once they feel safe. The Moon loves through felt presence, not declarations.',
  attraction='Number 2 is drawn to people who can hold emotion without flinching, partners who do not run from sadness, who can sit with complexity, who can be patient with a heart that needs time to open.',
  green_flags=[
    'Texts back even when the conversation has paused for hours',
    'Notices small things, your favourite mug, the way you tense before phone calls',
    'Does not punish you for emotional honesty',
    'Creates routines, weekly dinner, Sunday walk, that anchor the relationship',
  ],
  shadow='Number 2 can over-absorb the partner\'s feelings until they lose track of their own. The shadow looks like resentment that arrives late, after months of unspoken accommodation.',
  longterm='With a Number 2, long-term love is a slow-built sanctuary. The Moon\'s gift is that the relationship deepens with time, the early intensity matures into a quiet, reliable closeness most people never reach.',
  best_with=[1, 2, 7],
  good_with=[4, 6, 8],
  caution_with=[3, 5, 9],
),
3: dict(
  planet='Jupiter',
  love_style='Number 3 in love is generous, expressive, and openly affectionate. Jupiter does not under-state. When Number 3 loves you, you (and likely several other people) will hear about it.',
  attraction='Number 3 is drawn to partners who can match their range, conversation, social life, intellectual play, travel. They get bored with sameness and thrive with someone whose world keeps expanding.',
  green_flags=[
    'Introduces you to their world, friends, family, work, quickly',
    'Plans experiences, trips, dinners, dates that feel like events',
    'Speaks openly about the relationship, even to strangers',
    'Encourages your ambition, even when it pulls you away from them',
  ],
  shadow='Number 3 can confuse charm with depth. The shadow shows up when the love stays in the warm-but-public layer and never goes into the harder private conversations the relationship needs.',
  longterm='With a Number 3, long-term love means committing to keep growing together. Jupiter rewards expansion; stasis suffocates it. Couples who plan rituals of newness, learning, travel, new shared projects, last longest.',
  best_with=[3, 6, 9],
  good_with=[1, 5],
  caution_with=[2, 4, 8],
),
4: dict(
  planet='Rahu',
  love_style='Number 4 in love is unconventional, intensely loyal, and not easily understood. Rahu does not love the way scripts say to love; it builds something that does not have a name yet.',
  attraction='Number 4 is drawn to partners who do not require them to be normal. They want someone who finds their oddness interesting, not something to manage.',
  green_flags=[
    'Lets you be strange without translating',
    'Does not need the relationship to look like other relationships',
    'Reliable in private, even if unconventional in public',
    'Talks about long-term plans without flinching at the foreign-feeling parts of them',
  ],
  shadow='Number 4 can ghost emotionally when the conventional pressure builds. The shadow is not cruelty; it is overwhelm at being asked to perform a version of love they do not actually believe in.',
  longterm='With a Number 4, long-term love is freer than most. Rahu rewards couples who write their own rules and resist comparing the relationship to anyone else\'s.',
  best_with=[1, 2, 4, 8],
  good_with=[6, 7],
  caution_with=[3, 5, 9],
),
5: dict(
  planet='Mercury',
  love_style='Number 5 in love is playful, curious, mentally electric, and allergic to anything that feels like a cage. Mercury loves through conversation, ideas, jokes, and shared adventures, not through declarations.',
  attraction='Number 5 is drawn to partners who can keep up, intellectually, conversationally, and in terms of movement. They want a fellow explorer, not a stationary anchor.',
  green_flags=[
    'Texts you something interesting every day, not just check-ins',
    'Plans spontaneous things and is delighted when you do too',
    'Does not require routine, but shows up reliably for the things that matter',
    'Talks ideas openly, including the half-formed ones',
  ],
  shadow='Number 5 can chase novelty into territory that costs the relationship. The shadow is not always infidelity; it is the slow drift of attention to anywhere except here.',
  longterm='With a Number 5, long-term love is built on shared evolution. Couples who keep learning, moving, travelling, starting new things together last longest. The Mercury mind needs newness, even within commitment.',
  best_with=[1, 5, 9],
  good_with=[3, 6],
  caution_with=[2, 4, 8],
),
6: dict(
  planet='Venus',
  love_style='Number 6 in love is romantic, sensual, devoted, and aesthetically present. Venus loves through beauty, comfort, the body, food, music, touch, the small daily rituals that say "you matter".',
  attraction='Number 6 is drawn to people who appreciate beauty in the same register, who notice details, who treat the relationship as something worth making lovely.',
  green_flags=[
    'Creates the home you both live in, literally and emotionally',
    'Remembers anniversaries, but more importantly, ordinary Tuesdays',
    'Is physically affectionate without prompting',
    'Treats the relationship as a creative project, beautiful, made, not just maintained',
  ],
  shadow='Number 6 can confuse harmony with health. The shadow is keeping the peace at the cost of saying hard things, until the unsaid hardens into resentment.',
  longterm='With a Number 6, long-term love is sensorial. The home is beautiful, the meals are good, the touch never thins out. The Venus relationship dies fastest when aesthetic care fades, so couples who keep tending the daily ritual last longest.',
  best_with=[3, 6, 9],
  good_with=[1, 2, 4],
  caution_with=[5, 7, 8],
),
7: dict(
  planet='Ketu',
  love_style='Number 7 in love is depth-oriented, quietly devoted, and uninterested in performance. Ketu does not flirt; it observes. When Number 7 falls, it is usually because someone showed them an inner world they could not look away from.',
  attraction='Number 7 is drawn to people with mystery, an undertone of solitude even in company, a private inner life that does not need to be performed. They are repelled by people who need constant validation.',
  green_flags=[
    'Comfortable with long silences in your company',
    'Asks questions most people do not think to ask',
    'Does not need daily proof; absences do not threaten them',
    'Shares a few real things instead of many surface things',
  ],
  shadow='Number 7 can disappear into solitude when the relationship asks for ordinary intimacy. The shadow is not coldness; it is a retreat from a closeness that started to feel demanding.',
  longterm='With a Number 7, long-term love is unusually quiet. Ketu rewards couples who protect each other\'s solitude, who do not require constant reassurance, who can sit together without needing to fill the space.',
  best_with=[1, 2, 7],
  good_with=[4, 9],
  caution_with=[3, 5, 6, 8],
),
8: dict(
  planet='Saturn',
  love_style='Number 8 in love is slow, careful, deeply serious, and built for the long haul. Saturn does not waste time; if they are putting time into you, they have already decided this matters.',
  attraction='Number 8 is drawn to people with maturity beyond their age, a sense of responsibility, and a willingness to build something durable rather than chase intensity.',
  green_flags=[
    'Shows you their plans, finances, work, calendar, real life, not a curated version',
    'Pays for things without keeping score',
    'Tells you what they are afraid of, eventually',
    'Treats your family with the same seriousness as their own',
  ],
  shadow='Number 8 can confuse responsibility with romance. The shadow is staying in a relationship because the structure is built, even when the love has gone cold.',
  longterm='With a Number 8, long-term love is rare in its solidity. Saturn rewards couples who do the unglamorous work, money conversations, family logistics, future planning, with the same attention they gave each other on the first date.',
  best_with=[3, 5, 6],
  good_with=[1, 2, 4],
  caution_with=[7, 8, 9],
),
9: dict(
  planet='Mars',
  love_style='Number 9 in love is intense, protective, passionate, and not subtle. Mars loves at temperature. When Number 9 is in, you feel it; when they pull back, you feel that too.',
  attraction='Number 9 is drawn to courage, in the partner\'s work, opinions, conflicts, willingness to fight for things. They are bored by people who play it safe in their own life.',
  green_flags=[
    'Defends you to others without being asked',
    'Tells you when you are being unfair, even when it costs the moment',
    'Initiates the hard conversations',
    'Brings physical, kinetic, active energy into the relationship, sport, dance, movement, building',
  ],
  shadow='Number 9 can mistake heat for love. The shadow is fighting often and calling it passion when it is actually unprocessed anger getting routed through the relationship.',
  longterm='With a Number 9, long-term love is alive. Mars rewards couples who keep the energy direct, who fight clean, who say what they mean, who do not let the resentment compost. The relationship dies of suppression long before it dies of conflict.',
  best_with=[3, 6, 9],
  good_with=[1, 5],
  caution_with=[2, 4, 7, 8],
),
}


def build():
    for n, d in DATA.items():
        planet = d['planet']
        title = f'Number {n} in Love · How {planet}-Led People Show Up in Relationships'
        desc  = f'Dating, married to, or wondering about a Number {n}? The {planet}-led love style, what they need, their green flags, their shadow, and who they are most compatible with. Chaldean numerology.'
        og_desc = f'How Number {n} loves, what they need, who they are best with.'
        canon = f'{BASE}/number-{n}-in-love'

        green_html = '\n'.join(f'      <li>{g}</li>' for g in d['green_flags'])

        body_html = f'''
  <p>If you were born on the {n}th of any month (or with Life Path {n}), your love style runs on <strong>{planet}</strong> energy. Whether you are the Number {n}, dating one, or married to one, the pattern below describes a specific way of showing up in love, not a personality stereotype, but a felt signature you can usually recognise once you see it named.</p>

  <h2>How Number {n} loves</h2>
  <p>{d["love_style"]}</p>

  <h2>What attracts Number {n}</h2>
  <p>{d["attraction"]}</p>

  <div class="seo-tells">
    <h3>Green flags from a Number {n} partner</h3>
    <ul>
{green_html}
    </ul>
  </div>

  <h2>The shadow side</h2>
  <p>Every {planet}-led love has a shadow. Naming it is not an accusation; it is information that helps the relationship survive its own pattern.</p>
  <p>{d["shadow"]}</p>

  <h2>What Number {n} long-term love looks like</h2>
  <p>{d["longterm"]}</p>

  <h2>Compatibility map for Number {n}</h2>
  <ul>
    <li><strong>Strongest harmony:</strong> Numbers {", ".join(str(x) for x in d["best_with"])}</li>
    <li><strong>Supportive:</strong> Numbers {", ".join(str(x) for x in d["good_with"])}</li>
    <li><strong>Asks for awareness:</strong> Numbers {", ".join(str(x) for x in d["caution_with"])}</li>
  </ul>
  <p>Compatibility in Chaldean numerology is not destiny. It describes the natural slope, who fits without friction, who fits with conscious work. Many long marriages are between "caution" pairs who became masters at the friction itself.</p>
'''

        faqs = [
          (f'Is Number {n} good in relationships?',
           f'Number {n} is genuinely strong in relationships once you understand the {planet}-led love style. The shadow described above is the cost of the strength, not a flaw to fix.'),
          (f'Who is the best match for Number {n}?',
           f'Strongest natural harmony with Numbers {", ".join(str(x) for x in d["best_with"])}. These pairings tend to find a rhythm with the least friction.'),
          (f'Does this apply if my Life Path is {n} but I was born on a different day?',
           f'Yes, partially. Life Path {n} (Bhagyank) shapes the long-arc themes of how you love over time. Your Birth Number (Moolank, the day you were born) shapes the day-to-day expression. Both matter; the patterns above blend the two.'),
          (f'How do I check my Number {n} partner\'s real compatibility with me?',
           f'Use the free compatibility tool below. It reads both birth dates against Chaldean planetary compatibility and gives you a more nuanced picture than a single-number match score.'),
        ]

        related = [
          ('Compatibility', 'Free Chaldean compatibility check', '/love-compatibility-numerology'),
          (f'Life Path {n}', f'Life Path Number {n} Meaning · {planet}', f'/life-path-number-{n}-meaning'),
          ('Emotional Pattern', f'Why Number {n} overthinks', f'/why-number-{n}-overthinks'),
          ('Talk to Aura', f'Ask Aura about your relationship', '/ask-aura'),
        ]

        keywords = f'number {n} in love, number {n} relationship, moolank {n} love, life path {n} love, dating number {n}, {planet.lower()} love style, chaldean numerology love'

        html = render_page(
          n=n, title=title, desc=desc, og_desc=og_desc, canon=canon,
          crumb_label=f'Number {n} in Love',
          keywords=keywords,
          hero_badge=f'Love Style · Number {n}',
          hero_h1=f'Number {n} in Love · How {planet}-Led People Show Up',
          hero_tag=f'The {planet}-led love style, what they need, what attracts them, what to watch for, and who they fit best with. Chaldean numerology, plain English.',
          body_html=body_html, faqs=faqs, related_links=related,
        )
        out_path = os.path.join(OUT, f'number-{n}-in-love.html')
        with open(out_path, 'w') as fh: fh.write(html)
        print(f'  wrote {out_path}')


if __name__ == '__main__':
    build()
    print('\n9 in-love pages built.')
