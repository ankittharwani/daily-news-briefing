#!/usr/bin/env python3
"""
Renders one day's edition of The Date Line (Ankit's morning briefing) as a
single self-contained HTML page.

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

The first story of the first section is the day's LEAD: its headline renders at
display size under the masthead, above everything else. Order the World stories
so the most consequential one is first. Every skim line renders in full below.

Set "continues": true on a story that follows up on one from a previous edition —
it renders a small CONTINUING tag. That is the whole point of keeping an archive:
the reader should be able to see at a glance what is genuinely new versus what is
the next chapter of something they already read.

The "icon" key on a section is accepted but unused — the design carries section
identity through an accent rule rather than a glyph.

Never invent an image URL. Leave "img" null and the story renders as a text-led
card with no image well at all, which is the intended look, not a degraded one.
"""

import argparse
import html
import itertools
import json

_ID_SEQ = itertools.count(1)


def next_id(prefix):
    """A stable, page-unique anchor id for a card or fixture — used both as the
    DOM id share links jump to and as the fragment in the copied/shared URL."""
    return f"{prefix}-{next(_ID_SEQ)}"


def share_title(headline):
    """Story headlines are authored as raw inline HTML (entities like &rsquo;).
    Round-trip through unescape+escape so the data-share-title attribute holds
    a real quote/apostrophe character (what navigator.share should display),
    while staying safe to embed inside a double-quoted HTML attribute."""
    return html.escape(html.unescape(headline), quote=True)


# --- Identity ---------------------------------------------------------------
#
# The dL monogram: one vertical stroke serves as both the d's ascender and the
# L's stem, and runs on past the letter at top and bottom — that overrun is the
# date line. Drawn in currentColor with the bowl's counter punched out via
# evenodd, so the same markup reverses on ink and prints on paper.
MARK_SVG = (
    '<svg class="mark" viewBox="11 3 42 58" fill="currentColor" aria-hidden="true">'
    '<path fill-rule="evenodd" d="M24 22a11 11 0 1 0 0 22 11 11 0 1 0 0-22Zm-.6 3a5.6 8 0 1 0 0 16 5.6 8 0 1 0 0-16Z"/><rect x="36" y="40.6" width="15" height="3.4"/><rect x="30" y="5" width="2.5" height="54"/><rect x="33.5" y="5" width="2.5" height="54"/><rect x="30" y="5" width="6" height="1.5"/><rect x="30" y="8" width="6" height="2"/><rect x="30" y="11.5" width="6" height="2"/><rect x="30" y="15" width="6" height="2"/><rect x="30" y="18.5" width="6" height="2"/><rect x="30" y="22" width="6" height="2"/><rect x="30" y="25.5" width="6" height="2"/><rect x="30" y="29" width="6" height="2"/><rect x="30" y="32.5" width="6" height="2"/><rect x="30" y="36" width="6" height="2"/><rect x="30" y="39.5" width="6" height="2"/><rect x="30" y="43" width="6" height="2"/><rect x="30" y="46.5" width="6" height="2"/><rect x="30" y="50" width="6" height="2"/><rect x="30" y="53.5" width="6" height="2"/><rect x="30" y="57" width="6" height="0.5"/><rect x="30" y="57.5" width="6" height="1.5"/>'
    "</svg>"
)

SHARE_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/>'
    '<circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>'
    '<path d="M8.59 13.51l6.83 3.98M15.41 6.51L8.59 10.49"/></svg>'
)

SUN_ICON = (
    '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/>'
    '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
)

MOON_ICON = (
    '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5Z"/></svg>'
)

TOP_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>'
)

# The fallback when a story has no verified photograph: the mark itself, at low
# contrast. A missing image should read as this publication's own furniture
# rather than as a broken-image glyph borrowed from somewhere else.
FALLBACK_MARK = (
    '<svg class="mark" viewBox="11 3 42 58" fill="currentColor" aria-hidden="true">'
    '<path fill-rule="evenodd" d="M24 22a11 11 0 1 0 0 22 11 11 0 1 0 0-22Z'
    'm-.6 3a5.6 8 0 1 0 0 16 5.6 8 0 1 0 0-16Z"/>'
    '<rect x="36" y="40.6" width="15" height="3.4"/>'
    '<rect x="30" y="5" width="6" height="54"/>'
    "</svg>"
)

