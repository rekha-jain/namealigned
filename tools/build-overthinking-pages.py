#!/usr/bin/env python3
"""
Build the "Why does Number N overthink" SEO cluster (9 pages).

Target: long-tail self-discovery queries:
  - why do number 7 people overthink
  - why is my mind always racing numerology
  - moolank N overthinking pattern
  - chaldean numerology and anxiety
  - life path N overthinking

URL pattern: /why-number-{n}-overthinks
"""
import os
from _seo_template import render_page, PLANETS, BASE

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each number's unique overthinking pattern, written for emotional self-recognition.
DATA = {
1: dict(
  planet='Sun',
  pattern='Sun-led overthinking sounds like "is this idea good enough to be worth my name on it?" Number 1 overthinks visibility, not the work itself. The loop is rarely "can I do this", it is "will the version of me people see line up with the version of me I want them to see".',
  triggers=[
    'About to put something visible into the world',
    'Compared to a peer who is moving faster',
    'Being asked to defer to someone with weaker judgement',
    'Public criticism, even from people whose opinion you do not respect',
  ],
  exit_pattern='Number 1 minds quiet when they ship. Stop refining, publish, and let the next idea pull you forward.',
  why_it_helps='The Sun rewards initiative more than perfection. A live thing in the world teaches you faster than another week of revision.',
),
2: dict(
  planet='Moon',
  pattern='Moon-led overthinking sounds like reading other people\'s emotions in your head, then looping over what their pause meant, their tone meant, what you might have missed. Number 2 minds rarely overthink themselves; they overthink the felt atmosphere around them.',
  triggers=[
    'A message that did not arrive when expected',
    'A tone shift in someone close to you',
    'A group conversation where you sensed unspoken tension',
    'A decision that affects someone you love',
  ],
  exit_pattern='Number 2 minds quiet when they write the feeling down or share it with one trusted person. Naming the emotion shrinks it.',
  why_it_helps='The Moon thrives on rhythm. Daily decompression, water, journaling, slow walks, prevents the overflow.',
),
3: dict(
  planet='Jupiter',
  pattern='Jupiter-led overthinking sounds like ten possible directions, all good, none chosen. Number 3 minds overthink not problems but choices. The loop is "but what if the other path is better".',
  triggers=[
    'A new opportunity opening on top of existing commitments',
    'A teacher or mentor figure giving conflicting advice',
    'Imagining the life you would have if you said yes to everything',
    'Watching a peer succeed in a field you also wanted',
  ],
  exit_pattern='Number 3 minds quiet when they commit to one path for a set time window. Jupiter rewards expansion, but only if you stop revising the strategy weekly.',
  why_it_helps='You are not missing the better path. Better and yours are different questions.',
),
4: dict(
  planet='Rahu',
  pattern='Rahu-led overthinking sounds like seeing fifteen failure modes nobody else noticed, then being told you are paranoid. Number 4 minds run pattern detection at high speed; the loop is the gap between what you see and what you can prove.',
  triggers=[
    'A team moving forward on a plan with obvious blind spots',
    'Being asked to trust a system you have already spotted breaking',
    'A change that feels too sudden, even when it is good',
    'A power dynamic where your unconventional read is being dismissed',
  ],
  exit_pattern='Number 4 minds quiet when they ship the prototype that proves the pattern. Words rarely convince; built things do.',
  why_it_helps='You are not paranoid. You are early. The job is finding the evidence others can also see.',
),
5: dict(
  planet='Mercury',
  pattern='Mercury-led overthinking sounds like seventeen tabs open in the mind at once, each with a half-thought, none completed. Number 5 minds overthink in breadth not depth, jumping across topics faster than any one of them lands.',
  triggers=[
    'A slow meeting after a high-stimulation morning',
    'Being asked to commit to one thing when the menu is large',
    'A long-term project you started but the curiosity drifted',
    'Information overload, news, scrolling, multiple group chats',
  ],
  exit_pattern='Number 5 minds quiet when they narrow the input. One task, one window, one trail of thought, until completion.',
  why_it_helps='Mercury is not anxiety. Mercury is movement. The fix is direction, not stillness.',
),
6: dict(
  planet='Venus',
  pattern='Venus-led overthinking sounds like running other people\'s comfort through your own mind, looping over what you might have said better, what they need, whether the relationship is okay. Number 6 minds overthink harmony, not strategy.',
  triggers=[
    'A friend pulling back without explanation',
    'A creative project where someone you care about will see the result',
    'A choice that puts your needs above someone else\'s',
    'Aesthetic dissatisfaction, your space, your work, your image feels off',
  ],
  exit_pattern='Number 6 minds quiet when they create something beautiful. The hands take over from the head.',
  why_it_helps='Venus needs the body involved. Cooking, writing, decorating, making, anything that turns thought into form.',
),
7: dict(
  planet='Ketu',
  pattern='Ketu-led overthinking sounds like an inner observer watching the watcher watch the watcher, recursive, philosophical, hard to escape. Number 7 minds overthink meaning itself. The loop is "what is this for, what am I actually doing, why does any of it matter".',
  triggers=[
    'A long stretch of routine work without meaning',
    'A relationship that became transactional',
    'A milestone that did not feel as significant as expected',
    'Quiet weekends, the absence of distraction',
  ],
  exit_pattern='Number 7 minds quiet when they touch something larger than themselves. Nature, silence, prayer, a long walk, the company of one person who can sit in depth with you.',
  why_it_helps='Ketu is not a problem to solve. The depth is the point. The job is not to escape it but to give it a container, daily contemplative time you choose, instead of letting it ambush you at 3am.',
),
8: dict(
  planet='Saturn',
  pattern='Saturn-led overthinking sounds like running every long-term consequence of every present decision, then looping over the cost of getting it wrong. Number 8 minds overthink consequence and responsibility. The loop is rarely the choice itself; it is everyone affected by the choice.',
  triggers=[
    'A major financial or career decision',
    'A family responsibility no one else is shouldering',
    'A delay that feels personal even though it is structural',
    'Looking back at the years invested in a path that did not pay off as expected',
  ],
  exit_pattern='Number 8 minds quiet when they shrink the time horizon. What is the next ninety days of this, not the next ten years.',
  why_it_helps='Saturn rewards persistence, but persistence is built ninety days at a time, not in single ten-year leaps.',
),
9: dict(
  planet='Mars',
  pattern='Mars-led overthinking sounds like replaying a conflict you have already left, re-arguing the case in your mind for hours. Number 9 minds overthink justice, fairness, and the things they did not get to say.',
  triggers=[
    'A boundary someone crossed without consequence',
    'A cause you cared about losing momentum',
    'A misunderstanding where your motives were misread',
    'Being told to calm down by people not carrying the weight',
  ],
  exit_pattern='Number 9 minds quiet when they channel the fire into action, not rumination. Move the body, work the problem, write the thing.',
  why_it_helps='Mars is not for sitting with. Mars is for using. The overthinking is fuel that has nowhere to go.',
),
}


