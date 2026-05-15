#!/usr/bin/env python3
"""
Build 4 E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
pages that Google increasingly weights for spiritual / numerology content:

  /methodology
  /how-it-works
  /ai-disclosure
  /sources

Each is a substantive content page (~600-1000 words) explaining the
underlying tradition, calculation, AI usage, and source material.
Same cosmic theme, same JSON-LD schema pattern as the rest of the site.
"""
import os
import json
from _seo_template import HEAD, NAV, FOOTER, BASE, make_article, make_breadcrumb, make_faq, jsonld

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def render(*, slug, title, desc, og_desc, crumb_label, hero_badge, hero_h1, hero_tag, body_html, faqs):
    canon = f'{BASE}/{slug}'
    article = make_article(title, desc, canon)
    breadcrumb = make_breadcrumb(crumb_label, canon)
    faq_dict = make_faq(faqs)
    aj, bj, fj = jsonld(article, breadcrumb, faq_dict)

    head = HEAD.format(
        n=1,  # og:image placeholder uses moolank-1.jpg as the brand card
        title=title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        keywords=f'NameAligned {slug}, chaldean numerology methodology, how chaldean numerology works, AI numerology disclosure, numerology sources, NameAligned trust',
        article_json=aj, breadcrumb_json=bj, faq_json=fj,
    )

    faq_html = '\n'.join(
        f'    <details><summary>{q}</summary><p>{a}</p></details>'
        for q, a in faqs
    )

    page = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/about">About</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">{crumb_label}</span>
</nav>

<header class="seo-hero">
  <div class="container">
    <div class="badge">{hero_badge}</div>
    <h1 style="margin-top:.5rem;">{hero_h1}</h1>
    <div class="tag">{hero_tag}</div>
  </div>
</header>

<div class="seo-wrap">
  <main class="seo-body">

{body_html}

    <h2>Frequently asked</h2>
    <div class="seo-faq">
{faq_html}
    </div>

  </main>

  <aside class="seo-aside">
    <div class="article-sidebar">
      <div class="eyebrow">Try It Yourself</div>
      <h3>Run your own analysis</h3>
      <p>Free Chaldean check in 10 seconds. See your numbers, the math behind them, and what they suggest.</p>
      <a href="/analyzer" class="cta">Free Analysis →</a>
      <a href="/ask-aura" class="cta outline">✦ Ask Aura</a>
      <div class="sep"></div>
      <div class="eyebrow">Full Destiny Report</div>
      <h3>Personalised PDF</h3>
      <div class="price-row">
        <span class="price-inr">INR 499</span>
        <span class="price-usd">or $5 USD</span>
      </div>
      <p>Complete chart, name corrections, compatibility, 5-year forecast.</p>
      <a href="/report" class="cta">Get the report →</a>
    </div>
  </aside>
</div>

