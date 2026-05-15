#!/usr/bin/env python3
"""
Build the "Number N spiritual meaning" SEO cluster (9 pages).

Target: high-intent spiritual / self-discovery queries:
  - "number 7 spiritual meaning"
  - "what is the spiritual meaning of number 9"
  - "moolank 3 spiritual significance"
  - "life path 4 spiritual journey"

URL pattern: /number-{n}-spiritual-meaning
"""
import os
from _seo_template import render_page, PLANETS, BASE

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA = {
1: dict(
  planet='Sun',
  essence='The spiritual meaning of Number 1 is the soul that came here to begin, to initiate, to be the first light into a darkness others did not yet see. The Sun does not borrow its light. Number 1 souls are not here to follow inherited spiritual paths; they are here to find their own relationship with the divine, even if that relationship looks like nothing their family taught them.',
  lesson='The spiritual lesson is sovereignty. Real authority comes from inner alignment, not from credentials, lineage, or permission. Number 1 grows by learning to trust the inner light when no external system validates it yet.',
  practice='Solo morning ritual. Even fifteen minutes. The Sun strengthens through deliberate one-on-one time with itself, no community, no teacher, no script.',
  symbols=['The single flame', 'The dawn', 'The crown', 'The lone figure on a mountain'],
  shadow='The shadow is becoming the false guru, mistaking personal certainty for universal truth. The spiritual work is to stay a seeker even as you become a teacher.',
),
2: dict(
  planet='Moon',
  essence='The spiritual meaning of Number 2 is the soul that came here to feel, to mirror, to hold space for others\' emotional reality. The Moon does not generate light; it receives and reflects. Number 2 souls are here to do the deeply spiritual work of attunement, of being present to what is, without needing to fix it.',
  lesson='The spiritual lesson is receptivity without dissolution. To be deeply open and still know where you end and the other begins. Number 2 grows by learning that empathy is not the same as merging.',
  practice='Water rituals. Bathing, swimming, sitting near water. Journaling at dawn or dusk. The Moon strengthens through emotional decompression, not stimulation.',
  symbols=['The crescent', 'The mirror', 'The pearl', 'The chalice'],
  shadow='The shadow is losing yourself in others\' emotional weather. The spiritual work is becoming a clear mirror, not a sponge.',
),
3: dict(
  planet='Jupiter',
  essence='The spiritual meaning of Number 3 is the soul that came here to expand, to teach, to make the invisible visible through expression. Jupiter is the guru, the wisdom-keeper, the one who carries inherited knowledge forward. Number 3 souls feel called to share what they discover, often without being asked.',
  lesson='The spiritual lesson is discernment within abundance. Jupiter offers many paths; choosing one and going deep takes more wisdom than sampling all of them. Number 3 grows by committing.',
  practice='Daily writing or speaking. Even five minutes. Jupiter strengthens through expression, not silence. Sharing what you have learned with one person a day clarifies it for yourself.',
  symbols=['The tree', 'The book', 'The compass', 'The teacher and student'],
  shadow='The shadow is the dilettante, the one who knows a little about many traditions but commits to none. The spiritual work is becoming a real student of one thing.',
),
4: dict(
  planet='Rahu',
  essence='The spiritual meaning of Number 4 is the soul that came here to break inherited patterns, often through paths their ancestors would not recognise as spiritual at all. Rahu is the disruptor; Number 4 souls often feel called to traditions outside their birth culture, or to forge entirely new spiritual frameworks.',
  lesson='The spiritual lesson is groundedness within disruption. Rahu can spin too fast; Number 4 grows by anchoring in daily ritual even as the outer life keeps reinventing.',
  practice='Embodied practice. Yoga, breathwork, martial arts, walking meditation. Rahu strengthens through the body, not the mind, because the mind alone runs too fast.',
  symbols=['The dragon\'s head', 'The lightning bolt', 'The bridge between worlds', 'The translator'],
  shadow='The shadow is restlessness disguised as seeking. The spiritual work is staying with one practice long enough for it to actually transform you, not just inform you.',
),
5: dict(
  planet='Mercury',
  essence='The spiritual meaning of Number 5 is the soul that came here to move between worlds, to translate, to ask the questions others have stopped asking. Mercury is the messenger; Number 5 souls often serve as a bridge between traditions, generations, or ways of knowing.',
  lesson='The spiritual lesson is depth within breadth. Mercury can collect spiritual ideas without metabolising any of them. Number 5 grows by sitting with one practice long enough to feel its weight.',
  practice='Conscious silence. A daily window where the mind is not consuming information. Mercury strengthens not through more input but through digestion.',
  symbols=['The winged sandal', 'The crossroads', 'The scroll', 'The traveller'],
  shadow='The shadow is spiritual ADHD: switching teachers, methods, and frameworks before any one has time to work. The spiritual work is choosing depth.',
),
6: dict(
  planet='Venus',
  essence='The spiritual meaning of Number 6 is the soul that came here to find the sacred in beauty, in love, in the body. Venus is the bridge between the spirit and the senses; Number 6 souls often feel the divine more easily through art, food, music, and intimacy than through abstract doctrine.',
  lesson='The spiritual lesson is devotion without attachment. Number 6 loves deeply, and the work is learning to love without needing the loved thing to stay the same. Venus matures into pure devotion only when the grip loosens.',
  practice='Aesthetic ritual. Lighting a candle. Arranging flowers. Cooking with attention. Venus strengthens through any act that honours beauty without consuming it.',
  symbols=['The rose', 'The dove', 'The chalice of wine', 'The lover and beloved'],
  shadow='The shadow is mistaking comfort for spiritual practice. The work is letting beauty crack you open, not soothe you to sleep.',
),
7: dict(
  planet='Ketu',
  essence='The spiritual meaning of Number 7 is the most explicitly spiritual of all the numbers. Ketu is the moksha karaka, the planet of liberation. Number 7 souls came here to remember what they already know, to peel away the layers that the world insists are them, and to find what was here before the layers.',
  lesson='The spiritual lesson is detachment without coldness. Ketu can become so disinterested in the world that it loses tenderness. Number 7 grows by learning that liberation includes love, not bypasses it.',
  practice='Silent retreat, even short ones. Half a day a week, no input. Reading sacred text slowly. Ketu strengthens through stillness, not stimulation.',
  symbols=['The dragon\'s tail', 'The empty cup', 'The mountain cave', 'The hermit\'s lamp'],
  shadow='The shadow is spiritual bypassing, using detachment to avoid the ordinary human work of relationships, money, and responsibility. The work is staying engaged while remembering you are not the engagement.',
),
8: dict(
  planet='Saturn',
  essence='The spiritual meaning of Number 8 is the soul that came here to learn through structure, time, and consequence. Saturn is the karma karaka, the lord of the long-arc lesson. Number 8 souls are not here for quick awakenings; they are here for the slow, durable work that takes a lifetime to compound.',
  lesson='The spiritual lesson is faith inside the long delay. Saturn rarely rewards immediately. Number 8 grows by trusting the work even when no result is yet visible. The Saturn return at 28-30 is often the threshold where the early seeds begin to flower.',
  practice='Daily discipline. The same time, the same place, the same simple practice. Saturn strengthens through repetition, not novelty. Twenty minutes a day for ten years compounds into something fifteen minutes a day for one week never does.',
  symbols=['The mountain', 'The hourglass', 'The black stone', 'The patient teacher'],
  shadow='The shadow is grimness, treating spiritual life as another duty. The work is finding the quiet joy inside the discipline itself.',
),
9: dict(
  planet='Mars',
  essence='The spiritual meaning of Number 9 is the soul that came here to fight for something larger than itself, to bring fire to causes that need defending. Mars is the warrior, but the highest expression of Mars is the protector, not the conqueror. Number 9 souls are often spiritual activists, whether or not they would use that word.',
  lesson='The spiritual lesson is anger transmuted into devotion. Mars feels everything sharply, and Number 9 grows by learning to channel the fire into the work, not into the people in the way of the work.',
  practice='Physical practice with intention. Running, climbing, building, dancing. Mars strengthens through the body in motion, ideally for a purpose larger than fitness alone.',
  symbols=['The sword', 'The flame', 'The warrior on horseback', 'The blacksmith'],
  shadow='The shadow is righteous anger that consumes the cause it was meant to defend. The work is staying soft enough that the fire heals rather than burns.',
),
}


