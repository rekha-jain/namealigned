#!/usr/bin/env python3
"""
Emotional long-tail SEO cluster.

Target: high-volume emotional / relationship search intent that does NOT
fit the existing numerology long-tails. Written in human, psychologically
believable voice. Each page links into the archetype hub at the bottom,
so SEO from these pages funnels into the engagement loop, but the body
of each page never mentions Chaldean numerology, ruling planet, or
moolank in the spine. The voice is the product.

Pages:
  /why-some-people-emotionally-withdraw
  /reassurance-needs-in-relationships
  /emotional-communication-styles
  /why-some-people-feel-too-much
  /the-emotionally-analytical-personality
  /conflict-styles-in-emotional-relationships
"""
import os
import json
from _seo_template import HEAD, NAV, FOOTER, BASE, make_article, make_breadcrumb, make_faq, jsonld

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


PAGES = [
    dict(
        slug='why-some-people-emotionally-withdraw',
        title='Why Some People Emotionally Withdraw When They Care Most',
        desc='Some people pull back exactly when the closeness matters most. A psychologically grounded read on emotional withdrawal, the patterns underneath, and what the people around them can actually do.',
        hero_h1='Why Some People Emotionally Withdraw When They Care Most',
        hero_tag='The retreat is rarely about distance. Read what is actually happening underneath.',
        archetype_match=7,  # The Inward Witness
        body_html='''
  <p>If you have ever watched someone you love go quiet on you, sometimes for hours, sometimes for days, you have probably already learned that the quiet is not always what it looks like. Withdrawal in the people who care most is rarely indifference. It is usually overload, or a learned protection, or a private way of metabolising something they cannot yet say out loud.</p>

  <h2>What emotional withdrawal actually is</h2>
  <p>Emotional withdrawal is the deliberate or instinctive turning-inward of someone who is processing. It is not the same as the silent treatment, which is a punishment with intent. Withdrawal is a state, not a strategy. The person inside it often does not know how long they will be there, or even why this particular thing tipped them in.</p>

  <p>The pattern shows up in introverts, in people who grew up in households where big emotions were unsafe, in people whose nervous systems run hotter than they show, and in people who learned early that their feelings became other people&rsquo;s problems if expressed out loud. Underneath the retreat is almost always not less feeling but more, more than the room could absorb, more than the moment could contain.</p>

  <h2>The three most common reasons it happens</h2>
  <p><strong>1. Capacity has run out.</strong> Some people can carry a stressful day, a difficult conversation, and the emotional temperature of the people around them, until they suddenly cannot. Withdrawal here is the body refusing to take in one more thing. It is rarely about you specifically; it is about cumulative load.</p>
  <p><strong>2. The thing being felt is too large to name yet.</strong> Some emotional states need solitude to find their shape before words. The person who needs to walk for an hour after a hard conversation is not punishing anyone. They are letting the feeling form into something they can later speak about. Interrupting that process tends to delay it, not shorten it.</p>
  <p><strong>3. A past pattern is activating.</strong> If someone learned in childhood that expressing distress made things worse, they may go silent in adult relationships at the moments distress builds, even with partners who are entirely safe. The pattern is not a judgement of the partner. It is older than the partner.</p>

  <h2>What the people around them can actually do</h2>
  <p>The most useful response is the least intuitive: do less, not more. The person withdrawing rarely needs more questions. They need an indication that you are not going to leave, and a sign that there is room to come back without performing or explaining. A short message, "take the time you need, I am here when you want", costs you nothing and removes the secondary stress of feeling pursued while already overwhelmed.</p>

  <p>If you are the one who withdraws, the most useful thing you can give a partner is a small piece of language they can hold during the silence. "I need a couple of hours, I am not upset with you, I will be back" lets the relationship breathe in the gap. Most withdrawers are not avoiding the conversation, they are avoiding the conversation arriving at the wrong moment. Naming the moment is half the work.</p>

  <h2>When withdrawal becomes a problem</h2>
  <p>Withdrawal becomes a problem when it is consistently used to avoid the conversation entirely, when the silence outlasts the trigger by days or weeks, when it becomes the default response to all stress and not just acute moments, or when the person re-emerges as if nothing happened and refuses to talk about what was unspoken. The pattern is workable when both people can name it. It corrodes silently when one or both pretend it does not exist.</p>
''',
        faqs=[
            ('Is emotional withdrawal the same as the silent treatment?',
             'No. The silent treatment is intentional, used to punish or coerce. Emotional withdrawal is a state, usually involuntary, more about the person\'s capacity than about you.'),
            ('How long should I wait before reaching out?',
             'Depends on the person. For someone who has shown the pattern before, give them the time they have historically needed plus a small buffer. A short message acknowledging the space (not asking them to come out of it) usually helps.'),
            ('Why does my partner withdraw when things are good?',
             'For some people, closeness itself activates the withdrawal pattern. Intimacy was unsafe at some earlier point in their life, and the body responds to closeness the way it once responded to risk. Naming the pattern out loud, gently, is usually the start of changing it.'),
            ('Can someone be taught not to withdraw?',
             'Not exactly. But they can learn to name the withdrawal, to leave one short message before going inward, and to come back faster. The pattern softens with awareness much more than with confrontation.'),
        ],
    ),

    dict(
        slug='reassurance-needs-in-relationships',
        title='Reassurance Needs in Relationships, What Each Person Actually Needs',
        desc='Some people need words. Some need consistency. Some need to be left to figure it out. A psychologically honest read on how different people receive reassurance, and why the wrong kind feels like nothing at all.',
        hero_h1='Why "I Love You" Isn\'t Always Enough Reassurance',
        hero_tag='Different people need different proofs. Sending the wrong kind feels, to them, like sending none at all.',
        archetype_match=2,  # The Mirror
        body_html='''
  <p>Most relationship friction blamed on "she needs too much reassurance" or "he is emotionally unavailable" is actually a translation problem. Two people, both genuinely caring, sending each other the wrong currency. He keeps depositing words, she keeps emptying out. She keeps showing up consistently, he keeps feeling she does not really love him. The love is real; the currency is wrong.</p>

  <h2>The four major reassurance languages</h2>
  <p><strong>1. Verbal reassurance.</strong> Some people genuinely need to hear it. "I love you" out loud, "I am not upset with you", "we are okay" said in words. These people receive love through language. Silence reads as a problem regardless of how warm the silence actually is.</p>
  <p><strong>2. Consistency reassurance.</strong> Some people do not need the words at all; what reassures them is that the small daily things keep happening. The morning text, the weekly Sunday call to their mother, the way you still load their plate first. Words are nice but they are not the proof. The proof is in the pattern.</p>
  <p><strong>3. Presence reassurance.</strong> Some people need physical proximity. Sit next to them on the bad day, even without speaking. Their body needs to feel yours nearby. Reassurance over text reaches them less than ten minutes of just being in the same room.</p>
  <p><strong>4. Initiative reassurance.</strong> Some people need to feel chosen, in real time. The unsolicited "thinking of you" text. The plan you made for the weekend without them having to ask. Being chased a little, not because they are insecure, but because effort is how they feel love is being practised, not just declared.</p>

  <h2>Why the wrong kind lands as nothing</h2>
  <p>If your partner needs verbal reassurance and you operate in consistency, you can show up perfectly for years and they will still feel quietly unmet. They are not ungrateful. They genuinely do not register the consistency as the message you intended. The currency you keep depositing is in a denomination they cannot spend.</p>
  <p>The reverse: if your partner is consistency-led and you keep saying "I love you" but forget the small daily things, the words land as performance. They hear them and feel less believed, not more. To them, words without the small actions are evidence the relationship has shifted into something that has to be said because it cannot be felt.</p>

  <h2>How to figure out what your partner actually needs</h2>
  <p>Ask. The conversation often goes: "When I last did something that made you feel really loved, what was it?" Specific, recent, concrete. The answer is usually data. If they remember a Sunday morning where you cancelled a meeting to be home, that is presence/initiative reassurance. If they remember the time you said "I want to grow old with you, and I mean that", that is verbal. If they remember the way you remembered, without prompting, that their dad was having surgery, that is consistency.</p>
  <p>Most people are some blend, but one of the four is usually dominant. Once you know what your partner&rsquo;s dominant currency is, you can stop spending the wrong one and feel less unappreciated yourself.</p>

  <h2>What to do when both of you are running low</h2>
  <p>The trickiest version of this is when neither of you has the energy to send any reassurance because both of you are quietly waiting to receive some. The fix is rarely fairness. It is usually one of you saying out loud, "I know we are both empty, but I am going to start." A small, deliberate act in your partner&rsquo;s primary currency, even when you do not feel like giving it, almost always restarts the loop. The fairness rebalances over the next week. Insisting on fairness in the moment usually does not.</p>
''',
        faqs=[
            ('How do I know which reassurance language my partner needs?',
             'Ask them to remember the last specific moment they felt deeply loved by you. The shape of the moment usually reveals their primary currency.'),
            ('Is needing reassurance the same as being insecure?',
             'No. Everyone needs reassurance; people just need different KINDS of it. Insecurity is when the same reassurance keeps being given but never lands, which usually means it is in the wrong currency.'),
            ('What if my partner needs verbal reassurance but I am not a words person?',
             'You can learn the words. One specific phrase your partner needs, said twice a week, often closes the gap. You do not have to become poetic; you have to become consistent in the one form they read as love.'),
            ('Can the dominant currency change over time?',
             'Yes, especially around big life events. A consistency-led partner becomes verbal during a stressful phase. A verbal partner becomes presence-led during grief. The conversation is worth having again every couple of years.'),
        ],
    ),

    dict(
        slug='emotional-communication-styles',
        title='The Five Emotional Communication Styles, And Why Most Fights Are Translation Errors',
        desc='Some people talk fast, some pause, some need to write it down before they can say it. The five emotional communication styles, how they collide in relationships, and what to do when yours does not match theirs.',
        hero_h1='Why Most Fights Are Actually Translation Errors',
        hero_tag='Five different ways of putting feelings into words. When two styles collide, the conversation goes sideways before either person says what they meant.',
        archetype_match=3,  # The Translator
        body_html='''
  <p>Most conflicts in relationships are not about the surface thing. They are about the way the surface thing was said. He raised his voice and she heard contempt; he meant urgency. She took a long pause and he heard rejection; she was just thinking. The content was fine. The transmission failed.</p>

  <h2>The five styles, in plain language</h2>
  <p><strong>1. Direct-fast.</strong> Says it plainly, says it now. Short sentences. Volume matches stakes. This style reads tone-softening as evasion. Most useful in crises, least gentle in everyday life. Receives indirect communication as confusing or manipulative.</p>
  <p><strong>2. Direct-warm.</strong> Says it plainly but cushioned. "I want to tell you something, and I am saying it because I love you, not because I am angry." Longer setup, same content as direct-fast underneath. Reads direct-fast as harsh and indirect styles as evasive. Often the highest-investment style to sustain because every conversation includes the relational frame.</p>
  <p><strong>3. Reflective-pause.</strong> Needs silence before words. Hears the question, goes inward, comes back with the answer twenty minutes or twenty hours later. This style is not stalling. The silence is the processing. Reads direct-fast styles as overwhelming and direct-warm styles as exhausting in their constant framing.</p>
  <p><strong>4. Written-first.</strong> Cannot find the words in real time but can write them. The text message you send to your partner from the next room is not avoidance; it is how the truth actually arrives for some people. Reads expectations of live conversation as pressure, not intimacy.</p>
  <p><strong>5. Indirect-layered.</strong> Communicates feeling through tone, atmosphere, the way the kitchen looks, the way the door closes. This is not passive aggression unless used punitively. For some people the indirect is genuinely how they speak. The content is in the room before it is in the sentence.</p>

  <h2>When two styles collide</h2>
  <p>Most relationship friction is between two specific style pairings. Direct-fast meeting reflective-pause produces "why won&rsquo;t you just answer me" against "why are you pressuring me before I have thought". Direct-warm meeting written-first produces "we should have this conversation face to face" against "I cannot find the words when I am in front of you, please read this". Both people are trying. Neither knows the other&rsquo;s native language.</p>

  <h2>The bridge</h2>
  <p>The only thing that actually works is for both people to name their style out loud, once, and then refer to it in real time when conversations start to wobble. "I know I am being direct-fast right now, take your time, I will wait." "I am going to write this down because I cannot find the words live, will you read it?" The naming itself does most of the work. It removes the misreading of intent that was driving the heat.</p>

  <h2>Why this is harder than it sounds</h2>
  <p>Most people think their style is the universal correct one and other styles are dysfunctions. The reflective-pause person thinks direct-fast people are aggressive. The direct-fast person thinks reflective-pause people are checked out. The written-first person thinks people who insist on live conversation are imposing their own discomfort. Each style has a moral story about itself that flatters its native shape and pathologises others.</p>
  <p>Real partnership in adulthood usually requires learning to use a style that is not your default, at least sometimes, with the people who need it. It is the unsexy work most relationships avoid until they cannot avoid it any more.</p>
''',
        faqs=[
            ('How do I figure out my own communication style?',
             'Notice what you do in a moderately hard conversation. Do you speak immediately, take a pause, want to write it down first, soften everything in a frame, or convey it through tone? Most people are one dominant style with one secondary.'),
            ('Can two people with different styles work?',
             'Yes, and most lasting partnerships are exactly that. The work is naming the styles out loud and stretching toward each other in small ways, not converting the other person to yours.'),
            ('What if my partner refuses to name their style?',
             'Start by naming yours, repeatedly, in moments of calm. "I am about to say something the direct-fast way, just so you know." Modelling tends to slowly invite the same from the other person.'),
            ('Is indirect-layered just passive aggression?',
             'No, although it can become that if used punitively. For some people indirectness is genuinely their native register, and reading the room is how they communicate emotional information. The line between indirect-layered and passive-aggressive is intent, not form.'),
        ],
    ),

    dict(
        slug='why-some-people-feel-too-much',
        title='Why Some People Feel Too Much, And Why It Is Not a Weakness',
        desc='Some people register emotional information at a frequency most do not. A psychologically honest read on what high-feeling people actually carry, why it can feel like a burden, and why it is often the most useful person in the room.',
        hero_h1='Why Some People Feel Too Much',
        hero_tag='You are not too sensitive. You are running a perception system most people are not running.',
        archetype_match=2,  # The Mirror
        body_html='''
  <p>If you have ever been told you are too sensitive, you probably remember the exact tone of voice. It usually came from someone who could not feel what you were feeling and therefore concluded the feeling was the problem. The conclusion was wrong. The feeling was not the problem. The frequency was just different from theirs.</p>

  <h2>What "feels too much" actually is</h2>
  <p>Some people register emotional information the way some people register physical pain: at a higher amplitude than the people around them. They walk into a room and pick up tension that the others present have already filtered out. They read a text and feel the small word that does not belong. They sit in a meeting and notice the moment one person stopped engaging, even if no one else did.</p>
  <p>This is not weakness. This is a perception system tuned higher than the human default. In some lives, it is the central professional asset, in therapy, in design, in writing, in caregiving, in leadership when the room is unwell. In other lives, it is an exhausting tax that the world keeps refusing to value.</p>

  <h2>What it costs</h2>
  <p>You take other people&rsquo;s moods home with you. You replay conversations late at night, finishing the parts you could not say out loud. You absorb the temperature of a room before you have decided to. You apologise for being emotional, then quietly notice no one else apologises for being cold. Your boundaries are harder to enforce than other people&rsquo;s because you can feel the cost on the other side of saying no.</p>
  <p>You confuse care with self-care more often than you realise. You smooth other people&rsquo;s rough edges and quietly carry your own. Your peace is harder won than other people understand. You protect it because you had to build it.</p>

  <h2>Why it is not a weakness</h2>
  <p>The same antenna that picks up the tense room is also the antenna that lets you parent skilfully, write something a stranger reads and feels less alone with, hold a friend through a hard week, build a team that people actually want to stay in, or see the truth in a situation before it has the language. The cost is real. The value is also real. Most cultures undervalue it because it does not show up in spreadsheets. That does not mean it is not generating value. It means the spreadsheet is incomplete.</p>

  <h2>What helps</h2>
  <p>Three things consistently help high-feeling people. First, a daily decompression ritual: water, walking, journaling, music with no lyrics, anything that lets the day&rsquo;s collected weight discharge before bed. Without it the load just compounds. Second, a small circle of people who do not require you to translate your inner life into something more palatable; one or two real ones are enough. Third, the practice of saying the harder thing out loud, before it has been carried for a month. The thing held in the body too long always costs more than the thing said in the moment.</p>

  <h2>The line you were probably waiting for</h2>
  <p>You are not too much. You are calibrated for a world that mostly has not yet learned to use what you can read. Find the rooms where what you carry is the value, not the inconvenience. They exist. You will know them by how much less you have to translate yourself in them.</p>
''',
        faqs=[
            ('Is being a high-feeling person the same as being an empath?',
             'They overlap but are not identical. Empath is a popular term for someone whose sensitivity is primarily attuned to other people. Some high-feeling people are highly attuned to other people; others are attuned to atmosphere, music, beauty, injustice, ideas. The common factor is amplitude, not direction.'),
            ('Can I learn to feel less?',
             'You can learn to manage what you feel, and to discharge it daily so it does not compound. You probably cannot reduce the input itself, and over time most high-feeling people stop wanting to.'),
            ('Why do people call me too much?',
             'Often because your accurate read of a situation is making them uncomfortable, and "too much" is the easier conclusion than "they may be right". The label tells you more about their capacity than about your scale.'),
            ('How do I find people who can hold what I carry?',
             'They tend to be people who do not need to fix what you feel. The friend who can sit with your sadness without immediately offering solutions, the partner who does not flinch when you say a hard thing, the colleague who does not get smaller when you get bigger. Look for steadiness, not similarity.'),
        ],
    ),

    dict(
        slug='the-emotionally-analytical-personality',
        title='The Emotionally Analytical Personality, When You Think Your Way Through Feelings',
        desc='Some people process emotion through structure, words, framework, and analysis. A psychologically honest read on what that costs, what it gives, and how to be emotionally analytical without numbing yourself.',
        hero_h1='When You Think Your Way Through Feelings',
        hero_tag='You analyse not because you feel less, but because the analysis is how you stay safe enough to feel at all.',
        archetype_match=4,  # The Quiet Disruptor
        body_html='''
  <p>If you are someone who reaches for a framework when something hard happens, who reads the right book during the breakup, who can describe your emotional patterns with academic precision but cannot quite metabolise them in the moment, you have probably been told at some point that you "live too much in your head". That description is right and incomplete. You live in your head because that is where the safe room is. The cost is that the safe room is also where the feelings cannot fully complete.</p>

  <h2>What it actually means to be emotionally analytical</h2>
  <p>It means you process feeling through structure. You make sense of your inner life by mapping it: this is the anxiety pattern, this is the family-of-origin script, this is the avoidant style activating, this is the third-time-this-month I have felt this exact shape. The mapping is genuinely useful. It is also a way of holding the feeling at a slight distance, where it is observable and therefore less overwhelming.</p>
  <p>This style runs strongest in people who learned early that big feelings were unsafe or unwelcome. Analysis became the survival technology. The framework was the way to keep functioning. Many of the most thoughtful people you know operate this way. So do most therapists, in case that helps.</p>

  <h2>What it gives you</h2>
  <p>You catch your own patterns faster than most people catch theirs. You can articulate emotional dynamics other people only sense vaguely. You make excellent strategic decisions in moments where others are flooded. You can hold someone else&rsquo;s emotional reality without merging with it, which makes you a useful friend in a crisis. You read books about how people work and remember the frameworks years later.</p>

  <h2>What it costs</h2>
  <p>The feeling rarely fully arrives. You skip over the part where the body actually metabolises the grief, the joy, the anger. The framework moves you past the experience faster than the experience wanted to last. You can describe your sadness in great detail without ever quite letting it sit in your chest and breathe. Over time this catches up. The unmetabolised emotion compounds into something heavier than the original feelings would have been.</p>
  <p>Relationships become harder than they should be. Partners who are emotionally direct can find the analytical style cold or clinical, even when you are deeply moved. You may give them a framework when they wanted comfort. You may describe the dynamic when they wanted to be held in it.</p>

  <h2>What helps</h2>
  <p>Three slow shifts. First, give yourself a ten-minute window after a hard moment where you are not allowed to analyse, only to feel. The body needs the time. The framework can come later. Second, practice answering "how are you feeling" with a single feeling word and a stop, instead of a paragraph about your meta-relationship with the feeling. The brevity forces presence. Third, find a practice that is not analytical, music played slowly, water, walks without a podcast, anything where the mind is occupied without being asked to think. The mind needs to be tired before the body can rise.</p>

  <p>You do not need to stop being analytical. You need to add the felt experience back in alongside it, so the framework has something to map onto. The frameworks are not the problem. The frameworks without the felt life underneath are.</p>
''',
        faqs=[
            ('Is being emotionally analytical the same as being detached?',
             'Not quite. Detached people genuinely feel less. Emotionally analytical people often feel a great deal but hold it at a slight distance so they can stay functional. The feelings are there; they are just being mediated.'),
            ('Is it bad to use frameworks for my own emotions?',
             'No. The frameworks are useful. The risk is that they replace the felt experience entirely. The healthiest version is framework PLUS feeling, not framework instead of feeling.'),
            ('Why do my partners say I am cold when I do not feel cold?',
             'Because the moment you reach for the framework, they read the reaching as distance. The framework is your way of staying engaged; to them it can look like exiting. Naming this out loud helps a lot.'),
            ('Can I become less analytical?',
             'You probably do not want to. You want to ADD the felt experience back in alongside the analysis. The analytical style is a real asset; it just needs the body alongside it.'),
        ],
    ),

    dict(
        slug='conflict-styles-in-emotional-relationships',
        title='Conflict Styles in Emotional Relationships, And Which Ones Heal',
        desc='Some couples fight loud. Some go silent. Some write it down. A psychologically grounded read on the four conflict styles, which ones repair the relationship and which ones quietly erode it.',
        hero_h1='Not All Conflict Damages a Relationship',
        hero_tag='Some kinds of fight heal what they touch. Others quietly corrode. Which one are you in.',
        archetype_match=9,  # The Protector
        body_html='''
  <p>One of the most useful things to know about your relationship is which kind of conflict you have. Most people lump all fighting together as "we argue too much" or "we never argue". But the form the conflict takes matters more than the frequency. Some couples fight loudly twice a week and stay deeply in love for fifty years. Other couples never raise their voices and quietly grow into strangers. The difference is the style.</p>

  <h2>The four major conflict styles</h2>
  <p><strong>1. Direct-resolution.</strong> Both partners can name the issue out loud, sit with it for thirty minutes, find some version of repair, and move on. Voices may rise. Words may sting. But there is a beginning, a middle, and an end. The relationship is the same shape afterward, often slightly stronger. This is the style most marriage researchers consider healthy.</p>
  <p><strong>2. Avoidant-deferral.</strong> Both partners detect the issue but neither raises it. Days pass. The unsaid thing sits between them. It does not disappear; it gets metabolised slowly through small distances, slightly less touch, slightly fewer plans, slightly more polite conversation. The relationship does not break, but it slowly cools. This style is the most common cause of long marriages where the love quietly went somewhere else.</p>
  <p><strong>3. Volatile-cyclical.</strong> Both partners raise the issue but the conversation never lands at repair. Voices rise, accusations get filed, one person walks out, the next day everyone is polite and tense, and within ten days the same fight returns wearing slightly different clothes. The conflict is loud but not resolutive. The relationship runs hot and feels alive, but the same wound keeps reopening because it never quite closes.</p>
  <p><strong>4. Pursuer-distancer.</strong> One person needs to talk it through right now. The other needs space to process. Both are valid, but if they cannot find each other&rsquo;s rhythm, the pursuer escalates and the distancer retreats further, and the relationship&rsquo;s baseline shifts toward one person always chasing and the other always shrinking. Over years, the chasing tires; the shrinking calcifies.</p>

  <h2>Which ones heal</h2>
  <p>Direct-resolution heals because the issue is closed and the relationship returns to baseline. Volatile-cyclical and pursuer-distancer can both become resolutive if the couple learns to slow down, name the pattern out loud, and add the missing piece. Volatile-cyclical needs a repair step. Pursuer-distancer needs both partners to meet in a middle pace neither finds entirely comfortable.</p>
  <p>Avoidant-deferral is the only style that almost never heals on its own. The conflict goes silent, but the relationship slowly fades. Most people leaving long marriages do not point at a specific fight, they point at "we just stopped trying". The fight that was never had is what stopped them.</p>

  <h2>What changes the style</h2>
  <p>Most people inherit their conflict style from the home they grew up in. The volatile-cyclical adult was raised in a volatile-cyclical home. The avoidant-deferral adult had parents who never argued or never made up. The pursuer learned that escalation eventually got the other person&rsquo;s attention. The distancer learned that disappearing was the safest response. The patterns are old, but they are not fixed.</p>
  <p>What changes them is the slow, deliberate practice of new responses inside the same triggers. The volatile-cyclical partner who learns to say "I am about to escalate, I need fifteen minutes" instead of escalating. The avoidant-deferral partner who learns to say "there is something I have been not saying for two weeks, can we sit with it now" instead of letting another two weeks pass. The pursuer who learns to wait until the distancer is back in the room before opening the conversation. None of these are dramatic. All of them, repeated, change the shape of the relationship.</p>

  <h2>The one question worth asking</h2>
  <p>Pick a recent fight. Did you both end up understanding each other better afterward, even slightly, even imperfectly. If yes, the style is workable. If the answer is "we just stopped fighting and pretended it was fine", the relationship is in slow decline whether or not it feels like it today.</p>
''',
        faqs=[
            ('Is conflict bad for a relationship?',
             'Direct-resolution conflict is one of the strongest predictors of a healthy long-term relationship. Avoided conflict is one of the strongest predictors of slow decline. The form matters more than the frequency.'),
            ('How do we change a long-running pattern?',
             'Slowly, with awareness. Name the pattern out loud when you see it starting, even mid-fight. "We are doing the thing again, can we slow down." Most couples cannot change the pattern without first naming it.'),
            ('What if my partner refuses to engage in conflict?',
             'You probably cannot force them to. What you can do is be the one who keeps gently raising the unsaid things and modelling the repair. Sometimes that slowly invites the same from them. Sometimes it surfaces that the relationship is in a deeper kind of trouble that requires outside help.'),
            ('Can a volatile-cyclical relationship heal?',
             'Yes, with practice. The missing piece is almost always the repair step at the end. Adding it deliberately, even when neither partner feels like it, changes the cycle over a few months.'),
        ],
    ),
]


