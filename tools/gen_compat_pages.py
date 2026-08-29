#!/usr/bin/env python3
"""Generate the 16 compatibility pair pages that had no page.

Renders into the same structure as the 29 pre-existing
number-X-and-Y-compatibility.html pages. Verdicts and their basis are recorded
in docs/seo-urls/derived-compatibility-verdicts.md.

Run from the repo root:  python3 tools/gen_compat_pages.py
"""
import html
import os
import re

PLANET = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury",
          6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}
GLYPH = {1: "\u2600", 2: "\u263e", 3: "\u2643", 4: "\u25c8", 5: "\u263f",
         6: "\u2640", 7: "\u260b", 8: "\u2644", 9: "\u2642"}
ARCH = {1: ("the-inner-sovereign", "The Inner Sovereign"),
        2: ("the-mirror", "The Mirror"),
        3: ("the-translator", "The Translator"),
        4: ("the-quiet-disruptor", "The Quiet Disruptor"),
        5: ("the-restless-mind", "The Restless Mind"),
        6: ("the-devoted-beautifier", "The Devoted Beautifier"),
        7: ("the-inward-witness", "The Inward Witness"),
        8: ("the-patient-builder", "The Patient Builder"),
        9: ("the-protector", "The Protector")}
LOVE_BLURB = {1: "How Sun-led people show up", 2: "How Moon-led people show up",
              3: "How Jupiter-led people show up", 4: "How Rahu-led people show up",
              5: "How Mercury-led people show up", 6: "How Venus-led people show up",
              7: "How Ketu-led people show up", 8: "How Saturn-led people show up",
              9: "How Mars-led people show up"}

