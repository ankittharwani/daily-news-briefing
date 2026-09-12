# Ankit's Morning Briefing — repo guide for Claude Code

This repo is both a live site (db.labs.tocn.ai) and the durable source of
truth for the automation that builds it — see `README.md` for the published
vs. private layout, and `skill/SKILL.md` for the full daily pipeline
(research → render → deploy). This file is scoped to one thing: **redesigning
the visual design**, for a Claude Code session running locally (e.g. with
design/taste skills installed that aren't available in the cloud sandbox
that runs the daily scheduled job).

## Where the design actually lives

There is no separate stylesheet or component library. Two files are the
entire design system, and editing them is the entire redesign:

- **`skill/scripts/render_briefing.py`** — the `CSS` and `JS` Python string
  constants near the top of the file. This generates every
  `public/briefings/YYYY-MM-DD.html` page (masthead, filter pills, the
  30-second skim, section headers, story cards, the Market Watch ticker
  chips, Fixtures Ahead rows, share/copy-link behavior).
- **`skill/assets/index_template.html`** — the archive cover page
  (`public/index.html`): hero card, topic tiles, edition grid, search.

Both files are plain HTML/CSS/JS (Python only wraps the CSS/JS as string
constants) — read and edit them like any front-end code. There is nothing
elsewhere to find: no separate `.css` file, no build step, no framework.

**The favicon** is a separate small design system: `skill/assets/favicon/`
holds the source SVGs (`icon.svg` for the rounded/general-purpose mark,
`icon-square.svg` for the apple-touch-icon, which iOS masks itself) and a
Playwright-based `render.js` that rasterizes them to the PNG/ICO sizes in
`public/`. If the redesign changes the color palette, regenerate these too so
the icon stays in the same system as the page — see the "Favicon / app icon"
note in `skill/SKILL.md`.

## Current system, briefly (so you know what you're changing)

- Typography: Georgia/Times serif for all headings and the masthead;
  system sans-serif (`-apple-system, ... Helvetica, Arial`) for body text.
- Palette: ink `#2E2C27`, secondary text `#6B6A63`, hairline `#E4E3DC`, wash
  `#F9F9F7`, white `#FCFCFB` — plus one accent color per section
  (`ACCENT_MAP` in `render_briefing.py`): world `#2B4257`, sports `#B5563C`,
  business `#A9822E`, ai `#2C7A73`, geopolitics `#3E5C8A`, portfolio
  (Market Watch) `#4F6B4A`, country `#8C3A3A`, doha `#6B4C7A`.
- One responsive breakpoint (`@media (max-width: 760px)`); no dark-mode
  support currently (no `prefers-color-scheme`).
- Editorial/broadsheet tone: serif headlines, hairline rules, restrained
  color used only as section accents — not a typical "app" look.

None of the above is sacred — redesign it however the taste/impeccable
skills recommend. The palette and type choices above are just the starting
point so you're editing intentionally, not guessing at what's already there.

## Hard constraints that must survive any redesign

These aren't style preferences, they're functional requirements the daily
automation depends on:

1. **Eight sections in a fixed order**, plus the 30-Second Skim at the top:
   World, Sports (with a Fixtures Ahead block), Business & Markets, AI &
   Technology, Geopolitics, Market Watch, Country Updates (with India / UK /
   Qatar & GCC sub-groups), Doha Events. If you rename, reorder, or restyle
   sections, update `ACCENT_MAP` and `PILLS` in `render_briefing.py` *and*
   the section-order notes in `skill/references/research-guide.md` together
   — the unattended daily run reads that guide to decide what goes where,
   so the two must stay in sync.
2. **Market Watch must never render a share price, percentage move, position
   size, or share count** — see `skill/references/watchlist.md`. This is a
   hard privacy rule from Ankit, not a style choice, and it's about content
   the render script is given, not markup — but if you add any new
   data-driven display (e.g. a sparkline, a numeric badge), keep it clear of
   this.
3. **Each briefing page must stay a single self-contained HTML file** — no
   external CSS/JS files, no build pipeline. Images are the one exception
   (hotlinked to their original article's CDN). This is what makes every
   past edition a durable, independent artifact.
4. **Mobile must keep working** — the site is read on a phone most mornings.
   Keep (or improve) the existing breakpoint.

## How a redesign reaches the live site — no extra steps needed

The daily scheduled job (a cloud sandbox, separate from this Claude Code
session) clones `https://github.com/ankittharwani/daily-news-briefing` fresh
every morning and runs `skill/scripts/render_briefing.py` as-is from
whatever is on `main`. So the flow is just:

1. Redesign here, iterating locally (open the generated HTML in a browser;
   there's no dev server needed, `render_briefing.py` writes plain files).
2. Commit and push to `main` (normal `git push` — you're using your own
   GitHub credentials locally, not the sandbox's scoped token).
3. Done. Tomorrow's scheduled run automatically uses the new design — there
   is no separate deploy step for "the skill" versus "the site," and nothing
   to reconfigure on the scheduled-task side.

Pushing to `main` also triggers `.github/workflows/deploy.yml`, which
deploys `public/` to Netlify — so today's redesign of `index.html` /
`index_template.html` goes live immediately too, independent of the next
scheduled run.

## One thing a redesign does *not* automatically do

**Past editions in `public/briefings/*.html` are static, already-rendered
files — they will keep their old look.** They are not regenerated when you
change `render_briefing.py`; each is treated as an immutable snapshot of the
day it was published (this is a deliberate existing choice, not an
oversight). If you want the whole archive to match the new design, that's a
separate, optional batch step: every edition's structured content is still
available in `data/YYYY-MM-DD.json`, so re-running
`render_briefing.py --data data/<date>.json --date <date> ... --out
public/briefings/<date>.html` for every file in `data/` would re-render the
full history under the new design. Worth doing, but treat it as a deliberate
choice you make (and mention to Ankit), not something to do silently as
part of a design pass.
