---
name: The Date Line
description: A personal wire service, set with broadsheet care — two faces, no shadows, light and dark both first-class.
colors:
  ink: "#1A1815"
  paper: "#F7F4EA"
  paper-2: "#EFEADC"
  hair: "#D9D3C2"
  muted: "#6E6A5E"
  body-text: "#3A362D"
  bar: "#1A1815"
  bar-text: "#F7F4EA"
  gold: "#856420"
  mask-stop: "#000"
  ink-dark: "#ECE7DA"
  paper-dark: "#15140F"
  paper-2-dark: "#1E1C16"
  hair-dark: "#332F26"
  muted-dark: "#9B9483"
  body-text-dark: "#CFC9B9"
  gold-dark: "#C9A24E"
  accent-world: "#2B4257"
  accent-sports: "#A8482C"
  accent-business: "#8A6A1E"
  accent-ai: "#1F6B64"
  accent-geopolitics: "#3E5C8A"
  accent-portfolio: "#47633F"
  accent-country: "#8C3A3A"
  accent-doha: "#63456F"
  accent-world-dark: "#7FA5CC"
  accent-sports-dark: "#E08863"
  accent-business-dark: "#D9AA55"
  accent-ai-dark: "#5FBDB3"
  accent-geopolitics-dark: "#8CACD6"
  accent-portfolio-dark: "#8AB183"
  accent-country-dark: "#D97A7A"
  accent-doha-dark: "#B08BC2"
typography:
  nameplate:
    fontFamily: "Georgia, \"Iowan Old Style\", \"Palatino Linotype\", \"Times New Roman\", Times, serif"
    fontSize: "clamp(40px, 7.2vw, 68px)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "-0.018em"
  lead:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "clamp(24px, 3.4vw, 34px)"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "-0.012em"
  section-title:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "clamp(26px, 3.4vw, 34px)"
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: "-0.012em"
  headline:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "21px"
    fontWeight: 400
    lineHeight: 1.32
    letterSpacing: "-0.008em"
  skim:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "16.5px"
    fontWeight: 400
    lineHeight: 1.55
  hero-date:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "clamp(30px, 4vw, 44px)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.018em"
  search:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.3
  body:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.62
  fixture-body:
    fontFamily: "{typography.nameplate.fontFamily}"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "ui-monospace, SFMono-Regular, \"SF Mono\", Menlo, Consolas, \"Liberation Mono\", monospace"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.17em"
  meta:
    fontFamily: "{typography.label.fontFamily}"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.13em"
  stamp:
    fontFamily: "{typography.label.fontFamily}"
    fontSize: "11.5px"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.16em"
rounded:
  none: "0"
  mark-tile: "14px"
spacing:
  hair: "4px"
  xs: "9px"
  sm: "14px"
  md: "18px"
  lg: "26px"
  gutter: "34px"
  section: "48px"
components:
  story-card:
    backgroundColor: "transparent"
    textColor: "{colors.body-text}"
    typography: "{typography.headline}"
    rounded: "{rounded.none}"
    padding: "16px 0 0"
  tag-continuing:
    backgroundColor: "{colors.accent-world}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "3px 7px"
  tag-ticker:
    backgroundColor: "transparent"
    textColor: "{colors.accent-portfolio}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "3px 7px"
  lead-marker:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "5px 9px"
  index-link:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    typography: "{typography.meta}"
    rounded: "{rounded.none}"
    padding: "11px 15px"
  index-link-active:
    textColor: "{colors.ink}"
    typography: "{typography.meta}"
  read-more:
    backgroundColor: "transparent"
    textColor: "{colors.accent-world}"
    typography: "{typography.meta}"
    rounded: "{rounded.none}"
  share-button:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    rounded: "{rounded.none}"
    height: "27px"
    width: "27px"
  search-input:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.skim}"
    rounded: "{rounded.none}"
    padding: "13px 34px 13px 28px"
  pager-num-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.meta}"
    rounded: "{rounded.none}"
    padding: "8px 11px"
  back-to-top:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    height: "42px"
    width: "42px"
---

# Design System: The Date Line

## Overview

**Creative North Star: "The Personal Wire Service"**

The Date Line is a one-reader newswire that has been set with broadsheet care. It reads as if a wire desk printed a single edition for a single subscriber: a dateline stamp, a centred nameplate, a LEAD marker, eight numbered sections. The page refuses the obvious newspaper pastiche — cream card stock, coloured pills, drop shadows on rounded tiles — and gets its authority instead from division of labour between exactly two type faces and from rules drawn in ink.