# Each section accent ships a light- and dark-mode value; the dark value is
# lifted so it still clears contrast on a near-black ground. Accents appear as
# rules and small mono labels only — never as a filled pill or a coloured card
# border. The gold is the publication's own and belongs to the masthead rules
# and the LEAD marker, so it is deliberately not any section's accent.
ACCENT_MAP = {
    "world":       {"light": "#2B4257", "dark": "#7FA5CC"},
    "sports":      {"light": "#A8482C", "dark": "#E08863"},
    "business":    {"light": "#8A6A1E", "dark": "#D9AA55"},
    "ai":          {"light": "#1F6B64", "dark": "#5FBDB3"},
    "geopolitics": {"light": "#3E5C8A", "dark": "#8CACD6"},
    "portfolio":   {"light": "#47633F", "dark": "#8AB183"},
    "country":     {"light": "#8C3A3A", "dark": "#D97A7A"},
    "doha":        {"light": "#63456F", "dark": "#B08BC2"},
}
GOLD = {"light": "#856420", "dark": "#C9A24E"}

PILLS = [
    {"key": "all", "label": "All"},
    {"key": "world", "label": "World"},
    {"key": "sports", "label": "Sports"},
    {"key": "business", "label": "Business"},
    {"key": "ai", "label": "AI &amp; Tech"},
    {"key": "geopolitics", "label": "Geopolitics"},
    {"key": "portfolio", "label": "Market Watch"},
    {"key": "country", "label": "Country"},
    {"key": "doha", "label": "Doha"},
]


def thumb_html(img):
    # The site is served over https, so an http:// image is silently blocked by
    # the browser as mixed content — it looks exactly like a broken photo and
    # produces no error anywhere. Upgrade rather than trust the source.
    if img and img.startswith("http://"):
        img = "https://" + img[len("http://"):]
    if img and not img.startswith("https://"):
        img = None
    # A story with no verified photograph becomes a text-led card rather than a
    # card with an empty well in it — the ragged grid that produces is how a
    # newspaper page actually looks. The fallback below only covers an image
    # that was supplied and then failed to load.
    if not img:
        return ""
    return (
        f'<div class="thumb"><img src="{img}" alt="" referrerpolicy="no-referrer" loading="lazy" '
        f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\';">'
        f'<div class="thumb-fallback">{FALLBACK_MARK}</div></div>'
    )


def story_card(story, num, section_key, chip=None):
    tags = ""
    if story.get("continues"):
        tags += '<span class="tag continuing">Continuing</span>'
    chip_html = f'<span class="tag ticker">{chip}</span>' if chip else ""
    card_id = next_id("card")
    share_btn = (
        f'<button class="share-btn" data-share-id="{card_id}" '
        f'data-share-title="{share_title(story["headline"])}" '
        f'aria-label="Share this story" title="Share">{SHARE_ICON}</button>'
    )
    return f'''
        <article class="card" data-cat="{section_key}" id="{card_id}">
          {thumb_html(story.get("img"))}
          <div class="card-body">
            <div class="card-meta"><span class="num">{num:02d}</span>{chip_html}{tags}</div>
            <h3 class="headline"><a href="{story["url"]}" target="_blank" rel="noopener noreferrer">{story["headline"]}</a></h3>
            <p class="story-text">{story["body"]}</p>
            <div class="card-actions">
              <a class="read-more" href="{story["url"]}" target="_blank" rel="noopener noreferrer">Read more &rarr;</a>
              {share_btn}
            </div>
          </div>
        </article>'''


def render_fixtures(fixtures):
    if not fixtures:
        return ""
    rows = []
    for f in fixtures:
        fixture_id = next_id("fixture")
        share_btn = (
            f'<button class="share-btn fixture-share" data-share-id="{fixture_id}" '
            f'data-share-title="{share_title(f["headline"])}" '
            f'aria-label="Share this fixture" title="Share">{SHARE_ICON}</button>'
        )
        rows.append(f'''
          <div class="fixture" id="{fixture_id}">
            <span class="fixture-sport">{f["sport"]}</span>
            <a class="fixture-main" href="{f["url"]}" target="_blank" rel="noopener noreferrer">
              <span class="fixture-headline">{f["headline"]}</span>
              <span class="fixture-body">{f["body"]}</span>
            </a>
            <span class="fixture-when">{f["when"]}</span>
            {share_btn}
          </div>''')
    return f'''
      <div class="subblock">
        <h3 class="subblock-label">Fixtures Ahead</h3>
        <div class="fixture-list">{"".join(rows)}</div>
      </div>'''


