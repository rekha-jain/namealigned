"""Generate /lo-shu-grid-calculator.

The site had Lo Shu content but no Lo Shu tool: the guide's own "Plot your Lo Shu
grid" buttons pointed at the generic /analyzer, which shows present-vs-missing
only, with no repeat counts, no planes and no arrows.

Nav, breadcrumb and footer are lifted verbatim from an existing page so the
chrome cannot drift out of sync with the rest of the site.
"""

import html
import re
import sys

SRC = "name-numerology-calculator.html"
OUT = "lo-shu-grid-calculator.html"

TITLE = "Lo Shu Grid Calculator: Missing Numbers by Date of Birth"
DESC = ("Plot your Lo Shu grid free from your date of birth. See repeated digits, "
        "missing numbers, the three planes and all eight arrows explained.")
URL = "https://www.namealigned.com/lo-shu-grid-calculator"

MISSING = [
    (1, "Communication", "Difficulty expressing thoughts clearly, and asserting needs out loud. Often deeply thoughtful, but the thinking stays internal.", "Journalling, writing regularly, deliberate practice at speaking up."),
    (2, "Intuition and sensitivity", "Less natural emotional attunement. Non-verbal cues get missed, which can read as coldness from someone who genuinely cares.", "Meditation, listening practice, unhurried time in nature."),
    (3, "Action and social energy", "Initiative and spontaneity take effort. The instinct is to think it through once more before moving.", "Physical exercise, group activity, committing to act before feeling ready."),
    (4, "Practical organisation", "Systems, routines and disciplined follow-through are the weak point. Strong on ideas, inconsistent on implementation.", "Planning tools, accountability partners, small daily habits."),
    (5, "Balance and centre", "The most significant absence, since 5 sits at the centre of the grid. Its lack pulls behaviour toward extremes.", "Conscious moderation, breathwork, mindfulness."),
    (6, "Creative expression and home", "Domestic harmony, beauty and creative outlets get deprioritised, usually in favour of work.", "Creative hobbies, home projects, deliberately protected family time."),
    (7, "Spiritual awareness", "Little natural pull toward reflection or the unprovable. The worldview stays material.", "Philosophy and spiritual reading, regular solitude, meditation."),
    (8, "Material practicality", "Managing money and physical-world systems does not come naturally.", "Financial literacy, studying property, working with practical people."),
    (9, "Humanitarian breadth", "Focus narrows. The big picture and other people's vantage points are harder to hold.", "Volunteering, reading widely across disciplines, travel."),
]

LINES = [
    ("4-9-2", "Top row", "Arrow of the Mind", "Planning, memory and imagination work together.", "Arrow of Poor Memory", "Thoughts scatter before they finish forming."),
    ("3-5-7", "Middle row", "Arrow of Emotional Balance", "Feeling, centre and reflection are all available.", "Arrow of Scepticism", "Learns by trial and error rather than trust."),
    ("8-1-6", "Bottom row", "Arrow of Practicality", "Ideas reliably become finished things.", "Arrow of Disorder", "Follow-through needs external structure."),
    ("4-3-8", "Left column", "Arrow of Planning", "Naturally organises work into steps.", "Arrow of Confusion", "Order has to be imposed deliberately."),
    ("9-5-1", "Middle column", "Arrow of Determination", "Decides, and holds the decision.", "Arrow of Hesitation", "Choices get revisited long after they are made."),
    ("2-7-6", "Right column", "Arrow of Activity", "Emotion converts into visible output.", "Arrow of Passivity", "Waits for momentum instead of starting it."),
    ("4-5-6", "Diagonal", "Arrow of Compassion", "Reads other people generously and accurately.", "Arrow of Hypersensitivity", "Takes correction harder than it is meant."),
    ("2-5-8", "Diagonal", "Arrow of Spiritual Insight", "Comfortable with what cannot be proven.", "Arrow of Frustration", "Effort and reward feel chronically out of step."),
]