# Each pair carries fully distinct prose. Headings deliberately vary between
# pages so the cluster does not read as one template with swapped numbers.
PAIRS = {
 (1, 7): dict(
  verdict="Strong",
  tag="Sun and Ketu pairing. One wants to be seen, the other wants to see.",
  desc="Number 1 and 7 compatibility in Chaldean numerology: why the spotlight and the observer suit each other, plus the silence problem that breaks it.",
  intro="On paper this looks like a mismatch. Number 1 wants to be seen and Number 7 wants to see. In practice it is one of the quieter strong pairings in Chaldean numerology, because Number 7 is the one person in the room who is not competing with Number 1 for the light.",
  lede="Number 1 (Sun) and Number 7 (Ketu) both sit in Cheiro's first family of numbers, alongside 2 and 4. What Number 1 gets is a counsel with no agenda, someone who observes accurately and has no interest in the credit. What Number 7 gets is a partner who handles the outward world competently enough that the inner one stays undisturbed.",
  works_h2="Why the spotlight and the observer fit",
  works="Number 1 supplies direction, momentum and the willingness to be the public face. Number 7 supplies depth, perspective and the question nobody else thought to ask. When it works, Number 1 stops mistaking motion for progress because Number 7 keeps asking what it is for, and Number 7 stops disappearing into abstraction because Number 1 keeps building things that need deciding about.",
  watch_h2="The silence problem",
  watch="Almost every failure in this pairing runs through one misreading. Number 7 goes inward as a matter of routine, not as a verdict on the relationship, and Number 1 reads that withdrawal as rejection or disinterest. The repair is unglamorous and specific: Number 7 has to say <em>I am going quiet for a bit, it is not about you</em> out loud, and Number 1 has to stop interpreting silence as data about their own worth.",
  quick=["Communication style: 1 states positions early, 7 withholds until certain. Neither is being difficult.",
         "Conflict pattern: 1 escalates in order to resolve, 7 goes absent to think. The escalation makes the absence longer.",
         "Friendship depth: unusually strong. Often the person Number 1 trusts most, precisely because 7 wants nothing.",
         "Best moments: long drives, unstructured time, one-on-one over anything crowded."],
  verdict_para="In Cheiro's planetary families, Number 1 (Sun) and Number 7 (Ketu) sit together in the 1-2-4-7 group, which makes this a <strong>strong</strong> pairing by default. It is a quieter strength than 1 and 2: less obvious from outside, and dependent on Number 1 learning not to take silence personally.",
  faqs=[("Is 1 and 7 a good match for marriage?",
         "Yes, though it is a quiet marriage rather than a demonstrative one. It works when Number 1 accepts that Number 7 will never perform enthusiasm, and stops reading the absence of performance as the absence of feeling."),
        ("What is the main challenge between 1 and 7?",
         "Number 1 needs response and Number 7 needs retreat. Nothing is wrong with either need, but they arrive at the same moment, usually right after something significant has happened."),
        ("Are 1 and 7 compatible in business?",
         "Strongly, with a clear division. Number 1 fronts the venture and decides; Number 7 researches, models and finds the flaw. Putting Number 7 in a client-facing role wastes them and exhausts them."),
        ("Does 1 and 7 work in friendship?",
         "Very well, often for decades. Number 7 offers Number 1 something rare, an honest read from someone with nothing to gain from flattering them.")],
  share="Number 1 (Sun) and Number 7 (Ketu) compatibility, the spotlight and the observer:",
 ),
 (2, 3): dict(
  verdict="Supportive",
  tag="Moon and Jupiter pairing. Warm and easy, with one thing neither will say.",
  desc="Number 2 and 3 compatibility in Chaldean numerology: two benefic numbers, genuine warmth, and the politeness problem that quietly erodes it.",
  intro="This pairing is pleasant almost immediately, which is both the strength and the whole risk. Number 2 and Number 3 are two of the warmest numbers in the system, and neither has much appetite for confrontation.",
  lede="Number 2 (Moon) and Number 3 (Jupiter) sit in different Chaldean families but carry no traditional affliction between them. Both are benefic. Number 3 brings optimism, a social world and the assumption that things expand; Number 2 brings emotional attunement and somewhere private to land at the end of it.",
  works_h2="What the warmth actually buys",
  works="Number 3 pulls Number 2 up out of rumination and into the world, which is often exactly what a Moon-led mind needs and cannot generate alone. Number 2 gives Number 3 a place where nothing has to be performed, which Jupiter-led people rarely admit they need until they have it. There is usually a lot of laughter in this pairing, and it holds up under ordinary stress well.",
  watch_h2="The politeness problem",
  watch="Both of these numbers avoid the hard conversation, and they avoid it for different reasons: Number 2 because naming a need feels like imposing, Number 3 because the mood is good and why spoil it. So the unsaid accumulates politely for months. Number 2 grows quietly resentful about needs that were never actually stated, and Number 3 is genuinely blindsided, because from where they were standing everything looked fine.",
  quick=["Communication style: 3 communicates in volume, 2 communicates in tone. 3 often misses the tone entirely.",
         "Conflict pattern: mutual avoidance. Problems do not escalate here, they postpone, sometimes for years.",
         "Friendship depth: excellent and low-maintenance. This pairing survives long gaps without damage.",
         "Best moments: hosting, family gatherings, travel with no fixed itinerary."],
  verdict_para="Chaldean tradition puts Number 2 (Moon) and Number 3 (Jupiter) in separate families, so this is a <strong>supportive</strong> pairing rather than a natural one, but there is no affliction between them and both are benefic. What it asks for is not more warmth. It is the willingness to interrupt the warmth long enough to say something difficult.",
  faqs=[("Is 2 and 3 a good match for marriage?",
         "Yes, with one specific piece of work: both partners have to practise saying the hard thing early. Left alone, this marriage does not fracture, it slowly hollows out while remaining outwardly pleasant."),
        ("What is the main challenge between 2 and 3?",
         "Unspoken needs. Number 2 does not state them and Number 3 does not detect them, so both end up feeling reasonable while the distance grows."),
        ("Are 2 and 3 compatible in business?",
         "Good for anything public-facing or relationship-driven. Weak on detail and follow-through, so this partnership usually needs a third person who likes admin."),
        ("Does 2 and 3 work in friendship?",
         "Very well, and it is durable. This is often a decades-long friendship that picks up mid-sentence after a year apart.")],
  share="Number 2 (Moon) and Number 3 (Jupiter) compatibility, warm, easy, and quietly avoidant:",
 ),
 (2, 4): dict(
  verdict="Strong",
  tag="Moon and Rahu pairing. Unlikely on paper, strong in Cheiro's system.",
  desc="Number 2 and 4 compatibility in Chaldean numerology: why the intuitive and the unconventional recognise each other, and the double-withdrawal risk.",
  intro="Most compatibility writing treats Number 4 as the difficult one and Number 2 as too sensitive to handle it. Chaldean tradition disagrees, and puts them in the same family.",
  lede="Number 2 (Moon) and Number 4 (Rahu) both belong to Cheiro's 1-2-4-7 group. The reason it holds is specific: Number 2 is one of the few numbers who does not need Number 4 to be normal. Where others manage Number 4's oddness, Number 2 simply reads it, accurately and without alarm.",
  works_h2="Why the unconventional heart lands here",
  works="Number 4 spends a lot of life being told they are paranoid or difficult. Number 2's intuition registers what Number 4 is actually doing, which is pattern-detection running faster than the evidence, and treats it as information rather than a problem. In return Number 4 gives Number 2's intuition an ally who breaks rules on its behalf, which a Moon-led person will rarely do for themselves.",
  watch_h2="Two people going quiet in different rooms",
  watch="Both of these numbers withdraw under pressure, and that is the structural danger. Number 2 absorbs and goes silent; Number 4 disengages and goes silent. Nothing explodes, which is exactly why it can run for months. The other friction is rhythm: Number 4 changes direction suddenly, and Number 2's sense of safety is built on predictability.",
  quick=["Communication style: both indirect. A lot gets conveyed here without being said, and some of it gets conveyed wrong.",
         "Conflict pattern: parallel withdrawal rather than argument. The silence is the fight.",
         "Friendship depth: deep and unusual. Often the friendship where both feel least required to explain themselves.",
         "Best moments: quiet plans, odd hours, anything that does not require either of them to socialise on demand."],
  verdict_para="Number 2 (Moon) and Number 4 (Rahu) sit together in Cheiro's first family, making this a <strong>strong</strong> pairing. It is not a comfortable-looking one from outside, and it depends on both partners agreeing a rule about silence: whoever withdraws says roughly when they will be back.",
  faqs=[("Is 2 and 4 a good match for marriage?",
         "Yes, and often a more stable one than either expects. The work is agreeing in advance how withdrawal gets handled, because both partners do it and neither will chase."),
        ("What is the main challenge between 2 and 4?",
         "Simultaneous withdrawal. When both go quiet at once there is nobody left to reopen the conversation, so it stays closed by default."),
        ("Are 2 and 4 compatible in business?",
         "Yes, particularly on anything unconventional. Number 4 sees the flaw in the accepted approach and Number 2 manages the human cost of changing it."),
        ("Does 2 and 4 work in friendship?",
         "Strongly. This is frequently the friend Number 4 keeps longest, because Number 2 never asked them to be someone else.")],
  share="Number 2 (Moon) and Number 4 (Rahu) compatibility, unlikely on paper, strong in tradition:",
 ),
 (2, 5): dict(
  verdict="Supportive",
  tag="Moon and Mercury pairing. One processes by talking, one by absorbing.",
  desc="Number 2 and 5 compatibility in Chaldean numerology: how Mercury's talk meets the Moon's feeling, and why intimacy means different things to each.",
  intro="Number 5 processes life by talking about it. Number 2 processes life by absorbing it. Both are genuinely trying to get close, and each keeps offering the other the wrong currency.",
  lede="Number 2 (Moon) and Number 5 (Mercury) is a traditional friendship in the planetary scheme, and Number 5 is the adaptable number, supportive with nearly everyone. Number 5 brings movement, curiosity and a mind that will not sit still. Number 2 brings depth, and the ability to sit with something until it resolves.",
  works_h2="What Mercury gives the Moon",
  works="Number 5 is unusually good at interrupting a Moon-led spiral, not by soothing it but by redirecting it. A conversation with Number 5 goes somewhere, which is a relief to a mind that has been circling the same three sentences since midnight. Number 2 in turn gives Number 5's ideas somewhere to settle, and offers the emotional grounding that Mercury tends to skip past on the way to the next thought.",
  watch_h2="Where the mismatch shows",
  watch="Number 2 measures closeness in steady rhythm, and Number 5 finds steady rhythm slightly suffocating. Number 5 measures closeness in interesting conversation, and Number 2 can be sitting through an interesting conversation while feeling entirely unmet. Neither is withholding. They are each fluent in a language the other reads slowly.",
  quick=["Communication style: 5 talks to think, 2 thinks before talking. 5's half-formed ideas can land on 2 as decisions.",
         "Conflict pattern: 5 wants it aired immediately, 2 needs time before speaking. Pushing 2 to answer now guarantees the wrong answer.",
         "Friendship depth: strong and stimulating. Often works better as friendship than as marriage.",
         "Best moments: long conversations, new places, anything with something to notice."],
  verdict_para="Moon and Mercury is a traditional friendship, and Number 5's broad adaptability makes this a <strong>supportive</strong> pairing. The default tilt is favourable. What it asks is that each stops assuming their own definition of intimacy is the obvious one.",
  faqs=[("Is 2 and 5 a good match for marriage?",
         "It can be, with explicit negotiation about routine. Number 2 needs some fixed rhythm to feel safe and Number 5 needs some open space to feel alive; both are available if they are actually discussed."),
        ("What is the main challenge between 2 and 5?",
         "Different definitions of intimacy. Number 5 offers conversation, Number 2 wants presence, and each can feel unmet in a relationship where both are trying hard."),
        ("Are 2 and 5 compatible in business?",
         "Yes. Number 5 generates options and handles communication, Number 2 reads the people and notices what the enthusiasm is glossing over."),
        ("Does 2 and 5 work in friendship?",
         "Very well, and often better than in romance, because friendship does not require the rhythm question to be settled.")],
  share="Number 2 (Moon) and Number 5 (Mercury) compatibility, talking versus absorbing:",
 ),
 (2, 6): dict(
  verdict="Supportive",
  tag="Moon and Venus pairing. Two of the softest numbers in the system.",
  desc="Number 2 and 6 compatibility in Chaldean numerology: the most comfortable pairing in the set, and why comfort is the thing that endangers it.",
  intro="This is probably the most immediately comfortable pairing in the whole set. Both numbers lead with care, both notice small things, and both consider the emotional temperature of a room to be actual information.",
  lede="Number 2 (Moon) and Number 6 (Venus) are both receptive, benefic numbers, and they share a language: home, small gestures, the meal that was made without being asked for. Very little translation is needed here, which is rare and worth naming.",
  works_h2="The shared language",
  works="Neither partner has to be taught that a made bed or a remembered detail is a form of speech. Number 6 builds the beauty of the shared life and Number 2 holds its emotional weather, and those two jobs interlock cleanly. Under ordinary conditions this pairing is genuinely lovely, and both people usually feel more themselves inside it than outside it.",
  watch_h2="Why comfort is the risk",
  watch="Both of these numbers are peace-keepers, which means the hard thing goes unsaid on principle rather than by accident. Worse, both tend to <em>wait to be noticed</em> rather than ask, since asking feels like a failure of the other person's attentiveness. Two people waiting to be noticed can wait a very long time. The single most useful habit here is a standing, scheduled conversation where something uncomfortable is required to be said.",
  quick=["Communication style: both read subtext fluently, which means both over-trust their reading of it.",
         "Conflict pattern: avoidance dressed as kindness. Resentment here is quiet, slow and mutual.",
         "Friendship depth: very high. Often the friendship both describe as their easiest.",
         "Best moments: cooking, home projects, unhurried ordinary days."],
  verdict_para="Number 2 (Moon) and Number 6 (Venus) are in different Chaldean families but are both soft, receptive and benefic, making this a <strong>supportive</strong> pairing with an unusually high comfort floor. The tradition's caution is not about warmth, which is abundant, but about the honesty that warmth can crowd out.",
  faqs=[("Is 2 and 6 a good match for marriage?",
         "Yes, and it is one of the gentler marriages in the system. The risk is not conflict but accumulated silence, so this pairing benefits more than most from a deliberate habit of raising things early."),
        ("What is the main challenge between 2 and 6?",
         "Both wait to be noticed instead of asking. Two people doing that simultaneously produces a long, polite stalemate."),
        ("Are 2 and 6 compatible in business?",
         "Reasonably, in people-centred work. Both will avoid the difficult personnel decision, so this partnership struggles where firmness is required."),
        ("Does 2 and 6 work in friendship?",
         "Extremely well, usually for life. This is the friendship where neither has to explain why they are tired.")],
  share="Number 2 (Moon) and Number 6 (Venus) compatibility, the softest pairing in the set:",
 ),
 (2, 8): dict(
  verdict="Caution",
  tag="Moon and Saturn pairing. Reliable is not the same as responsive.",
  desc="Number 2 and 8 compatibility in Chaldean numerology: why Saturn's reliability does not answer the Moon's need, and what closes the gap.",
  intro="Number 8 will build a life that holds. Number 2 needs to be answered. Those are not the same offer, and the whole difficulty of this pairing lives in the gap between them.",
  lede="Number 2 (Moon) and Number 8 (Saturn) sit in different families, and Saturn is the number Chaldean tradition cautions about most broadly. Number 8 is not cold and not withholding. Saturn expresses care structurally, through provision, planning and staying, and Number 2 reads care through responsiveness, which is a channel Saturn barely transmits on.",
  works_h2="What Saturn does give",
  works="Number 8 offers something a Moon-led person often has never had: a floor that does not move. Financial seriousness, follow-through, an absence of drama. For a Number 2 who grew up managing other people's instability, that can feel like being able to breathe. And Number 2 gives Number 8 emotional access, frequently the only route by which a Saturn-led person says what they are actually carrying.",
  watch_h2="Where it usually goes wrong",
  watch="Under pressure Number 8 contracts and goes silent, treating that as the responsible way to handle a burden alone. Number 2 experiences the same event as love being withdrawn at the exact moment it was needed. Both then feel wronged, sincerely. The other slow failure is Number 8 mistaking provision for presence, and being genuinely bewildered that a well-run household did not answer the question being asked.",
  quick=["Communication style: 2 speaks in tone, 8 speaks in facts, and 8 does not hear tone as content.",
         "Conflict pattern: 8 goes quiet to shoulder it, 2 reads the quiet as abandonment. This is the core loop.",
         "Friendship depth: workable and loyal, less fraught than romance because less responsiveness is required.",
         "Best moments: long-term plans, building something concrete, quiet competence under real stress."],
  verdict_para="Chaldean tradition places Number 8 (Saturn) apart from the other numbers, pairing it naturally only with 4, so Number 2 and Number 8 is a <strong>caution</strong> pairing. That is not a prediction of failure. It means the friction is predictable, which is easier to work with than friction that keeps surprising you.",
  faqs=[("Is 2 and 8 a good match for marriage?",
         "It is one of the harder pairings, but it is not a doomed one. It works when Number 8 learns to narrate the silence rather than just endure it, and Number 2 learns to read provision as a genuine dialect of love."),
        ("What is the main challenge between 2 and 8?",
         "Number 8 withdraws under pressure to protect the family, and Number 2 experiences that withdrawal as the loss of the relationship."),
        ("Are 2 and 8 compatible in business?",
         "Yes, better than in romance. Number 8 handles structure, money and the long horizon; Number 2 handles people and notices morale before it collapses."),
        ("Does 2 and 8 work in friendship?",
         "Reasonably. A friendship makes fewer demands on Saturn's weakest channel, so the loyalty shows and the gap matters less.")],
  share="Number 2 (Moon) and Number 8 (Saturn) compatibility, reliable is not responsive:",
 ),
 (3, 4): dict(
  verdict="Caution",
  tag="Jupiter and Rahu pairing. One trusts the system, one knows it is broken.",
  desc="Number 3 and 4 compatibility in Chaldean numerology: the Guru-Chandal friction, why the optimist and the sceptic grind, and what makes it work.",
  intro="Number 3 believes the system basically works and can be expanded. Number 4 has already spotted the point where it breaks. Both are usually right, about different things, at the same time.",
  lede="Number 3 (Jupiter) and Number 4 (Rahu) is the pairing behind one of the oldest cautions in Indian tradition, the Guru-Chandal combination, where the teacher's expansiveness meets the node's disruption. Chaldean practice inherits the same wariness. This is a friction pairing, and the friction is philosophical before it is personal.",
  works_h2="What the tension is good for",
  works="When this pairing works, it works because Number 4's scepticism stops Number 3 walking cheerfully into an obvious trap, and Number 3's faith stops Number 4 concluding that everything is rigged and nothing is worth starting. Ventures built by a 3 and a 4 who genuinely respect each other tend to be both ambitious and unusually well stress-tested. That is a real combination, and it is not common.",
  watch_h2="How the grind sets in",
  watch="Number 3 experiences Number 4's objections as an endless supply of cold water, and starts editing the dream before sharing it. Number 4 experiences Number 3's optimism as refusal to look, and starts escalating the warning to be heard. Each response makes the other worse. Once Number 3 stops sharing plans and Number 4 stops bothering to flag risks, the pairing is functionally over while still nominally together.",
  quick=["Communication style: 3 pitches, 4 audits. Framing an idea as a question rather than a plan changes this entirely.",
         "Conflict pattern: 3 goes vague and cheerful, 4 gets sharper and more specific. Neither reads the other as engaging.",
         "Friendship depth: can be excellent, and is easier than romance. Distance defuses the philosophical difference.",
         "Best moments: building something concrete together, where 4's objections have a job to do."],
  verdict_para="Jupiter and Rahu carry a specific traditional affliction, and the two numbers sit in different Chaldean families, making this a <strong>caution</strong> pairing. What it needs is a shared agreement that Number 4's objection is a contribution rather than an attack, and that Number 3's optimism is a resource rather than a delusion.",
  faqs=[("Is 3 and 4 a good match for marriage?",
         "It is one of the more demanding pairings. It succeeds where both stop treating the difference in outlook as a character flaw in the other, which usually takes deliberate effort rather than time."),
        ("What is the main challenge between 3 and 4?",
         "Number 3 hears risk assessment as pessimism and Number 4 hears optimism as denial, so both stop bringing their actual thinking to the other."),
        ("Are 3 and 4 compatible in business?",
         "Surprisingly yes, and often better than in marriage. The tension is productive when it has a concrete object, and this pairing builds things that survive contact with reality."),
        ("Does 3 and 4 work in friendship?",
         "Yes, more easily than romance. Friendship allows the philosophical gap to stay interesting instead of becoming a daily negotiation.")],
  share="Number 3 (Jupiter) and Number 4 (Rahu) compatibility, the optimist and the sceptic:",
 ),
 (3, 7): dict(
  verdict="Caution",
  tag="Jupiter and Ketu pairing. Both seekers, opposite directions.",
  desc="Number 3 and 7 compatibility in Chaldean numerology: why two seekers with opposite methods struggle, and where they genuinely meet.",
  intro="Both of these numbers are looking for meaning. Number 3 looks for it by adding, more people, more travel, more study. Number 7 looks for it by subtracting. That is the whole pairing, and it is more of a problem than it sounds.",
  lede="Number 3 (Jupiter) and Number 7 (Ketu) sit in different Chaldean families, and the pairing carries an echo of the same Jupiter-and-node caution that applies to 3 and 4. What makes it poignant rather than merely difficult is that they want the same thing and cannot use each other's method to get it.",
  works_h2="Where they genuinely meet",
  works="The meeting point is real and worth protecting: both take the big questions seriously, and neither finds the other's interest in them strange. A Number 3 and a Number 7 can have a conversation at a depth that most pairings never reach, and both come away fed. Number 3 also brings Number 7 into a world they would not otherwise enter, and Number 7 gives Number 3 something Jupiter rarely gets, permission to stop expanding.",
  watch_h2="Where the methods collide",
  watch="Number 3's answer to almost everything is more, and to Number 7 that reads as noise, distraction, evasion. Number 7's answer is less, and to Number 3 that reads as withdrawal from life itself. The social calendar is where this becomes daily: Number 3 accepts invitations as a matter of temperament, and Number 7 pays for each one in a currency Number 3 does not track.",
  quick=["Communication style: 3 thinks out loud at length, 7 speaks once and expects it to count.",
         "Conflict pattern: 3 wants to talk it through now, 7 needs solitude first. The talking-through delays the resolution.",
         "Friendship depth: often excellent. This works far better with space in it than without.",
         "Best moments: one long conversation about something that matters, with nobody else present."],
  verdict_para="Different families and an inherited caution around Jupiter with the nodes make this a <strong>caution</strong> pairing. It is one of the more workable cautions, though, because the underlying values overlap. What has to be negotiated explicitly is the social calendar and the right to decline it.",
  faqs=[("Is 3 and 7 a good match for marriage?",
         "It is demanding but not unpromising, because the values align even where the methods do not. Most of the practical work is about how much social life is compulsory for both."),
        ("What is the main challenge between 3 and 7?",
         "Number 3 seeks meaning by adding and Number 7 by subtracting, so each reads the other's core strategy as a mistake."),
        ("Are 3 and 7 compatible in business?",
         "Workable with separated roles. Number 3 does the outward and relational work, Number 7 does the deep and analytical work, and they should not be in the same meetings all day."),
        ("Does 3 and 7 work in friendship?",
         "Yes, often very well. Friendship supplies the space this pairing needs, and the conversations are frequently the best either of them has.")],
  share="Number 3 (Jupiter) and Number 7 (Ketu) compatibility, two seekers going opposite ways:",
 ),
 (3, 8): dict(
  verdict="Caution",
  tag="Jupiter and Saturn pairing. Expansion against contraction.",
  desc="Number 3 and 8 compatibility in Chaldean numerology: the optimist and the realist, why the grind is structural, and the one thing that fixes it.",
  intro="Jupiter expands and Saturn contracts. This is the oldest opposition in the planetary scheme, and in a relationship it shows up as the same argument for thirty years, wearing different clothes.",
  lede="Number 3 (Jupiter) and Number 8 (Saturn) sit in different Chaldean families, and Saturn is the number tradition holds apart from the rest. Number 3 assumes the future is larger than the present. Number 8 assumes it must be paid for. Both assumptions are correct, which is precisely why neither partner ever concedes.",
  works_h2="The version that works",
  works="When this pairing succeeds it is formidable, because Number 3 supplies the vision and Number 8 supplies the delivery, and each is genuinely bad at the other's job. A plan that has survived Number 8's scrutiny and retained Number 3's ambition is usually a good plan. Some of the most durable family businesses run on exactly this combination.",
  watch_h2="Why it grinds",
  watch="The failure mode is mutual contempt arriving so gradually that neither notices. Number 8 starts to regard Number 3 as unserious; Number 3 starts to regard Number 8 as an anchor dressed up as prudence. Money is where it usually surfaces, because money is where optimism and caution have to produce a single number. The fix is boring and effective: separate the conversation about what is possible from the conversation about what it costs, and do not hold them on the same evening.",
  quick=["Communication style: 3 leads with possibility, 8 leads with cost. Both think the other has skipped a step.",
         "Conflict pattern: 3 gets louder and vaguer, 8 gets quieter and more concrete. Neither concedes.",
         "Friendship depth: moderate and often improves with age, as 3 gains realism and 8 loosens.",
         "Best moments: executing something ambitious that is already funded and planned."],
  verdict_para="Jupiter and Saturn are traditional opposites, and Saturn stands apart in the Chaldean scheme, so this is a <strong>caution</strong> pairing. It is also the caution with the highest ceiling: handled deliberately, it produces things neither number could build alone.",
  faqs=[("Is 3 and 8 a good match for marriage?",
         "Hard but often durable, particularly later in life. Younger versions of this pairing tend to fight about money; older versions tend to have worked out who decides what."),
        ("What is the main challenge between 3 and 8?",
         "Optimism against caution, usually surfacing as money. Both positions are defensible, which is why the argument recurs rather than resolves."),
        ("Are 3 and 8 compatible in business?",
         "Yes, and this is where the pairing is strongest. Number 3 finds the opportunity and Number 8 makes it survive, provided the vision and cost conversations are kept separate."),
        ("Does 3 and 8 work in friendship?",
         "Moderately, and it tends to improve over the years as each acquires a little of the other's outlook.")],
  share="Number 3 (Jupiter) and Number 8 (Saturn) compatibility, expansion against contraction:",
 ),
 (4, 6): dict(
  verdict="Supportive",
  tag="Rahu and Venus pairing. Venus makes the unconventional life livable.",
  desc="Number 4 and 6 compatibility in Chaldean numerology: why Rahu and Venus are traditionally allied, and how 6 makes 4's strangeness a home.",
  intro="Number 4 builds a life that does not match the template. Number 6 makes that life beautiful instead of merely unusual, which is the difference between a life people admire and a life people worry about.",
  lede="Rahu and Venus are traditionally allied in the planetary scheme, one of the few alliances that crosses the Chaldean families, and it shows in practice. Number 6 is drawn to what is interesting rather than what is correct, and Number 4 is definitionally interesting.",
  works_h2="What Venus does for Rahu",
  works="Number 4 is used to being tolerated. Number 6 does something different: they find the oddness appealing and then furnish it, literally and socially. A Number 6 will make the unconventional household warm, feed the strange friends, and present the whole arrangement to the world as obviously fine. For a Number 4 who has spent years translating themselves, that is a substantial relief. In return Number 4 gives Number 6 permission to stop performing respectability.",
  watch_h2="Where it strains",
  watch="Number 6 needs the relationship to feel harmonious and Number 4 periodically detonates the arrangement, not maliciously but because something had become false and staying in it was worse. Number 6 reads the disruption as a rejection of what they built. The other strain runs the other way: Number 6's attention to how things look can land on Number 4 as a request to be more normal, which is the one request Number 4 cannot grant.",
  quick=["Communication style: 6 softens to keep the peace, 4 says the blunt thing. 6 often hears bluntness as coldness.",
         "Conflict pattern: 4 disrupts, 6 repairs and smooths. Over time 6 tires of being the one who repairs.",
         "Friendship depth: strong. 6 is frequently the friend who normalises 4 to everybody else.",
         "Best moments: making a home, hosting on their own terms, building something that looks like nobody else's."],
  verdict_para="Rahu and Venus are traditionally allied despite sitting in different Chaldean families, making this a <strong>supportive</strong> pairing. It runs well as long as Number 6 does not mistake Number 4's need for authenticity for a verdict on the home they have made together.",
  faqs=[("Is 4 and 6 a good match for marriage?",
         "Yes, and it is one of the more pleasant cross-family pairings. Number 6 gives Number 4 a place to be strange in comfort, which is rarer than it sounds."),
        ("What is the main challenge between 4 and 6?",
         "Number 4 occasionally needs to break the arrangement to stay honest, and Number 6 experiences that as damage to something they built with care."),
        ("Are 4 and 6 compatible in business?",
         "Yes, especially in anything design-led or brand-led. Number 4 finds the unconventional angle and Number 6 makes it desirable rather than merely clever."),
        ("Does 4 and 6 work in friendship?",
         "Very well. Number 6 often becomes the person who explains Number 4 to the rest of the world, generously and accurately.")],
  share="Number 4 (Rahu) and Number 6 (Venus) compatibility, making the unconventional beautiful:",
 ),
 (4, 7): dict(
  verdict="Strong",
  tag="Rahu and Ketu pairing. The two nodes, both outsiders.",
  desc="Number 4 and 7 compatibility in Chaldean numerology: why the two lunar nodes recognise each other instantly, and the isolation risk that follows.",
  intro="Number 4 and Number 7 are the two nodes of the same axis, and the recognition between them is usually immediate. Both have spent their lives slightly outside the room, watching it.",
  lede="Rahu and Ketu are the ascending and descending nodes, opposite ends of one line, and both numbers sit in Cheiro's 1-2-4-7 family. Neither has to explain to the other why the conventional version of things never quite fitted. That shared position outside the mainstream is the foundation, and it is a strong one.",
  works_h2="The recognition",
  works="What each gets here is the end of translation. Number 4's pattern-detection and Number 7's inward observation are different faculties pointed at the same fact, that the accepted account of things is incomplete. They tend to reach conclusions in parallel and arrive at the same scepticism from different directions, which both find steadying. Conversations in this pairing skip several steps that other pairings have to walk through.",
  watch_h2="The isolation risk",
  watch="The specific danger is a closed loop. Two outsiders who validate each other's read can drift a long way from other people without either registering it, and there is nobody inside the relationship whose instinct is to check. Both also withdraw under pressure, so the same double-silence problem that affects 2 and 4 applies here with less counterweight. This pairing benefits, more than most, from deliberately keeping other people close.",
  quick=["Communication style: unusually efficient, often elliptical. Outsiders find the shorthand hard to follow.",
         "Conflict pattern: both go inward. Nobody chases, so a rift can hold for a long time without either intending it.",
         "Friendship depth: immediate and durable. Frequently the first friendship where either felt fully legible.",
         "Best moments: long unstructured stretches, odd projects, being unsociable together."],
  verdict_para="Both numbers belong to Cheiro's first family, and Rahu and Ketu are the two ends of a single axis, making this a <strong>strong</strong> pairing. The caveat is unusual: the risk here is not friction between them but the two of them jointly withdrawing from everyone else.",
  faqs=[("Is 4 and 7 a good match for marriage?",
         "Yes, and often a deeply private one. The work is outward rather than inward: maintaining friendships and obligations outside the pairing, which neither will do by instinct."),
        ("What is the main challenge between 4 and 7?",
         "Isolation. They agree too easily, and there is no one inside the relationship inclined to question the shared view."),
        ("Are 4 and 7 compatible in business?",
         "Yes, for research, analysis and anything requiring unconventional thinking. Both are poor at the client-facing half, so a third partner usually helps."),
        ("Does 4 and 7 work in friendship?",
         "Strongly. This is often the friendship where each stops feeling like the odd one, and it tends to last for decades.")],
  share="Number 4 (Rahu) and Number 7 (Ketu) compatibility, the two nodes, both outsiders:",
 ),
 (5, 8): dict(
  verdict="Caution",
  tag="Mercury and Saturn pairing. Speed against weight.",
  desc="Number 5 and 8 compatibility in Chaldean numerology: why the fast, light number clashes with the slow, heavy one, and where it can still work.",
  intro="Number 5 moves fast and travels light. Number 8 moves slowly and carries everything. Both approaches work, and each finds the other faintly irresponsible.",
  lede="Number 5 (Mercury) is supportive with almost every number, which makes this pairing an exception worth noting. Tradition already flags 4 and 5 as a caution, and Number 8 belongs with 4 in the Chaldean scheme. Mercury's lightness and Saturn's weight are simply built to different specifications.",
  works_h2="Where it can genuinely work",
  works="Number 5 can lift a Saturn-led person out of a rut that had come to feel like fate, which is a real gift and one Number 8 cannot give themselves. Number 8 can give Number 5's scattered energy a structure that finally converts it into something finished, which is the thing Number 5 most often lacks. Where both actively want that exchange, this pairing produces results.",
  watch_h2="How the friction accumulates",
  watch="Number 8 hears Number 5's improvisation as carelessness with things that matter, especially money and commitments. Number 5 hears Number 8's caution as a refusal to live. The daily version is pace: Number 5 decides in a minute, Number 8 wants a week, and both feel the other is doing it wrong on purpose. Left alone, Number 8 becomes controlling and Number 5 becomes evasive, which confirms each one's worst reading of the other.",
  quick=["Communication style: 5 thinks aloud and revises, 8 treats a stated position as a commitment. This causes real trouble.",
         "Conflict pattern: 5 deflects with humour or movement, 8 becomes immovable. The deflection hardens the immovability.",
         "Friendship depth: workable and often affectionate at a distance. Shared logistics are where it strains.",
         "Best moments: a defined project with a deadline, where 5 improvises inside 8's structure."],
  verdict_para="Following the tradition's caution about Mercury with the 4-and-8 pair, this is a <strong>caution</strong> pairing. The friction is about tempo rather than values, which makes it more tractable than it feels day to day: agreeing explicitly on which decisions are fast and which are slow removes most of it.",
  faqs=[("Is 5 and 8 a good match for marriage?",
         "One of the harder ones. It works where both stop moralising about pace, and it fails where Number 8 tries to slow Number 5 down and Number 5 starts making decisions without mentioning them."),
        ("What is the main challenge between 5 and 8?",
         "Tempo. Number 5 decides quickly and revises, Number 8 decides slowly and commits, and each reads the other's method as irresponsibility."),
        ("Are 5 and 8 compatible in business?",
         "Yes, better than in marriage, if the roles are split cleanly. Number 5 handles communication and opportunity, Number 8 handles finance and delivery, and neither reviews the other's method."),
        ("Does 5 and 8 work in friendship?",
         "Reasonably well, as long as they are not sharing money or logistics. The friendship is usually warmer than the partnership.")],
  share="Number 5 (Mercury) and Number 8 (Saturn) compatibility, speed against weight:",
 ),
 (5, 9): dict(
  verdict="Supportive",
  tag="Mercury and Mars pairing. Both fast, both direct, plenty of heat.",
  desc="Number 5 and 9 compatibility in Chaldean numerology: two quick, direct numbers, why it is exciting, and why nothing here cools down on its own.",
  intro="Two fast numbers, both direct, neither inclined to sit on a thought. This pairing has more energy than almost any other in the set, and no natural brake anywhere in it.",
  lede="Number 5 (Mercury) is the adaptable number and Number 9 (Mars) is the forceful one, and they share a tempo. Things happen quickly here: decisions, plans, arguments, reconciliations. Both would rather have the confrontation than the silence, which puts them ahead of most pairings on the thing that usually kills relationships.",
  works_h2="Why the pace suits them",
  works="Neither partner has to wait for the other to catch up, and neither has to decode anything. Number 9 gives Number 5's ideas force and follow-through, turning interest into action. Number 5 gives Number 9's intensity flexibility, and can defuse an escalating situation with a change of subject in a way no other number manages. When it is good, it is genuinely alive, and both tend to be more productive inside it than out.",
  watch_h2="No brake",
  watch="Because both escalate rather than withdraw, a small disagreement can be a serious one within minutes. Number 9 brings heat and Number 5 brings speed, and the combination means things are said at volume before either has finished thinking. The pairing also struggles with follow-through on the unglamorous: two fast numbers can start a great deal and finish very little, and the resulting mess becomes its own recurring argument.",
  quick=["Communication style: both blunt, both quick. Very little is left unsaid, including things better left unsaid.",
         "Conflict pattern: rapid escalation, and usually rapid repair. Sustained cold silence is rare here.",
         "Friendship depth: high-energy and durable. Often the friend who gets things moving.",
         "Best moments: anything physical, competitive or urgent. Shared projects with real deadlines."],
  verdict_para="Number 5's broad adaptability and a shared tempo make this a <strong>supportive</strong> pairing. The tilt is favourable. What it lacks is a natural cooling mechanism, so this is one of the few pairings where an agreed rule about pausing an argument does real work.",
  faqs=[("Is 5 and 9 a good match for marriage?",
         "Yes, and rarely a boring one. The work is agreeing on a way to stop an argument mid-flight, because neither partner will de-escalate by instinct."),
        ("What is the main challenge between 5 and 9?",
         "No brake. Both escalate, both are fast, and things get said at speed that take a long while to unsay."),
        ("Are 5 and 9 compatible in business?",
         "Yes, strongly, for launching things. Weak on maintenance and admin, so this partnership needs someone who finishes what they start."),
        ("Does 5 and 9 work in friendship?",
         "Very well. This is usually the friendship where plans actually happen rather than being discussed indefinitely.")],
  share="Number 5 (Mercury) and Number 9 (Mars) compatibility, two fast numbers and no brake:",
 ),
 (6, 7): dict(
  verdict="Supportive",
  tag="Venus and Ketu pairing. One wants closeness expressed, one wants it assumed.",
  desc="Number 6 and 7 compatibility in Chaldean numerology: how Venus softens Ketu's detachment, and the reassurance gap between them.",
  intro="Number 6 shows love by expressing it. Number 7 shows love by assuming it does not need saying. Both are being sincere, and each keeps failing the other's test without knowing a test was set.",
  lede="Number 6 (Venus) and Number 7 (Ketu) sit in different Chaldean families, but Venus has an unusual capacity to soften the nodes, and this pairing tends to work better in practice than its cross-family position suggests. Number 6 makes the world comfortable; Number 7 makes it meaningful.",
  works_h2="What Venus offers Ketu",
  works="Number 7 is often physically neglectful of themselves, living slightly outside the ordinary business of meals and warmth and company. Number 6 attends to all of it without making it a project, and for a Ketu-led person that care can be quietly transformative. Number 7 gives Number 6 something equally rare: attention that is not performative. When Number 7 listens, they are actually listening, and Number 6 tends to spend a lot of life being half-heard.",
  watch_h2="The reassurance gap",
  watch="Number 6 needs the bond confirmed, in words and gestures, at reasonably regular intervals. Number 7 considers a bond that requires confirmation to be a weak one, and finds the asking faintly diminishing. So Number 6 asks less and feels less secure, and Number 7 notices the withdrawal without understanding that they caused it. The other friction is social: Number 6 builds a life full of people and Number 7 needs most of them gone by nine.",
  quick=["Communication style: 6 states feelings directly, 7 assumes what is obvious need not be said.",
         "Conflict pattern: 6 seeks contact to repair, 7 seeks solitude to process. The pursuit lengthens the retreat.",
         "Friendship depth: strong and often surprising to both. 7 tends to allow 6 unusually close.",
         "Best moments: quiet domestic evenings, small numbers, unhurried time at home."],
  verdict_para="Venus and Ketu cross the Chaldean families, but Venus's softening effect on the nodes makes this a <strong>supportive</strong> pairing rather than a cautioned one. The whole negotiation is about reassurance: Number 7 has to accept that saying it out loud is not a weakness in the bond, and Number 6 has to accept that silence here is not distance.",
  faqs=[("Is 6 and 7 a good match for marriage?",
         "Yes, and often a peaceful one, provided the reassurance question gets addressed explicitly rather than left to instinct."),
        ("What is the main challenge between 6 and 7?",
         "Number 6 needs the bond expressed and Number 7 believes an expressed bond is a less certain one, so both keep failing a test neither announced."),
        ("Are 6 and 7 compatible in business?",
         "Moderately. Number 6 handles clients and culture, Number 7 handles depth and analysis. Neither enjoys confrontation, so difficult decisions tend to be deferred."),
        ("Does 6 and 7 work in friendship?",
         "Very well. Number 6 is frequently one of the few people Number 7 keeps close without finding it costly.")],
  share="Number 6 (Venus) and Number 7 (Ketu) compatibility, expressed versus assumed:",
 ),
 (6, 8): dict(
  verdict="Caution",
  tag="Venus and Saturn pairing. Beautiful now against secure later.",
  desc="Number 6 and 8 compatibility in Chaldean numerology: why Venus wants the present lovely and Saturn wants the future safe, and how the deferral wears.",
  intro="Number 6 wants the relationship to be good now. Number 8 wants it to be safe in twenty years. Almost every argument this pairing has is a version of that, whatever it appears to be about.",
  lede="Number 6 (Venus) and Number 8 (Saturn) sit in different Chaldean families, and Saturn is held apart from the rest in this system. Venus spends on the present because the present is where life is; Saturn defers the present because the future has to be paid for. Both are coherent positions, and they compete for the same money, time and attention.",
  works_h2="What each supplies",
  works="Number 8 provides the security inside which Number 6's care can actually flourish. It is much easier to make a home beautiful when the home is not at risk, and many Number 6s underestimate how much of their ease rests on someone else's planning. Number 8, in turn, gets something they will rarely build alone: a life that is pleasant to be inside. Saturn can construct a fortress and forget to furnish it, and Number 6 furnishes it.",
  watch_h2="How the deferral wears",
  watch="The pattern is a long series of small deferrals. Number 8 postpones the holiday, the renovation, the celebration, always for defensible reasons, and Number 6 experiences an accumulating sense that the actual life keeps being scheduled for later. Meanwhile Number 8 sees spending on beauty as a lack of seriousness about risk. Number 6 stops asking, spends quietly instead, and the finances become the site of a conflict that was never really about finances.",
  quick=["Communication style: 6 raises things gently and indirectly, 8 responds with numbers. 6 often feels answered rather than heard.",
         "Conflict pattern: 6 concedes to keep the peace and privately resents it, 8 concludes the matter was settled.",
         "Friendship depth: moderate. Works better without shared finances in it.",
         "Best moments: a milestone that 8 planned and 6 made beautiful. Both are proud of those."],
  verdict_para="Saturn stands apart in the Chaldean scheme and Venus sits in the opposing family, making this a <strong>caution</strong> pairing. The tractable version involves a genuinely agreed allocation for the present, so that beauty stops having to be justified case by case and Number 6 stops having to ask.",
  faqs=[("Is 6 and 8 a good match for marriage?",
         "Difficult but common, and workable. It comes down to a real agreement about spending on the present, held to by both, rather than a running negotiation."),
        ("What is the main challenge between 6 and 8?",
         "Number 8 defers the present for the future's sake and Number 6 experiences the present being permanently postponed."),
        ("Are 6 and 8 compatible in business?",
         "Yes, reasonably. Number 8 runs the finances and the long plan, Number 6 handles clients, culture and how the thing looks and feels."),
        ("Does 6 and 8 work in friendship?",
         "Moderately, and better than in marriage, because friendship rarely requires them to agree on a budget.")],
  share="Number 6 (Venus) and Number 8 (Saturn) compatibility, beautiful now versus secure later:",
 ),
 (7, 9): dict(
  verdict="Supportive",
  tag="Ketu and Mars pairing. Same fire, opposite settings.",
  desc="Number 7 and 9 compatibility in Chaldean numerology: why Ketu and Mars share a temperament, one turned inward and one outward.",
  intro="Chaldean tradition treats Ketu as carrying a Mars-like force, which makes this pairing less odd than it looks. Number 9 turns that force outward into action; Number 7 turns it inward into observation. Same fire, opposite settings.",
  lede="Number 7 (Ketu) and Number 9 (Mars) sit in different Chaldean families, but the shared underlying temperament gives them more common ground than the grouping implies. Both have strong convictions. Both are largely uninterested in social performance. Neither is remotely easy to move once they have decided something.",
  works_h2="The shared temperament",
  works="What each recognises in the other is intensity without pretence. Number 9 respects that Number 7's quiet is not timidity, and Number 7 respects that Number 9's heat is not mere temper. Number 9 gives Number 7 a route into action, which Ketu-led people can otherwise defer indefinitely. Number 7 gives Number 9 a place to put the fire down, and offers the one perspective Number 9 will usually accept, because it clearly comes without an agenda.",
  watch_h2="Where the settings clash",
  watch="Number 9 wants the issue engaged now, at volume if necessary. Number 7 wants to withdraw and consider, and experiences the demand for immediate engagement as an assault. Number 9 then reads the withdrawal as contempt, which is the reading most likely to make Number 7 withdraw further. There is also a quieter problem: both hold grudges, Number 9 loudly and Number 7 silently, and neither is much good at deciding a thing is finished.",
  quick=["Communication style: 9 confronts directly, 7 goes quiet and returns later with a considered position.",
         "Conflict pattern: 9 escalates to resolve, 7 exits to think. This is the central mismatch.",
         "Friendship depth: strong, often built on shared principle rather than shared activity.",
         "Best moments: a cause or a fight that both believe in, with 9 in front and 7 working out the strategy."],
  verdict_para="Different families, but Ketu's traditional Mars-like character makes this a <strong>supportive</strong> pairing rather than a cautioned one. The one thing that needs an explicit agreement is the timing of difficult conversations, because Number 9's instinct is now and Number 7's is later.",
  faqs=[("Is 7 and 9 a good match for marriage?",
         "Yes, with an agreed protocol for conflict. Number 9 has to accept that Number 7 will answer tomorrow, and Number 7 has to actually come back tomorrow rather than letting it lapse."),
        ("What is the main challenge between 7 and 9?",
         "Timing. Number 9 needs it out now and Number 7 needs to withdraw first, so the request for immediacy produces the opposite."),
        ("Are 7 and 9 compatible in business?",
         "Yes, particularly where conviction matters. Number 9 drives and fronts it, Number 7 thinks it through, and both are indifferent to office politics."),
        ("Does 7 and 9 work in friendship?",
         "Strongly, and usually for a long time. It tends to be founded on shared values rather than on spending much time together.")],
  share="Number 7 (Ketu) and Number 9 (Mars) compatibility, same fire, opposite settings:",
 ),
}