def section_shell(key, title, body, note=""):
    note_html = f'<p class="section-note">{note}</p>' if note else ""
    return f'''
    <section class="news-section" id="sec-{key}" data-section="{key}" data-cat="{key}">
      <header class="section-head">
        <h2>{title}</h2>
      </header>
      {note_html}
      {body}
    </section>'''


def render_section(section, fixtures=None):
    key = section["key"]
    cards = "\n".join(story_card(s, i + 1, key) for i, s in enumerate(section["stories"]))
    extra = render_fixtures(fixtures) if key == "sports" else ""
    return section_shell(key, section["title"], f'<div class="card-grid">{cards}</div>{extra}')


def render_portfolio(portfolio):
    if not portfolio:
        return ""
    cards = "\n".join(
        story_card(s, i + 1, "portfolio", chip=s.get("ticker")) for i, s in enumerate(portfolio)
    )
    return section_shell(
        "portfolio",
        "Market Watch",
        f'<div class="card-grid">{cards}</div>',
        note="Companies on the watchlist where something actually happened today.",
    )


def render_country_section(country_groups):
    groups_html = []
    for group in country_groups:
        cards = "\n".join(story_card(s, i + 1, "country") for i, s in enumerate(group["stories"]))
        groups_html.append(f'''
      <div class="country-group">
        <h3 class="subblock-label">{group["label"]}</h3>
        <div class="card-grid">{cards}</div>
      </div>''')
    return section_shell("country", "Country Updates", "".join(groups_html))


def render_doha_section(doha_events):
    cards = "\n".join(story_card(s, i + 1, "doha") for i, s in enumerate(doha_events))
    return section_shell("doha", "Doha Events", f'<div class="card-grid">{cards}</div>')


def lead_story(data):
    """The first story of the first section — the day's lead by construction."""
    for section in data.get("sections", []):
        if section.get("stories"):
            return section["stories"][0]
    return None


def render_lead(data):
    """The lead is a headline, not a summary paragraph. Using the skim's first
    line here put a 47-word sentence at display scale and pushed the skim off
    the first screen on a phone."""
    story = lead_story(data)
    if not story:
        return ""
    return f'''
  <div class="lead">
    <span class="lead-tag">Lead</span>
    <a class="lead-text" href="{story["url"]}" target="_blank" rel="noopener noreferrer">{story["headline"]}</a>
  </div>'''


def render_skim(skim):
    """Every skim line, numbered from 01. The lead above is a story headline,
    not a skim item, so nothing is held back from this list."""
    if not skim:
        return ""
    items = "\n".join(
        f'<li><span class="skim-num">{i+1:02d}</span><span class="skim-text">{s}</span></li>'
        for i, s in enumerate(skim)
    )
    return f'''
    <div class="skim">
      <h2 class="block-label">The 30-Second Skim</h2>
      <ol class="skim-list">{items}</ol>
    </div>'''


def render_index():
    items = []
    for p in PILLS:
        active = " active" if p["key"] == "all" else ""
        items.append(
            f'<button class="index-link{active}" data-filter="{p["key"]}">{p["label"]}</button>'
        )
    return "\n".join(items)


def estimate_reading(data):
    """Word count across every story and skim line, at ~200 wpm, min 1 minute."""
    words = 0
    for item in data.get("skim") or []:
        words += len(item.split())
    for s in data.get("sections", []):
        for story in s["stories"]:
            words += len(story["body"].split())
    for story in data.get("portfolio") or []:
        words += len(story["body"].split())
    for group in data.get("country_groups", []):
        for story in group["stories"]:
            words += len(story["body"].split())
    for story in data.get("doha_events", []):
        words += len(story["body"].split())
    story_count = (
        sum(len(s["stories"]) for s in data.get("sections", []))
        + len(data.get("portfolio") or [])
        + sum(len(g["stories"]) for g in data.get("country_groups", []))
        + len(data.get("doha_events") or [])
    )
    return story_count, max(1, round(words / 200))


def accent_vars(theme):
    lines = [f"    --accent-{k}: {v[theme]};" for k, v in ACCENT_MAP.items()]
    lines.append(f"    --gold: {GOLD[theme]};")
    return "\n".join(lines)


# Every section-scoped rule reads one --accent variable, repointed per section,
# so recolouring or adding a section never touches a component rule.
ACCENT_CSS = "\n".join(
    f'  [data-section="{k}"] {{ --accent: var(--accent-{k}); }}' for k in ACCENT_MAP
)