Everything mechanical is monospace: the dateline, the story numerals, the section index, the CONTINUING tag, the ticker chip, READ MORE, the edition and read-time meta, the colophon. Everything readable is serif: the nameplate, every headline, the skim, every sentence of body copy. There is no third face anywhere in the build, and no web font at all — the single-self-contained-file constraint means system stacks only, so the stacks themselves are the brand (Georgia leading the serif, `ui-monospace`/SF Mono leading the mono).

Light and dark are equal citizens, not a light design with a night filter bolted on. Every ground, hairline, text tone, gold and section accent ships a light value and a dark value; the theme is written to `data-theme` on `<html>` by an inline pre-paint script so the correct world is already on screen at first paint. This is a product decision made visible: the page is read on a phone at dawn.

**Key Characteristics:**
- Two faces and no third: monospace for machinery, serif for reading.
- Zero shadows, zero corner radius; hierarchy is rules, weight and space.
- Eight section accents, each with a light and a dark value, delivered through one `--accent` variable.
- A publication gold that belongs to the masthead and the LEAD alone.
- Story cards flow in CSS columns, so short and long stories pack like a printed page.
- A story with no verified photograph renders text-led — no empty image well.

## Colors

A warm paper-and-ink palette with one publication gold and eight muted section accents, every value doubled for dark mode.

### Primary
- **Publication Gold** (light `#856420` / dark `#C9A24E`): the masthead dateline rails, the filled LEAD marker, the skim numerals, the active section-index underline, the archive's edition dates, `::selection`, the focus ring, and the search field's focused underline. It is the publication's own colour and is deliberately **not** assigned to any section. The light value was darkened from an earlier `#9A7828` so it clears 4.5:1 as small text on paper.

### Secondary — Section Accents
Eight accents, one per fixed section, each with a lifted dark-mode value so it still carries on a near-black ground. They are exposed as `--accent-<key>` and repointed per section through a single `--accent`, so recolouring or adding a section never touches a component rule.
- **Wire Navy** — World (`#2B4257` / `#7FA5CC`)
- **Terracotta** — Sports (`#A8482C` / `#E08863`)
- **Old Brass** — Business & Markets (`#8A6A1E` / `#D9AA55`)
- **Verdigris** — AI & Technology (`#1F6B64` / `#5FBDB3`)
- **Chart Blue** — Geopolitics (`#3E5C8A` / `#8CACD6`)
- **Field Green** — Market Watch (`#47633F` / `#8AB183`)
- **Oxide Red** — Country Updates (`#8C3A3A` / `#D97A7A`)
- **Aubergine** — Doha Events (`#63456F` / `#B08BC2`)

An accent appears as: the 2px rule under a section head, the story numeral, the sub-block label (Fixtures Ahead, India), READ MORE, the share button's hover border, the outlined ticker chip, the archive's outlined result chip, and the fill of the CONTINUING tag. Nothing else is accent-coloured — never a card border, never a card background, never a headline.

### Neutral
- **Warm Ink** (`#1A1815` / `#ECE7DA`): the nameplate, headlines, section titles, the double rule, the colophon rule.
- **Warm Paper** (`#F7F4EA` / `#15140F`): the page ground and the sticky section-index ground.
- **Paper Shade** (`#EFEADC` / `#1E1C16`): image wells only — the ground a photograph sits on and the ground its fallback mark sits on.
- **Hairline** (`#D9D3C2` / `#332F26`): every 1px divider — card tops, skim rows, fixture rows, label tails, the share and pager borders, the scrollbar thumb.
- **Muted** (`#6E6A5E` / `#9B9483`): inactive index links, the standfirst, fixture dates, the colophon, the section note, empty states.
- **Reading Ink** (`#3A362D` / `#CFC9B9`): story body copy only — a step softer than headline ink so a dense column stays comfortable.
- **Bar / Bar Text** (`#1A1815` / `#F7F4EA`, unchanged in dark): the brand bar is ink in both themes. It is the one surface that does not invert, which is what makes it read as the publication's spine.

### Named Rules
**The Gold Belongs To The Paper Rule.** Gold marks the publication itself — dateline rails, LEAD, skim numerals, focus and selection. It is never a section's colour, and a section may never borrow it.

**The Accent Is A Rule, Not A Surface Rule.** Section colour is spent on 1–2px rules and 11px mono labels. It fills exactly one element in the whole system — the CONTINUING tag — and gold fills exactly one — the LEAD marker. Adding a third filled accent element breaks the page.

**The Both-Grounds Rule.** No colour enters the system without a dark-mode partner. A hard-coded hex inside a component rule is a bug, with three sanctioned exceptions already in the build: the ink brand bar, `#15140F` used as the text colour on gold fills in dark mode, and `#000` inside the `mask-image` gradients on the two horizontal scrollers — that one is an alpha channel, not a colour, and never paints a pixel.

