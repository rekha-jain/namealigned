#!/usr/bin/env python3
"""Anahata Acoustics music on namealigned.com.

Builds /meditation-music, injects one matching track into selected articles,
and writes sitemap-video.xml. Safe to re-run (injections live between markers),
including after the generators that own the injected pages.

    python3 tools/build-anahata-music.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.namealigned.com"
CHANNEL = "https://www.youtube.com/@AnahataAcoustics"
ASSET_V = "20261020"
START, END = "<!-- anahata:start -->", "<!-- anahata:end -->"

# id: (title on YouTube, seconds, uploadDate, short note written for this site)
VIDEOS = {
    "ZsJYeuugP2U": ("Fall Asleep in Minutes: Silence a Racing Mind with 432Hz Sarangi & Delta Waves", 3600, "2026-09-02T10:00:03-07:00",
                    "Slow sarangi in Raga Chikitsa over a low delta pulse. Built for the hour when the mind replays the day instead of letting it go."),
    "P7DM3Taupl4": ("Lower Cortisol Instantly | 432Hz Bansuri Flute for Deep Sleep & Relaxation", 3600, "2026-10-09T07:20:14-07:00",
                    "Long, unhurried bansuri phrases with plenty of silence between them. Good for cooling down after a heated or overstimulating day."),
    "Vk-4nvfavhA": ("Instant Emotional Peace | 432Hz Bansuri Flute Deep Relaxation", 1800, "2026-06-18T02:05:09-07:00",
                    "A moonlit bansuri session inspired by Vrindavan nights. Thirty minutes, soft enough to fall asleep to."),
    "qeZSXpkhBkQ": ("Deep Nervous System Reset | 432Hz Tanpura Drone for Anxiety & Stress Relief", 7128, "2026-05-29T01:37:06-07:00",
                    "Two hours of pure tanpura drone and nothing else. No melody to follow, so the mind has nothing to grip."),
    "bxR1-_bZp1k": ("Open Your Heart: 432Hz Meditative Sitar & Kashmiri Santoor for Emotional Healing & Deep Peace", 3600, "2026-09-11T09:15:09-07:00",
                    "Sitar and Kashmiri santoor in a slow, open alap. For the evenings when you have absorbed more than your share of other people's weather."),
    "ow554pr8esE": ("Release Anxiety & Feel Safe Again | Deep Healing Instrumental Sitar Music for Emotional Reset", 3600, "2026-09-09T05:00:12-07:00",
                    "Grounded, low sitar with a steady drone underneath. Made for the anxious loop of waiting to be reassured."),
    "ywUCSdLwD6I": ("Unclench Your Entire Body: Deep Somatic Healing Sarangi for Nervous System Reset & Calm", 5400, "2026-08-25T09:50:17-07:00",
                    "Ninety minutes of sarangi paced for a body scan. Let the jaw, shoulders and hands go one at a time."),
    "tFrpaoUC9GU": ("Put It All Down: Gentle Sitar Meditation for Burnout, Emotional Exhaustion & Inner Quiet", 1800, "2026-09-06T07:45:13-07:00",
                    "Gentle sitar for the person who is always the one carrying things. Thirty minutes of being allowed to stop."),
    "hkrX54fONrk": ("Digital Detox: 90 Minutes of Bansuri Flute for a Reset Mind", 5400, "2026-08-30T02:20:35-07:00",
                    "Bansuri flute for stepping away from screens and notifications. Put the phone face down and let it run."),
    "WyKnsPkn-Ss": ("Enter Deep Flow in 10 Minutes | Calming Bansuri & Tanpura Drone for Focus, Study & Mental Clarity", 3600, "2026-10-05T06:11:30-07:00",
                    "Bansuri over a tanpura drone, steady enough to work to. No sudden changes to pull your attention away."),
    "Q6W42qi9fTA": ("Pure Tanpura (1 Hour) | Clear Mental Fog, Enter Deep Flow State", 3600, "2026-09-16T06:55:59-07:00",
                    "A warm, sustained tanpura drone with light sitar. For reading, writing, or sitting with a question until it settles."),
    "GetYIeUvgF8": ("Enter Deep Flow State: 528Hz Sarangi & Indian Flute for Focus, Studying & Calm Mind", 3600, "2026-08-12T09:09:53-07:00",
                    "Sarangi and flute tuned to 528Hz. A quiet backdrop for long study sessions."),
    "4Sqzt8ZagGY": ("Bansuri & Sitar Flow: 60 Minutes of Positive Energy for Deep Work", 3600, "2026-09-15T07:34:02-07:00",
                    "Raga Bilawal on bansuri, sitar and tabla. Brighter and more rhythmic, for work that needs momentum."),
    "dVZBc-8NvQE": ("Wake Up Without Anxiety: Peaceful Morning Indian Flute & Sarangi to Quiet Overthinking & Find Calm", 3600, "2026-08-21T10:30:13-07:00",
                    "A dawn soundscape of flute and sarangi. Play it before you open your messages."),
    "De_EJcVCAkE": ("Find Stillness with Bansuri Flute | Raga Bhairavi", 1800, "2026-06-21T07:00:48-07:00",
                    "A devotional morning raga on bansuri. Thirty minutes of stillness to begin the day."),
    "XRk_QpJ6ZoI": ("Morning Joy | 432Hz Flute to Increase Morning Vitality & Happiness", 3600, "2026-07-01T06:37:06-07:00",
                    "Light, bright bansuri for the start of the day. The most energetic track in this list."),
    "WyED8Ry_r8w": ("You Don't Have to Fix Anything: Gentle Indian Instrumental Music for Deep Inner Peace", 3600, "2026-08-08T08:22:24-07:00",
                    "An evening soundscape for stepping out of doing, solving and planning. Nothing to respond to."),
}

SECTIONS = [
    ("sleep", "For sleep", "Low, slow and without surprises. Start one as you get into bed and let it run out.",
     ["ZsJYeuugP2U", "P7DM3Taupl4", "Vk-4nvfavhA", "qeZSXpkhBkQ"]),
    ("calm", "For anxiety and emotional overload", "For the evenings when the feeling is bigger than the situation, or when you have taken on other people's moods.",
     ["bxR1-_bZp1k", "ow554pr8esE", "ywUCSdLwD6I", "tFrpaoUC9GU", "hkrX54fONrk"]),
    ("focus", "For focus and study", "Steady drones and long phrases. Enough sound to cover a noisy room, not enough to pull you in.",
     ["WyKnsPkn-Ss", "Q6W42qi9fTA", "GetYIeUvgF8", "4Sqzt8ZagGY"]),
    ("morning", "For the morning", "Morning ragas, played before the inbox gets a vote.",
     ["dVZBc-8NvQE", "De_EJcVCAkE", "XRk_QpJ6ZoI"]),
]

# Birth number (moolank) -> ruling planet -> a starting track
BY_NUMBER = [
    (1, "Sun", "XRk_QpJ6ZoI", "Bright morning bansuri to match a Sun-ruled drive."),
    (2, "Moon", "Vk-4nvfavhA", "Moonlit flute for the most feeling-led number."),
    (3, "Jupiter", "De_EJcVCAkE", "A devotional raga for the teacher and seeker."),
    (4, "Rahu", "hkrX54fONrk", "A detox from the overstimulation Rahu attracts."),
    (5, "Mercury", "WyKnsPkn-Ss", "A steady drone to hold Mercury's many open tabs."),
    (6, "Venus", "bxR1-_bZp1k", "Sitar and santoor for the heart-led harmoniser."),
    (7, "Ketu", "Q6W42qi9fTA", "Pure tanpura for the inward, searching mind."),
    (8, "Saturn", "tFrpaoUC9GU", "Permission to put the load down for a while."),
    (9, "Mars", "P7DM3Taupl4", "Slow bansuri to cool Mars heat before sleep."),
]

# Article -> (track, eyebrow, heading, note)
INJECT = {
    "numerology-and-overthinking.html": ("ZsJYeuugP2U", "Listen while the loop quiets",
        "Sarangi for a racing mind at night",
        "If the loop is loudest at bedtime, try this before reaching for your phone. One hour of slow sarangi, made by our music channel, Anahata Acoustics."),
    "why-some-people-feel-too-much.html": ("bxR1-_bZp1k", "A daily decompression ritual",
        "Music with no lyrics, for the end of a heavy day",
        "This page suggests music without words as a way to discharge the day. This is one we made for exactly that: an hour of sitar and santoor from Anahata Acoustics."),
    "why-some-people-emotionally-withdraw.html": ("WyED8Ry_r8w", "Before you reach back out",
        "You don't have to fix anything",
        "An evening track for the quiet stretch after withdrawing, before you are ready to talk. From our music channel, Anahata Acoustics."),
    "reassurance-needs-in-relationships.html": ("ow554pr8esE", "While you wait for the reply",
        "Sitar to help you feel safe again",
        "For the anxious hour of checking your phone. Grounded sitar over a steady drone, from our music channel, Anahata Acoustics."),
    "numerology-spiritual-meaning.html": ("De_EJcVCAkE", "A practice to pair with your number",
        "Raga Bhairavi on bansuri flute",
        "A thirty-minute morning raga for sitting quietly with what your number points to. From our music channel, Anahata Acoustics."),
    "the-emotionally-analytical-personality.html": ("Q6W42qi9fTA", "For a mind that will not stop analysing",
        "Pure tanpura to clear mental fog",
        "One hour of tanpura drone with no melody to follow, so the analysis has nothing to grip. From our music channel, Anahata Acoustics."),
}

e = lambda s: html.escape(s, quote=True)


def dur_iso(sec):
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "") + (f"{s}S" if s or not (h or m) else "")


def dur_label(sec):
    if sec < 3600:
        return f"{round(sec / 60)} min"
    return f"{round(sec / 1800) / 2:g} hr"


def thumb(vid):
    return f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"


def video_ld(vid):
    title, sec, up, note = VIDEOS[vid]
    return {
        "@type": "VideoObject", "name": title, "description": note,
        "thumbnailUrl": thumb(vid), "uploadDate": up, "duration": dur_iso(sec),
        "embedUrl": f"https://www.youtube.com/embed/{vid}",
        "contentUrl": f"https://www.youtube.com/watch?v={vid}",
        "publisher": {"@type": "Organization", "name": "Anahata Acoustics", "url": CHANNEL},
    }


def player(vid):
    title, sec, _, _ = VIDEOS[vid]
    return (f'<div class="na-video" data-id="{vid}"><button type="button" aria-label="Play {e(title)}">'
            f'<img src="{thumb(vid)}" alt="" loading="lazy" width="480" height="360">'
            f'<span class="na-play"></span><span class="na-len">{dur_label(sec)}</span></button></div>')


def card(vid, eyebrow=None, head=None, note=None, anchor=False):
    title, _, _, default_note = VIDEOS[vid]
    out = [f'<div class="na-track"{f' id="t-{vid}"' if anchor else ""}>']
    if eyebrow:
        out.append(f'<div class="na-eyebrow">{e(eyebrow)}</div>')
    out.append(f'<div class="na-head">{e(head or title)}</div>')
    out.append(f'<p class="na-note">{e(note or default_note)}</p>')
    out.append(player(vid))
    out.append(f'<div class="na-meta"><span>Anahata Acoustics</span>'
               f'<a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">Watch on YouTube</a></div>')
    out.append("</div>")
    return "".join(out)


def ld_script(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


# ---------- article injections ----------

def inject():
    for page, (vid, eyebrow, head, note) in INJECT.items():
        path = ROOT / page
        src = path.read_text(encoding="utf-8")
        src = re.sub(r"\n?[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", "\n", src, flags=re.S)
        block = (f"    {START}\n"
                 f'    <link rel="stylesheet" href="/assets/music-embed.css?v={ASSET_V}"/>\n'
                 f"    {card(vid, eyebrow, head, note)}\n"
                 f"    {ld_script({'@context': 'https://schema.org', **video_ld(vid)})}\n"
                 f'    <p style="font-family:sans-serif;font-size:13px;margin:-1.25rem 0 2rem;"><a href="/meditation-music" style="color:var(--gold-d);">More tracks for sleep, calm and focus &rarr;</a></p>\n'
                 f'    <script src="/assets/music-embed.js?v={ASSET_V}" defer></script>\n'
                 f"    {END}\n")
        m = re.search(r'^[ \t]*<div class="share-strip"', src, re.M) or re.search(r"^[ \t]*<h2>Frequently asked</h2>", src, re.M)
        if not m:
            raise SystemExit(f"No insertion point in {page}")
        src = src[:m.start()] + block + src[m.start():]
        path.write_text(src, encoding="utf-8")
        print("injected", page)


# ---------- /meditation-music ----------

def build_page():
    shell = (ROOT / "why-some-people-feel-too-much.html").read_text(encoding="utf-8")
    head_top = shell[:shell.index("<title>")]
    style = shell[shell.index("<style>"):shell.index("</style>") + len("</style>")]
    nav = shell[shell.index('<nav class="nav">'):shell.index("</nav>") + len("</nav>")]
    aside = shell[shell.index('<aside class="seo-aside">'):shell.index("</aside>") + len("</aside>")]
    aside = aside.replace("why-some-people-feel-too-much", "meditation-music")
    footer = shell[shell.index('<footer class="footer">'):]

    url = f"{BASE}/meditation-music"
    title = "Meditation Music for Sleep, Calm and Focus, by Birth Number"
    desc = ("Free Indian classical meditation music for sleep, anxiety and focus: bansuri, sarangi, sitar and tanpura. "
            "Plus a starting track for each Chaldean birth number.")
    all_ids = [v for s in SECTIONS for v in s[3]]
    faq = [
        ("Which track should I start with?",
         "Start with the track for your birth number in the table above. If you do not know your number, add the digits of your birth day until you reach a single digit. Born on the 23rd: 2 + 3 = 5."),
        ("What does 432Hz mean in the titles?",
         "It is the tuning of the instruments. Many listeners find 432Hz tuning warmer and softer than the standard 440Hz. Treat it as a matter of taste rather than a medical claim."),
        ("Can this music replace treatment for anxiety or insomnia?",
         "No. It can help you wind down, but it is not a treatment. If sleep or anxiety is affecting your daily life, please speak to a doctor."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-IN"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Meditation Music", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": video_ld(v)} for i, v in enumerate(all_ids)]},
    ]}

    rows = "".join(
        f'<tr><td class="n">{n}</td><td>{p}</td><td><a href="#t-{v}">{e(VIDEOS[v][0].split(" | ")[0].split(":")[0])}</a><span class="why">{e(why)}</span></td></tr>'
        for n, p, v, why in BY_NUMBER)
    sections = "".join(
        f'<h2 id="{sid}">{e(h)}</h2><p>{e(intro)}</p><div class="na-grid">' + "".join(card(v, anchor=True) for v in ids) + "</div>"
        for sid, h, intro, ids in SECTIONS)

    page = f"""{head_top}<title>{e(title)}</title>