N_TO_ARCHETYPE = {
    1: ('the-inner-sovereign', 'The Inner Sovereign'),
    2: ('the-mirror', 'The Mirror'),
    3: ('the-translator', 'The Translator'),
    4: ('the-quiet-disruptor', 'The Quiet Disruptor'),
    5: ('the-restless-mind', 'The Restless Mind'),
    6: ('the-devoted-beautifier', 'The Devoted Beautifier'),
    7: ('the-inward-witness', 'The Inward Witness'),
    8: ('the-patient-builder', 'The Patient Builder'),
    9: ('the-protector', 'The Protector'),
}


def render(p):
    slug = p['slug']
    canon = f'{BASE}/{slug}'
    title = p['title']
    desc  = p['desc']
    og_desc = desc[:160]

    article = make_article(title, desc, canon)
    breadcrumb = make_breadcrumb(p['hero_h1'][:60], canon)
    faqs = p['faqs']
    faq_dict = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs
    ]}
    aj, bj, fj = jsonld(article, breadcrumb, faq_dict)

    head = HEAD.format(
        n=1, title=title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        keywords=f'{slug.replace("-"," ")}, emotional patterns, relationship dynamics, psychological reading, namealigned',
        article_json=aj, breadcrumb_json=bj, faq_json=fj,
    )

    archetype_n = p['archetype_match']
    a_slug, a_name = N_TO_ARCHETYPE[archetype_n]

    faq_html = '\n'.join(
        f'        <details><summary>{q}</summary><p>{a}</p></details>'
        for q, a in faqs
    )

    body = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">&rsaquo;</span>
  <a href="/emotional-archetypes">Emotional Reading</a> <span style="margin:0 8px;">&rsaquo;</span>
  <span style="color:var(--text2);">{p['hero_h1'][:60]}</span>