CSS = """
  :root {
    --ink: #1A1815; --paper: #F7F4EA; --paper-2: #EFEADC; --hair: #D9D3C2;
    --muted: #6E6A5E; --body: #3A362D; --bar: #1A1815; --bar-text: #F7F4EA;
    --serif: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", Times, serif;
    --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
__ACCENT_LIGHT__
  }
  [data-theme="dark"] {
    --ink: #ECE7DA; --paper: #15140F; --paper-2: #1E1C16; --hair: #332F26;
    --muted: #9B9483; --body: #CFC9B9;
__ACCENT_DARK__
  }
  * { box-sizing: border-box; }
  html { color-scheme: light dark; scroll-behavior: smooth; }
  html, body { margin: 0; padding: 0; background: var(--paper); color: var(--ink);
    font-family: var(--serif); -webkit-font-smoothing: antialiased; }
  a { color: inherit; }
  ::selection { background: var(--gold); color: var(--paper); }
  [data-theme="dark"] ::selection { color: #15140F; }
  :focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
  * { scrollbar-color: var(--hair) transparent; }
  ::-webkit-scrollbar { width: 11px; height: 11px; }
  ::-webkit-scrollbar-thumb { background: var(--hair); }
  ::-webkit-scrollbar-track { background: transparent; }
  .wrap { max-width: 1120px; margin: 0 auto; padding: 0 34px; }

  /* --- Brand bar ------------------------------------------------------- */
  .brand-bar { background: var(--bar); color: var(--bar-text); }
  .brand-bar-inner { max-width: 1120px; margin: 0 auto; padding: 10px 34px;
    display: flex; align-items: center; gap: 11px; }
  .mark { height: 21px; width: auto; display: block; flex: none; }
  .brand-word { font-family: var(--mono); font-size: 11px; font-weight: 700;
    letter-spacing: 0.17em; text-transform: uppercase; text-decoration: none;
    color: inherit; white-space: nowrap; display: flex; align-items: center; gap: 11px; }
  .brand-spacer { flex: 1; }
  .brand-back, .brand-date { font-family: var(--mono); font-size: 11px;
    letter-spacing: 0.08em; color: inherit; text-decoration: none; white-space: nowrap; }
  .brand-back { opacity: .72; }
  .brand-back:hover { opacity: 1; text-decoration: underline; text-underline-offset: 3px; }
  .theme-toggle { flex: none; width: 28px; height: 28px; border: 1px solid rgba(247,244,234,.24);
    background: transparent; color: inherit; display: inline-flex; align-items: center;
    justify-content: center; cursor: pointer; padding: 0; transition: background .15s ease; }
  .theme-toggle:hover { background: rgba(247,244,234,.12); }
  .theme-toggle svg { width: 14px; height: 14px; }
  .theme-toggle .icon-moon { display: none; }
  [data-theme="dark"] .theme-toggle .icon-sun { display: none; }
  [data-theme="dark"] .theme-toggle .icon-moon { display: inline-block; }

  /* --- Masthead -------------------------------------------------------- */
  .masthead { max-width: 1120px; margin: 0 auto; padding: 46px 34px 0; text-align: center; }
  .dateline { display: flex; align-items: center; gap: 18px; justify-content: center;
    margin-bottom: 20px; }
  .dateline .rail { height: 1px; background: var(--gold); flex: 1; max-width: 230px; }
  .dateline .stamp { font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.16em;
    text-transform: uppercase; white-space: nowrap; font-variant-numeric: tabular-nums; }
  .nameplate { font-weight: 400; font-size: clamp(40px, 7.2vw, 68px); line-height: 1;
    letter-spacing: -0.018em; margin: 0 0 14px; }
  .nameplate a { text-decoration: none; }
  .standfirst { font-family: var(--mono); font-size: 11px; letter-spacing: 0.15em;
    text-transform: uppercase; color: var(--muted); margin: 0 0 22px;
    font-variant-numeric: tabular-nums; }
  .rule-double { border-top: 2.5px solid var(--ink); border-bottom: 1px solid var(--ink);
    height: 4px; }

  /* --- Lead ------------------------------------------------------------ */
  .lead { max-width: 1120px; margin: 0 auto; padding: 24px 34px 26px;
    display: flex; gap: 18px; align-items: flex-start;
    --lead-fs: clamp(24px, 3.4vw, 34px); --lead-lh: 1.3; --lead-tag-h: 23px; }
  /* Centre the marker on the headline's FIRST line box, not on the whole
     block and not on its baseline. The headline is a clamp(), so the offset
     has to be derived from it rather than typed as a fixed margin. */
  .lead-tag { font-family: var(--mono); font-size: 11px; font-weight: 700;
    letter-spacing: 0.17em; text-transform: uppercase; background: var(--gold);
    color: var(--paper); padding: 5px 9px; line-height: 1.2; flex: none;
    margin-top: calc((var(--lead-fs) * var(--lead-lh) - var(--lead-tag-h)) / 2); }
  [data-theme="dark"] .lead-tag { color: #15140F; }
  .lead-text { font-size: var(--lead-fs); line-height: var(--lead-lh); margin: 0;
    letter-spacing: -0.012em; max-width: 24ch; text-decoration: none; text-wrap: balance; }
  .lead-text:hover { text-decoration: underline; text-underline-offset: 4px;
    text-decoration-thickness: 1px; }

  /* --- Section index --------------------------------------------------- */
  .index-bar { position: sticky; top: 0; z-index: 50; background: var(--paper);
    border-top: 1px solid var(--ink); border-bottom: 1px solid var(--ink); }
  .index-inner { max-width: 1120px; margin: 0 auto; padding: 0 34px; display: flex;
    justify-content: center; flex-wrap: wrap; }
  .index-link { font-family: var(--mono); font-size: 11px; letter-spacing: 0.13em;
    text-transform: uppercase; background: none; border: none; color: var(--muted);
    padding: 11px 15px; cursor: pointer; position: relative; white-space: nowrap;
    border-right: 1px solid var(--hair); transition: color .15s ease; }
  .index-link:last-child { border-right: none; }
  .index-link:hover { color: var(--ink); }
  .index-link.active { color: var(--ink); font-weight: 700; }
  .index-link.active::after { content: ""; position: absolute; left: 15px; right: 15px;
    bottom: 5px; height: 2px; background: var(--gold); }

  /* --- Skim ------------------------------------------------------------ */
  .block-label { font-family: var(--mono); font-size: 11px; font-weight: 700;
    letter-spacing: 0.17em; text-transform: uppercase; color: var(--ink); margin: 0;
    display: flex; align-items: center; gap: 16px; white-space: nowrap; }
  .block-label::after { content: ""; height: 1px; background: var(--hair); flex: 1; }
  .skim { max-width: 1120px; margin: 0 auto; padding: 34px 34px 6px; }
  .skim-list { list-style: none; margin: 18px 0 0; padding: 0; display: flex;
    flex-direction: column; }
  .skim-list li { display: flex; gap: 18px; align-items: baseline; padding: 13px 0;
    border-bottom: 1px solid var(--hair); }
  .skim-list li:last-child { border-bottom: none; }
  .skim-num { font-family: var(--mono); font-size: 11px; color: var(--gold); flex: none;
    font-variant-numeric: tabular-nums; letter-spacing: 0.06em; }
  .skim-text { font-size: 16.5px; line-height: 1.55; }

  /* --- Sections -------------------------------------------------------- */
  .news-section { max-width: 1120px; margin: 0 auto; padding: 48px 34px 0;
    scroll-margin-top: 54px; }
  .section-head { border-bottom: 2px solid var(--accent); padding-bottom: 10px;
    margin-bottom: 26px; }
  .section-head h2 { font-weight: 400; font-size: clamp(26px, 3.4vw, 34px); margin: 0;
    letter-spacing: -0.012em; }
  .section-note { font-size: 14.5px; font-style: italic; color: var(--muted);
    margin: -16px 0 24px; max-width: 62ch; }
  .subblock { margin-top: 38px; }
  .subblock-label { font-family: var(--mono); font-size: 11px; font-weight: 700;
    letter-spacing: 0.17em; text-transform: uppercase; color: var(--accent);
    margin: 0 0 16px; display: flex; align-items: center; gap: 16px; white-space: nowrap; }
  .subblock-label::after { content: ""; height: 1px; background: var(--hair); flex: 1; }
  .country-group { margin-top: 34px; }
  .country-group:first-of-type { margin-top: 0; }

  /* --- Story cards ----------------------------------------------------- */
  /* Columns rather than a grid: stories are different lengths, and a grid row
     sized to its tallest card leaves a hole under every short one. Columns
     flow the way a printed page does. */
  .card-grid { column-count: 2; column-gap: 34px; }
  .card { display: block; break-inside: avoid; -webkit-column-break-inside: avoid;
    background: none; border-top: 1px solid var(--hair); padding-top: 16px;
    margin-bottom: 30px; }
  .thumb { position: relative; width: 100%; aspect-ratio: 16 / 9; background: var(--paper-2);
    overflow: hidden; margin-bottom: 14px; }
  .thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .thumb-fallback { display: none; position: absolute; inset: 0; align-items: center;
    justify-content: center; color: var(--hair); background: var(--paper-2); }
  .thumb-fallback .mark { height: 40px; }
  .card-body { display: flex; flex-direction: column; gap: 9px; }
  .card-meta { display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
  .num { font-family: var(--mono); font-size: 11px; color: var(--accent); font-weight: 700;
    letter-spacing: 0.08em; font-variant-numeric: tabular-nums; }
  .tag { font-family: var(--mono); font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; padding: 3px 7px; border: 1px solid var(--accent);
    color: var(--accent); }
  .tag.continuing { background: var(--accent); color: var(--paper); border-color: var(--accent); }
  .headline { font-size: 21px; line-height: 1.32; margin: 0; font-weight: 400;
    letter-spacing: -0.008em; text-wrap: balance; }
  .headline a { text-decoration: none; }
  .headline a:hover { text-decoration: underline; text-underline-offset: 3px;
    text-decoration-thickness: 1px; }
  .story-text { font-size: 15px; line-height: 1.62; color: var(--body); margin: 0;
    max-width: 62ch; }
  .card-actions { margin-top: 4px; display: flex; align-items: center;
    justify-content: space-between; gap: 10px; }
  .read-more { font-family: var(--mono); font-size: 11px; letter-spacing: 0.13em;
    text-transform: uppercase; text-decoration: none; color: var(--accent); }
  .read-more:hover { text-decoration: underline; text-underline-offset: 3px; }
  .share-btn { display: inline-flex; align-items: center; justify-content: center;
    width: 27px; height: 27px; border: 1px solid var(--hair); background: none;
    color: var(--muted); cursor: pointer; padding: 0; flex: none;
    transition: border-color .15s ease, color .15s ease; }
  .share-btn:hover { border-color: var(--accent); color: var(--accent); }
  .share-btn svg { width: 14px; height: 14px; }
  .card, .fixture { scroll-margin-top: 66px; }

  /* --- Fixtures -------------------------------------------------------- */
  .fixture-list { display: flex; flex-direction: column; }
  .fixture { display: grid; grid-template-columns: 104px 1fr auto auto; gap: 18px;
    align-items: baseline; padding: 15px 0; border-top: 1px solid var(--hair); }
  .fixture:last-child { border-bottom: 1px solid var(--hair); }
  .fixture-sport { font-family: var(--mono); font-size: 11px; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); }
  .fixture-main { text-decoration: none; }
  .fixture-headline { display: block; font-size: 17px; line-height: 1.3; margin-bottom: 4px; }
  .fixture-main:hover .fixture-headline { text-decoration: underline; text-underline-offset: 3px; }
  .fixture-body { display: block; font-size: 14px; line-height: 1.55; color: var(--body); }
  .fixture-when { font-family: var(--mono); font-size: 11px; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted); white-space: nowrap;
    font-variant-numeric: tabular-nums; }

  /* --- Footer & chrome -------------------------------------------------- */
  .colophon { max-width: 1120px; margin: 64px auto 0; padding: 26px 34px 64px;
    text-align: center; border-top: 1px solid var(--ink); }
  .colophon .mark { height: 26px; margin: 0 auto 14px; color: var(--ink); }
  .colophon p { font-family: var(--mono); font-size: 11px; letter-spacing: 0.04em;
    color: var(--muted); margin: 0; line-height: 1.9; }

  .back-to-top { position: fixed; right: 22px; bottom: 22px; z-index: 60; width: 42px;
    height: 42px; border: 1px solid var(--ink); background: var(--paper); color: var(--ink);
    display: flex; align-items: center; justify-content: center; cursor: pointer;
    opacity: 0; pointer-events: none; transform: translateY(6px);
    transition: opacity .25s cubic-bezier(.2,.7,.3,1), transform .25s cubic-bezier(.2,.7,.3,1); }
  .back-to-top.show { opacity: 1; pointer-events: auto; transform: translateY(0); }
  .back-to-top:hover { background: var(--ink); color: var(--paper); }
  .back-to-top svg { width: 17px; height: 17px; }

  .share-toast { position: fixed; left: 50%; bottom: 26px; transform: translateX(-50%) translateY(10px);
    background: var(--bar); color: var(--bar-text); font-family: var(--mono); font-size: 11px;
    letter-spacing: 0.13em; text-transform: uppercase; padding: 10px 18px; opacity: 0;
    pointer-events: none; transition: opacity .2s ease, transform .2s ease; z-index: 99; }
  .share-toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }

  @keyframes markFound {
    0%   { background: color-mix(in srgb, var(--accent) 22%, transparent); }
    100% { background: transparent; }
  }
  .highlight-pulse { animation: markFound 2s ease-out 1; }

  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
  }

  @media (max-width: 860px) {
    .card-grid { column-count: 1; }
  }
  @media (max-width: 700px) {
    .brand-bar-inner { padding: 9px 18px; gap: 9px; }
    .brand-back { display: none; }
    .wrap, .masthead, .lead, .skim, .news-section, .colophon, .index-inner { padding-left: 18px; padding-right: 18px; }
    .masthead { padding-top: 34px; }
    .dateline { gap: 12px; margin-bottom: 16px; }
    .dateline .rail { max-width: 40px; }
    .dateline .stamp { font-size: 11px; letter-spacing: 0.1em; }
    .lead { gap: 13px; padding-top: 20px; padding-bottom: 22px; }
    .index-inner { justify-content: flex-start; flex-wrap: nowrap; overflow-x: auto;
      scrollbar-width: none;
      -webkit-mask-image: linear-gradient(90deg, #000 86%, transparent 100%);
      mask-image: linear-gradient(90deg, #000 86%, transparent 100%); }
    .index-inner.scroll-end { -webkit-mask-image: none; mask-image: none; }
    .index-inner::-webkit-scrollbar { display: none; }
    .fixture { grid-template-columns: 1fr auto; gap: 5px 12px; }
    .fixture-sport { grid-column: 1 / -1; }
    .back-to-top { right: 14px; bottom: 14px; width: 38px; height: 38px; }
  }
  .hidden-by-filter { display: none !important; }
"""