{FOOTER}
'''
    return head + page


# ── 1. METHODOLOGY ──────────────────────────────────────────────────
methodology_body = '''
  <p>NameAligned uses the <strong>Chaldean system</strong> of numerology, the oldest documented method, taught in early Babylonian/Sumerian schools and brought into modern English-language practice by Cheiro (Count Louis Hamon, 1866-1936) in his foundational text <em>Cheiro\'s Book of Numbers</em>.</p>

  <p>This page explains exactly what we calculate, the values we use, and where the math comes from. We do not believe numerology is magic. We believe it is a structured symbolic system, and that structured systems deserve transparent explanations.</p>

  <h2>The Chaldean letter-value table</h2>
  <p>Unlike the more common (and less accurate) Pythagorean system that maps A=1, B=2 sequentially, Chaldean numerology assigns each letter a numerical value based on the <strong>vibration of its sound</strong>, derived from ancient Phoenician and Hebrew alphabets. The number 9 is intentionally absent in name calculation; it is considered too sacred to be applied to ordinary names.</p>

  <table style="width:100%;border-collapse:collapse;font-family:sans-serif;font-size:14px;margin:1.25rem 0;">
    <thead><tr style="border-bottom:1px solid var(--gold-b);"><th style="text-align:left;padding:.55rem .8rem;">Value</th><th style="text-align:left;padding:.55rem .8rem;">Letters</th></tr></thead>
    <tbody>
      <tr><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;"><strong>1</strong></td><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;">A, I, J, Q, Y</td></tr>
      <tr><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;"><strong>2</strong></td><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;">B, K, R</td></tr>
      <tr><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;"><strong>3</strong></td><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;">C, G, L, S</td></tr>
      <tr><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;"><strong>4</strong></td><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;">D, M, T</td></tr>
      <tr><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;"><strong>5</strong></td><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;">E, H, N, X</td></tr>
      <tr><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;"><strong>6</strong></td><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;">U, V, W</td></tr>
      <tr><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;"><strong>7</strong></td><td style="padding:.45rem .8rem;border-bottom:1px solid #eee;">O, Z</td></tr>
      <tr><td style="padding:.45rem .8rem;"><strong>8</strong></td><td style="padding:.45rem .8rem;">F, P</td></tr>
    </tbody>
  </table>

  <p>You can verify these values in Cheiro\'s <em>Book of Numbers</em>, chapter on "The Chaldean System". Most modern Chaldean numerology software (including ours) follows this table without modification.</p>

  <h2>How we calculate your Birth Number (Moolank)</h2>
  <p>Your Birth Number is the single-digit reduction of the day of the month you were born. We do not include the month or year. Example: a person born on the <strong>14th</strong> has Birth Number 1+4 = <strong>5</strong>. A person born on the <strong>27th</strong> has 2+7 = 9. This is your daily vibration, the energy you express moment-to-moment.</p>

  <h2>How we calculate your Life Path Number (Bhagyank)</h2>
  <p>Your Life Path Number is the single-digit reduction of your full date of birth (day + month + year). Example: 14 March 1992 → 1+4+0+3+1+9+9+2 = 29 → 2+9 = 11 → 1+1 = <strong>2</strong>. This is the long-arc destiny vibration of your life.</p>

  <h2>How we calculate your Name Number</h2>
  <p>We sum the Chaldean values of every letter in your full name (as commonly used, not just legal), then reduce to a single digit. Both the reduced number and the unreduced "compound" number are interpreted, since compound numbers carry their own significance in Cheiro\'s system. Example: <em>RAMESH</em> → 2+1+4+5+3+5 = 20 → 2+0 = <strong>2</strong>; compound is 20.</p>

  <h2>What "name correction" actually means</h2>
  <p>If your current Name Number conflicts with your Birth or Life Path Number (according to Cheiro\'s planetary compatibility chart), we suggest alternate spellings that bring the Name Number into harmony. This is a structured suggestion, not magic. The change is in how the name vibrates, not in the legal document.</p>

  <h2>Compatibility math</h2>
  <p>Two people\'s compatibility is read through the relationship between their ruling planets. Cheiro\'s framework groups numbers into harmonic triangles (1-3-9 fire, 2-7 water, etc.) and notes which pairings traditionally produce friction (4-8 is the most cautioned). We render this honestly, including the cautions, rather than hiding inconvenient results.</p>

  <h2>What we deliberately do NOT do</h2>
  <ul>
    <li><strong>We do not invent values.</strong> The letter-value table is Cheiro\'s, unmodified.</li>
    <li><strong>We do not predict specific events.</strong> No "you will receive a job offer on May 14". Numerology indicates tendencies and timing windows, not fixed events.</li>
    <li><strong>We do not sell rituals, gemstones or "remedy services".</strong> Where Cheiro suggests gemstone correspondences, we mention them as traditional, not as required purchases.</li>
    <li><strong>We do not claim scientific validity.</strong> Numerology is a symbolic system. It can produce useful self-reflection without needing to be physically "true".</li>
  </ul>
'''

# ── 2. HOW IT WORKS ─────────────────────────────────────────────────
how_it_works_body = '''
  <p>NameAligned is built so a complete first analysis takes less than ten seconds. Here is what happens when you use it, step by step.</p>

  <h2>Step 1: You enter your name and date of birth</h2>
  <p>One screen, two fields. We ask for your <strong>name as you commonly use it</strong> (not necessarily your legal name) and your <strong>full date of birth</strong>. Optional fields, partner\'s name (for compatibility), and a phone number (for mobile-number numerology), can be filled later.</p>
  <p>We do not require an email, account, OTP, or signup of any kind for the free analysis. You are not added to a mailing list.</p>

  <h2>Step 2: We calculate your core numbers instantly in your browser</h2>
  <p>The math happens client-side, in your browser, the moment you submit. The Chaldean letter-value table runs against your name. Your day of birth becomes your Moolank. Your full date of birth becomes your Bhagyank. The compound number behind each reduced digit is also captured for interpretation.</p>
  <p>Nothing is sent to a server unless you choose to save your results or buy the report.</p>

  <h2>Step 3: You see the breakdown immediately</h2>
  <p>You get nine sections in the free analysis: birth number, name number, life path, alignment score, lucky attributes (colours, days, gemstones traditionally associated with your number), career domains that suit your planetary energy, personal year (where in the 1-9 cycle you currently are), relationship compass, and a soft preview of the full 5-year forecast.</p>
  <p>Every section explains the math: what was calculated, from what input, and what tradition says about it. No black box.</p>

  <h2>Step 4: You can deepen the analysis (optional)</h2>
  <p>If the free reading was useful, three optional next steps are available, none required, none up-sold aggressively:</p>
  <ul>
    <li><strong>Ask Aura</strong>, our conversational companion, free, no signup. You can ask anything about your numbers in plain language.</li>
    <li><strong>Run a compatibility check</strong> with a partner, friend, family member, or coworker. Free.</li>
    <li><strong>Buy the Full Destiny Report</strong> (INR 499 &middot; $5 USD), a personalised PDF with the 5-year forecast, name-correction options, mobile-number analysis, remedies (in Cheiro\'s framework, not as paid services) and full compatibility map.</li>
  </ul>

  <h2>Step 5: Your data, if you saved it, is yours</h2>
  <p>If you bought the report, we keep the minimum needed to deliver it (name, DOB, email, payment record) and nothing more. If you used the free analyzer without saving, no record exists. You can request deletion of any saved data at any time by emailing us; see the <a href="/privacy">Privacy Policy</a>.</p>

  <h2>What you receive in the paid report</h2>
  <p>The full Destiny Report is a single personalised PDF (typically 25-35 pages) containing:</p>
  <ul>
    <li>Birth, Life Path, Name, and Compound number deep readings</li>
    <li>Detailed personality, career and relationship sections</li>
    <li>5-year personal-year forecast with specific theme windows</li>
    <li>Name-correction suggestions (when needed), with multiple alternative spellings</li>
    <li>Mobile-number analysis, useful for choosing a new SIM</li>
    <li>Compatibility chart, including any second name you supply</li>
    <li>Traditional remedies in Cheiro\'s framework (colours, days, fasting practices, mantras, never paid "remedy services")</li>
  </ul>
  <p>The report is delivered within 5 minutes of payment. If anything is unclear, our refund policy is straightforward: see <a href="/refund">Refund</a>.</p>

  <h2>What we deliberately do NOT do at any step</h2>
  <ul>
    <li>We do not predict death, divorce, or any single life event with certainty.</li>
    <li>We do not call/text/email asking for additional money for "stronger remedies".</li>
    <li>We do not require a phone consultation; everything is in writing.</li>
    <li>We do not store sensitive details we do not need.</li>
  </ul>
'''

# ── 3. AI DISCLOSURE ─────────────────────────────────────────────────
ai_disclosure_body = '''
  <p>This site uses AI in two specific places. Honesty about how is more useful than vague reassurances, so here is exactly what runs where, and what is human-authored.</p>

  <h2>Where AI is used</h2>
  <p><strong>1. Aura, the conversational companion at /ask-aura.</strong> When you chat with Aura, your message is sent (along with optional numerology context if you have entered your birth date) to <strong>Google\'s Gemini Flash</strong> language model. Aura\'s personality, voice rules and conversational structure are defined in a system prompt we wrote and maintain; Gemini generates the specific reply. We do not store the contents of your conversation beyond what is needed to make subsequent replies feel continuous (handled by our V2 architecture, your messages remain associated only with an anonymous browser token unless you sign in).</p>
  <p><strong>2. Long-form content generation, partially.</strong> Some sections of the deeper articles and reports are drafted with AI assistance. Every output is human-reviewed before publishing. The factual claims, the letter-value table, the planetary correspondences, the compatibility framework, all come from Cheiro\'s primary texts, not from AI.</p>

  <h2>Where AI is NOT used</h2>
  <ul>
    <li><strong>The core numerology math.</strong> Birth number, life path, name number, and compatibility scores are computed deterministically in JavaScript using Cheiro\'s tables. No AI inference is involved.</li>
    <li><strong>Letter-value tables and planetary correspondences.</strong> These are fixed reference data, sourced from <em>Cheiro\'s Book of Numbers</em> and verified against secondary sources.</li>
    <li><strong>Payment processing and report generation.</strong> Razorpay (India) and PayPal (international) handle payments. The PDF is generated server-side from your computed numbers with templates we wrote.</li>
  </ul>

  <h2>What Aura is and is not</h2>
  <p>Aura is designed to be a <strong>reflective companion</strong>, not an oracle. She speaks in patterns and possibilities, never absolute predictions. She is instructed not to give medical, legal, or specific financial advice. If you ever raise a safety concern (self-harm, mental health crisis), Aura is wired to bypass the LLM entirely and surface helpline numbers.</p>
  <p>Aura makes mistakes. She is an AI language model, not a credentialed practitioner. Treat her replies as a thinking-partner, not as authoritative guidance. If something matters, run it past a real person.</p>

  <h2>Your data inside Aura</h2>
  <p>When you chat with Aura, the following happens:</p>
  <ul>
    <li>An anonymous browser token is generated on your first visit, stored in your browser as <code>aura_anon</code>.</li>
    <li>Your messages and Aura\'s replies are stored in our database (Supabase, hosted in India/Singapore) and associated with that anonymous token.</li>
    <li>The conversation is sent to Gemini one turn at a time, with no persistent storage on Google\'s side beyond their standard API logging.</li>
    <li>You can clear your data by clearing browser storage on the site, or by emailing us for deletion.</li>
  </ul>
  <p>We do not sell, share, or rent your conversation data to anyone. Ever.</p>

  <h2>AI inference cost &amp; daily limits</h2>
  <p>NameAligned uses Google\'s free tier of Gemini, which has a global daily request limit. Aura serves users on a first-come, first-served basis until the daily quota is reached, at which point she goes into a "resting" state until quota resets the next morning. This is a deliberate choice, we run free for users without forcing accounts or upsells. If you ever see "Aura is resting tonight", come back tomorrow.</p>

  <h2>Why we are transparent about this</h2>
  <p>The spiritual / numerology space has a long history of obscuring methods. We want NameAligned to be the opposite, transparent calculations, transparent AI use, transparent pricing. The more clearly you can see how something works, the more useful it becomes to you, and the more we can be trusted with the next iteration.</p>
'''

# ── 4. SOURCES ──────────────────────────────────────────────────────
sources_body = '''
  <p>Every interpretation on NameAligned is anchored in a documented tradition. We do not invent meanings. This page lists the primary and secondary sources behind the readings you see, so you can verify or read deeper if you choose.</p>

  <h2>Primary numerology sources</h2>

  <h3>Cheiro, <em>Book of Numbers</em> (1926)</h3>
  <p>The single most important source for our system. Cheiro (Count Louis Hamon) was a British-Irish astrologer and palmist active in the late 1800s and early 1900s, who consulted with Mark Twain, Queen Victoria, Thomas Edison, and Oscar Wilde, among many others. <em>Book of Numbers</em> codified the Chaldean letter-value table and the planetary correspondences that form the foundation of modern Chaldean numerology. Public domain. Our letter table, planetary triangles, and compound-number interpretations follow Cheiro directly.</p>

  <h3>Cheiro, <em>Language of the Hand</em> (1894)</h3>
  <p>Cheiro\'s earlier work on palmistry, which intersects with numerology through the planetary correspondences. Public domain.</p>

  <h3>William Lilly, <em>Christian Astrology</em> (1647)</h3>
  <p>The foundational text of Western horary astrology, the practice of reading a chart cast at the moment of a question. We draw on Lilly\'s framework, not for date-of-birth numerology, but for the horary-style conversational logic in Aura. Public domain.</p>

  <h2>Indic horary &amp; symbolic traditions</h2>

  <h3>Prashna Marga</h3>
  <p>A 17th-century Sanskrit treatise on horary astrology (<em>prashna</em> meaning "question"). The framework, reading the chart of the moment a question is asked, deeply informs Aura\'s conversational design. We do not quote any specific English translation verbatim; modern translations are largely under copyright. The system-level concepts (significators, time-based reading, question chart) are framework, not copyrighted expression.</p>

  <h3>Prashna Tantra</h3>
  <p>A related Indic horary text. Same notes apply.</p>

  <h3>Lal Kitab</h3>
  <p>An early 20th-century tradition combining Vedic astrology with practical karmic interpretation. We reference the framework (planetary "rishtas", karmic patterns) without quoting any specific English translation. Original Urdu/Hindi farmans are anonymous folk-tradition material.</p>

  <h2>Western esoteric tradition</h2>

  <h3><em>The Kybalion</em> (1908, anonymous, "Three Initiates")</h3>
  <p>The most accessible summary of Hermetic principles (the law of mentalism, correspondence, vibration, polarity, rhythm, cause and effect, gender). Public domain. Aura\'s philosophical undertone draws on Hermetic correspondence, "as above, so below", read as a way of seeing patterns rather than literal cosmology.</p>

  <h2>Depth psychology</h2>

  <h3>Carl Gustav Jung, archetypal psychology</h3>
  <p>Aura\'s use of archetypes (the wounded healer, the shadow, the senex, the puer, the warrior, the sage) draws on Jung\'s framework. We do not quote Jung\'s specific texts, all of which remain in copyright in most jurisdictions; we use his ideas at the framework level, which are not copyrightable.</p>

  <h2>What "framework, not quote" means</h2>
  <p>Copyright protects specific expression (the exact words of a translator, the specific case examples of an author), not ideas or systems. When we say "Aura draws on Prashna Marga", we mean she uses the framework, the idea of reading the moment, the time-based significator logic, not any specific translator\'s phrasing. This is the same way a yoga teacher can teach pranayama without infringing on any specific translator of the Yoga Sutras.</p>

  <h2>Why we publish our sources</h2>
  <p>Most numerology and astrology sites do not name their sources because the field has historically operated on authority alone. We think that is a mistake. Naming the books and traditions behind a reading invites the user to <strong>verify, read deeper, or disagree</strong>, all of which are healthy responses. NameAligned is a starting point, not an end-point.</p>

  <h2>If you spot an error</h2>
  <p>If you ever find a calculation, citation, or interpretation that contradicts Cheiro\'s primary text or a major secondary source, please write to us. We treat factual corrections seriously and will update the affected page within seven days.</p>
'''


PAGES = [
  dict(
    slug='methodology',
    title='Methodology · How NameAligned Calculates Your Chaldean Numbers',
    desc='The full methodology behind NameAligned: the Chaldean letter-value table, how we calculate birth number, life path and name number, and what we deliberately do not do.',
    og_desc='Transparent methodology behind NameAligned. Cheiro\'s system, the letter table, the math, and our limits.',
    crumb_label='Methodology',
    hero_badge='How We Calculate',
    hero_h1='Methodology &middot; The Chaldean System',
    hero_tag='Transparent math, transparent tradition. Here is exactly what we calculate, and from what source.',
    body_html=methodology_body,
    faqs=[
      ('Is NameAligned numerology accurate?',
       'Our calculations match Cheiro\'s primary texts exactly. "Accurate" in numerology means faithful to the documented tradition. We do not claim scientific predictive validity, but we are rigorous about the math.'),
      ('Why Chaldean and not Pythagorean?',
       'Chaldean is older, sound-based, and the system Cheiro and most serious traditional practitioners use. Pythagorean (A=1, B=2 sequential) is more common in pop numerology because it is simpler, but it lacks the vibrational logic of Chaldean.'),
      ('Why is the number 9 excluded from name values?',
       'In Chaldean tradition, 9 is considered too sacred to assign to ordinary letter-values. It only appears in birth-number / life-path calculations, where its meaning is preserved.'),
      ('Where can I verify this myself?',
       'Cheiro\'s Book of Numbers is public domain and available on archive.org. The chapter "The Chaldean System" contains the letter-value table.'),
    ],
  ),
  dict(
    slug='how-it-works',
    title='How NameAligned Works · Step-by-Step',
    desc='The complete walkthrough of using NameAligned: what we ask, what we calculate, what you receive, and what we deliberately do not do. No black box.',
    og_desc='Step by step: how NameAligned\'s free analysis works, what you receive in the paid report, and what we do not do.',
    crumb_label='How It Works',
    hero_badge='User Journey',
    hero_h1='How NameAligned Works',
    hero_tag='From your name and birth date to a full analysis, in under ten seconds. Here is every step.',
    body_html=how_it_works_body,
    faqs=[
      ('Do I need to create an account?',
       'No. The free analysis works without signup, email, or OTP. Only paying for the report requires email (for delivery) and payment details.'),
      ('How long does the free analysis take?',
       'Under ten seconds from form submission to seeing your numbers. The math runs in your browser.'),
      ('Will you call or message me?',
       'No. We do not have a phone team. We do not contact you for upsells. Email support is available for questions.'),
      ('What if my report is wrong?',
       'We treat factual errors (calculation mistakes, miscalculated compatibilities) as bugs. Email us and we will issue a corrected report and refund if appropriate. See our Refund Policy.'),
    ],
  ),
  dict(
    slug='ai-disclosure',
    title='AI Disclosure · How NameAligned Uses Gemini',
    desc='Transparent disclosure of where AI is used in NameAligned: Aura the conversational companion (Google Gemini Flash), partial long-form drafting, and where AI is deliberately not used.',
    og_desc='Honest AI disclosure: Aura uses Gemini for conversation; the numerology math is deterministic JavaScript, not AI.',
    crumb_label='AI Disclosure',
    hero_badge='Transparency',
    hero_h1='AI Disclosure',
    hero_tag='Where we use AI, where we deliberately do not, and what your data does (and does not) do inside Aura.',
    body_html=ai_disclosure_body,
    faqs=[
      ('Is the numerology calculation done by AI?',
       'No. All numerology math (birth number, life path, name number, compatibility) is deterministic JavaScript running on Cheiro\'s tables. AI is only used for Aura\'s conversational replies.'),
      ('Does Aura store my conversations?',
       'Yes, in our Supabase database, associated with an anonymous browser token. We do not sell or share this data. You can request deletion any time.'),
      ('Why does Aura sometimes rest?',
       'NameAligned uses Google\'s free Gemini tier, which has a daily request limit. When it is exhausted, Aura rests until the next reset (around 12:30 PM IST). This is how we keep Aura free for everyone without accounts or upsells.'),
      ('Can AI replace a real numerologist?',
       'No, and we do not claim to. Aura is a reflective tool. For consequential decisions, consult a real practitioner.'),
    ],
  ),
  dict(
    slug='sources',
    title='Sources · The Texts &amp; Traditions Behind NameAligned',
    desc='Every interpretation on NameAligned is anchored in a documented source. Cheiro, Lal Kitab, Prashna Marga, William Lilly, Hermetic and Jungian traditions explained.',
    og_desc='The primary and secondary sources behind every interpretation on NameAligned. Verified, named, citable.',
    crumb_label='Sources',
    hero_badge='Tradition',
    hero_h1='Sources &middot; What\'s Behind the Readings',
    hero_tag='Every interpretation is anchored in a documented tradition. Verify, read deeper, or disagree.',
    body_html=sources_body,
    faqs=[
      ('Is NameAligned based on real numerology traditions?',
       'Yes. Primary source is Cheiro\'s Book of Numbers (1926). Aura\'s conversational design draws on Prashna Marga, William Lilly, Hermetic principles and Jungian archetypes (framework only, not specific translations).'),
      ('Can I verify your sources?',
       'Yes. Cheiro\'s texts and The Kybalion are public domain on archive.org. Other traditions are framework-level references.'),
      ('Do you use AI to write the interpretations?',
       'Partially. AI assists drafting; humans review every interpretation before publishing. The factual claims (planetary correspondences, letter tables, compatibility logic) come from Cheiro, not AI.'),
      ('What if a translation says something different?',
       'Send us the citation. We will compare against Cheiro\'s primary text and update if we are in error. We treat factual corrections as priority bugs.'),
    ],
  ),
]


def build():
    for p in PAGES:
        html = render(**p)
        out_path = os.path.join(OUT, f'{p["slug"]}.html')
        with open(out_path, 'w') as fh: fh.write(html)
        print(f'  wrote {out_path}')


if __name__ == '__main__':
    build()
    print(f'\n{len(PAGES)} E-E-A-T pages built.')
