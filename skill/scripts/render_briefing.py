#!/usr/bin/env python3
"""
Renders one day's Ankit's Morning Briefing HTML page from a content JSON file.

Usage:
    python3 render_briefing.py --data content.json --date 2026-07-29 \
        --display-date "Wednesday, July 29, 2026" --out briefings/2026-07-29.html

content.json shape:
{
  "skim": ["one-line takeaway", ...],          # optional, 5 items ideal
  "sections": [
    {"key": "world", "title": "World", "icon": "news", "stories": [...]},
    {"key": "sports", "title": "Sports", "icon": "trophy", "stories": [...]},
    {"key": "business", ...}, {"key": "ai", ...}, {"key": "geopolitics", ...}
  ],
  "fixtures": [                                  # optional; renders inside Sports
    {"sport": "Cricket", "headline": "...", "body": "...", "url": "...", "when": "Aug 15-19"}
  ],
  "portfolio": [                                 # optional; own section
    {"ticker": "NVDA", "company": "Nvidia", "headline": "...", "body": "...",
     "img": "... or null", "url": "..."}
  ],
  "country_groups": [
    {"label": "India", "stories": [...]},
    {"label": "United Kingdom", "stories": [...]},
    {"label": "Qatar & the GCC", "stories": [...]}
  ],
  "doha_events": [...]
}

Story shape: {"headline", "body", "img" (URL or null), "url", "continues" (optional bool)}

Set "continues": true on a story that follows up on one from a previous edition —
it renders a small CONTINUING tag. That is the whole point of keeping an archive:
the reader should be able to see at a glance what is genuinely new versus what is
the next chapter of something they already read.

Never invent an image URL. Leave "img" null and the fallback line-art icon renders.
"""

import argparse
import json

ICONS = {
    "trophy": '<path d="M8 21h8M12 17v4M7 4h10v4a5 5 0 0 1-10 0V4Z"/><path d="M7 5H4a3 3 0 0 0 3 3M17 5h3a3 3 0 0 1-3 3"/>',
    "bars": '<path d="M4 20V11M10 20V4M16 20v-6M22 20H2"/>',
    "cpu": '<rect x="7" y="7" width="10" height="10" rx="1"/><path d="M9 1v4M15 1v4M9 19v4M15 19v4M1 9h4M1 15h4M19 9h4M19 15h4"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a13.5 13.5 0 0 1 0 18"/><path d="M12 3a13.5 13.5 0 0 0 0 18"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h13l-3 4 3 4H5"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "news": '<path d="M4 6h12v14H4z"/><path d="M16 10h4v8a2 2 0 0 1-2 2H4"/><path d="M7 9.5h6M7 12.5h6M7 15.5h4"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M7 15l4-5 3 3 5-7"/>',
    "all": '<path d="M4 4h7v7H4z"/><path d="M13 4h7v7h-7z"/><path d="M4 13h7v7H4z"/><path d="M13 13h7v7h-7z"/>',
}

FALLBACK_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/>'
    '<circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>'
)

ACCENT_MAP = {
    "world": "#2B4257",
    "sports": "#B5563C",
    "business": "#A9822E",
    "ai": "#2C7A73",
    "geopolitics": "#3E5C8A",
    "portfolio": "#4F6B4A",
    "country": "#8C3A3A",
    "doha": "#6B4C7A",
}

PILLS = [
    {"key": "all", "label": "All", "icon": "all"},
    {"key": "world", "label": "World", "icon": "news"},
    {"key": "sports", "label": "Sports", "icon": "trophy"},
    {"key": "business", "label": "Business & Markets", "icon": "bars"},
    {"key": "ai", "label": "AI & Technology", "icon": "cpu"},
    {"key": "geopolitics", "label": "Geopolitics", "icon": "globe"},
    {"key": "portfolio", "label": "Market Watch", "icon": "chart"},
    {"key": "country", "label": "Country Updates", "icon": "flag"},
    {"key": "doha", "label": "Doha Events", "icon": "calendar"},
]