def build_css():
    return CSS.replace("__ACCENT_LIGHT__", accent_vars("light")).replace(
        "__ACCENT_DARK__", accent_vars("dark")
    )


# Inlined at the top of <head>, before any CSS, so the stored (or system) theme
# applies before first paint rather than flashing the wrong one.
THEME_INIT_SCRIPT = """(function(){try{
  var t = localStorage.getItem('dateline-theme');
  if (!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', t);
}catch(e){}})();"""

JS = """
(function () {
  var links = document.querySelectorAll('.index-link');
  var sections = document.querySelectorAll('.news-section');
  links.forEach(function (link) {
    link.addEventListener('click', function () {
      links.forEach(function (l) { l.classList.remove('active'); });
      link.classList.add('active');
      var filter = link.getAttribute('data-filter');
      sections.forEach(function (sec) {
        sec.classList.toggle('hidden-by-filter',
          filter !== 'all' && sec.getAttribute('data-section') !== filter);
      });
      if (filter !== 'all') {
        var target = document.getElementById('sec-' + filter);
        if (target) target.scrollIntoView({ block: 'start' });
      }
    });
  });

  // --- Share: native share sheet on mobile, "Link copied" toast elsewhere ---
  function showToast(msg) {
    var t = document.getElementById('share-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'share-toast';
      t.className = 'share-toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._hideTimer);
    t._hideTimer = setTimeout(function () { t.classList.remove('show'); }, 1800);
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); showToast('Link copied'); } catch (e) { /* no-op */ }
    document.body.removeChild(ta);
  }

  document.querySelectorAll('.share-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var id = btn.getAttribute('data-share-id');
      var title = btn.getAttribute('data-share-title') || document.title;
      var url = location.origin + location.pathname + '#' + id;
      if (navigator.share) {
        navigator.share({ title: title, url: url }).catch(function () { /* cancelled */ });
      } else if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () { showToast('Link copied'); })
          .catch(function () { fallbackCopy(url); });
      } else {
        fallbackCopy(url);
      }
    });
  });

  // --- Jump straight to a shared card/fixture and mark it briefly ---
  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target) {
      setTimeout(function () {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        target.classList.add('highlight-pulse');
        setTimeout(function () { target.classList.remove('highlight-pulse'); }, 2200);
      }, 60);
    }
  }

  var themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var root = document.documentElement;
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('dateline-theme', next); } catch (e) { /* no-op */ }
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute('content', next === 'dark' ? '#15140F' : '#1A1815');
    });
  }

  // The section index scrolls horizontally on a phone with its scrollbar
  // hidden; a fade on the right edge is the only cue that it does. Clear the
  // fade once there is nothing left to scroll to.
  var indexInner = document.querySelector('.index-inner');
  if (indexInner) {
    var syncEdge = function () {
      var atEnd = indexInner.scrollLeft + indexInner.clientWidth >= indexInner.scrollWidth - 2;
      indexInner.classList.toggle('scroll-end', atEnd);
    };
    indexInner.addEventListener('scroll', syncEdge, { passive: true });
    window.addEventListener('resize', syncEdge);
    syncEdge();
  }

  var backToTop = document.getElementById('back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', function () {
      backToTop.classList.toggle('show', window.scrollY > window.innerHeight * 0.9);
    }, { passive: true });
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();
"""