def build():
    for n, d in DATA.items():
        planet = d['planet']
        title = f'Why Number {n} People Overthink (Chaldean Numerology + {planet})'
        desc  = f'Born on the {n}th, the 1{n}th, the 2{n}th or with Life Path {n}? The {planet}-led overthinking pattern, what triggers it, and how to quiet it. Plain English, Chaldean numerology.'
        og_desc = f'The overthinking pattern of Number {n} ({planet}-led), and how to quiet it.'
        canon = f'{BASE}/why-number-{n}-overthinks'

        triggers_html = '\n'.join(f'      <li>{t}</li>' for t in d['triggers'])

        body_html = f'''
  <p>If you were born on the {n}th, 1{n}th or 2{n}th of any month (or your Life Path Number reduces to {n}), your mind runs on <strong>{planet}</strong> energy. The overthinking pattern that comes with {planet} is specific, recognisable, and not a flaw you need to fix. It is information about what your mind is actually for.</p>

  <h2>The {planet}-led overthinking pattern</h2>
  <p>{d["pattern"]}</p>

  <div class="seo-tells">
    <h3>What sets it off</h3>
    <ul>
{triggers_html}
    </ul>
  </div>

  <h2>How to quiet it (without trying to think less)</h2>
  <p>{d["exit_pattern"]}</p>
  <p>{d["why_it_helps"]}</p>

  <h2>Is overthinking always bad for Number {n}?</h2>
  <p>No. The same {planet}-driven mind that loops at 3am is also the mind that sees what others miss in a meeting, anticipates a problem before it lands, or writes the thing that lasts. Overthinking is the cost of a perception system tuned higher than average. The skill is not turning it off, it is recognising the loop early and redirecting before it costs you sleep.</p>

  <p>If you carry Number {n} energy and you found this page on a tired night, that is not coincidence. The {planet}-led mind goes looking for itself in language. Reading the pattern named back to you is often the first thing that quiets the loop.</p>
'''

        faqs = [
          (f'Why does Number {n} overthink more than other numbers?',
           f'It is not "more", it is differently. Each ruling planet creates a unique overthinking signature. Number {n} loops on {planet}\'s specific themes, not on every theme at once.'),
          (f'Will my Number {n} overthinking go away with age?',
           f'The intensity often softens after the early 30s as {planet}\'s pattern becomes familiar and you stop being surprised by it. The loop itself rarely disappears entirely; you just stop fighting it.'),
          (f'Should I change my name to reduce overthinking?',
           f'No. Your Life Path Number comes from your birth date and cannot be changed. A name correction can support better alignment with your destiny number but it does not erase the cognitive style of your ruling planet.'),
          (f'Does this apply if my Moolank is different from my Bhagyank?',
           f'If you were born on the {n}th, the daily expression of {planet} energy is strongest. If your Bhagyank (sum of full birth date) is {n}, the long-arc pattern of {planet} shapes your destiny. Most overthinking patterns show up in both, with Moolank being more immediate.'),
        ]

        related = [
          (f'Life Path {n}', f'Life Path Number {n} Meaning · {planet}', f'/life-path-number-{n}-meaning'),
          (f'Name Number {n}', f'Name Number {n} Meaning · How your name vibrates', f'/name-number-{n}-meaning'),
          ('Love & Compatibility', f'Number {n} in love · what to expect', f'/number-{n}-in-love'),
          ('Talk to Aura', 'Ask Aura about your overthinking pattern', '/ask-aura'),
        ]

        keywords = f'why number {n} overthinks, number {n} overthinking, moolank {n} anxiety, life path {n} overthinking, {planet.lower()} overthinking, chaldean numerology overthinking, why my mind races numerology'

        html = render_page(
          n=n, title=title, desc=desc, og_desc=og_desc, canon=canon,
          crumb_label=f'Why Number {n} Overthinks',
          keywords=keywords,
          hero_badge=f'Emotional Pattern · Number {n}',
          hero_h1=f'Why Number {n} People Overthink',
          hero_tag=f'The {planet}-led mind has a specific overthinking signature. Once you can name it, you can stop fighting it.',
          body_html=body_html, faqs=faqs, related_links=related,
        )
        out_path = os.path.join(OUT, f'why-number-{n}-overthinks.html')
        with open(out_path, 'w') as fh: fh.write(html)
        print(f'  wrote {out_path}')


if __name__ == '__main__':
    build()
    print('\n9 overthinking pages built.')