TEMPLATE = """<!DOCTYPE html><html lang="en"><head>
<!-- Google tag (gtag.js) -->
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-70GFTN27M6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-70GFTN27M6');
</script>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="icon" type="image/svg+xml" href="/assets/namealigned-favicon.svg">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="NameAligned.com">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-IN" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="NameAligned.com">
<meta property="og:locale" content="en_IN">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og}">

<script type="application/ld+json">
{article_ld}
</script>
<script type="application/ld+json">
{breadcrumb_ld}
</script>
<script type="application/ld+json">
{faq_ld}
</script>

<link rel="stylesheet" href="/assets/style.css">
<link rel="stylesheet" href="/assets/theme-cosmic-light.css">
<style>
.seo-hero{{padding:3.5rem 0 1.75rem;text-align:center;background:linear-gradient(160deg,#1a1340 0%,#2a1a5c 100%);color:#f0ece0;}}
.seo-hero .badge{{display:inline-block;font-family:sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f0b429 !important;background:rgba(240,180,41,.12);padding:5px 14px;border-radius:20px;border:1px solid rgba(240,180,41,.35);margin-bottom:1rem;}}
.seo-hero h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4.2vw,42px);line-height:1.2;margin:0 auto .5rem;max-width:780px;color:#f0ece0 !important;text-shadow:0 2px 24px rgba(124,92,255,.35);}}
.seo-hero .glyph{{font-size:42px;color:#f0b429 !important;line-height:1;margin-bottom:.75rem;}}
.seo-hero .tag{{font-family:sans-serif;font-size:14px;color:rgba(240,236,224,.85) !important;letter-spacing:.04em;max-width:680px;margin:0 auto;line-height:1.5;}}
/* Two-column layout: article + sticky CTA sidebar (matches /blog) */
.seo-wrap{{max-width:1080px;margin:0 auto;padding:0 1.25rem;display:grid;grid-template-columns:1fr 280px;gap:2.5rem;align-items:start;}}
@media(max-width:880px){{.seo-wrap{{grid-template-columns:1fr;gap:0;}}}}
.seo-body{{padding:2rem 0;}}
.seo-aside{{padding-top:2rem;}}
@media(max-width:880px){{.seo-aside{{padding-top:0;margin-bottom:2rem;}}}}
.article-sidebar{{position:sticky;top:90px;background:linear-gradient(135deg,#03090f,#060d18);border-radius:14px;padding:1.5rem;color:#f0ece0;border:1px solid rgba(157,127,255,.18);}}
.article-sidebar .eyebrow{{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#f0b429;font-family:sans-serif;margin-bottom:.6rem;font-weight:600;}}
.article-sidebar h3{{font-family:Georgia,serif;font-size:18px;color:#f0ece0;margin:0 0 .55rem;line-height:1.3;}}
.article-sidebar p{{font-size:13px;color:#b0a898;font-family:sans-serif;line-height:1.6;margin:0 0 1rem;}}
.article-sidebar .price-row{{display:flex;gap:.5rem;align-items:baseline;margin-bottom:1rem;}}
.article-sidebar .price-inr{{font-size:18px;color:#f0b429;font-weight:700;font-family:sans-serif;}}
.article-sidebar .price-usd{{font-size:13px;color:#9d7fff;font-family:sans-serif;}}
.article-sidebar a.cta{{display:block;text-align:center;background:#f0b429;color:#0a0820;font-family:sans-serif;font-size:13.5px;font-weight:700;padding:10px 14px;border-radius:8px;text-decoration:none;transition:background .2s;}}
.article-sidebar a.cta:hover{{background:#f5c247;}}
.article-sidebar a.cta.outline{{background:transparent;color:#cbb8e8;border:1px solid rgba(157,127,255,.35);margin-top:.55rem;}}
.article-sidebar .sep{{height:1px;background:rgba(157,127,255,.15);margin:1.1rem 0;}}
.seo-body h2{{font-family:'Playfair Display',Georgia,serif;font-size:24px;color:var(--text);margin:2rem 0 .65rem;line-height:1.25;}}
.seo-body h3{{font-family:'Playfair Display',Georgia,serif;font-size:18px;color:var(--text);margin:1.5rem 0 .5rem;}}
.seo-body p{{font-family:sans-serif;font-size:14.5px;line-height:1.75;color:var(--text);margin-bottom:1rem;}}
.seo-body ul{{font-family:sans-serif;font-size:14px;line-height:1.85;color:var(--text);padding-left:1.25rem;margin-bottom:1.25rem;}}
.seo-body li{{margin-bottom:.35rem;}}
.seo-body em{{color:var(--gold-d);font-style:italic;}}
.seo-cta-band{{background:var(--gold-l);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.5rem;margin:2rem 0;text-align:center;}}
.seo-cta-band h3{{margin:0 0 .35rem;font-family:Georgia,serif;font-size:19px;color:var(--text);}}
.seo-cta-band p{{margin:0 0 1rem;font-size:13.5px;color:var(--text2);font-family:sans-serif;}}
.seo-cta-band .btn-pair{{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;}}
.seo-cta-band a{{display:inline-block;font-family:sans-serif;font-size:13.5px;font-weight:600;padding:9px 18px;border-radius:8px;text-decoration:none;}}
.seo-cta-band a.primary{{background:var(--gold);color:#0a0820;}}
.seo-cta-band a.primary:hover{{background:#f5c247;}}
.seo-cta-band a.outline{{background:transparent;color:var(--text);border:1.5px solid var(--gold-b);}}
.seo-faq{{margin:2rem 0;}}
.seo-faq details{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem 1.1rem;margin-bottom:.6rem;}}
.seo-faq summary{{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--text);cursor:pointer;line-height:1.4;}}
.seo-faq details[open] summary{{margin-bottom:.5rem;}}
.seo-faq details p{{font-family:sans-serif;font-size:13.5px;line-height:1.7;color:var(--text2);margin:0;}}
.seo-related{{margin:2.5rem 0 1rem;}}
.seo-related-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;}}
@media(max-width:640px){{.seo-related-grid{{grid-template-columns:1fr;}}}}
.seo-rel-card{{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.9rem 1rem;text-decoration:none;color:var(--text);transition:transform .15s ease,box-shadow .15s ease;}}
.seo-rel-card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(201,162,39,.12);}}
.seo-rel-card .eb{{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:.25rem;}}
.seo-rel-card .ti{{font-family:Georgia,serif;font-size:14.5px;font-weight:700;line-height:1.3;}}
nav.crumb{{font-family:sans-serif;font-size:12px;color:var(--text3);padding:1rem 1.25rem 0;max-width:1080px;margin:0 auto;}}
nav.crumb a{{color:var(--text3);text-decoration:none;}}
.seo-tells{{background:rgba(157,127,255,.05);border:1px solid rgba(157,127,255,.18);border-radius:12px;padding:1.25rem 1.5rem;margin:1.5rem 0;}}
.seo-tells h3{{margin:0 0 .65rem;font-family:Georgia,serif;font-size:17px;color:var(--gold-d);}}
.seo-tells ul{{margin:0;padding-left:1.25rem;}}
</style>
<link rel="stylesheet" href="assets/internal-linking.css">
</head>
<body>

<nav class="nav">
  <div class="container nav-inner">
    <a href="/" class="nav-logo" aria-label="NameAligned.com" style="font-family:'Playfair Display',Georgia,serif;text-decoration:none;display:inline-flex;flex-direction:column;align-items:stretch;gap:0;line-height:1;">
      <span style="font-size:26px;font-weight:700;color:#0a0820;letter-spacing:-.01em;line-height:1;white-space:nowrap;">Name<span style="color:#6d4ed1;">Aligned</span><span style="color:#6d4ed1;font-weight:600;">.com</span></span>
      <span style="font-family:'Inter','Helvetica Neue',Arial,sans-serif;font-size:9.5px;font-weight:600;color:#8a7ba8;text-transform:uppercase;margin-top:5px;display:flex;justify-content:space-between;width:100%;"><span>C</span><span>H</span><span>A</span><span>L</span><span>D</span><span>E</span><span>A</span><span>N</span><span>&nbsp;</span><span>N</span><span>U</span><span>M</span><span>E</span><span>R</span><span>O</span><span>L</span><span>O</span><span>G</span><span>Y</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="/analyzer">Free Analysis</a></li>
      <li><a href="/number">Numbers</a></li>
      <li><a href="/love-compatibility-numerology">Compatibility</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/analyzer" class="nav-cta">Try Free →</a></li>
    </ul>
  </div>
</nav>


<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/sitemap-pages">Numerology Guides</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">Number {a} &amp; {b} Compatibility</span>
</nav>

<header class="seo-hero">
  <div class="container">
    <div class="badge">Compatibility · {pa} &amp; {pb}</div>
    <div class="glyph">{ga}{gb}</div>
    <h1>Number {a} and {b} Compatibility</h1>
    <div class="tag">{tag}</div>
  </div>
</header>

<div class="seo-wrap">

  <main class="seo-body">


  <p>{intro}</p>
  <div class="emotional-pair-insights emotional-insights-strip" data-pair="{a}-{b}"></div>


  <p>{lede}</p>

  <h2>{works_h2}</h2>
  <p>{works}</p>

  <h2>{watch_h2}</h2>
  <p>{watch}</p>

  <div class="seo-tells">
    <h3>Quick read: how this pairing actually plays out</h3>
    <ul>
{quick}
    </ul>
  </div>

  <h2>Compatibility verdict: {verdict}</h2>
  <p>{verdict_para}</p>



<div class="seo-cta-band">
  <h3>Curious how this lands for your own number?</h3>
  <p>Run a free Chaldean check, takes a few seconds. The full personalised destiny report is <strong>$2.50 / ₹249 · 50% off</strong>.</p>
  <div class="btn-pair">
    <a href="/love-compatibility-numerology" class="primary">Compatibility check →</a>
    <a href="/report" class="outline">Full Report $2.50 / ₹249 · 50% off</a>
    <a href="/ask-aura" class="outline">Ask Aura</a>
  </div>
</div>
<div class="share-strip"
     data-share-source="compat-pair"
     data-emotion-headline="Send this to the person you are wondering about."
     data-emotion-prompt="Ask them which lines hit. The conversation that follows is usually more useful than the reading."
     data-share-text="{share}"></div>



    <h2>Frequently asked</h2>
    <div class="seo-faq">
{faq_html}
    </div>

    <section class="seo-related">
      <h2>Continue exploring</h2>
      <div class="seo-related-grid">
      <a href="/emotional-archetype-{arch_a}" class="seo-rel-card" data-na-event="archetype_viewed" data-na-params='{{"archetype":"{arch_a}","number":{a},"from":"compat-{a}-{b}"}}'><span class="eb">Their archetype</span><span class="ti">{arch_a_name}, the deeper read for Number {a}</span></a>
      <a href="/emotional-archetype-{arch_b}" class="seo-rel-card" data-na-event="archetype_viewed" data-na-params='{{"archetype":"{arch_b}","number":{b},"from":"compat-{a}-{b}"}}'><span class="eb">Their archetype</span><span class="ti">{arch_b_name}, the deeper read for Number {b}</span></a>
      <a href="/numerology-love-styles#number-{a}" class="seo-rel-card"><span class="eb">Number {a}</span><span class="ti">Number {a} in Love · {love_a}</span></a>
      <a href="/numerology-love-styles#number-{b}" class="seo-rel-card"><span class="eb">Number {b}</span><span class="ti">Number {b} in Love · {love_b}</span></a>
      <a href="/life-path-number-{a}-meaning" class="seo-rel-card"><span class="eb">Life Path {a}</span><span class="ti">Life Path Number {a} · {pa}</span></a>
      <a href="/life-path-number-{b}-meaning" class="seo-rel-card"><span class="eb">Life Path {b}</span><span class="ti">Life Path Number {b} · {pb}</span></a>
      <a href="/love-compatibility-numerology" class="seo-rel-card"><span class="eb">Compatibility</span><span class="ti">Free Chaldean compatibility check</span></a>
      <a href="/ask-aura" class="seo-rel-card"><span class="eb">Ask Aura</span><span class="ti">Ask Aura about your relationship</span></a>
      </div>
    </section>

  </main>


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


</div>




<!-- NA_RELATED_INSIGHTS_START -->
<section class="na-related-insights" aria-labelledby="na-related-title">
  <div class="na-related-inner">
    <div class="na-related-kicker">Continue the pattern</div>
    <h2 id="na-related-title">Related relationship insights</h2>
    <p>After reading this pair, it helps to look at each person separately, then come back to the relationship as a living dynamic rather than a fixed verdict.</p>
    <div class="na-related-grid">
      <a class="na-related-card" href="/love-compatibility-numerology"><span>Use both names and birth dates</span><strong>Read your own relationship dynamic</strong></a>
      <a class="na-related-card" href="/blog/relationship-compatibility-numerology"><span>The relationship framework behind the score</span><strong>How compatibility scoring works</strong></a>
      <a class="na-related-card" href="/number/{a}-personality"><span>{pa} side of the match</span><strong>Number {a} personality pattern</strong></a>
      <a class="na-related-card" href="/number/{b}-personality"><span>{pb} side of the match</span><strong>Number {b} personality pattern</strong></a>
      <a class="na-related-card" href="/numerology-love-styles#number-{a}"><span>How this side bonds</span><strong>Number {a} in love</strong></a>
      <a class="na-related-card" href="/numerology-love-styles#number-{b}"><span>How this side bonds</span><strong>Number {b} in love</strong></a>
      <a class="na-related-card" href="/numerology-and-overthinking#number-{a}"><span>What pressure can trigger</span><strong>Number {a} stress pattern</strong></a>
      <a class="na-related-card" href="/numerology-and-overthinking#number-{b}"><span>What pressure can trigger</span><strong>Number {b} stress pattern</strong></a>
      <a class="na-related-card" href="/numerology-love-styles"><span>All nine love styles and the full matrix</span><strong>Compare every pairing at once</strong></a>
      <a class="na-related-card" href="/report"><span>Personalised PDF context</span><strong>See compatibility inside a full report</strong></a>
      <a class="na-related-card" href="/analyzer"><span>Start with your full number map</span><strong>Run your free Chaldean analysis</strong></a>
      <a class="na-related-card" href="/ask-aura"><span>Turn the insight into a conversation</span><strong>Ask Aura a personal follow-up</strong></a>
    </div>
  </div>
</section>
<!-- NA_RELATED_INSIGHTS_END -->

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div><div class="footer-brand">☽ NameAligned.com</div><p class="footer-tagline">Free Chaldean numerology for everyone.</p></div>
      <div><div class="footer-col-title">Free Tools</div><ul class="footer-links"><li><a href="/name-numerology-calculator">Name Calculator</a></li><li><a href="/name-correction-numerology">Name Correction</a></li><li><a href="/business-name-numerology">Business Name</a></li><li><a href="/love-compatibility-numerology">Love Compatibility</a></li><li><a href="/ask-aura">Ask Aura</a></li><li><a href="/report">Full Report $2.50 / ₹249 · 50% off</a></li></ul></div>
      <div><div class="footer-col-title">Guides</div><ul class="footer-links"><li><a href="/blog/chaldean-numerology-guide">Chaldean Guide</a></li><li><a href="/blog/moolank-meanings">Birth Number Meanings</a></li><li><a href="/blog/personal-year-guide">Personal Year</a></li><li><a href="/blog/name-correction-guide">Name Correction</a></li><li><a href="/blog/compound-numbers-cheiro">Compound Numbers</a></li><li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid</a></li></ul></div>
      <div><div class="footer-col-title">More</div><ul class="footer-links"><li><a href="/blog">All Articles</a></li><li><a href="/about">About</a></li><li><a href="/sitemap-pages">Site Map</a></li><li><a href="/privacy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/refund">Refund</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 NameAligned.com</span><span>Made with <span style="color:#e8526b;">❤</span> in India</span></div>
  </div>
</footer>



<script src="/assets/emotional-insights.js" defer></script>
<script src="/assets/share-helpers.js" defer></script>
</body></html>
"""


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def jstr(s):
    """JSON string body: strip tags, unescape entities, escape quotes."""
    return html.unescape(strip_tags(s)).replace('"', '\\"')