FAQ = [
    ("What is a Lo Shu grid?",
     "A 3x3 magic square from ancient China, arranged 4-9-2 / 3-5-7 / 8-1-6, where every row, column and diagonal sums to 15. In numerology the digits of your date of birth are plotted onto it to show which energies you carry in abundance and which are absent."),
    ("How do I calculate my Lo Shu grid?",
     "Write your date of birth in full, then place every digit into its matching cell. A digit appearing three times is written three times, because repetition intensifies that energy. Zero is never plotted; it represents absence. Any cell left empty is a missing number."),
    ("What do missing numbers in the Lo Shu grid mean?",
     "They mark energies you have less of by default, so they must be developed deliberately rather than relied on. They are lessons, not defects. Missing 5 matters most, since 5 is the centre of the grid and governs balance."),
    ("What are the arrows in a Lo Shu grid?",
     "The grid contains exactly eight straight lines: three rows, three columns and two diagonals. A line whose three cells are all filled is an arrow of strength. The same line with all three cells empty is the matching arrow of weakness, such as the Arrow of Frustration when 2, 5 and 8 are all absent."),
    ("Is the Lo Shu grid the same as Chaldean numerology?",
     "No, and they answer different questions. Chaldean reduces you to single numbers with planetary rulers, such as Moolank and Bhagyank. Lo Shu ignores reduction and shows the pattern of your digits instead. Read together, one gives the vibration and the other gives its distribution."),
    ("Does a repeated number in the Lo Shu grid make it stronger?",
     "Usually, but not without limit. Two of a digit strengthens it. Three or more tends to overexpress it, so the trait starts to work against the person, for example a triple 1 becoming difficulty staying quiet rather than strong communication."),
]


def chrome():
    s = open(SRC, encoding="utf-8").read()
    nav = re.search(r'<nav class="nav".*?</nav>', s, re.S).group(0)
    footer = re.search(r"<footer.*?</footer>", s, re.S).group(0)
    head_links = "\n".join(re.findall(r'<link rel="stylesheet" href="[^"]*">', s))
    scripts = "\n".join(re.findall(r'<script src="/assets/[^"]*"[^>]*></script>', s))
    return nav, footer, head_links, scripts


