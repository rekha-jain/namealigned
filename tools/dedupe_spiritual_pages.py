#!/usr/bin/env python3
"""Replace the boilerplate shared by all 9 number-N-spiritual-meaning pages.

Four paragraphs appeared verbatim on all nine pages (two in the "Is the
spiritual meaning fixed?" section, two as FAQ answers), driving 55% body
overlap. Each is replaced with prose specific to that number, grounded in the
essence / lesson / practice / shadow already described on the same page.

The two FAQ answers are duplicated into the FAQPage JSON-LD, so both copies are
updated together.

Run from the repo root:  python3 tools/dedupe_spiritual_pages.py
"""
import json
import os
import re

# Sentences that must not survive anywhere (the shared boilerplate).
BANNED = [
    "The vibration is fixed, what you do with it is not.",
    "The spiritual work is becoming conscious of which one you are running, and choosing.",
    "If you came to this page on a night when something felt unsettled or strangely sharp",
    "Reading the path back to yourself is often the first step.",
    'Every number is "lucky" when its path is consciously walked',
    "The opportunity is in becoming aware of the vibration, not in escaping it.",
    "You can, but the slope works against you.",
    "Most who try eventually return to the practice that matches their vibration",
]

C = {
 1: dict(
  fixed_a="Nobody is issued a different Sun. What differs is how it gets carried, and the same Number 1 vibration produces strikingly different lives. Two people born to the same Sun-led path can look nothing alike: one spends decades waiting for an institution to confirm what they already sense and calls that humility, while the other learns to move on their own authority and discovers the confirmation was never going to arrive. Number 1 is unusual in that nobody else can grant you this. The path only opens when you stop asking for permission to walk it.",
  fixed_b="If you arrived here restless, or with the particular loneliness of seeing something before anyone around you sees it, that is the Sun-led signature rather than a mood. Number 1 tends to recognise itself in plain description more readily than in doctrine, because doctrine arrives pre-approved by someone else. Naming the pattern is usually where the work starts.",
  lucky="Number 1 is fortunate in a specific and demanding way: it gets first sight of things. Walked consciously that becomes genuine initiative, and the luck looks obvious in hindsight. Run unconsciously it becomes certainty without examination, which is the same gift turned into a liability. The Sun does not make the path easy, it makes it yours.",
  other="You can, and Number 1 will often try, usually by submitting to a lineage in the hope that someone else's structure will settle the question of authority. It rarely holds. Sun-led souls tend to leave the tradition and keep the fragment of it that actually worked, which is the more honest outcome anyway. Fifteen deliberate minutes alone each morning will do more here than a decade inside a system that requires you to defer.",
  means="It means your soul is running a Sun-led path: here to begin things, to see first, and to build an authority that comes from inner alignment rather than from anyone's permission. The essence is initiation, the lesson is sovereignty, and the shadow is mistaking your own certainty for universal truth.",
 ),
 2: dict(
  fixed_a="The Moon's pull is not negotiable. Whether there is a shoreline is. One Moon-led life is spent absorbing everyone else's weather until there is no reliable sense of where you end, and calling that love. Another is spent developing the same sensitivity into something accurate and unshakeable, so that you can feel a room completely and still know which feelings are yours. The raw capacity is identical in both. Only the boundary differs.",
  fixed_b="If you came here after a day of carrying something that was never yours to carry, that is the Moon-led pattern rather than a bad week. Number 2 recognises itself through feeling rather than argument, which is why plain language tends to land harder than doctrine. Noticing the pattern is usually the first genuine relief.",
  lucky="Number 2 is fortunate in the way water is fortunate: it reaches places nothing else can. Walked consciously, that becomes a rare capacity to be present to what is actually happening in a person. Run unconsciously, the same openness becomes absorption, and the gift exhausts its owner. The Moon asks for a shoreline, not a smaller ocean.",
  other="You can, though Moon-led souls tend to struggle inside practices built on force, striving or relentless self-examination, which frequently produce more turbulence than clarity. Most eventually drift back toward water, toward journaling at dawn or dusk, toward anything that lets the emotional body decompress rather than perform. That is not a lesser path. It is the one your vibration can actually sustain.",
  means="It means your soul is running a Moon-led path: here to feel, to reflect, and to hold emotional reality for others without dissolving into it. The essence is attunement, the lesson is receptivity without losing yourself, and the shadow is becoming a sponge rather than a clear mirror.",
 ),
 3: dict(
  fixed_a="Jupiter hands every Number 3 the same generosity. What varies enormously is what gets done with it. One Jupiter-led path collects teachers, traditions and frameworks for thirty years and arrives nowhere in particular, mistaking breadth for depth the whole way. Another commits to a single thing long enough for it to become genuinely known, and then has something real to give away. Both people are curious, generous and quick. Only one of them stayed.",
  fixed_b="If you arrived here mid-search, with several traditions already half-explored, that is the Jupiter-led signature rather than indecision. Number 3 recognises itself through language, which is both the gift and the trap, since a good description can feel like an arrival when it is only a signpost. Naming the pattern is useful precisely because it interrupts the collecting.",
  lucky="Number 3 is traditionally the most fortunate vibration in the system, and it is worth being precise about why. Jupiter opens doors generously, so opportunity genuinely does arrive more often. What Jupiter does not supply is the discipline to walk through one door and close the rest. Walked consciously the abundance becomes wisdom; run unconsciously it becomes a long, pleasant sampling of everything.",
  other="You can, more easily than most numbers, and that is exactly the difficulty. Jupiter adapts to almost any tradition well enough to feel at home, which means Number 3 can borrow indefinitely without ever committing. The question worth asking is not whether a path suits you but whether you have stayed with it long enough to be changed by it. Five minutes of daily expression inside one practice beats a year of intelligent visiting.",
  means="It means your soul is running a Jupiter-led path: here to expand, to teach, and to make the invisible visible through expression. The essence is wisdom shared, the lesson is discernment within abundance, and the shadow is the dilettante who knows a little of everything and commits to nothing.",
 ),
 4: dict(
  fixed_a="Rahu is never going to settle down, and this path does not ask it to. One Rahu-led path mistakes constant motion for progress, changing practice, teacher and city every eighteen months and never staying long enough to be altered by any of it. Another keeps the same disruptive intelligence but anchors it in something daily and unremarkable, and that combination is genuinely powerful. Rahu does not need to be slowed down. It needs something to hold on to while it moves.",
  fixed_b="If you came here having already left the tradition you were raised in, or drawn to something your family would not recognise as spiritual at all, that is the Rahu-led pattern rather than rebellion. Number 4 tends to recognise itself in descriptions that do not ask it to fit in. Seeing the pattern is often the first time the restlessness reads as direction.",
  lucky="Number 4 has a reputation for difficulty that the tradition partly earns and largely overstates. Rahu's function is disruption, and disruption is uncomfortable whether or not it is useful. Walked consciously, this is the vibration that breaks an inherited pattern nobody else in the family could break. Run unconsciously, it breaks things indiscriminately and calls the wreckage a search.",
  other="You can, and Number 4 usually will, since Rahu is drawn to precisely what it was not raised inside. The caution is different here than for other numbers: the risk is not that the borrowed path is wrong but that you will leave it before it has done anything. Embodied practice tends to hold Number 4 best, because the body cannot move as fast as the mind and will not let you skip ahead.",
  means="It means your soul is running a Rahu-led path: here to break inherited patterns, often through traditions your ancestors would not recognise. The essence is disruption in service of change, the lesson is staying grounded while everything reinvents, and the shadow is restlessness dressed up as seeking.",
 ),
 5: dict(
  fixed_a="Mercury runs at one speed for everyone born to it. The variable is not the speed but what gets kept. One Mercury-led life gathers spiritual information for decades without metabolising any of it, fluent in the vocabulary of five traditions and transformed by none. Another takes the same quick, translating mind and holds it still long enough for one practice to sink past the intellect. The difference is not intelligence, which is abundant either way. It is digestion.",
  fixed_b="If you arrived here already knowing roughly what the page would say, that recognition is the Mercury-led signature and also its central hazard. Number 5 understands things quickly enough to mistake understanding for change. The pattern is worth naming precisely because naming it is not the same as doing anything about it.",
  lucky="Number 5 is fortunate in adaptability: it fits almost anywhere, converses with almost anyone, and finds a way through most closed doors. Walked consciously, that becomes a genuine gift for translating between worlds that cannot otherwise hear each other. Run unconsciously, the same fluency becomes a way of never being anywhere long enough to be held to account.",
  other="You can, and you will be unusually good at it, which is the problem rather than the reassurance. Mercury can speak the language of any tradition within weeks and will often move on just as the difficult, unglamorous part begins. What Number 5 needs is not a better-matched path but a daily window with no input at all, where the mind digests instead of collecting.",
  means="It means your soul is running a Mercury-led path: here to move between worlds, to translate, and to keep asking the questions others have stopped asking. The essence is bridging, the lesson is depth within breadth, and the shadow is switching methods before any one of them has time to work.",
 ),
 6: dict(
  fixed_a="Venus gives every Number 6 the same access to beauty. It does not specify what the beauty is for. One Venus-led path uses beauty as an anaesthetic, arranging a life so pleasant that nothing difficult ever quite has to be faced, and calls the result peace. Another lets beauty do the harder thing it is capable of, which is opening you up rather than settling you down. The same candle, the same flowers, the same care. Entirely different outcomes.",
  fixed_b="If you came here from a day spent making things lovely for other people and feeling faintly unmet inside it, that is the Venus-led pattern rather than ingratitude. Number 6 recognises itself through the senses more readily than through argument, which is why abstract doctrine so often slides off. Naming the pattern usually lands somewhere physical first.",
  lucky="Number 6 is fortunate in access: Venus feels the sacred through art, food, music and intimacy, which means the divine is rarely far away or hard to reach. Walked consciously that is a genuine advantage over paths that require years of abstraction. Run unconsciously it becomes comfort mistaken for practice, and the very ease that was the gift becomes the reason nothing deepens.",
  other="You can, though Venus-led souls tend to find austere or body-denying practices quietly corrosive, since they treat as an obstacle the exact channel through which you actually perceive the sacred. Most return to something aesthetic and embodied. That is not indulgence or a lesser route. Lighting one candle with full attention is, for Number 6, a more serious practice than an hour of doctrine.",
  means="It means your soul is running a Venus-led path: here to find the sacred through beauty, love and the body rather than through abstraction. The essence is devotion, the lesson is loving without needing the loved thing to stay unchanged, and the shadow is mistaking comfort for spiritual practice.",
 ),
 7: dict(
  fixed_a="Ketu grants everyone on this path the same detachment. Whether that becomes freedom or an exit is not settled by the vibration itself. One Ketu-led path uses detachment as an exit, becoming impressively unbothered while quietly avoiding money, relationships and responsibility, and calls the avoidance liberation. Another holds the same capacity for stillness without letting it harden into distance from other people. Ketu is the most naturally spiritual vibration in the system, which is precisely why its shadow is the hardest to spot from inside.",
  fixed_b="If you came here already suspecting that most of what you are told about yourself is a layer rather than the thing underneath, that is the Ketu-led signature rather than cynicism. Number 7 tends to recognise itself in what a description leaves out. Naming the pattern is less a discovery than a confirmation of something long assumed.",
  lucky="Number 7 is fortunate in a way that does not resemble luck from outside. Ketu is the moksha karaka, and the vibration comes with unusual access to stillness and a native indifference to what most people spend their lives pursuing. Walked consciously that is a considerable head start. Run unconsciously it becomes spiritual bypassing, where the head start is spent avoiding the ordinary work.",
  other="You can, though Number 7 rarely needs to look far, since Ketu tends to arrive already oriented toward liberation. The greater risk is the opposite: retreating into practice so completely that the human obligations go unattended. If a borrowed path pulls you back toward relationships, money and responsibility, it may be doing more genuine work for you than another silent retreat.",
  means="It means your soul is running a Ketu-led path: here to remember what you already know, and to peel away the layers the world insists are you. The essence is liberation, the lesson is detachment that stays tender, and the shadow is using that detachment to bypass ordinary human work.",
 ),
 8: dict(
  fixed_a="Saturn's terms are identical for every Number 8: time, structure, consequence. What those terms produce across a lifetime is not identical at all. One Saturn-led path treats spiritual life as one more obligation, executes it faithfully for thirty years and arrives dutiful, competent and joyless. Another does exactly the same practice at the same hour and finds something quiet inside the repetition itself. Saturn will grant both people the discipline. It does not automatically supply the reason.",
  fixed_b="If you came here in the middle of a long stretch where the work has not visibly paid off, that is the Saturn-led pattern rather than evidence you chose wrong. Number 8 is the vibration most often mid-delay, and the delay is structural rather than personal. Naming it does not shorten it, but it does make it possible to keep going.",
  lucky="Number 8 carries the heaviest reputation in the system and the most misunderstood one. Saturn is the karma karaka: it does not withhold reward, it defers it, and it charges interest on shortcuts. Walked consciously, this is the vibration that builds the thing that outlasts everyone. Run unconsciously, it becomes grimness, and the discipline that was the gift turns into a sentence being served.",
  other="You can, though Saturn-led souls tend to fare badly inside practices built on intensity, novelty or rapid breakthrough, which promise a speed this vibration was never issued. Most return to something plain and repeatable. Twenty minutes at the same hour for ten years is not a modest version of the path for Number 8. It is the path.",
  means="It means your soul is running a Saturn-led path: here to learn through structure, time and consequence rather than sudden insight. The essence is durability, the lesson is faith inside the long delay, and the shadow is grimness that treats the whole thing as a duty.",
 ),
 9: dict(
  fixed_a="Mars issues the same quantity of fire to everyone here. It says nothing about where to point it. One Mars-led life burns through the very cause it meant to protect, along with several of the people standing near it, and calls the damage conviction. Another carries the same intensity and learns to aim it at the work instead of at whoever is obstructing the work. The heat is not the problem and never was. Nothing here is achieved by trying to feel less.",
  fixed_b="If you arrived here with something still hot from earlier today, an injustice you cannot put down or an anger you are not sure what to do with, that is the Mars-led pattern rather than a failure of composure. Number 9 recognises itself in directness. Naming the pattern tends to give the fire somewhere to go.",
  lucky="Number 9 is fortunate in force: Mars supplies the energy to actually do the thing, which is what most good intentions are missing. Walked consciously, the vibration matures from conqueror into protector, and the fire defends something worth defending. Run unconsciously, it becomes righteous anger that consumes its own cause and leaves the person exhausted and certain they were right.",
  other="You can, though Mars-led souls usually find purely contemplative practices quietly intolerable, since sitting still with this much energy tends to raise the temperature rather than lower it. Most return to something physical done with intention: running, climbing, building, dancing. For Number 9 the body in motion is not a warm-up for the practice. It is where the practice happens.",
  means="It means your soul is running a Mars-led path: here to fight for something larger than yourself, with the highest expression being the protector rather than the conqueror. The essence is courage in service, the lesson is anger transmuted into devotion, and the shadow is righteousness that burns the cause it meant to defend.",
 ),
}