def svg_icon(name, cls=""):
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'
    )


def thumb_html(img):
    # The site is served over https, so an http:// image is silently blocked by
    # the browser as mixed content — it looks exactly like a broken photo and
    # produces no error anywhere. Upgrade rather than trust the source.
    if img and img.startswith("http://"):
        img = "https://" + img[len("http://"):]
    if img and not img.startswith("https://"):
        img = None
    if img:
        return (
            f'<div class="thumb"><img src="{img}" alt="" referrerpolicy="no-referrer" loading="lazy" '
            f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\';">'
            f'<div class="thumb-fallback">{FALLBACK_ICON}</div></div>'
        )
    return f'<div class="thumb"><div class="thumb-fallback" style="display:flex;">{FALLBACK_ICON}</div></div>'


def story_card(story, num, section_key, chip=None):
    tags = ""
    if story.get("continues"):
        tags += '<span class="continuing">Continuing</span>'
    chip_html = f'<span class="ticker-chip">{chip}</span>' if chip else ""
    meta = f'<div class="card-meta"><div class="num">{num:02d}</div>{chip_html}{tags}</div>'
    return f'''
        <article class="card" data-cat="{section_key}">
          {thumb_html(story.get("img"))}
          <div class="card-body">
            {meta}
            <h3 class="headline">{story["headline"]}</h3>
            <p class="story-text">{story["body"]}</p>
            <a class="read-more" href="{story["url"]}" target="_blank" rel="noopener noreferrer">Read more &rarr;</a>
          </div>
        </article>'''


def render_fixtures(fixtures):
    if not fixtures:
        return ""
    rows = []
    for f in fixtures:
        rows.append(f'''
          <a class="fixture" href="{f["url"]}" target="_blank" rel="noopener noreferrer">
            <span class="fixture-sport">{f["sport"]}</span>
            <span class="fixture-main">
              <span class="fixture-headline">{f["headline"]}</span>
              <span class="fixture-body">{f["body"]}</span>
            </span>
            <span class="fixture-when">{f["when"]}</span>
          </a>''')
    return f'''
      <div class="fixtures-block">
        <h3 class="subblock-label">Fixtures Ahead</h3>
        <div class="fixture-list">{"".join(rows)}</div>
      </div>'''


def render_section(section, fixtures=None):
    key = section["key"]
    icon = svg_icon(section["icon"], "section-icon")
    cards = "\n".join(story_card(s, i + 1, key) for i, s in enumerate(section["stories"]))
    extra = render_fixtures(fixtures) if key == "sports" else ""
    return f'''
    <section class="news-section" id="sec-{key}" data-section="{key}" data-cat="{key}">
      <div class="section-head">
        {icon}
        <h2>{section["title"]}</h2>
      </div>
      <div class="card-grid">
        {cards}
      </div>
      {extra}
    </section>'''


def render_portfolio(portfolio):
    if not portfolio:
        return ""
    key = "portfolio"
    icon = svg_icon("chart", "section-icon")
    cards = "\n".join(
        story_card(s, i + 1, key, chip=s.get("ticker")) for i, s in enumerate(portfolio)
    )
    return f'''
    <section class="news-section" id="sec-{key}" data-section="{key}" data-cat="{key}">
      <div class="section-head">
        {icon}
        <h2>Market Watch</h2>
      </div>
      <p class="section-note">Companies on Ankit's watchlist where something actually happened today.</p>
      <div class="card-grid">
        {cards}
      </div>
    </section>'''