<meta name="description" content="{e(desc)}"/>
<meta name="author" content="NameAligned.com"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
<link rel="canonical" href="{url}"/>
<meta property="og:title" content="{e(title)}"/>
<meta property="og:description" content="{e(desc)}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{url}"/>
<meta property="og:site_name" content="NameAligned.com"/>
<meta property="og:image" content="{thumb('bxR1-_bZp1k')}"/>
<meta name="twitter:card" content="summary_large_image"/>
{ld_script(ld)}

<link rel="stylesheet" href="/assets/style.css?v=20261017"/>
<link rel="stylesheet" href="/assets/theme-cosmic-light.css?v=20261017"/>
<link rel="stylesheet" href="/assets/music-embed.css?v={ASSET_V}"/>
{style}
<style>
.na-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;}}
.na-grid .na-track{{margin:0;display:flex;flex-direction:column;}}
.na-grid .na-note{{flex:1;}}
@media(max-width:640px){{.na-grid{{grid-template-columns:1fr;}}}}
.na-jump{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0 0;}}
.na-jump a{{font-family:sans-serif;font-size:13px;font-weight:600;color:var(--text);border:1px solid var(--gold-b);border-radius:20px;padding:5px 12px;text-decoration:none;background:var(--card);}}
.na-num{{width:100%;border-collapse:collapse;font-family:sans-serif;font-size:13.5px;}}
.na-num th{{text-align:left;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);padding:.5rem .6rem;border-bottom:1.5px solid var(--gold-b);}}
.na-num td{{padding:.6rem;border-bottom:1px solid var(--gold-b);vertical-align:top;color:var(--text);}}
.na-num td.n{{font-family:'Playfair Display',Georgia,serif;font-size:20px;font-weight:700;color:var(--gold-d);width:2.5rem;font-variant-numeric:tabular-nums;}}
.na-num a{{color:var(--text);font-weight:600;}}
.na-num .why{{display:block;color:var(--text2);font-size:12.5px;margin-top:2px;}}
.na-table-wrap{{overflow-x:auto;}}
</style>
</head>
<body>

