#!/usr/bin/env python3
"""
Build the 9 same-number compatibility pages.

Each describes what happens when two people share the same Chaldean number
(both birth date or life path), the mirror effect, the amplified strength,
the amplified shadow.

URL pattern: /number-{n}-and-{n}-compatibility
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location(
    'first_batch',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build-compatibility-pair-pages.py')
)
first_batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first_batch)
render_pair = first_batch.render_pair

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS = [
  (1, 1, 'Mirror', 'Two Suns', dict(
    one_liner='Two Suns: the most ambitious, visible, and potentially turbulent of all the same-number pairings.',
    para1='When two Number 1s come together, the relationship is unmistakable. Both partners are decisive, ambitious, used to leading. When the energy is channelled toward a shared external mission, two 1s build something the world notices. When it turns inward, both partners try to be the leader of the relationship itself.',
    para2='The strength: an enormous capacity for visible work. Both partners understand ambition without needing it explained. Decisions are fast. Trajectories are confident. The relationship has clarity.',
    para3='The risk: ego clashes. Neither partner is built to defer. The fix is structural: clear domains where each partner unambiguously leads. When that is in place, two 1s last longest. When it is not, neither feels respected and both burn out.',
    bullets=[
      'Communication style: direct, decisive, sometimes terse.',
      'Conflict pattern: short, sharp, and either resolved fast or escalated fast.',
      'Friendship depth: respect-based; built on shared ambition.',
      'Watch for: competing for the same recognition or the same authority.',
    ],
  ), [
    ('Is 1 and 1 a good match?',
     'Strong when both partners have separate ambitions and respect each other\'s leadership domains. Difficult when both want to lead the same thing.'),
    ('Are two Number 1s competitive in love?',
     'Yes, naturally. The work is consciously redirecting that competitiveness outward toward shared goals rather than at each other.'),
    ('Do 1-1 marriages last?',
     'They can, often beautifully. Mature 1-1 marriages tend to be among the most respect-driven and aspirational partnerships you will meet.'),
    ('What is the main 1-1 friction?',
     'Authority. Both partners are used to being the one who decides. Negotiating shared decision-making early sets the tone for the whole relationship.'),
  ]),

  (2, 2, 'Mirror', 'Two Moons', dict(
    one_liner='Two Moons: emotionally attuned beyond words, but at risk of mutual withdrawal under stress.',
    para1='Two Number 2s share an extraordinarily attuned emotional register. Both partners read the other before words are spoken; both honour the quiet, the felt, the unspoken. When the relationship is healthy, the closeness is rare in its depth.',
    para2='The strength: emotional safety. Each partner is met where they are without having to translate. Conflict is uncommon because both partners would rather feel into the issue than fight about it. The relationship can become a true sanctuary.',
    para3='The risk: mutual withdrawal. When stress hits, both partners go inward. Neither naturally pulls the other back out. Couples must build deliberate practices (a weekly check-in, a question that names what is unspoken) to keep the closeness from drifting.',
    bullets=[
      'Communication style: layered, intuitive, often non-verbal.',
      'Conflict pattern: rare, quiet, slow to surface.',
      'Friendship depth: profound, often life-altering.',
      'Watch for: synchronised retreat into separate inner worlds.',
    ],
  ), [
    ('Is 2 and 2 a good match for marriage?',
     'Strong, with the caveat that both partners must build practices that prevent mutual emotional withdrawal during stress.'),
    ('Do two Number 2s fight?',
     'Rarely directly. The risk is unspoken resentment that compounds slowly. Naming feelings out loud, even when it feels redundant, is the practice.'),
    ('Are 2-2 partnerships emotionally close?',
     'Among the closest of any Chaldean pairing, when the relationship is tended.'),
    ('What does a 2-2 couple need to practise?',
     'Verbal honesty. Both partners default to atmosphere; both must consciously bring words to the felt sense.'),
  ]),

  (3, 3, 'Mirror', 'Two Jupiters', dict(
    one_liner='Two Jupiters: expansive, generous, often the most socially radiant couple in the room.',
    para1='Two Number 3s share Jupiter\'s outward-radiating warmth. Both partners are expressive, curious, generous, and drawn to teaching, publishing, performing, or any work that lives in language. Together this couple has range.',
    para2='The strength: rarely bored. Conversation is rich; both partners learn from each other; social life is full and visible. Couples in education, media, hospitality, or creative arts often combine these vibrations.',
    para3='The risk: scattered focus. Jupiter expands without naturally contracting. Two 3s can have many projects and few finished. The fix is shared discipline: a small number of shared commitments held to completion.',
    bullets=[
      'Communication style: animated, warm, articulate.',
      'Conflict pattern: rare; both prefer talking it through.',
      'Friendship depth: easy, wide, mutually stimulating.',
      'Watch for: too many open projects, too few closed loops.',
    ],
  ), [
    ('Is 3 and 3 a strong match?',
     'Yes, naturally. Two Jupiter vibrations resonate easily, especially in social or creative work.'),
    ('Do two Number 3s argue?',
     'Less than most pairings. Both prefer expansion over confrontation, which is mostly a strength but can hide unresolved issues.'),
    ('Are 3-3 marriages successful?',
     'Often, especially when both partners commit to finishing things together rather than just starting them.'),
    ('What is the 3-3 risk?',
     'Surface enthusiasm covering unspoken depth. Couples who build in periodic deeper-conversation rituals last longest.'),
  ]),

  (4, 4, 'Mirror', 'Two Rahus', dict(
    one_liner='Two Rahus: an intensely unconventional pairing. Either the most original partnership you will see, or unstable.',
    para1='Two Number 4s carry Rahu\'s unconventional charge in stereo. Both partners see patterns others miss; both are willing to leave well-trodden paths; both can feel slightly outside the standard frame even in their own families. When they find each other, the recognition is fast and unmistakable.',
    para2='The strength: real intellectual and creative partnership. Two 4s often build something genuinely new together, often in tech, research, art, or unconventional business models. Neither needs the relationship to look conventional.',
    para3='The risk: instability. Rahu does not naturally anchor itself; neither partner is the steadying force. Without conscious grounding (routine, daily ritual, predictable rhythms), the relationship can run too fast and dissolve.',
    bullets=[
      'Communication style: idea-rich, often non-linear.',
      'Conflict pattern: intellectual rather than emotional, sometimes unresolved.',
      'Friendship depth: rare, deep, built on shared outsider experience.',
      'Watch for: relationship lacking grounding rhythms.',
    ],
  ), [
    ('Is 4 and 4 a good match?',
     'In creative and intellectual partnerships, very. In daily life, the pair must consciously build the grounding routines neither naturally provides.'),
    ('Are two Number 4s emotionally compatible?',
     'They share the felt experience of being outside the standard frame, which is itself an emotional bond. The work is consciously bringing emotion to surface through words.'),
    ('Do 4-4 couples make stable marriages?',
     'They can, with deliberate effort. Mature 4-4 marriages often have unusual structures (separate creative time, unconventional living arrangements) that work for them.'),
    ('What is the 4-4 main risk?',
     'Lack of daily anchor. Both partners pull toward novelty. Calendar discipline and shared routine matter more than for most pairings.'),
  ]),

  (5, 5, 'Mirror', 'Two Mercuries', dict(
    one_liner='Two Mercuries: fast, conversational, mentally electric. The relationship lives in language and motion.',
    para1='Two Number 5s share Mercury\'s speed. Both partners are quick-minded, adaptive, social, and easily bored by sameness. When they find each other, the early stages feel exhilarating, conversations until 3am, ideas firing back and forth, a sense of being matched in mental tempo.',
    para2='The strength: mental partnership. Few pairings can keep up with each other intellectually the way two 5s can. The relationship has range, conversation, learning, and shared adventure.',
    para3='The risk: scattered commitment. Mercury chases novelty. Two 5s can struggle to deepen, to commit to one shared project, one home, one rhythm. The fix is conscious choice, deliberately staying with one direction long enough to compound, even when newer options appear.',
    bullets=[
      'Communication style: fast, articulate, often clever.',
      'Conflict pattern: quick; talked through; sometimes not deeply resolved.',
      'Friendship depth: mentally stimulating, built on shared curiosity.',
      'Watch for: novelty consuming commitment.',
    ],
  ), [
    ('Is 5 and 5 compatible?',
     'In short-term partnership and creative collaboration, very strongly. For long-term commitment, both partners must consciously practise depth over novelty.'),
    ('Do 5-5 couples last?',
     'Often yes when both partners share a long-term project (business, family, creative work) that requires them to keep choosing each other.'),
    ('Are 5-5 partnerships emotionally deep?',
     'They can be, but emotion sometimes hides behind the intellectual fast pace. Both partners must slow down to feel.'),
    ('What does a 5-5 couple need to practise?',
     'Stillness. The thing neither partner naturally provides.'),
  ]),

  (6, 6, 'Mirror', 'Two Venuses', dict(
    one_liner='Two Venuses: the most aesthetically harmonious of all same-number pairings. Beauty in stereo.',
    para1='Two Number 6s share Venus\'s love of beauty, comfort, the body, and the felt warmth of relationship itself. The home built by two 6s is unmistakable, well-tended, sensorial, full of small intentional pleasures. The relationship feels good to be in and good to be around.',
    para2='The strength: aesthetic and emotional alignment. Both partners value the same things, beautiful food, warm hosting, daily affection, an attractive home. The values rarely need to be argued.',
    para3='The risk: harmony at the cost of truth. Both partners prefer pleasantness to confrontation. Issues that need surfacing can be smoothed over until they compound. The fix is deliberate honesty practised early, before harmony hardens into avoidance.',
    bullets=[
      'Communication style: warm, attentive, often gentle.',
      'Conflict pattern: avoided. Disagreement feels like aesthetic disruption.',
      'Friendship depth: high warmth, frequent shared rituals.',
      'Watch for: pleasantness becoming a substitute for honesty.',
    ],
  ), [
    ('Is 6 and 6 a strong match for marriage?',
     'Among the most aesthetically and emotionally harmonious pairings. The work is bringing honest hard truths into the relationship before they fester.'),
    ('Do 6-6 couples fight?',
     'Rarely visibly. The risk is the unsaid building under the surface. Couples who practise direct conversation early do best.'),
    ('Are two Number 6s emotionally compatible?',
     'Yes, deeply. Both partners experience love through similar registers, food, touch, beauty, daily care.'),
    ('What is the 6-6 main risk?',
     'Conflict avoidance. Both partners would rather restore harmony than resolve the underlying issue.'),
  ]),

  (7, 7, 'Mirror', 'Two Ketus', dict(
    one_liner='Two Ketus: rare, profoundly spiritual, often recognised as a soul-level connection. Quiet beyond most other pairings.',
    para1='Two Number 7s share Ketu\'s depth, introspection, and uninterest in performance. When they meet, the recognition is often unspoken and immediate, both partners feel "this person knows" without needing to explain why. The relationship rarely operates on small talk.',
    para2='The strength: real depth. Two 7s can sit in silence and feel met. They share an introverted, contemplative orientation that most pairings struggle to access. The relationship often has a meditative quality.',
    para3='The risk: dual retreat. Both partners default inward under stress. Neither pulls the other back out. The relationship can develop a deep mutual respect alongside an actual emotional distance, both partners feel known but not always close.',
    bullets=[
      'Communication style: spare, intuitive, often non-verbal.',
      'Conflict pattern: rare and quiet; resolution slow.',
      'Friendship depth: profound, life-altering, often spiritual.',
      'Watch for: both partners going internal at once and losing daily intimacy.',
    ],
  ), [
    ('Is 7 and 7 spiritually compatible?',
     'Profoundly. This is one of the most spiritually attuned same-number pairings, often described as soul-recognition.'),
    ('Do two Number 7s have a good marriage?',
     'They can, when both partners deliberately practise daily warmth alongside the natural depth. Ketu does not generate warmth automatically.'),
    ('Are 7-7 couples introverted?',
     'Strongly. The relationship is often quiet, contemplative, and protected from social demands.'),
    ('What is the 7-7 risk?',
     'Synchronised withdrawal. Both partners need to practise reaching toward each other during stress, not away.'),
  ]),

  (8, 8, 'Mirror', 'Two Saturns', dict(
    one_liner='Two Saturns: the most structurally durable same-number pairing. Slow to build, hard to break.',
    para1='Two Number 8s share Saturn\'s patience, responsibility, and orientation toward long-arc work. Neither partner expects quick rewards. Both understand the cost of sustained effort over decades. When two 8s commit to each other, the relationship is built to last.',
    para2='The strength: durability. Two 8s can outlast almost anything, financial difficulty, family complexity, geographic separation. The mutual respect for hard work and structural responsibility is rare.',
    para3='The risk: heaviness. Two 8s can default to seriousness. The relationship can lose lightness, play, and spontaneous joy. Saturn\'s discipline is healthy when balanced with the practice of small daily delights, not when treated as the only mode.',
    bullets=[
      'Communication style: deliberate, weighted, slow.',
      'Conflict pattern: cold and structural rather than hot.',
      'Friendship depth: builds slowly, lasts lifetimes.',
      'Watch for: relationship becoming purely about responsibility.',
    ],
  ), [
    ('Is 8 and 8 a good match?',
     'In durability and mutual respect, very strong. The work is keeping joy alive alongside the seriousness.'),
    ('Do two Number 8s have a stable marriage?',
     'Often the most structurally stable of all pairings. Both partners understand long-term commitment.'),
    ('Are 8-8 couples too serious?',
     'They can be. Deliberate practices of play, humour, and shared lightness protect the relationship from becoming a shared duty.'),
    ('What is the 8-8 strength?',
     'Persistence. When both partners are committed, the relationship outlasts almost everything.'),
  ]),

  (9, 9, 'Mirror', 'Two Mars', dict(
    one_liner='Two Mars: passionate, kinetic, intense. Either the most alive partnership you will see, or the most explosive.',
    para1='Two Number 9s share Mars\'s heat in stereo. Both partners are courageous, direct, action-oriented, and unwilling to back down. When they share a common cause, the partnership is unstoppable. When they turn the fire on each other, the relationship combusts fast.',
    para2='The strength: vitality. The relationship is alive. Both partners value courage in the other; both are willing to fight for things; both bring physical, kinetic energy to whatever they do together.',
    para3='The risk: friction without resolution. Two 9s can fight often and resolve nothing because both partners would rather move forward than process. The fix is deliberate practice of slowness, cool-down rituals, scheduled reconciliation conversations, refusing to let heat compost into resentment.',
    bullets=[
      'Communication style: direct from both. Volume rises fast.',
      'Conflict pattern: explosive, often unresolved.',
      'Friendship depth: built on shared loyalty and shared cause.',
      'Watch for: chronic conflict becoming the relationship\'s default texture.',
    ],
  ), [
    ('Is 9 and 9 compatible?',
     'In passion and shared mission, intensely. The work is preventing the fire from consuming the partnership.'),
    ('Do two Number 9s fight a lot?',
     'Yes, naturally. Both are direct and unwilling to back down. The relationship needs structural cool-down practices.'),
    ('Are 9-9 marriages successful?',
     'They can be, particularly when both partners channel the energy outward toward shared causes rather than at each other.'),
    ('What does a 9-9 couple need?',
     'A practice for slowing down. Mars does not slow itself. Couples must deliberately build pauses, scheduled breathing rooms, and clean fighting rules.'),
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
    print(f'\n{len(PAIRS)} same-number compatibility pages built.')