## Typography

**Display / Reading Font:** Georgia (with Iowan Old Style, Palatino Linotype, Times New Roman, Times, serif)
**Label / Machinery Font:** `ui-monospace` (with SF Mono, Menlo, Consolas, Liberation Mono, monospace)

**Character:** A bookish, generously-eyed serif doing all the talking, and a tight tabular monospace doing all the labelling. The contrast is the identity: you can tell what is information and what is apparatus without reading a word.

### Hierarchy
- **Nameplate** (serif, 400, `clamp(40px, 7.2vw, 68px)`, line-height 1, tracking -0.018em): "The Date Line", centred, once per page, on both the edition and the archive.
- **Lead** (serif, 400, `clamp(24px, 3.4vw, 34px)`, 1.3, max-width 24ch, `text-wrap: balance`): the day's first story headline beside the gold LEAD marker. It is a headline, never a summary sentence — a long sentence at this scale pushes the skim off a phone's first screen.
- **Section Title** (serif, 400, `clamp(26px, 3.4vw, 34px)`): the eight section heads, over a 2px accent rule.
- **Headline** (serif, 400, 21px, 1.32, balanced): every story card. Underline on hover at 1px with 3px offset; never underlined at rest.
- **Skim** (serif, 16.5px, 1.55): the 30-Second Skim lines, against a gold mono numeral.
- **Hero Date** (serif, 400, `clamp(30px, 4vw, 44px)`, 1.12, tracking -0.018em): the archive's latest-edition hero, where the edition's own date is the headline and the caption drops to a standfirst beneath it.
- **Body** (serif, 15px, 1.62, max-width 62ch, Reading Ink): story summaries. The archive's result body runs 14.5px/1.6 at 72ch, its edition captions 16.5px/1.45, its hero standfirst 17px/1.5 at 46ch, and its search field 19px.
- **Fixture** (serif, 17px/1.3 headline over 14px/1.55 body): the Fixtures Ahead rows, the one place a story-like item is set below Body size.
- **Label** (mono, 700, 11px, tracking 0.17em, uppercase): block labels, sub-block labels, the brand word, the LEAD marker, CONTINUING and ticker tags.
- **Meta** (mono, 400, 11px, tracking 0.08–0.13em, uppercase): index links, READ MORE, fixture dates, pager, colophon, toast.
- **Stamp** (mono, 11.5px, tracking 0.16em, uppercase, tabular): the dateline — `DOHA · SAT 12 SEP 2026`.

### Named Rules
**The Two Faces Rule.** Monospace carries every piece of machinery; serif carries every piece of reading. There is no third face and no web font. If a new element is neither apparatus nor prose, decide which it is before styling it.

**The Tabular Numerals Rule.** Every mono numeral that sits in a column or a stamp sets `font-variant-numeric: tabular-nums` — dateline, standfirst, story numerals, fixture dates, edition dates, pager.

**The Weight Ceiling Rule.** Serif never goes above 400. Emphasis comes from size, rules and space. Mono uses exactly two weights: 700 for labels, 400 for meta.

## Layout

A single 1120px measure with a 34px gutter (18px under 700px), centred, with no sidebar and no asymmetric grid. Vertical rhythm is coarse and consistent: 46px above the masthead, 48px above each section, 26px under a section head, 30px between cards, 64px before the colophon.

**Edition page.** Brand bar → centred masthead (dateline rail, nameplate, standfirst, double rule) → LEAD → sticky section index → skim → eight sections → colophon. The index bar sticks to the top at `z-index: 50` with ink rules above and below; sections carry `scroll-margin-top: 54px` and cards 66px so a jump never lands under it.

**Story columns, not a grid.** `.card-grid` is `column-count: 2` with a 34px gap and `break-inside: avoid` on each card. A grid row sized to its tallest card leaves a hole under every short story; columns pack ragged, the way a printed page does. This collapses to one column at 860px.

**Archive page.** Same masthead, then a search field and topic rail, a two-column latest-edition hero (1.15fr / 1fr), and a three-up edition grid (30px × 34px gaps) that steps to two columns at 900px and one at 620px.

**Responsive.** The edition page breaks at 860px (columns to one) and 700px (gutters, dateline rails shrink to 40px, the "All editions" link drops, the index rail scrolls horizontally under a right-edge mask that clears at the end of the scroll). The archive page breaks at 900px and 620px. The two files do not share breakpoint values; this is a known consequence of the duplication hazard below, not a deliberate difference.