def render_country_section(country_groups):
    key = "country"
    icon = svg_icon("flag", "section-icon")
    groups_html = []
    for group in country_groups:
        cards = "\n".join(story_card(s, i + 1, key) for i, s in enumerate(group["stories"]))
        groups_html.append(f'''
      <div class="country-group">
        <h3 class="country-label">{group["label"]}</h3>
        <div class="card-grid">
          {cards}
        </div>
      </div>''')
    return f'''
    <section class="news-section" id="sec-{key}" data-section="{key}" data-cat="{key}">
      <div class="section-head">
        {icon}
        <h2>Country Updates</h2>
      </div>
      {"".join(groups_html)}
    </section>'''


def render_doha_section(doha_events):
    key = "doha"
    icon = svg_icon("calendar", "section-icon")
    cards = "\n".join(story_card(s, i + 1, key) for i, s in enumerate(doha_events))
    return f'''
    <section class="news-section" id="sec-{key}" data-section="{key}" data-cat="{key}">
      <div class="section-head">
        {icon}
        <h2>Doha Events</h2>
      </div>
      <div class="card-grid">
        {cards}
      </div>
    </section>'''


def render_skim(skim):
    if not skim:
        return ""
    items = "\n".join(
        f'<li><span class="skim-num">{i+1}</span><span>{s}</span></li>'
        for i, s in enumerate(skim)
    )
    return f'''
    <div class="skim">
      <h2 class="skim-title">The 30-Second Skim</h2>
      <ol class="skim-list">{items}</ol>
    </div>'''


def render_pills():
    items = []
    for p in PILLS:
        accent = ACCENT_MAP.get(p["key"], "#2E2C27")
        active_cls = " active" if p["key"] == "all" else ""
        items.append(
            f'<button class="pill{active_cls}" data-filter="{p["key"]}" style="--pill-accent:{accent}">'
            f'{svg_icon(p["icon"], "pill-icon")}<span>{p["label"]}</span></button>'
        )
    return "\n".join(items)


ACCENT_CSS = "\n".join(
    f'''  [data-section="{k}"] .section-icon, [data-section="{k}"] .num,
  [data-section="{k}"] .read-more {{ color: {v}; }}
  [data-section="{k}"] .card {{ border-left-color: {v}; }}
  [data-section="{k}"] .section-head h2 {{ border-bottom-color: {v}; }}
  [data-section="{k}"] .ticker-chip, [data-section="{k}"] .continuing {{
    color: {v}; border-color: {v}33; background: {v}0F; }}'''
    for k, v in ACCENT_MAP.items()
)