{nav}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">&rsaquo;</span>
  <span style="color:var(--text2);">Meditation Music</span>
</nav>

<header class="seo-hero">
  <div class="container">
    <div class="badge">Anahata Acoustics</div>
    <h1>Meditation Music for Sleep, Calm and Focus</h1>
    <div class="tag">Bansuri, sarangi, sitar and tanpura, recorded by our music channel. Every track runs 30 minutes or longer, so you can start it and forget it.</div>
  </div>
</header>

<div class="seo-wrap">
  <main class="seo-body">
  <p>These are long-form Indian classical soundscapes from <a href="{CHANNEL}" target="_blank" rel="noopener">Anahata Acoustics</a>, the music side of NameAligned. No vocals and no sudden changes, so they stay in the background whether you are falling asleep, calming down or working. Tap any thumbnail to play it here.</p>
  <div class="na-jump"><a href="#by-number">By birth number</a><a href="#sleep">Sleep</a><a href="#calm">Calm</a><a href="#focus">Focus</a><a href="#morning">Morning</a></div>

  <h2 id="by-number">A starting track for your birth number</h2>
  <p>In Chaldean numerology your birth number (moolank) is ruled by a planet, and each planet has its own temperament. Use this as a first pick, then follow what actually helps.</p>
  <div class="na-table-wrap"><table class="na-num">
    <thead><tr><th>No.</th><th>Planet</th><th>Start with</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p style="margin-top:.75rem;font-size:13.5px;">Not sure of your number? <a href="/analyzer">Find it free in the analyzer</a>.</p>

  {sections}

  <h2>Frequently asked</h2>
  <div class="seo-faq">
    {"".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)}
  </div>

  <div class="seo-cta-band">
    <h3>New sessions every week</h3>
    <p>Subscribe on YouTube to get each new long-form session when it is uploaded.</p>
    <div class="btn-pair"><a class="primary" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">Subscribe to Anahata Acoustics</a><a class="outline" href="/analyzer">Find your number</a></div>
  </div>
  </main>

  {aside}