### Named Rules
**The One Measure Rule.** Every band — bar, masthead, lead, index, skim, section, colophon — is 1120px wide with the same gutter. Nothing runs full-bleed except the ink brand bar's background.

## Elevation & Depth

**This system has no shadows and no elevation.** Not one `box-shadow` is used for depth anywhere in either file. Depth is conveyed entirely by rules and tone: a 1px hairline above each card, a 2px accent rule under each section head, the 2.5px/1px double rule closing the masthead, ink rules bounding the sticky index, and the Paper Shade well behind an image. Surfaces do not float; they are printed.

The single `box-shadow` in the build is `inset 0 -0.42em 0` on the archive's `<mark>`, used as a translucent gold highlighter stroke under matched search text. That is ink, not lift.

### Named Rules
**The Printed Surface Rule.** No `box-shadow` for elevation, no blur, no scrim, no glass. If an element needs separation, give it a hairline or a change of ground.

## Shapes

Every corner in the interface is square: cards, tags, chips, buttons, image wells, the theme toggle, the back-to-top control, pager buttons. `border-radius` is unset across both files. The only rounded form in the whole system is the app-icon tile (14px on a 64px artboard), and that exists because the OS expects a tile, not because the interface is soft.

Form language is therefore rectangular and typographic: a card is a hairline and a stack, a chip is a 1px accent outline with 3px/7px padding, a button is a 27px or 42px square with a 1px border. Image wells are 16:9 on story cards and edition tiles, 16:10 on the archive hero, `object-fit: cover`.

## Components

### Brand Bar
The publication's spine, ink in both themes. 10px/34px padding, 21px dL mark, the brand word in tracked mono 700, a spacer, a context note (`All editions →` on an edition, `Latest 12 Sep 2026` on the archive), and the theme toggle. The note hides below the small breakpoint; the mark and word never do.

### Masthead
Centred. A mono dateline stamp flanked by two 1px gold rails (max 230px each, 40px on a phone); the nameplate; a mono standfirst carrying `Ankit's morning briefing · N stories · ~N min`; then the double hairline close (2.5px over 1px ink). The dateline rails, the nameplate and the double rule are the page's fingerprint — with all content removed, this is how the publication is recognised.

### LEAD marker
A filled gold block in mono 700 (5px/9px) beside the day's first headline at lead scale. One per edition. In dark mode its text drops to `#15140F` so it stays legible on the lifted gold.

### Story Card
Borderless and background-less. A 1px hairline on top, 16px of air, the optional 16:9 image well, then a 9px-gapped stack: meta row (accent numeral `01`, optional outlined ticker chip, optional filled CONTINUING tag), serif headline, body paragraph, and an action row with accent READ MORE on the left and a 27px square share button on the right. Hover underlines the headline; the share button's border and glyph take the section accent.
- **No photograph:** the card renders text-led with no well at all. This is the intended look, not a degraded one.
- **Broken photograph:** the well falls back to the dL mark at hairline contrast on Paper Shade — the publication's own furniture, never a foreign broken-image glyph.

### Section Index (edition) / Topic Rail (archive)
Mono 11px uppercase links, muted at rest, ink on hover, ink 700 when active, divided by hairline separators (edition) and underlined by a 2px bar — gold on the edition index, the topic's own accent on the archive rail. On a phone the rail scrolls horizontally with its scrollbar hidden and a right-edge mask that clears once there is nothing left to scroll to.

### Fixtures Ahead
A row list, not cards: `104px 1fr auto auto` grid, hairline above each row and below the last. Sport in accent mono, headline 17px serif with body under it, date in muted mono, share button last. On a phone the sport label takes its own full-width line above the fixture.

### Search Field (archive)
A serif 19px input with no box — no border, no background, no radius — sitting on a 1px ink underline, with a muted magnifier at the left and a clear button at the right that appears once there is a value. Focus swaps the underline to gold. `/` focuses it, `Escape` blurs it.

### Controls
- **Theme toggle:** 28px square, 1px border at 24% paper on the ink bar, sun in light and moon in dark, hover lifts the ground to 12% paper.
- **Back to top:** fixed 42px square, ink border on paper, appears past 0.9 viewport heights, inverts to ink on hover, rises 6px on a 250ms `cubic-bezier(.2,.7,.3,1)`.
- **Share toast:** an ink chip, centred, bottom 26px, mono uppercase, 1.8s.
- **Pager:** hairline-bordered mono squares, active fills ink on paper, windowed as `1 … 4 5 [6] 7 8 … 40`.

