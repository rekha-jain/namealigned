#!/usr/bin/env python3
"""
Build the "Lucky days, colors, gemstones for Number N" SEO cluster (9 pages).

Target: high-intent practical queries:
  - "lucky color for number 7"
  - "lucky gemstone moolank 5"
  - "lucky days for number 1"
  - "lucky number for number 8 people"

URL pattern: /lucky-attributes-number-{n}
"""
import os
from _seo_template import render_page, PLANETS, BASE

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA = {
1: dict(
  planet='Sun',
  lucky_days=['Sunday', 'Monday'],
  good_dates=['1', '10', '19', '28'],
  lucky_colors=['Gold', 'Orange', 'Yellow', 'Bronze'],
  avoid_colors=['Black', 'Dark Blue'],
  gemstones=['Ruby (primary)', 'Yellow sapphire', 'Sunstone'],
  lucky_numbers=['1', '2', '4'],
  direction='East',
  best_months=['July', 'August', 'September'],
  metal='Gold',
  intro='Number 1 people draw vitality from the Sun. The luckiest hours fall between sunrise and noon, when the Sun is climbing. Decisions, signatures, presentations, and new beginnings made in that window tend to land more cleanly than those made later in the day.',
),
2: dict(
  planet='Moon',
  lucky_days=['Monday', 'Friday'],
  good_dates=['2', '11', '20', '29'],
  lucky_colors=['White', 'Cream', 'Silver', 'Pale Green'],
  avoid_colors=['Dark Red', 'Black'],
  gemstones=['Pearl (primary)', 'Moonstone', 'White sapphire'],
  lucky_numbers=['1', '2', '7'],
  direction='North-West',
  best_months=['June', 'July'],
  metal='Silver',
  intro='Number 2 people are most aligned during the waxing Moon phase. Initiatives launched between the new moon and full moon tend to find their footing more easily. The full moon itself often brings emotional clarity.',
),
3: dict(
  planet='Jupiter',
  lucky_days=['Thursday', 'Friday'],
  good_dates=['3', '12', '21', '30'],
  lucky_colors=['Yellow', 'Cream', 'Violet', 'Light Blue'],
  avoid_colors=['Black', 'Dark Brown'],
  gemstones=['Yellow Sapphire (primary)', 'Topaz', 'Citrine'],
  lucky_numbers=['3', '6', '9'],
  direction='North-East',
  best_months=['February', 'May', 'November'],
  metal='Gold',
  intro='Number 3 people thrive when Jupiter is strong, traditionally on Thursdays and during spring. Public-facing work like teaching, speaking, publishing or counselling tends to expand outward when initiated under these conditions.',
),
4: dict(
  planet='Rahu',
  lucky_days=['Saturday', 'Sunday'],
  good_dates=['4', '13', '22', '31'],
  lucky_colors=['Electric Blue', 'Grey', 'Khaki'],
  avoid_colors=['Pure Red', 'Pure White'],
  gemstones=['Hessonite / Gomedh (primary)', 'Smoky quartz'],
  lucky_numbers=['1', '5', '7'],
  direction='South-West',
  best_months=['June', 'July', 'August'],
  metal='Iron / Steel',
  intro='Number 4 people, ruled by Rahu, often find that luck arrives through unconventional channels and on days others consider "off". Saturday and Sunday hold steadiest energy. The unexpected route is frequently the right one.',
),
5: dict(
  planet='Mercury',
  lucky_days=['Wednesday', 'Friday'],
  good_dates=['5', '14', '23'],
  lucky_colors=['Light Green', 'Light Grey', 'Turquoise'],
  avoid_colors=['Brown', 'Pure Black'],
  gemstones=['Emerald (primary)', 'Peridot', 'Jade'],
  lucky_numbers=['5', '6', '9'],
  direction='North',
  best_months=['May', 'June', 'September'],
  metal='Mercury / Bronze',
  intro='Number 5 people resonate with Mercury\'s speed. Communication-heavy days (sending out applications, making asks, launching campaigns, signing contracts) work best on Wednesdays. Travel begun on Wednesday often unfolds smoothly.',
),
6: dict(
  planet='Venus',
  lucky_days=['Friday', 'Tuesday'],
  good_dates=['6', '15', '24'],
  lucky_colors=['Pink', 'Light Blue', 'White', 'Pastel Green'],
  avoid_colors=['Pure Black', 'Dark Brown'],
  gemstones=['Diamond (primary)', 'White sapphire', 'Opal'],
  lucky_numbers=['3', '6', '9'],
  direction='South-East',
  best_months=['April', 'May', 'October', 'November'],
  metal='Silver / Platinum',
  intro='Number 6 people are favoured by Venus on Fridays. Relationship moves, wedding dates, creative launches, hospitality openings and aesthetic decisions made on Friday tend to take well. Beauty-related work compounds.',
),
7: dict(
  planet='Ketu',
  lucky_days=['Monday', 'Sunday'],
  good_dates=['7', '16', '25'],
  lucky_colors=['Sea Green', 'Light Yellow', 'Cream', 'Pale Grey'],
  avoid_colors=['Dark Red', 'Pure Black'],
  gemstones=['Cat\'s Eye (primary)', 'Pearl', 'Moonstone'],
  lucky_numbers=['2', '7'],
  direction='North-East',
  best_months=['June', 'July'],
  metal='Silver',
  intro='Number 7 people, under Ketu, are most aligned when the energy is quiet. Major decisions made in early morning or late evening, away from public attention, tend to land more truly. Solo reflection often outperforms group consultation.',
),
8: dict(
  planet='Saturn',
  lucky_days=['Saturday', 'Sunday'],
  good_dates=['8', '17', '26'],
  lucky_colors=['Dark Blue', 'Black', 'Indigo', 'Charcoal'],
  avoid_colors=['Pure Red'],
  gemstones=['Blue Sapphire (primary, with caution)', 'Black tourmaline', 'Amethyst'],
  lucky_numbers=['4', '8'],
  direction='West',
  best_months=['December', 'January', 'February'],
  metal='Iron / Lead',
  intro='Number 8 people, under Saturn, find that the long-arc rewards arrive after persistence rather than around quick wins. Major commitments (long-term investments, marriage, real estate) made on Saturdays tend to last. Note: blue sapphire is powerful but must be tested before sustained wear.',
),
9: dict(
  planet='Mars',
  lucky_days=['Tuesday', 'Friday'],
  good_dates=['9', '18', '27'],
  lucky_colors=['Red', 'Pink', 'Crimson', 'Orange'],
  avoid_colors=['Black', 'Dark Brown'],
  gemstones=['Red Coral (primary)', 'Carnelian', 'Bloodstone'],
  lucky_numbers=['3', '6', '9'],
  direction='South',
  best_months=['April', 'October', 'November'],
  metal='Copper',
  intro='Number 9 people draw strength from Mars. Tuesday is the warrior\'s day, well-suited for confrontations, sport, surgical procedures, advocacy work, and any situation that requires courage. Physical exertion in the morning amplifies the day\'s effectiveness.',
),
}