def stamp_line(display_date):
    """DOHA · SAT 12 SEP 2026 — the dateline a wire story carries."""
    try:
        weekday, rest = display_date.split(",", 1)
        month_day, year = rest.rsplit(",", 1)
        month, day = month_day.strip().split(" ")
        return f"Doha &middot; {weekday[:3]} {int(day):02d} {month[:3]} {year.strip()}"
    except (ValueError, IndexError):
        return f"Doha &middot; {display_date}"


def build_html(data, display_date, archive_rel="../index.html"):
    body = render_skim(data.get("skim"))
    fixtures = data.get("fixtures")
    for s in data["sections"]:
        body += "\n" + render_section(s, fixtures=fixtures)
    body += "\n" + render_portfolio(data.get("portfolio"))
    body += "\n" + render_country_section(data["country_groups"])
    body += "\n" + render_doha_section(data["doha_events"])

    # archive_rel points at index.html relative to this page (default "../index.html");
    # the icon set lives alongside index.html at the site root, so reuse that same
    # relative prefix rather than hard-coding a page depth.
    icon_base = archive_rel.rsplit("/", 1)[0] + "/" if "/" in archive_rel else ""
    story_count, read_minutes = estimate_reading(data)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>{THEME_INIT_SCRIPT}</script>
<title>The Date Line &mdash; {display_date}</title>
<meta name="description" content="Ankit's morning briefing for {display_date} — world, sport, business, AI, geopolitics, market watch, country updates and Doha events.">
<link rel="icon" href="{icon_base}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{icon_base}favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="{icon_base}favicon-16.png" sizes="16x16" type="image/png">
<link rel="shortcut icon" href="{icon_base}favicon.ico">
<link rel="apple-touch-icon" href="{icon_base}apple-touch-icon.png">
<link rel="manifest" href="{icon_base}site.webmanifest">
<meta name="theme-color" content="#1A1815">
<meta name="apple-mobile-web-app-title" content="The Date Line">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<style>{build_css()}
{ACCENT_CSS}
</style>
</head>
<body>