</div>

<script src="/assets/music-embed.js?v={ASSET_V}" defer></script>
<script src="/assets/analytics.js?v=20261017" defer></script>

{footer}"""
    (ROOT / "meditation-music.html").write_text(page, encoding="utf-8")
    print("built meditation-music.html")


# ---------- video sitemap ----------

def build_sitemap():
    entries = [(f"{BASE}/meditation-music", [v for s in SECTIONS for v in s[3]])]
    entries += [(f"{BASE}/{p[:-5]}", [vid]) for p, (vid, *_) in INJECT.items()]
    x = lambda s: html.escape(s, quote=False)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">']
    for loc, ids in entries:
        out.append(f"  <url>\n    <loc>{loc}</loc>")
        for v in ids:
            title, sec, up, note = VIDEOS[v]
            out.append(f"    <video:video>\n      <video:thumbnail_loc>{thumb(v)}</video:thumbnail_loc>\n"
                       f"      <video:title>{x(title)}</video:title>\n      <video:description>{x(note)}</video:description>\n"
                       f"      <video:player_loc>https://www.youtube.com/embed/{v}</video:player_loc>\n"
                       f"      <video:duration>{sec}</video:duration>\n      <video:publication_date>{up}</video:publication_date>\n"
                       f"    </video:video>")
        out.append("  </url>")
    out.append("</urlset>\n")
    (ROOT / "sitemap-video.xml").write_text("\n".join(out), encoding="utf-8")
    print("wrote sitemap-video.xml")


if __name__ == "__main__":
    build_page()
    inject()
    build_sitemap()