def build():
    for n, d in DATA.items():
        planet = d['planet']
        title = f'Number {n} Spiritual Meaning · The {planet}-Led Soul Path'
        desc  = f'The spiritual meaning of Number {n} ({planet}), what your soul came here to learn, the lesson, the practice, the symbols and the shadow. Chaldean numerology, plain English.'
        og_desc = f'The spiritual meaning of Number {n}, the {planet}-led soul path, lesson, practice and shadow.'
        canon = f'{BASE}/number-{n}-spiritual-meaning'

        symbols_html = '\n'.join(f'      <li>{s}</li>' for s in d['symbols'])

        body_html = f'''
  <p>Numerology is often read as a personality system. Read deeper, every number is also a <strong>soul path</strong>, a felt direction your spirit is travelling in this lifetime. The spiritual meaning of Number {n} is the <strong>{planet}-led journey</strong>, and it does not look the same as any other number\'s journey.</p>

  <h2>The essence of the {planet}-led path</h2>
  <p>{d["essence"]}</p>

  <h2>The spiritual lesson</h2>
  <p>{d["lesson"]}</p>

  <h2>How Number {n} grows spiritually</h2>
  <p>{d["practice"]}</p>

  <div class="seo-tells">
    <h3>Symbols that speak to Number {n}</h3>
    <ul>
{symbols_html}
    </ul>
  </div>

  <h2>The spiritual shadow of Number {n}</h2>
  <p>Every soul path has its corresponding shadow, the way the same vibration can go sideways when unconscious. For Number {n}:</p>
  <p>{d["shadow"]}</p>

  <h2>Is the spiritual meaning of Number {n} fixed?</h2>
  <p>The vibration is fixed, what you do with it is not. Two people with the same Number {n} can live entirely different spiritual lives, one running mostly the shadow, the other gradually unfolding into the essence. The spiritual work is becoming conscious of which one you are running, and choosing.</p>
  <p>If you came to this page on a night when something felt unsettled or strangely sharp, that is not coincidence. The {planet}-led soul recognises itself in language. Reading the path back to yourself is often the first step.</p>
'''

        faqs = [
          (f'What does Number {n} mean spiritually?',
           f'It means your soul is on a {planet}-led path, with its own essence, lesson, practice and shadow. The page above describes each in detail.'),
          (f'Is Number {n} a lucky spiritual number?',
           f'Every number is "lucky" when its path is consciously walked, and "unlucky" when it is run as shadow. Number {n} is no different. The opportunity is in becoming aware of the vibration, not in escaping it.'),
          (f'Can I follow a spiritual path that is not natural to my Number {n}?',
           f'You can, but the slope works against you. Most who try eventually return to the practice that matches their vibration, the one that lets the spiritual work feel like coming home rather than effortful climbing.'),
          (f'Does my Life Path Number {n} or my Birth Number {n} shape this more?',
           f'Both. Life Path {n} (Bhagyank) shapes the long-arc soul direction; Birth Number {n} (Moolank, day of birth) shapes the daily expression. If both are {n}, the {planet}-led path is the most pronounced.'),
        ]

        related = [
          (f'Life Path {n}', f'Life Path Number {n} · {planet}', f'/life-path-number-{n}-meaning'),
          (f'Name Number {n}', f'Name Number {n} · How your name vibrates', f'/name-number-{n}-meaning'),
          (f'Emotional Pattern', f'Why Number {n} overthinks', f'/why-number-{n}-overthinks'),
          (f'Love Style', f'Number {n} in love', f'/number-{n}-in-love'),
          ('Ask Aura', 'Ask Aura about your path', '/ask-aura'),
          ('Free Analysis', 'See your full Chaldean chart', '/analyzer'),
        ]

        keywords = (
          f'number {n} spiritual meaning, {planet.lower()} spiritual meaning, '
          f'moolank {n} spiritual, life path {n} spiritual, '
          f'number {n} soul path, chaldean numerology spiritual, '
          f'number {n} meaning life path'
        )

        html = render_page(
          n=n, title=title, desc=desc, og_desc=og_desc, canon=canon,
          crumb_label=f'Number {n} Spiritual Meaning',
          keywords=keywords,
          hero_badge=f'Spiritual Meaning · Number {n}',
          hero_h1=f'Number {n} Spiritual Meaning · The {planet}-Led Soul Path',
          hero_tag=f'What your soul came here to learn under {planet}. The essence, the lesson, the practice, the shadow, in plain English.',
          body_html=body_html, faqs=faqs, related_links=related,
        )
        out_path = os.path.join(OUT, f'number-{n}-spiritual-meaning.html')
        with open(out_path, 'w') as fh: fh.write(html)
        print(f'  wrote {out_path}')


if __name__ == '__main__':
    build()
    print('\n9 spiritual meaning pages built.')