<div class="brand-bar">
  <div class="brand-bar-inner">
    <a class="brand-word" href="{archive_rel}">{MARK_SVG}<span>The Date Line</span></a>
    <div class="brand-spacer"></div>
    <a class="brand-back" href="{archive_rel}">All editions &rarr;</a>
    <button class="theme-toggle" id="theme-toggle" aria-label="Switch between light and dark" title="Switch between light and dark">
      {SUN_ICON}{MOON_ICON}
    </button>
  </div>
</div>

<header class="masthead">
  <div class="dateline">
    <span class="rail"></span>
    <span class="stamp">{stamp_line(display_date)}</span>
    <span class="rail"></span>
  </div>
  <h1 class="nameplate">The Date Line</h1>
  <p class="standfirst">Ankit&rsquo;s morning briefing &middot; {story_count} stories &middot; ~{read_minutes} min</p>
  <div class="rule-double"></div>
</header>

{render_lead(data)}

<nav class="index-bar" aria-label="Sections">
  <div class="index-inner">
{render_index()}
  </div>
</nav>

<main>
{body}
</main>

<footer class="colophon">
  {MARK_SVG}
  <p>Compiled from public reporting &middot; Doha, Qatar<br>{display_date}</p>
</footer>

<button class="back-to-top" id="back-to-top" aria-label="Back to top" title="Back to top">{TOP_ICON}</button>

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

    html_out = build_html(data, args.display_date, args.archive_rel)
    with open(args.out, "w") as f:
        f.write(html_out)
    print(f"Wrote {args.out} ({len(html_out)} bytes)")


if __name__ == "__main__":
    main()