def build():
    for n, d in DATA.items():
        planet = d['planet']
        title = f'Lucky Days, Colors &amp; Gemstones for Number {n} ({planet})'
        desc  = f'Number {n} lucky day, lucky color, gemstone, direction and dates under {planet}. Plain-English Chaldean guidance, what works and what to avoid. Free Chaldean check at the bottom.'
        og_desc = f'Number {n} lucky attributes, days, colors, gemstones, direction, decoded under {planet}.'
        canon = f'{BASE}/lucky-attributes-number-{n}'

        lucky_days_html  = ', '.join(d['lucky_days'])
        good_dates_html  = ', '.join(d['good_dates'])
        lucky_colors_html = ', '.join(d['lucky_colors'])
        avoid_colors_html = ', '.join(d['avoid_colors'])
        gemstones_html   = '\n'.join(f'      <li>{g}</li>' for g in d['gemstones'])
        lucky_numbers_html = ', '.join(d['lucky_numbers'])
        months_html      = ', '.join(d['best_months'])

        body_html = f'''
  <p>If you were born on the {n}th, 1{n}th or 2{n}th of any month (or your Life Path Number reduces to {n}), your luck patterns follow <strong>{planet}</strong>. The attributes below come from Cheiro\'s tradition and have been used by Chaldean practitioners for over a century.</p>

  <p>{d["intro"]}</p>

  <h2>Lucky days for Number {n}</h2>
  <p>Your strongest days of the week, in descending order: <strong>{lucky_days_html}</strong>. Plan significant launches, signings, conversations and beginnings on these days. They are not "magic"; they are weighted in your favour because the ruling planet is most accessible.</p>

  <h2>Lucky dates of the month</h2>
  <p>Dates that reduce to your number, or are inherently aligned with {planet}: <strong>{good_dates_html}</strong>. For very high-stakes events (marriage, business launch, registration), Chaldean practitioners often combine a lucky date with a lucky day. For example, a 14th that falls on a Friday is more strongly aligned than either alone.</p>

  <h2>Lucky colors</h2>
  <p>Wear, paint, or surround yourself with: <strong>{lucky_colors_html}</strong>.</p>
  <p>Avoid (especially on important days): <strong>{avoid_colors_html}</strong>.</p>
  <p>Color works subtly. You will not feel it dramatically, but over months of wearing your lucky colors during important moments, the slope tilts in your favour. Bridal outfits, business launches, key presentations are where the choice matters most.</p>

  <h2>Lucky gemstones</h2>
  <p>Traditional Chaldean stones for Number {n}, in descending order of power:</p>
  <ul>
{gemstones_html}
  </ul>
  <p><strong>Important caveat:</strong> Powerful stones (especially blue sapphire for Number 8 and cat\'s eye for Number 7) should be <em>tested</em> for 7-10 days before sustained wear. Wear it casually first; if anything in your daily life noticeably destabilises, remove it. Stones interact with each chart differently; tradition recommends professional consultation for the high-impact stones.</p>

  <h2>Lucky numbers (for phone, addresses, registrations)</h2>
  <p>Your luckiest numbers for things you choose, mobile numbers, vehicle registrations, addresses, are: <strong>{lucky_numbers_html}</strong>. These are not just your own number; they include numbers in harmonic relationship with yours under Cheiro\'s planetary triangles.</p>

  <h2>Direction</h2>
  <p>Sleep with your head toward <strong>{d["direction"]}</strong> for steadier energy. For homes and offices, position desk/study facing in this direction when possible.</p>

  <h2>Best months of the year</h2>
  <p>The months when {planet} is naturally elevated and your numerological resonance is strongest: <strong>{months_html}</strong>. Important launches, weddings, large investments and life-direction decisions made in these months tend to take well.</p>

  <h2>Metal</h2>
  <p>Wear or surround yourself with <strong>{d["metal"]}</strong>. This is the metal of your ruling planet and aligns subtly with your number\'s vibration. Rings, watches, pen-clips, and similar small daily items are practical entry points.</p>

  <h2>One honest note</h2>
  <p>None of these attributes are deterministic. A perfect lucky-day, lucky-color, lucky-gemstone combination will not save a fundamentally misaligned decision. And none of them are required for a good life. They are <em>tilt</em>, not <em>truth</em>. Use them where the tilt matters; ignore them where it does not.</p>
'''

        faqs = [
          (f'What is the luckiest day for Number {n}?',
           f'{d["lucky_days"][0]}, followed by {d["lucky_days"][1] if len(d["lucky_days"]) > 1 else d["lucky_days"][0]}. Both align with {planet}\'s strongest weekday positions in Chaldean tradition.'),
          (f'What is the luckiest color for Number {n}?',
           f'{d["lucky_colors"][0]} is the primary lucky color, with {", ".join(d["lucky_colors"][1:])} also supportive. {planet} is the planet behind these choices.'),
          (f'Should Number {n} wear {d["gemstones"][0].split(" (")[0]}?',
           f'{d["gemstones"][0].split(" (")[0]} is the traditional primary stone. Wear it on a trial basis (7-10 days) before sustained wear; some stones, like blue sapphire, are strong enough that practitioners recommend testing first.'),
          (f'What is the unluckiest color for Number {n}?',
           f'Avoid {d["avoid_colors"][0]} and {d["avoid_colors"][1] if len(d["avoid_colors"]) > 1 else d["avoid_colors"][0]} on important days. These work against {planet}\'s natural vibration.'),
        ]

        related = [
          (f'Life Path {n}', f'Life Path Number {n} · {planet}', f'/life-path-number-{n}-meaning'),
          (f'Name Number {n}', f'Name Number {n} · How your name vibrates', f'/name-number-{n}-meaning'),
          (f'Spiritual Meaning', f'Number {n} spiritual meaning', f'/number-{n}-spiritual-meaning'),
          (f'Love Style', f'Number {n} in love', f'/number-{n}-in-love'),
          ('Free Analysis', 'See your full Chaldean chart', '/analyzer'),
          ('Ask Aura', f'Ask Aura about Number {n}', '/ask-aura'),
        ]

        keywords = (
          f'lucky color for number {n}, lucky day number {n}, lucky gemstone moolank {n}, '
          f'number {n} lucky days, {planet.lower()} lucky color, moolank {n} lucky stone, '
          f'lucky number for number {n}, chaldean numerology lucky'
        )

        html = render_page(
          n=n, title=title, desc=desc, og_desc=og_desc, canon=canon,
          crumb_label=f'Lucky Attributes Number {n}',
          keywords=keywords,
          hero_badge=f'Lucky Attributes · Number {n}',
          hero_h1=f'Lucky Days, Colors &amp; Gemstones for Number {n}',
          hero_tag=f'{planet}-aligned attributes from Chaldean tradition. Days, colors, dates, gemstones, directions, decoded.',
          body_html=body_html, faqs=faqs, related_links=related,
        )
        out_path = os.path.join(OUT, f'lucky-attributes-number-{n}.html')
        with open(out_path, 'w') as fh: fh.write(html)
        print(f'  wrote {out_path}')


if __name__ == '__main__':
    build()
    print('\n9 lucky-attributes pages built.')