</nav>

<link rel="stylesheet" href="/assets/emotional-insights.css"/>

<header class="seo-hero">
  <div class="container">
    <div class="badge">Emotional Pattern</div>
    <h1>{p['hero_h1']}</h1>
    <div class="tag">{p['hero_tag']}</div>
  </div>
</header>

<div class="seo-wrap">
  <main class="seo-body">

{p['body_html']}

    <div class="share-strip"
         data-share-source="emotional-cluster-{slug}"
         data-emotion-headline="Send this to someone who needs to read it."
         data-emotion-prompt="Ask them which paragraph hit. The conversation usually goes somewhere real from there."
         data-share-text="{p['hero_h1']}, this is the read I needed:"
         data-share-url="{canon}"></div>

    <h2>Frequently asked</h2>
    <div class="seo-faq">
{faq_html}
    </div>

    <section class="seo-related">
      <h2>Continue exploring</h2>
      <div class="seo-related-grid">
        <a href="/emotional-archetype-{a_slug}" class="seo-rel-card" data-na-event="archetype_viewed" data-na-params='{{"archetype":"{a_slug}","number":{archetype_n},"from":"{slug}"}}'><span class="eb">Related Archetype</span><span class="ti">{a_name}, the deeper read</span></a>
        <a href="/emotional-archetypes" class="seo-rel-card" data-na-event="related_insight_clicked"><span class="eb">Hub</span><span class="ti">All 9 emotional archetypes</span></a>
        <a href="/love-compatibility-numerology" class="seo-rel-card" data-na-event="compatibility_started" data-na-params='{{"source":"{slug}"}}'><span class="eb">Compatibility</span><span class="ti">Read the dynamic between two people</span></a>
        <a href="/analyzer" class="seo-rel-card" data-na-event="analyzer_started" data-na-params='{{"source":"{slug}"}}'><span class="eb">Free Analysis</span><span class="ti">Find your own emotional pattern</span></a>
        <a href="/ask-aura" class="seo-rel-card" data-na-event="related_insight_clicked"><span class="eb">Ask Aura</span><span class="ti">Talk to a reflective companion</span></a>
        <a href="/report" class="seo-rel-card" data-na-event="report_clicked"><span class="eb">Full Report</span><span class="ti">All of this, deeper, in a PDF</span></a>
      </div>
    </section>

  </main>

  <aside class="seo-aside">
    <div class="article-sidebar">
      <div class="eyebrow">Free Analysis</div>
      <h3>Find your emotional pattern</h3>
      <p>Enter your name and birth date, see your emotional archetype + the patterns underneath.</p>
      <a href="/analyzer" class="cta" data-na-event="analyzer_started" data-na-params='{{"source":"{slug}-sidebar"}}'>Start free &rarr;</a>
      <a href="/love-compatibility-numerology" class="cta outline" data-na-event="compatibility_started">Read a relationship</a>
      <div class="sep"></div>
      <div class="eyebrow">Full Destiny Report</div>
      <h3>Personalised PDF</h3>
      <div class="price-row"><span class="price-inr">INR 499</span><span class="price-usd">or $5 USD</span></div>
      <p>Complete chart, name corrections, compatibility map, 5-year forecast.</p>
      <a href="/report" class="cta" data-na-event="report_clicked" data-na-params='{{"source":"{slug}-sidebar"}}'>Get the report &rarr;</a>
    </div>
  </aside>
</div>

<script src="/assets/emotional-insights.js" defer></script>
<script src="/assets/share-helpers.js" defer></script>
<script src="/assets/analytics.js" defer></script>

{FOOTER}
'''
    return head + body


def build():
    for p in PAGES:
        html = render(p)
        path = os.path.join(OUT, f'{p["slug"]}.html')
        with open(path, 'w') as fh: fh.write(html)
        print(f'  wrote {p["slug"]}.html')
    print(f'\n{len(PAGES)} emotional long-tail pages built.')


if __name__ == '__main__':
    build()