CSS = """
  :root {
    --ink: #2E2C27; --secondary: #6B6A63; --hairline: #E4E3DC;
    --wash: #F9F9F7; --white: #FCFCFB;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--white); color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased; }
  .band-top { background: var(--wash); border-bottom: 1px solid var(--hairline); }
  .band-bottom { background: var(--white); }
  .masthead { padding: 56px 32px 28px; text-align: center; }
  .masthead .eyebrow { font-size: 12.5px; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--secondary); margin: 0 0 14px; font-weight: 600; }
  .masthead h1 { font-family: Georgia, "Times New Roman", Times, serif; font-weight: 400;
    font-size: 46px; line-height: 1.15; margin: 0 0 12px; color: var(--ink); letter-spacing: -0.01em; }
  .masthead .date-line { font-family: Georgia, "Times New Roman", Times, serif; font-style: italic;
    font-size: 18px; color: var(--secondary); margin: 0; }
  .archive-nav { background: var(--ink); color: #fff; }
  .archive-nav .archive-nav-inner { max-width: 1180px; margin: 0 auto; padding: 10px 32px;
    display: flex; align-items: center; justify-content: space-between; font-size: 12.5px; }
  .archive-nav a { color: #fff; text-decoration: none; opacity: 0.85; font-weight: 600; letter-spacing: 0.02em; }
  .archive-nav a:hover { opacity: 1; text-decoration: underline; }
  .filter-bar { position: sticky; top: 0; z-index: 50; background: var(--wash);
    border-bottom: 1px solid var(--hairline); }
  .filter-inner { max-width: 1180px; margin: 0 auto; padding: 14px 32px; display: flex;
    flex-wrap: wrap; gap: 10px; justify-content: center; }
  .pill { display: inline-flex; align-items: center; gap: 7px; padding: 8px 16px; border-radius: 999px;
    border: 1px solid var(--hairline); background: var(--white); color: var(--secondary);
    font-size: 13.5px; font-weight: 600; cursor: pointer; transition: all 0.15s ease; white-space: nowrap; }
  .pill:hover { border-color: var(--pill-accent, var(--ink)); color: var(--ink); }
  .pill.active { background: var(--pill-accent, var(--ink)); border-color: var(--pill-accent, var(--ink)); color: #fff; }
  .pill-icon { width: 15px; height: 15px; flex: none; }
  .content-band { padding: 40px 0 80px; }

  .skim { max-width: 1180px; margin: 0 auto 12px; padding: 26px 32px 28px; }
  .skim-title { font-family: Georgia, serif; font-weight: 400; font-size: 22px; margin: 0 0 18px;
    color: var(--ink); }
  .skim-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 11px; }
  .skim-list li { display: flex; gap: 13px; align-items: baseline; font-size: 15.5px;
    line-height: 1.55; color: #4A4943; }
  .skim-num { font-family: Georgia, serif; font-weight: 700; font-size: 13px; color: var(--secondary);
    flex: none; width: 16px; }

  .news-section { max-width: 1180px; margin: 0 auto; padding: 44px 32px 8px; scroll-margin-top: 80px; }
  .section-head { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
  .section-icon { width: 26px; height: 26px; flex: none; }
  .section-head h2 { font-family: Georgia, "Times New Roman", Times, serif; font-weight: 400;
    font-size: 27px; margin: 0; padding-bottom: 12px; border-bottom: 2px solid var(--ink); flex: 1; }
  .section-note { font-size: 13.5px; color: var(--secondary); margin: 14px 0 0; font-style: italic; }
  .country-group { margin-top: 26px; }
  .country-label { font-family: Georgia, "Times New Roman", Times, serif; font-style: italic;
    font-weight: 400; font-size: 19px; color: #8C3A3A; margin: 0 0 16px; }

  .card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 22px; }
  .card { display: flex; flex-direction: column; border: 1px solid var(--hairline);
    border-left: 3px solid var(--ink); border-radius: 10px; overflow: hidden; background: var(--white); }
  .thumb { position: relative; width: 100%; aspect-ratio: 16 / 9; background: #F1F0EA; overflow: hidden; }
  .thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .thumb-fallback { display: none; position: absolute; inset: 0; align-items: center; justify-content: center;
    color: var(--secondary); background: #F1F0EA; }
  .thumb-fallback svg { width: 34px; height: 34px; }
  .card-body { padding: 16px 20px 20px; display: flex; flex-direction: column; gap: 8px; }
  .card-meta { display: flex; align-items: center; gap: 9px; }
  .num { font-family: Georgia, "Times New Roman", Times, serif; font-size: 15px; font-weight: 700; }
  .ticker-chip, .continuing { font-size: 10.5px; font-weight: 700; letter-spacing: 0.06em;
    text-transform: uppercase; padding: 3px 8px; border-radius: 4px; border: 1px solid; }
  .headline { font-size: 17px; line-height: 1.35; margin: 0; font-weight: 700; color: var(--ink); }
  .story-text { font-size: 14.5px; line-height: 1.6; color: #4A4943; margin: 0; }
  .read-more { margin-top: 4px; font-size: 13.5px; font-weight: 700; text-decoration: none; }
  .read-more:hover { text-decoration: underline; }

  .fixtures-block { margin-top: 30px; }
  .subblock-label { font-family: Georgia, serif; font-style: italic; font-weight: 400;
    font-size: 18px; color: #B5563C; margin: 0 0 14px; }
  .fixture-list { display: grid; gap: 1px; background: var(--hairline);
    border: 1px solid var(--hairline); border-radius: 10px; overflow: hidden; }
  .fixture { display: grid; grid-template-columns: 92px 1fr auto; gap: 16px; align-items: baseline;
    padding: 14px 18px; background: var(--white); text-decoration: none; color: inherit; }
  .fixture:hover { background: var(--wash); }
  .fixture-sport { font-size: 10.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
    color: #B5563C; }
  .fixture-headline { display: block; font-size: 15px; font-weight: 700; margin-bottom: 3px; }
  .fixture-body { display: block; font-size: 13.5px; line-height: 1.55; color: #4A4943; }
  .fixture-when { font-family: Georgia, serif; font-size: 13px; font-weight: 700; color: var(--secondary);
    white-space: nowrap; }

  footer.masthead-footer { max-width: 1180px; margin: 24px auto 0; padding: 20px 32px 60px;
    color: var(--secondary); font-size: 12.5px; text-align: center; border-top: 1px solid var(--hairline); }
  @media (max-width: 760px) {
    .archive-nav .archive-nav-inner { padding: 9px 18px; font-size: 11.5px; }
    .masthead { padding: 40px 20px 22px; } .masthead h1 { font-size: 32px; } .masthead .date-line { font-size: 15px; }
    .news-section, .filter-inner, .skim, footer.masthead-footer { padding-left: 18px; padding-right: 18px; }
    .card-grid { grid-template-columns: 1fr; } .pill { padding: 7px 12px; font-size: 12.5px; }
    .section-head h2 { font-size: 23px; }
    .fixture { grid-template-columns: 1fr; gap: 5px; }
    .fixture-when { font-size: 12.5px; }
  }
  .hidden-by-filter { display: none !important; }
"""