### Motion
Only four durations exist: 150ms ease on colour and border hovers, 200ms on the toast, 250ms `cubic-bezier(.2,.7,.3,1)` on the back-to-top, and a 2s `markFound` flash that tints a shared card with 22% of its section accent on arrival. `prefers-reduced-motion` collapses every animation and transition to 0.001ms and disables smooth scrolling.

### The dL Mark
One vertical stroke serves as both the *d*'s ascender and the *L*'s stem, and runs past the letter at top and bottom — that overrun **is** the date line. Drawn as a bowl with its counter punched out via `fill-rule="evenodd"`, plus the *L*'s foot and the stroke, on a `11 3 43 58` viewBox in `currentColor`, so the same markup prints on paper and reverses on ink with no second copy.
- **Clear space:** at least the width of the vertical stroke (7.5 units, ≈ 17% of the mark's width) on all sides. In the bar this is satisfied by the 11px gap to the brand word.
- **Sizes in use:** 21px in the brand bar, 26px in the colophon, 34–48px as an image-well fallback. **Minimum 16px**; below that the bowl's counter closes up.
- **Two SVG sources:** `skill/assets/favicon/icon.svg` is the rounded tile (14px radius) used for `favicon.svg`, the ICO and every PNG; `skill/assets/favicon/icon-square.svg` is the identical mark full-bleed with no rounding, used only for `apple-touch-icon.png`, because iOS applies its own mask and would clip a pre-rounded tile. Both are drawn in paper `#F7F4EA` on ink `#1A1815` and do not follow the theme; only the inline `MARK_SVG` copy does.
- **Regenerating the raster set:** run `skill/assets/favicon/render.js` under Playwright/Chromium (it emits 512/192/48/32/16 PNGs from `icon.svg` and the 180px apple-touch icon from `icon-square.svg`), then build `favicon.ico` from the 16/32/48 PNGs and copy the results into `public/`. The exact commands are in `skill/SKILL.md`.

## Do's and Don'ts

### Do:
- **Do** decide first whether a new element is machinery or reading, then give it the mono label/meta role or the serif headline/body role. Nothing sits between.
- **Do** reach section colour through `var(--accent)`; a section-specific selector in a component rule is a mistake the `[data-section]` mapping exists to prevent.
- **Do** give every new colour both a light and a dark value in the same edit.
- **Do** separate things with a hairline (`var(--hair)`) or a change of ground, at 1px, 2px for a section head, 2.5px/1px for the masthead close.
- **Do** set `font-variant-numeric: tabular-nums` on any mono numeral that sits in a column or a stamp.
- **Do** make the same token edit in **both** `skill/scripts/render_briefing.py` and `skill/assets/index_template.html`. The no-build-step rule means there is nowhere shared for tokens to live, so the `:root` block is duplicated verbatim between the two files. This is the system's main maintenance hazard: a token changed in one file only will silently split the archive from the editions. Diff the two `:root` blocks before committing any palette or type change.
- **Do** keep the eight sections in their fixed order — World, Sports (with Fixtures Ahead), Business & Markets, AI & Technology, Geopolitics, Market Watch, Country Updates, Doha Events — topped by the 30-Second Skim, and keep `ACCENT_MAP`, `PILLS`, the archive's `TOPICS` array and `skill/references/research-guide.md` in sync when anything about that set changes.
- **Do** keep every page a single self-contained HTML file: inline CSS and JS, no external stylesheet, no build step, no web font. Hotlinked article images are the only exception, upgraded to `https://` before they are emitted.
- **Do** test both themes and a phone width for every change; the theme is set pre-paint from `localStorage['dateline-theme']`, so a change that only looks right in light is half-built.

### Don't:
- **Don't** introduce a third type family, a web font, or a serif weight above 400.
- **Don't** add a `box-shadow` for elevation or a `border-radius` to any interface element. The one rounded form in the system is the app-icon tile; the one shadow is the search highlighter.
- **Don't** fill a shape with a section accent. The CONTINUING tag is the only accent fill and the LEAD marker is the only gold fill; a third filled marker flattens the distinction both rely on.
- **Don't** give gold to a section, or borrow a section accent for masthead furniture.
- **Don't** replace the column flow with a CSS grid; a row sized to its tallest card is exactly the hole the columns exist to avoid.
- **Don't** render an empty or placeholder image well for a story with no photograph — let the card go text-led.
- **Don't** render a share price, percentage move, position size or share count anywhere in Market Watch, and don't add any visual element (sparkline, numeric badge, delta arrow) that would require one.
- **Don't** substitute a glyph or emoji for the dL mark, and don't redraw the mark per theme — it is `currentColor` by design.
- **Don't** add a kicker or eyebrow label above a headline as a new pattern. The archive's "Latest edition" line is a carried defect, not a component to copy.
