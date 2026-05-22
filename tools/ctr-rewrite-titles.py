#!/usr/bin/env python3
"""
Rewrite <title> and <meta description> on long-tail pages for emotional
curiosity-driven CTR. Replaces generic numerology framing with the
emotional-pattern framing the user actually responds to in SERPs.

Examples:
  Before: "Why Number 7 People Overthink (Chaldean Numerology + Ketu)"
  After:  "Why Some People Overthink Everything, A Number 7 Read"

  Before: "Number 4 in Love, How Rahu-Led People Show Up in Relationships"
  After:  "Why Number 4 People Love Differently, The Unconventional Heart"
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Per-cluster CTR rewrites. (title, description) by number.
OVERTHINK = {
1: ('Why Some Sun-Led Minds Cannot Stop Strategising, A Number 1 Read',
    'The Number 1 overthinking signature is not anxiety, it is the pressure of self-led ambition. What sets it off, what quiets it, and what the loop is actually about.'),
2: ('Why Some People Replay Conversations All Night, A Number 2 Read',
    'The emotionally porous Number 2 mind reads tone, atmosphere, and silences as data. Why it does that, when it tips into overthinking, and what actually settles it.'),
3: ('Why Number 3 People Cannot Choose Just One Path',
    'The expressive, opportunity-rich Number 3 mind overthinks choices, not problems. Where the loops come from, and how to commit without feeling caged.'),
4: ('Why Number 4 People See Problems Others Will Notice in Three Months',
    'Born on the 4th, 13th, 22nd or 31st? Your unconventional pattern-vision is the gift behind the overthinking. Read what triggers it, and what to do with it.'),
5: ('Why Number 5 People Have Seventeen Tabs Open in Their Mind',
    'The Mercury-led mind absorbs faster than it digests. The Number 5 overthinking signature, and the one practice that genuinely slows it down.'),
6: ('Why Number 6 People Worry About Other People First',
    'The Venus-led mind overthinks harmony, comfort, and what other people need, often at the cost of their own. Why this happens, and how to break the cycle.'),
7: ('Why Number 7 People Cannot Switch Off the Inner Observer',
    'The Number 7 mind runs depth-philosophical loops at 3am, asking what any of it is for. Where the loop comes from, why it is not a flaw, and how to give it a container.'),
8: ('Why Number 8 People Carry Pressure No One Else Can See',
    'The Saturn-led mind overthinks consequence and responsibility, often for everyone around them. The Number 8 signature, and the one shift that actually helps.'),
9: ('Why Number 9 People Replay Arguments and Re-Win Them in Their Head',
    'The Mars-led mind overthinks justice and the things they did not get to say out loud. The Number 9 signature, the triggers, and how to channel the fire usefully.'),
}

IN_LOVE = {
1: ('Why Number 1 People Love Slowly and Stay Hard',
    'Sun-led love is steady, protective, and immovable once committed. What attracts them, their green flags, their shadow, and who they pair best with.'),
2: ('Why Number 2 People Love Through Tone, Not Words',
    'Moon-led love reads the unsaid before it is said. How a Number 2 partner shows up, what they need most, and which pairings let their loyalty actually bloom.'),
3: ('Why Number 3 People Love Out Loud and Quietly Need Depth',
    'Jupiter-led love is warm, generous, openly affectionate, and sometimes stops at the social surface. What Number 3 love really needs from a partner.'),
4: ('Why Number 4 People Love Differently, The Unconventional Heart',
    'Rahu-led love rarely fits scripts. Born on the 4th? See how Number 4 people actually show up in love, who fits, who suffocates them, and what their loyalty looks like.'),
5: ('Why Number 5 People Need Conversation More Than Comfort in Love',
    'Mercury-led love thrives on mental electricity, shared movement, and curiosity. How a Number 5 partner stays in love, and the kind of partner who keeps them.'),
6: ('Why Number 6 People Love Through Daily Acts, Not Grand Ones',
    'Venus-led love is sensorial, devoted, and quietly relentless. What a Number 6 partner needs to feel safe, and where their devotion tips into self-erasure.'),
7: ('Why Number 7 People Need a Partner Who Honours Silence',
    'Ketu-led love is quiet, depth-driven, allergic to performance. How Number 7 people actually fall, what they need to stay, and who can hold their solitude with them.'),
8: ('Why Number 8 People Take Long to Love and Stay When They Do',
    'Saturn-led love is slow, careful, structured for the long haul. How a Number 8 partner shows commitment, and why the wrong partner finds the pace cold.'),
9: ('Why Number 9 People Love Loud and Loyal',
    'Mars-led love is intense, protective, and not subtle. How a Number 9 partner fights, defends, and forgives, and the kind of love that can hold their fire.'),
}

SPIRITUAL = {
1: ('The Soul Path of Number 1, The Sovereign Walk',
    'Beyond the personality reading, every Number 1 is on a sovereignty-led soul path. The essence, the lesson, the daily practice, the shadow side.'),
2: ('The Soul Path of Number 2, The Mirror Walk',
    'The Moon-led soul came here to feel, mirror, and hold space for others. The essence, the spiritual lesson, the practice that strengthens the path.'),
3: ('The Soul Path of Number 3, The Expression Walk',
    'The Jupiter-led soul is here to expand, teach, and make the invisible visible through language. The essence, the lesson, the practice, the shadow.'),
4: ('The Soul Path of Number 4, The Disruptor Walk',
    'The Rahu-led soul came here to break inherited patterns, often through paths their ancestors would not recognise as spiritual at all. The essence and the work.'),
5: ('The Soul Path of Number 5, The Translator Walk',
    'The Mercury-led soul came here to move between worlds and ask the questions others have stopped asking. The essence, the lesson, the practice, the shadow.'),
6: ('The Soul Path of Number 6, The Devotion Walk',
    'The Venus-led soul came here to find the sacred in beauty, love, and the body. The essence, the lesson, the practice that strengthens this path.'),
7: ('The Soul Path of Number 7, The Liberation Walk',
    'The Ketu-led soul is the most explicitly spiritual of the nine. The essence, the lesson around detachment-with-tenderness, the practice, the shadow.'),
8: ('The Soul Path of Number 8, The Karma Walk',
    'The Saturn-led soul came here to learn through structure, time, and consequence. The essence, the lesson of faith inside the long delay, the practice.'),
9: ('The Soul Path of Number 9, The Protector Walk',
    'The Mars-led soul came here to fight for something larger than itself. The essence, the lesson of anger transmuted into devotion, the practice, the shadow.'),
}

LUCKY = {
1: ('Lucky Days, Colours and Gemstones for Number 1 (Sun)',
    'Sun-aligned attributes for people born on the 1st, 10th, 19th or 28th. Lucky days, colours, stones, directions, and which days to avoid for big decisions.'),
2: ('Lucky Days, Colours and Gemstones for Number 2 (Moon)',
    'Moon-aligned attributes for people born on the 2nd, 11th, 20th or 29th. Lucky days, colours, pearl as primary stone, directions, and traditional cautions.'),
3: ('Lucky Days, Colours and Gemstones for Number 3 (Jupiter)',
    'Jupiter-aligned attributes for people born on the 3rd, 12th, 21st or 30th. Lucky days, colours, yellow sapphire as primary stone, and what to wear when it matters.'),
4: ('Lucky Days, Colours and Gemstones for Number 4 (Rahu)',
    'Rahu-aligned attributes for people born on the 4th, 13th, 22nd or 31st. Lucky days, colours, hessonite as primary stone, directions, and the unconventional preferences.'),
5: ('Lucky Days, Colours and Gemstones for Number 5 (Mercury)',
    'Mercury-aligned attributes for people born on the 5th, 14th or 23rd. Lucky days for communication, colours, emerald as primary stone, and travel timing.'),
6: ('Lucky Days, Colours and Gemstones for Number 6 (Venus)',
    'Venus-aligned attributes for people born on the 6th, 15th or 24th. Lucky days, soft colours, diamond as primary stone, and the strongest weekday for relationship moves.'),
7: ('Lucky Days, Colours and Gemstones for Number 7 (Ketu)',
    'Ketu-aligned attributes for people born on the 7th, 16th or 25th. Lucky days, sea-green and cream tones, cat\'s eye as primary stone, with practitioner cautions.'),
8: ('Lucky Days, Colours and Gemstones for Number 8 (Saturn)',
    'Saturn-aligned attributes for people born on the 8th, 17th or 26th. Lucky days, deep colours, blue sapphire as primary stone (with cautions), long-term decision timing.'),
9: ('Lucky Days, Colours and Gemstones for Number 9 (Mars)',
    'Mars-aligned attributes for people born on the 9th, 18th or 27th. Lucky days, reds and crimson tones, red coral as primary stone, and the warrior\'s weekday.'),
}

CLUSTERS = [
    ('why-number-{n}-overthinks.html', OVERTHINK),
    ('number-{n}-in-love.html',        IN_LOVE),
    ('number-{n}-spiritual-meaning.html', SPIRITUAL),
    ('lucky-attributes-number-{n}.html',  LUCKY),
]


def rewrite_file(filepath, new_title, new_desc):
    with open(filepath) as fh: c = fh.read()
    orig = c
    # Replace <title>...</title>
    c = re.sub(r'<title>[^<]*</title>', f'<title>{new_title}</title>', c, count=1)
    # Replace <meta name="description" content="...">
    c = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{new_desc}"', c, count=1,
    )
    # Also OG title + Twitter title for consistency.
    c = re.sub(r'<meta property="og:title" content="[^"]*"',
               f'<meta property="og:title" content="{new_title}"', c, count=1)
    c = re.sub(r'<meta name="twitter:title" content="[^"]*"',
               f'<meta name="twitter:title" content="{new_title}"', c, count=1)
    if c != orig:
        with open(filepath, 'w') as fh: fh.write(c)
        return True
    return False


def main():
    total = 0
    for tmpl, data in CLUSTERS:
        for n in range(1, 10):
            fp = os.path.join(ROOT, tmpl.format(n=n))
            if not os.path.exists(fp): continue
            title, desc = data[n]
            if rewrite_file(fp, title, desc):
                total += 1
                print(f'  rewrote {os.path.basename(fp)}')
    print(f'\nRewrote {total} titles + meta descriptions.')


if __name__ == '__main__':
    main()