def build(a, b, d):
    pa, pb = PLANET[a], PLANET[b]
    url = f"https://www.namealigned.com/number-{a}-and-{b}-compatibility"
    title = f"Number {a} and {b} Compatibility: {pa} and {pb}"
    og = f"https://www.namealigned.com/assets/og/moolank-{a}.jpg"
    keywords = ", ".join([
        f"number {a} and {b} compatibility", f"{a} {b} compatibility",
        f"moolank {a} {b} compatibility", f"life path {a} and {b}",
        f"{pa.lower()} {pb.lower()} compatibility",
        "chaldean numerology compatibility",
        f"number {a} number {b} marriage",
    ])
    article_ld = (
        '{"@context": "https://schema.org", "@type": "Article", "headline": '
        f'"Number {a} and {b} Compatibility ({pa} &amp; {pb}) \u00b7 Chaldean Numerology", '
        f'"description": "{jstr(d["desc"])}", "url": "{url}", '
        '"datePublished": "2026-08-29", "dateModified": "2026-08-29", '
        '"author": {"@type": "Organization", "name": "NameAligned.com", "url": "https://www.namealigned.com/"}, '
        '"publisher": {"@type": "Organization", "name": "NameAligned.com", "url": "https://www.namealigned.com/", '
        '"logo": {"@type": "ImageObject", "url": "https://www.namealigned.com/assets/namealigned-logo-full.svg"}}, '
        f'"inLanguage": "en-IN", "mainEntityOfPage": {{"@type": "WebPage", "@id": "{url}"}}}}'
    )
    breadcrumb_ld = (
        '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ['
        '{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.namealigned.com/"}, '
        '{"@type": "ListItem", "position": 2, "name": "Numerology Guides", "item": "https://www.namealigned.com/sitemap-pages"}, '
        f'{{"@type": "ListItem", "position": 3, "name": "Number {a} &amp; {b} Compatibility", "item": "{url}"}}]}}'
    )
    faq_items = ", ".join(
        '{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}'
        % (jstr(q), jstr(ans)) for q, ans in d["faqs"])
    faq_ld = ('{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ['
              + faq_items + "]}")
    faq_html = "\n".join(
        f"    <details><summary>{q}</summary><p>{ans}</p></details>"
        for q, ans in d["faqs"])
    quick = "\n".join(f"      <li>{x}</li>" for x in d["quick"])

    return TEMPLATE.format(
        a=a, b=b, pa=pa, pb=pb, ga=GLYPH[a], gb=GLYPH[b],
        title=title, desc=d["desc"], keywords=keywords, url=url, og=og,
        article_ld=article_ld, breadcrumb_ld=breadcrumb_ld, faq_ld=faq_ld,
        tag=d["tag"], intro=d["intro"], lede=d["lede"],
        works_h2=d["works_h2"], works=d["works"],
        watch_h2=d["watch_h2"], watch=d["watch"],
        quick=quick, verdict=d["verdict"], verdict_para=d["verdict_para"],
        share=d["share"], faq_html=faq_html,
        arch_a=ARCH[a][0], arch_a_name=ARCH[a][1],
        arch_b=ARCH[b][0], arch_b_name=ARCH[b][1],
        love_a=LOVE_BLURB[a], love_b=LOVE_BLURB[b],
    )


def main():
    if not os.path.exists("vercel.json"):
        raise SystemExit("run this from the repo root")
    written = []
    for (a, b), d in sorted(PAIRS.items()):
        assert a < b, f"pair must be ordered low-high: {a}-{b}"
        path = f"number-{a}-and-{b}-compatibility.html"
        if os.path.exists(path):
            print(f"  SKIP {path} (already exists)")
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build(a, b, d))
        written.append(path)
        print(f"  wrote {path}  [{d['verdict']}]")
    print(f"\n{len(written)} pages written")


if __name__ == "__main__":
    main()