JS = """
(function () {
  var pills = document.querySelectorAll('.pill');
  var sections = document.querySelectorAll('.news-section');
  pills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      pills.forEach(function (p) { p.classList.remove('active'); });
      pill.classList.add('active');
      var filter = pill.getAttribute('data-filter');
      sections.forEach(function (sec) {
        if (filter === 'all' || sec.getAttribute('data-section') === filter) {
          sec.classList.remove('hidden-by-filter');
        } else {
          sec.classList.add('hidden-by-filter');
        }
      });
    });
  });
})();
"""


def build_html(data, display_date, archive_rel="../index.html"):
    body = render_skim(data.get("skim"))
    fixtures = data.get("fixtures")
    for s in data["sections"]:
        body += "\n" + render_section(s, fixtures=fixtures)
    body += "\n" + render_portfolio(data.get("portfolio"))
    body += "\n" + render_country_section(data["country_groups"])
    body += "\n" + render_doha_section(data["doha_events"])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ankit's Morning Briefing — {display_date}</title>
<style>{CSS}
{ACCENT_CSS}
</style>
</head>
<body>

<div class="archive-nav">
  <div class="archive-nav-inner">
    <a href="{archive_rel}">&larr; All Briefings</a>
    <div class="nav-links"><span style="opacity:.7;">{display_date}</span></div>
  </div>
</div>

<div class="band-top">
  <div class="masthead">
    <p class="eyebrow">Doha, Qatar</p>
    <h1>Ankit's Morning Briefing</h1>
    <p class="date-line">{display_date}</p>
  </div>
  <div class="filter-bar">
    <div class="filter-inner">
{render_pills()}
    </div>
  </div>
</div>

<div class="band-bottom">
  <div class="content-band">
{body}
  </div>
  <footer class="masthead-footer">
    Compiled from public reporting for Ankit &middot; Doha, Qatar &middot; {display_date}
  </footer>
</div>

<script>{JS}</script>
</body>
</html>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--display-date", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--archive-rel", default="../index.html")
    args = ap.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    html = build_html(data, args.display_date, args.archive_rel)
    with open(args.out, "w") as f:
        f.write(html)
    print(f"Wrote {args.out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