def jsonld():
    faq = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (jstr(q), jstr(a)) for q, a in FAQ)
    return f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebApplication","name":"Lo Shu Grid Calculator","url":"{URL}","description":{jstr(DESC)},"applicationCategory":"LifestyleApplication","operatingSystem":"Any","offers":{{"@type":"Offer","price":"0","priceCurrency":"INR"}},"publisher":{{"@type":"Organization","name":"NameAligned.com","url":"https://www.namealigned.com/"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.namealigned.com/"}},
{{"@type":"ListItem","position":2,"name":"Lo Shu Grid Calculator","item":"{URL}"}}
]}}
</script>"""


def jstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def e(s):
    return html.escape(s, quote=False)


def build():
    nav, footer, head_links, scripts = chrome()

    missing_rows = "\n".join(
        f'    <div class="loshu-miss"><div class="loshu-miss-n">{n}</div>'
        f'<div><strong>Missing {n}, {e(t)}.</strong> {e(d)} '
        f'<span class="loshu-remedy">Develop it through: {e(r)}</span></div></div>'
        for n, t, d, r in MISSING)

    line_rows = "\n".join(
        f"      <tr><td><code>{c}</code></td><td>{e(ax)}</td>"
        f"<td><strong>{e(sn)}</strong><br><span class=\"loshu-dim\">{e(sd)}</span></td>"
        f"<td><strong>{e(wn)}</strong><br><span class=\"loshu-dim\">{e(wd)}</span></td></tr>"
        for c, ax, sn, sd, wn, wd in LINES)

    faq_html = "\n".join(
        f"    <details class=\"loshu-faq\"><summary>{e(q)}</summary><p>{e(a)}</p></details>"
        for q, a in FAQ)

    return f"""<!DOCTYPE html><html lang="en"><head>
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
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<link rel="alternate" hreflang="en-IN" href="{URL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://www.namealigned.com/assets/og/moolank-5.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
{head_links}
{jsonld()}
<style>
  .loshu-wrap{{max-width:760px;margin:0 auto}}
  .loshu-form{{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;justify-content:center;margin:1.4rem 0}}
  .loshu-form label{{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;color:#4a3f6b;text-align:left}}
  .loshu-form input{{font:inherit;font-size:16px;padding:11px 14px;border:1px solid rgba(124,58,237,.28);border-radius:10px;background:#fff;color:#19142d}}
  .loshu-form input:focus{{outline:0;border-color:#f0b429}}
  #loshuOut{{display:none;margin-top:1.8rem}}
  #loshuOut.show{{display:block}}
  .loshu-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:330px;margin:0 auto 1.2rem}}
  .loshu-cell{{aspect-ratio:1;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border:1px solid rgba(124,58,237,.14);background:rgba(124,58,237,.04)}}
  .loshu-cell.on{{border-color:rgba(245,196,81,.75);background:linear-gradient(135deg,rgba(245,196,81,.20),rgba(245,196,81,.06))}}
  .loshu-cell .d{{font-family:'Playfair Display',Georgia,serif;font-size:26px;font-weight:700;line-height:1;color:rgba(124,58,237,.32)}}
  .loshu-cell.on .d{{color:#b4801a}}
  .loshu-cell .rep{{font-size:11px;font-weight:700;letter-spacing:.08em;color:#b4801a;min-height:13px}}
  .loshu-cell .lb{{font-size:9.5px;text-transform:uppercase;letter-spacing:.09em;color:#8a7ba8}}
  .loshu-sum{{background:rgba(124,58,237,.05);border:1px solid rgba(124,58,237,.14);border-radius:12px;padding:14px 16px;margin-bottom:1rem;font-size:14.5px;line-height:1.6}}
  .loshu-pill{{display:inline-block;font-size:12px;font-weight:700;border-radius:999px;padding:3px 10px;margin:2px 4px 2px 0}}
  .loshu-pill.good{{background:rgba(46,160,110,.12);color:#1f7a52}}
  .loshu-pill.warn{{background:rgba(214,109,32,.12);color:#a1521a}}
  .loshu-pill.none{{background:rgba(124,58,237,.08);color:#6d4ed1}}
  .loshu-miss{{display:flex;gap:12px;padding:11px 0;border-top:1px solid rgba(124,58,237,.10);font-size:14.5px;line-height:1.6}}
  .loshu-miss-n{{flex:0 0 30px;height:30px;border-radius:50%;background:rgba(124,58,237,.09);color:#6d4ed1;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:14px}}
  .loshu-remedy{{color:#6b5f86;font-style:italic}}
  .loshu-table{{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:.6rem}}
  .loshu-table th,.loshu-table td{{text-align:left;padding:9px 10px;border-bottom:1px solid rgba(124,58,237,.12);vertical-align:top}}
  .loshu-table th{{font-size:11.5px;text-transform:uppercase;letter-spacing:.08em;color:#6b5f86}}
  .loshu-table code{{background:rgba(124,58,237,.07);border-radius:5px;padding:2px 6px;font-size:12.5px;color:#6d4ed1;white-space:nowrap}}
  .loshu-dim{{color:#6b5f86}}
  .loshu-faq{{border-bottom:1px solid rgba(124,58,237,.12);padding:11px 0}}
  .loshu-faq summary{{cursor:pointer;font-weight:600;color:#2d2450;font-size:15px}}
  .loshu-faq p{{margin:.6rem 0 0;color:#4a3f6b;font-size:14.5px;line-height:1.65}}
  @media(max-width:520px){{.loshu-table th:nth-child(2),.loshu-table td:nth-child(2){{display:none}}}}
</style>
</head>
<body>

{nav}

<nav class="na-breadcrumb" aria-label="Breadcrumb">
  <a href="/">Home</a><span>/</span><a href="/sitemap-pages">Site Map</a><span>/</span><span>Lo Shu Grid Calculator</span>
</nav>

<main>

<section class="tool-hero">
  <div class="eyebrow">&#10022; Free &bull; Instant &bull; No signup</div>
  <h1>Lo Shu Grid Calculator <em>plot your 3&times;3 grid from your date of birth</em></h1>
  <p>Enter your date of birth and see the full grid: which digits repeat, which are missing entirely, how your three planes sit, and which of the eight arrows your birth date forms.</p>
</section>

<section class="section loshu-wrap" style="padding-top:1rem">
  <form class="loshu-form" id="loshuForm" autocomplete="off">
    <label>Date of birth
      <input type="date" id="loshuDob" required>
    </label>
    <button type="submit" class="btn btn-gold">Plot my grid</button>
  </form>

  <div id="loshuOut" aria-live="polite">
    <div class="loshu-grid" id="loshuGridEl"></div>
    <div class="loshu-sum" id="loshuMissEl"></div>
    <div class="loshu-sum" id="loshuPlaneEl"></div>
    <div class="loshu-sum" id="loshuArrowEl"></div>
    <p style="font-size:13.5px;color:#6b5f86;text-align:center">
      Lo Shu shows the pattern. For the planetary side, run the
      <a href="/analyzer">free Chaldean analysis</a> for your Moolank and Bhagyank.
    </p>
  </div>
</section>

<section class="section loshu-wrap">
  <h2>How to plot a Lo Shu grid by hand</h2>
  <p>The layout never changes. It is a magic square, so every row, column and diagonal adds to 15:</p>
  <div class="loshu-grid" aria-hidden="true">
    <div class="loshu-cell on"><span class="d">4</span><span class="lb">Will</span></div>
    <div class="loshu-cell on"><span class="d">9</span><span class="lb">Intellect</span></div>
    <div class="loshu-cell on"><span class="d">2</span><span class="lb">Intuition</span></div>
    <div class="loshu-cell on"><span class="d">3</span><span class="lb">Action</span></div>
    <div class="loshu-cell on"><span class="d">5</span><span class="lb">Balance</span></div>
    <div class="loshu-cell on"><span class="d">7</span><span class="lb">Sacrifice</span></div>
    <div class="loshu-cell on"><span class="d">8</span><span class="lb">Practical</span></div>
    <div class="loshu-cell on"><span class="d">1</span><span class="lb">Communication</span></div>
    <div class="loshu-cell on"><span class="d">6</span><span class="lb">Creativity</span></div>
  </div>
  <p>Take every digit of your full date of birth and mark it in its cell. Repetition is not collapsed: a digit that appears three times is written three times, because repeats intensify that energy. Zero is never plotted, it stands for absence. Whatever cell stays empty is a <strong>missing number</strong>.</p>
  <p>Worked example, 14 May 1985. The digits are 1, 4, 0, 5, 1, 9, 8, 5. Dropping the zero leaves 1 twice, 5 twice, and one each of 4, 8 and 9. Cells 2, 3, 6 and 7 stay empty, so those are the missing numbers.</p>
</section>

<section class="section loshu-wrap">
  <h2>The three planes</h2>
  <p>The grid is read in horizontal bands as well as cell by cell.</p>
  <ul>
    <li><strong>Top row, 4-9-2, the mental plane.</strong> How the person thinks, plans and imagines.</li>
    <li><strong>Middle row, 3-5-7, the emotional plane.</strong> Sensitivity, balance and inner life. The most revealing row for emotional intelligence.</li>
    <li><strong>Bottom row, 8-1-6, the physical plane.</strong> How effectively the person acts in the material world.</li>
  </ul>
  <p>A full row means strong energy in that plane. An empty row marks an area needing conscious development. A full row with several repeats suggests overdevelopment: the energy dominates, but without much counterweight.</p>
</section>

<section class="section loshu-wrap">
  <h2>All eight arrows</h2>
  <p>The grid contains exactly eight straight lines, three rows, three columns and two diagonals. Three filled cells on a line form an <strong>arrow of strength</strong>; the same line left entirely empty is the matching <strong>arrow of weakness</strong>. No other combination is an arrow, because no other set of three cells sits in a straight line.</p>
  <div style="overflow-x:auto">
    <table class="loshu-table">
      <thead><tr><th>Line</th><th>Position</th><th>All three present</th><th>All three absent</th></tr></thead>
      <tbody>
{line_rows}
      </tbody>
    </table>
  </div>
</section>

<section class="section loshu-wrap">
  <h2>What each missing number means</h2>
  <p>A missing number is not a defect. It marks an energy you carry less of by default, so it has to be built deliberately instead of relied on.</p>
{missing_rows}
</section>

<section class="section loshu-wrap">
  <h2>Lo Shu and Chaldean together</h2>
  <p>The two systems answer different questions, which is why they are worth running side by side. Chaldean reduces you to single numbers with planetary rulers, your <a href="/blog/moolank-meanings">Moolank</a> from the day of birth and your <a href="/life-path-number-1-meaning">Bhagyank</a> from the full date. Lo Shu refuses to reduce, and shows the distribution instead.</p>
  <p>The combination is where it gets useful. Someone with Moolank 5 carries Mercury's quick, communicative energy, but if 1 is missing from their grid, self-expression is still the thing they have to work at consciously. The vibration says one thing, the pattern qualifies it.</p>
  <p>For the full Chaldean side, including name number and compound number, run the <a href="/analyzer">free analysis</a> or read the <a href="/blog/lo-shu-grid-guide">long-form Lo Shu guide</a>.</p>
</section>

<section class="section loshu-wrap">
  <h2>Common questions</h2>
{faq_html}
</section>

<section class="section loshu-wrap">
  <h2>Keep reading</h2>
  <ul>
    <li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid Explained</a>, the long-form guide with origins and worked detail.</li>
    <li><a href="/blog/moolank-meanings">Moolank 1-9</a>, what your day-of-birth number means.</li>
    <li><a href="/blog/chaldean-numerology-guide">Complete Chaldean Numerology Guide</a>.</li>
    <li><a href="/methodology">Our methodology</a>, exactly how each number is calculated.</li>
  </ul>
</section>

</main>

{footer}

<script src="/assets/numerology.js" defer=""></script>
{scripts}
<script>
document.addEventListener('DOMContentLoaded', function () {{
  var form = document.getElementById('loshuForm');
  var out  = document.getElementById('loshuOut');
  var LABEL = {{1:'Communication',2:'Intuition',3:'Action',4:'Will',5:'Balance',6:'Creativity',7:'Sacrifice',8:'Practical',9:'Intellect'}};

  function pills(list, cls) {{
    if (!list.length) return '<span class="loshu-pill none">None</span>';
    return list.map(function (a) {{
      return '<span class="loshu-pill ' + cls + '" title="' + a.note + '">' + a.name + ' (' + a.cells.join('-') + ')</span>';
    }}).join('');
  }}

  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var dob = document.getElementById('loshuDob').value;
    if (!dob) return;

    var counts  = getLoshuCounts(dob);
    var missing = getLoshuMissing(dob);
    var arrows  = getLoshuArrows(counts);
    var planes  = getLoshuPlanes(counts);

    document.getElementById('loshuGridEl').innerHTML = [].concat.apply([], LOSHU_GRID).map(function (n) {{
      var c = counts[n];
      return '<div class="loshu-cell' + (c ? ' on' : '') + '">' +
             '<span class="d">' + (c ? String(n).repeat(Math.min(c, 3)) : n) + '</span>' +
             '<span class="rep">' + (c > 1 ? '&times;' + c : '') + '</span>' +
             '<span class="lb">' + LABEL[n] + '</span></div>';
    }}).join('');

    document.getElementById('loshuMissEl').innerHTML = missing.length
      ? '<strong>Missing numbers:</strong> ' + missing.join(', ') +
        '. These are the energies to build deliberately, explained below.'
      : '<strong>No missing numbers.</strong> Every one of the nine energies appears in your date of birth, which is uncommon.';

    document.getElementById('loshuPlaneEl').innerHTML = '<strong>Planes:</strong> ' + planes.map(function (p) {{
      return '<span class="loshu-pill ' + (p.state === 'complete' ? 'good' : p.state === 'empty' ? 'warn' : 'none') +
             '">' + p.name + ' ' + p.filled + '/3</span>';
    }}).join('');

    document.getElementById('loshuArrowEl').innerHTML =
      '<strong>Arrows of strength:</strong> ' + pills(arrows.strength, 'good') +
      '<br style="margin-bottom:6px"><strong>Arrows of weakness:</strong> ' + pills(arrows.weakness, 'warn');

    out.classList.add('show');
    if (typeof gtag === 'function') gtag('event', 'loshu_grid_plotted', {{ missing: missing.length }});
  }});
}});
</script>

</body></html>
"""


def main():
    open(OUT, "w", encoding="utf-8").write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    sys.exit(main())
