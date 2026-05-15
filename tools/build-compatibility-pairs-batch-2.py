#!/usr/bin/env python3
"""
Build batch 2 of "Number A and B Compatibility" pages (10 more pairs).

Reuses the render_pair logic from build-compatibility-pair-pages.py;
this script supplies the additional pair content and invokes the same
rendering pipeline.

URL pattern: /number-{a}-and-{b}-compatibility   (a < b)
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Re-use the render_pair function from the first batch script.
import importlib.util
spec = importlib.util.spec_from_file_location(
    'first_batch',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build-compatibility-pair-pages.py')
)
first_batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first_batch)
render_pair = first_batch.render_pair

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 10 additional high-search pairs.
PAIRS = [
  (1, 3, 'Supportive', 'Sun and Jupiter', dict(
    one_liner='Sun meets Jupiter: a warm, expansive pairing built for public partnerships and shared ambition.',
    para1='Number 1 (Sun) and Number 3 (Jupiter) form a naturally warm pairing. The Sun provides direction and the will to lead; Jupiter provides wisdom, expression and an unmistakable generosity. Together this couple tends to be visible, well-spoken-of, and good at building things that involve other people.',
    para2='Strength: both partners enjoy the world. Neither hides. The relationship feels socially full, with friendships, teaching, family gatherings and travel woven through it.',
    para3='Friction: both can over-commit. Number 1 says yes to opportunity; Number 3 says yes to people. A 1-3 couple can find themselves doing too much and not protecting their own time together. The fix is calendar discipline, deliberate blank weeks, not always-on availability.',
    bullets=[
      'Communication style: warm, direct, often public.',
      'Conflict pattern: rare in early years, can surface when over-committed.',
      'Friendship depth: easy, wide, often lifelong.',
      'Watch for: schedule sprawl, not protecting the inner relationship.',
    ],
  ), [
    ('Is 1 and 3 a good match?', 'Yes, supportive in the Chaldean compatibility model. Sun and Jupiter share warmth and outward energy.'),
    ('Do 1 and 3 work in marriage?', 'Generally yes, with attention paid to not letting external life crowd out the relationship.'),
    ('Are 1 and 3 compatible in business?', 'Strongly. The combination of leadership (1) and teaching/expression (3) suits founder + spokesperson roles.'),
    ('What is the main risk for 1 and 3?', 'Over-commitment. Both numbers thrive in expansion; the relationship needs deliberate quiet time.'),
  ]),

  (1, 4, 'Strong', 'Sun and Rahu', dict(
    one_liner='Sun meets Rahu: a powerful but unconventional pairing. Either creates something new in the world together, or struggles to find a shared frame.',
    para1='Number 1 (Sun) and Number 4 (Rahu) is an unusual pairing because Rahu is the unconventional, future-leaning energy and the Sun is the established authority figure. When they align, the combination produces real innovation under strong leadership. When they don\'t, Number 4 feels controlled and Number 1 feels confused.',
    para2='Strength: enormous capacity for building something new. Number 1 brings clarity of direction; Number 4 brings the unconventional thinking that makes the direction interesting rather than derivative.',
    para3='Friction: Number 1 wants understandable patterns; Number 4 sees the patterns that do not yet have names. The 1 can dismiss the 4\'s reads as paranoid; the 4 can experience the 1\'s leadership as resistance to seeing what is actually happening.',
    bullets=[
      'Communication style: direct from 1, oblique from 4. Translation often required.',
      'Conflict pattern: 1 dismisses, 4 withdraws. Both feel unseen.',
      'Friendship depth: respect-driven, often built on shared work or shared outsider feeling.',
      'Watch for: 1 overriding 4\'s unconventional reads on principle alone.',
    ],
  ), [
    ('Is 1 and 4 compatible?', 'Yes, particularly in partnerships building something new. Sun + Rahu produces innovative ventures when both partners respect the other\'s frame.'),
    ('Is 1 and 4 difficult for marriage?', 'It can be if 1 needs the relationship to look conventional and 4 cannot live within those frames. With awareness, it is a powerful match.'),
    ('Do 1 and 4 work in business?', 'Often very well. 1 provides leadership and visibility; 4 provides innovation and pattern-vision.'),
    ('What is the main 1-4 friction?', 'Frame mismatch. 1 wants known frameworks; 4 sees gaps in them. Trust takes time.'),
  ]),

  (1, 5, 'Supportive', 'Sun and Mercury', dict(
    one_liner='Sun meets Mercury: leadership meets communication. A pairing built for partnerships that need to be heard.',
    para1='Number 1 (Sun) and Number 5 (Mercury) is a fluid, agile pairing. The Sun provides direction; Mercury provides the language, adaptability and social texture that makes the direction reach people. Together this couple is often visible, articulate and well-positioned.',
    para2='Strength: communication is rarely the problem. Both partners speak openly; both partners value intellectual engagement. The relationship has range, conversation, social life, and shared curiosity.',
    para3='Friction: Number 5 needs novelty; Number 1 needs commitment. When 5 starts chasing new directions and 1 wants the original plan executed, the friction is between depth and breadth.',
    bullets=[
      'Communication style: articulate, fast, mutually stimulating.',
      'Conflict pattern: drift rather than confrontation. 5 wanders; 1 anchors.',
      'Friendship depth: easy, social, built on shared interests.',
      'Watch for: 5\'s attention scattering across new things.',
    ],
  ), [
    ('Is 1 and 5 compatible?', 'Yes, supportive in Chaldean compatibility. Sun and Mercury work well together in articulate, fast-moving partnerships.'),
    ('Do 1 and 5 last in marriage?', 'They can, when 1 accepts that 5 needs novelty and 5 commits to the relationship even as interests shift.'),
    ('Are 1 and 5 compatible in business?', 'Very. 1 leads, 5 communicates, sells, networks. Founder + business-development is a classic 1-5 split.'),
    ('What is the 1-5 risk?', 'Pace mismatch. 5 wants new; 1 wants finished. Mutual respect for both needs.'),
  ]),

  (1, 6, 'Supportive', 'Sun and Venus', dict(
    one_liner='Sun meets Venus: authority meets beauty. A pairing built for relationships that look as good as they feel.',
    para1='Number 1 (Sun) and Number 6 (Venus) is a classically warm pairing. The Sun provides direction, drive and outward ambition; Venus provides aesthetic care, emotional warmth and the felt quality of the home and the partnership itself.',
    para2='Strength: the relationship is well-tended. Number 6 makes the daily texture of life beautiful; Number 1 makes the long-arc direction clear. Together this couple often builds a visibly settled life with both substance and aesthetic.',
    para3='Friction: Number 1 can dismiss Number 6\'s aesthetic care as decoration when stressed; Number 6 can feel that the relationship\'s comfort is being sacrificed for the 1\'s ambition. The fix is mutual recognition that both registers matter, the outer build and the inner sanctuary.',
    bullets=[
      'Communication style: 1 plain, 6 emotionally attuned. Both must adjust.',
      'Conflict pattern: 1 wants to resolve fast, 6 wants the feeling to be honoured first.',
      'Friendship depth: warm, sensory, built around food, gatherings, beauty.',
      'Watch for: 1 treating the relationship\'s daily care as overhead instead of essential.',
    ],
  ), [
    ('Is 1 and 6 compatible for marriage?', 'Yes, often a warm, settled pairing. Sun + Venus balances ambition and care.'),
    ('Do 1 and 6 share values?', 'Generally yes, both value building something lasting. Different emphases (1 outward, 6 inward) complement.'),
    ('Are 1 and 6 compatible in business?', 'Yes in fields where leadership and aesthetic both matter: design, hospitality, premium brands.'),
    ('What is the 1-6 risk?', 'Number 1 under stress can deprioritise care. The 6 must speak up when the daily texture is being sacrificed.'),
  ]),

  (1, 8, 'Caution', 'Sun and Saturn', dict(
    one_liner='Sun meets Saturn: light meets gravity. A pairing of substantial weight, often heavy but capable of great durability.',
    para1='Number 1 (Sun) and Number 8 (Saturn) is one of the more cautioned pairings in Cheiro\'s framework. Saturn is traditionally the planet that delays, restrains, and tests; the Sun wants to move, lead and be seen. The pairing produces friction unless both partners consciously work with the dynamic instead of against it.',
    para2='Why it can work: 8 brings the structural patience and durability that 1\'s ambition often lacks. Many of the most lasting 1-8 marriages are built in adulthood after both partners have already matured into their numbers.',
    para3='Why it can struggle: in early relationships, 1 can experience 8\'s pacing as obstruction, and 8 can experience 1\'s urgency as immaturity. Both feel slightly wrong-paced for the other.',
    bullets=[
      'Communication style: 1 quick, 8 considered. Both must slow / speed up.',
      'Conflict pattern: heavy and slow to resolve. Avoid letting it compost.',
      'Friendship depth: rare in youth, deepens significantly in midlife.',
      'Watch for: 1 reading 8\'s caution as rejection.',
    ],
  ), [
    ('Is 1 and 8 a bad match?', 'Cautioned in classical Chaldean compatibility. Sun and Saturn pull in different time horizons. With awareness, it can mature into a deeply durable pairing.'),
    ('Do 1 and 8 work in marriage?', 'Yes, more often in second-half-of-life marriages than early ones.'),
    ('Are 1 and 8 compatible in business?', 'Selectively. 1 in vision, 8 in operations. Clear role boundaries help.'),
    ('What ages does 1-8 work best at?', 'Often after both partners have crossed their Saturn returns, around age 30+. Both numbers mature into their gifts with time.'),
  ]),

  (2, 9, 'Caution', 'Moon and Mars', dict(
    one_liner='Moon meets Mars: water meets fire. A challenging pairing where both partners must work to translate across registers.',
    para1='Number 2 (Moon) and Number 9 (Mars) is one of the more difficult classic pairings. The Moon is emotional, receptive, slow-moving; Mars is direct, kinetic, fast-moving. Each can feel like the other is speaking a foreign emotional language.',
    para2='Strength: when it works, the pairing is alive. Mars protects what the Moon holds; the Moon softens what Mars hardens. The relationship has both heat and depth.',
    para3='Friction: 9 can experience 2\'s emotional pace as withholding; 2 can experience 9\'s heat as aggression. Both can leave conversations feeling unseen. The fix is explicit translation, naming what is happening in real time instead of expecting the other to read it.',
    bullets=[
      'Communication style: 2 indirect, 9 direct. Both feel mistranslated.',
      'Conflict pattern: 9 escalates fast, 2 shuts down fast. Cool the room first.',
      'Friendship depth: variable. Either profoundly bonding or distantly polite.',
      'Watch for: 9 reading 2\'s quiet as rejection; 2 reading 9\'s heat as attack.',
    ],
  ), [
    ('Is 2 and 9 compatible?', 'Traditionally cautioned. Moon and Mars come from different registers; the pairing requires conscious translation work.'),
    ('Do 2 and 9 work in marriage?', 'They can, with mutual practice in slowing down and naming feelings explicitly.'),
    ('Are 2 and 9 compatible in business?', 'Mixed. 9 leads action, 2 holds team well-being. Roles must not overlap.'),
    ('What is the main 2-9 issue?', 'Pace and tone. The conscious work is bringing both registers into the conversation, not assuming one is right.'),
  ]),

  (3, 5, 'Supportive', 'Jupiter and Mercury', dict(
    one_liner='Jupiter meets Mercury: expansion meets speed. A pairing built for communication-driven work and shared learning.',
    para1='Number 3 (Jupiter) and Number 5 (Mercury) is a naturally articulate pairing. Jupiter is the teacher, Mercury is the messenger; together this couple lives in language. Conversation, writing, teaching and travel are common shared territory.',
    para2='Strength: rarely bored together. The intellectual register is high; both partners are curious, expressive, and stimulated by ideas. Many of the most successful partnerships in publishing, education and media combine these two vibrations.',
    para3='Friction: both can scatter. 3 over-commits to people; 5 over-commits to new directions. Without discipline, the relationship can have lots of activity but little compounded work.',
    bullets=[
      'Communication style: rich, articulate, mutually stimulating.',
      'Conflict pattern: rare; both prefer talking it through. Watch for unsaid resentments.',
      'Friendship depth: easy, wide, frequently mentor-student dynamic.',
      'Watch for: too much breadth, not enough finished work.',
    ],
  ), [
    ('Is 3 and 5 compatible?', 'Yes, supportive in Chaldean compatibility. Jupiter and Mercury share intellectual orientation.'),
    ('Do 3 and 5 work in marriage?', 'Often yes, especially when both partners have shared work or shared learning practice.'),
    ('Are 3 and 5 compatible in business?', 'Strongly. Education, media, publishing, content, anything language-led.'),
    ('What is the 3-5 risk?', 'Distraction. The relationship can have lots of conversation but little finished output without intentional structure.'),
  ]),

  (4, 5, 'Caution', 'Rahu and Mercury', dict(
    one_liner='Rahu meets Mercury: unconventional pattern meets quicksilver speed. Innovative but can feel unstable.',
    para1='Number 4 (Rahu) and Number 5 (Mercury) is a fast-moving, idea-rich pairing where both partners value the unconventional. Rahu sees the new patterns; Mercury translates and communicates them. Together this couple can be on the leading edge of a field.',
    para2='Strength: real intellectual partnership. Both partners can hold complex, non-obvious ideas. The relationship is rarely conventional and rarely boring.',
    para3='Friction: stability. Both numbers run on novelty. Neither naturally anchors the daily rhythm of the relationship. Couples must build deliberate routines to keep the partnership grounded.',
    bullets=[
      'Communication style: fast, idea-rich, often non-linear.',
      'Conflict pattern: quick, intellectual, often unresolved emotionally.',
      'Friendship depth: built on shared curiosity, often surviving long absences.',
      'Watch for: lack of grounding. Both partners must consciously slow down sometimes.',
    ],
  ), [
    ('Is 4 and 5 compatible?', 'Cautioned. Both share unconventional energy, which is exciting but unstable without conscious grounding.'),
    ('Do 4 and 5 work in marriage?', 'Yes when both partners deliberately build routine and stability into the relationship.'),
    ('Are 4 and 5 compatible in business?', 'Strongly in innovation-driven ventures. Founders and early-stage companies often have this dynamic.'),
    ('What is the 4-5 main issue?', 'Daily groundedness. Neither number naturally provides it. Build it into the calendar.'),
  ]),

  (4, 9, 'Caution', 'Rahu and Mars', dict(
    one_liner='Rahu meets Mars: disruption meets fire. High-intensity pairing, easily explosive if not channelled.',
    para1='Number 4 (Rahu) and Number 9 (Mars) is an intensely energetic pairing. Rahu is the unconventional, Mars is the warrior; together this couple often takes on big, public causes and projects, sometimes at significant personal cost.',
    para2='Strength: capacity for impact. When both partners are aligned around a cause larger than themselves, the relationship produces real work in the world. Activists, founders, and creative duos often hold this combination.',
    para3='Friction: temperature. Both run hot. Disagreements escalate quickly, and both partners are unwilling to back down. The fix is structural, agreed-upon cool-down practices that engage before the heat gets to the point of no return.',
    bullets=[
      'Communication style: direct from both. Volume can rise fast.',
      'Conflict pattern: explosive, often unresolved.',
      'Friendship depth: shared-mission bond; lasting if the mission lasts.',
      'Watch for: the relationship becoming the battlefield instead of the safe place.',
    ],
  ), [
    ('Is 4 and 9 compatible?', 'Cautioned. Both numbers run hot, and without practice the heat can consume the relationship.'),
    ('Do 4 and 9 work in marriage?', 'Yes when both partners are aligned on a shared cause and have agreed cool-down rituals.'),
    ('Are 4 and 9 compatible in business?', 'In high-stakes, high-energy ventures, yes. In slow-burn corporate work, less so.'),
    ('What is the 4-9 risk?', 'The fire becoming the relationship. Both partners must actively bring softness into the partnership.'),
  ]),

  (5, 6, 'Supportive', 'Mercury and Venus', dict(
    one_liner='Mercury meets Venus: speed meets beauty. A conversational, warm, socially fluent pairing.',
    para1='Number 5 (Mercury) and Number 6 (Venus) is a naturally easy pairing. Mercury provides articulation and adaptability; Venus provides aesthetic care and emotional warmth. Together this couple tends to have an inviting, talkative, beautifully-tended life.',
    para2='Strength: low-friction. Both partners value warmth, beauty, conversation, and social connection. The relationship feels good to be in and good to be around.',
    para3='Friction: both can avoid hard truths to keep the harmony. The relationship runs smoothly until the underlying issues compound. The fix is deliberate honesty, practised early and often, before harmony becomes performance.',
    bullets=[
      'Communication style: warm, easy, mutually appreciative.',
      'Conflict pattern: avoided. Both partners prefer harmony to confrontation.',
      'Friendship depth: easy, socially fluent, often built around shared meals and events.',
      'Watch for: pleasantness covering unspoken tension.',
    ],
  ), [
    ('Is 5 and 6 compatible?', 'Yes, supportive in Chaldean compatibility. Mercury and Venus pair warmly.'),
    ('Do 5 and 6 work in marriage?', 'Often, particularly when both partners commit to honest conversation alongside the natural warmth.'),
    ('Are 5 and 6 compatible in business?', 'Strongly in hospitality, design, content, lifestyle brands, anything where charm + aesthetic matters.'),
    ('What is the 5-6 risk?', 'Avoiding the hard conversation. The pleasantness must not become a substitute for truth-telling.'),
  ]),
]


def build():
    for (a, b, rating, planet_summary, content, faqs) in PAIRS:
        html = render_pair(a, b, rating, planet_summary, content, faqs)
        out_path = os.path.join(OUT, f'number-{a}-and-{b}-compatibility.html')
        with open(out_path, 'w') as fh: fh.write(html)
        print(f'  wrote {out_path}')


if __name__ == '__main__':
    build()
    print(f'\n{len(PAIRS)} additional compatibility pair pages built.')