def replace_para(s, marker, new, label):
    """Replace the <p> whose text starts with marker."""
    pat = re.compile(r'<p>\s*' + re.escape(marker) + r'.*?</p>', re.S)
    if not pat.search(s):
        raise SystemExit(f"  !! {label}: paragraph not found ({marker[:40]!r})")
    return pat.sub(lambda _: f"<p>{new}</p>", s, count=1)


def replace_faq(s, qfrag, new, label):
    """Replace the <details> answer whose summary contains qfrag."""
    pat = re.compile(
        r'(<details><summary>[^<]*' + re.escape(qfrag) + r'[^<]*</summary>\s*<p>).*?(</p>)', re.S)
    if not pat.search(s):
        raise SystemExit(f"  !! {label}: FAQ not found ({qfrag!r})")
    return pat.sub(lambda m: m.group(1) + new + m.group(2), s, count=1)


def update_faq_schema(s, mapping, label):
    """Rewrite matching answers inside the FAQPage JSON-LD."""
    blocks = list(re.finditer(
        r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)', s, re.S))
    for m in blocks:
        try:
            data = json.loads(m.group(2))
        except json.JSONDecodeError:
            continue
        if data.get("@type") != "FAQPage":
            continue
        hits = 0
        for qa in data.get("mainEntity", []):
            for frag, new in mapping.items():
                if frag in qa["name"]:
                    qa["acceptedAnswer"]["text"] = re.sub(r'<[^>]+>', '', new)
                    hits += 1
        if hits != len(mapping):
            raise SystemExit(f"  !! {label}: schema matched {hits}/{len(mapping)} questions")
        return s[:m.start(2)] + json.dumps(data, ensure_ascii=False) + s[m.end(2):]
    raise SystemExit(f"  !! {label}: no FAQPage schema found")


def main():
    if not os.path.exists("vercel.json"):
        raise SystemExit("run this from the repo root")
    for n in range(1, 10):
        f = f"number-{n}-spiritual-meaning.html"
        c = C[n]
        s = open(f, encoding="utf-8").read()
        s = replace_para(s, "The vibration is fixed, what you do with it is not.", c["fixed_a"], f)
        s = replace_para(s, "If you came to this page on a night", c["fixed_b"], f)
        s = replace_faq(s, "lucky spiritual number", c["lucky"], f)
        s = replace_faq(s, "spiritual path that is not natural", c["other"], f)
        s = replace_faq(s, "mean spiritually", c["means"], f)
        s = update_faq_schema(s, {
            "lucky spiritual number": c["lucky"],
            "spiritual path that is not natural": c["other"],
            "mean spiritually": c["means"],
        }, f)
        leftover = [b for b in BANNED if b in s]
        if leftover:
            raise SystemExit(f"  !! {f}: boilerplate survived: {leftover}")
        open(f, "w", encoding="utf-8").write(s)
        print(f"  rewrote {f}")
    print("\n9 pages de-duplicated")


if __name__ == "__main__":
    main()
