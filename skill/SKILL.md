---
name: ankit-morning-briefing
description: Builds and publishes Ankit's daily morning news briefing — an eight-section HTML news digest (World, Sports with fixtures, Business & Markets, AI & Technology, Geopolitics, Market Watch on his stock watchlist, Country Updates for India/UK/Qatar & GCC, and Doha Events) plus a searchable dated archive at db.labs.tocn.ai. Use this whenever asked to run, build, regenerate, or troubleshoot Ankit's morning briefing, its Market Watch/stock section, or its archive site — including when invoked unattended by the daily scheduled task, or when Ankit asks to see a past edition, add or drop tickers from the watchlist, change the home page, add a section, or redeploy. Do not use for a generic personal calendar/schedule "morning brief" — that's a different, unrelated concept.
---

# Ankit's Morning Briefing

A fully-automated daily pipeline: research real news → render a single-file
HTML digest in a fixed editorial design → fold it into a multi-day archive with
a browsable cover page → push to GitHub, which deploys the whole archive to
Netlify via Actions → hand today's edition to Ankit directly.

This skill is normally invoked **unattended**, once a day, by a scheduled task.
Treat every run as a fresh session with no memory of previous runs: everything
you need to know is either in this skill or in the GitHub repo that is the
archive's source of truth (see `references/netlify-deploy.md`). Never block on
a clarifying question in an unattended run — make the most reasonable
judgment call, note the assumption, and keep going. (If a human is actively
chatting with you right now and asks you to tweak something, of course talk it
through normally — that's not an unattended run.)

## What's in an edition

Eight sections, in this order: **World**, **Sports** (with a *Fixtures Ahead*
block), **Business & Markets**, **AI & Technology**, **Geopolitics**, **Market
Watch**, **Country Updates** (India / United Kingdom / Qatar & the GCC), and
**Doha Events** — topped by a five-line **30-Second Skim**.

World leads deliberately: every other section is a special interest, so without
it a major global story has nowhere to sit and the edition opens with sport.
See `references/research-guide.md` for the World/Geopolitics boundary.

## Overview of the seven steps


1. **Clone the archive repo first** — `github.com/ankittharwani/daily-news-briefing`
   is the source of truth for every prior edition, and yesterday's edition is
   what makes step 2's continuity work possible. See
   `references/netlify-deploy.md` for the command and token.
2. **Research** today's news (`references/research-guide.md`) and scan the
   market watchlist (`references/market-watch.md`).
3. **Render** today's briefing with `scripts/render_briefing.py`.
4. **Update the manifest and rebuild the search index**
   (`scripts/update_manifest.py`, `scripts/build_search_index.py`).
5. **Render-check** today's page *and* the home page with Playwright.
6. **Commit and push** — this is what deploys, via GitHub Actions.
7. **Deliver** to Ankit via `SendUserFile` and share the live archive URL.

## Step 1: Clone the archive repo

Do this **first**, before researching. See `references/netlify-deploy.md` for
the token:

```bash
git clone https://<GITHUB_TOKEN>@github.com/ankittharwani/daily-news-briefing.git site
```

Then read yesterday's edition — `site/public/briefings/<most-recent-date>.html` — or
at minimum skim its headlines. This is what lets today's edition say what
*changed* rather than restating a running story from scratch, which is the main
thing a personal briefing can do that a news site cannot.

## Step 2: Research

Read `references/research-guide.md` in full first. It has the section order,
per-section sourcing rules (WION for India, The Peninsula Qatar / Al Jazeera for
Qatar & the GCC), which WebFetch patterns fail and how to route around them, and
the writing and citation rules.

For **Market Watch**, read `references/market-watch.md` and `references/watchlist.md`.
The short version: batch-scan 46 tickers for movement, investigate only what
moved, and never put a share price or percentage move on the page.

For **Fixtures Ahead**, find what's *coming up* in cricket, football and F1 over
the next week or two — the reader learns results elsewhere; what they can act on
is knowing a Test starts Saturday.

Structure everything into one `content.json`. Read the docstring at the top of
`scripts/render_briefing.py` for the exact shape; the top-level keys are
`skim`, `sections` (world, sports, business, ai, geopolitics), `fixtures`,
`portfolio`, `country_groups` and `doha_events`.

Collect image URLs into a **separate `images.json`** map of
`{article_url: image_url}` and apply it rather than writing `img` fields by
hand — see the images section of `references/research-guide.md` for why:

```bash
python3 <skill_dir>/scripts/patch_images.py --data content.json --map images.json
```

It reports which stories ended up with no image, so a dropped photo is visible
instead of silent.

Two things to carry through the whole research pass:

**Continuity.** When a story follows up on something in a recent edition, set
`"continues": true` on it — it renders a small CONTINUING tag. Use the body text
to say what actually moved since, not to re-explain the background.

**The day's single most distinctive story.** You need it twice later: as the
one-line `SendUserFile` caption and as the manifest `caption` that becomes the
home-page hero. Also note that story's image URL for `--hero-image`.

## Step 3: Render today's briefing

```bash
python3 <skill_dir>/scripts/render_briefing.py \
  --data content.json \
  --date 2026-07-29 \
  --display-date "Wednesday, July 29, 2026" \
  --out site/public/briefings/2026-07-29.html
```

Read today's date from the environment in the **Asia/Qatar timezone (UTC+3)**
— don't assume the container's local timezone. `TZ=Asia/Qatar date "+%A, %B %d, %Y"`
gives you the display date; `TZ=Asia/Qatar date "+%Y-%m-%d"` gives the file
date.

`--archive-rel` defaults to `../index.html`, which is correct as long as the
briefing lives at `site/public/briefings/<file>.html` and the cover page lives at
`site/public/index.html` — leave it alone unless you've changed that layout.

## Step 4: Update the manifest and search index

```bash
python3 <skill_dir>/scripts/update_manifest.py \
  --manifest site/public/manifest.json \
  --date 2026-07-29 --weekday Wednesday \
  --display-date "Wednesday, July 29, 2026" \
  --month-label "July 2026" \
  --file "briefings/2026-07-29.html" \
  --hero-image "<image URL from today's lead story, or omit>" \
  --caption "<the one-line most-notable-story sentence>"

python3 <skill_dir>/scripts/build_search_index.py \
  --briefings-dir site/public/briefings --out site/public/search-index.json
```

The manifest drives the home page's hero and edition cards; the search index
makes every story in every past edition findable. Rebuild the index from the
whole `briefings/` directory each day rather than appending — it's cheap, and it
means a fixed typo in an old edition propagates.

`site/public/index.html`, `netlify.toml` and `.github/workflows/deploy.yml` already
exist in the repo and don't normally need touching. If you change the home page,
edit `assets/index_template.html` in the skill and copy it over, so the skill
stays the source of truth.

## Step 5: Render-check

Serve the site locally first — the home page fetches `manifest.json` and
`search-index.json`, which fails under `file://` due to CORS:

```bash
cd site/public && python3 -m http.server 8811 &
NODE_PATH=/opt/node-tools/node_modules node <skill_dir>/scripts/screenshot.js \
  "http://localhost:8811/index.html" home
NODE_PATH=/opt/node-tools/node_modules node <skill_dir>/scripts/screenshot.js \
  "http://localhost:8811/briefings/2026-07-29.html" briefing
```

Actually look at all four screenshots. Check the skim block, the filter pills,
the card grid, the Market Watch ticker chips, the Fixtures Ahead rows, and the
home page's hero and topic tiles.

**Hotlinked images will not load in this sandbox** — its network egress is
allowlisted, so photo CDNs return 403 and you'll see fallback icons everywhere.
That is expected and not a bug; the same images load fine in Ankit's browser.
Judge layout, not whether photos appear. Never run `playwright install`.

## Step 5: Commit and push (this is the deploy step)

```bash
cd site
git add -A
git commit -m "Add 2026-07-29 edition"
git push origin main
```

The push triggers GitHub Actions, which deploys to Netlify — you do not call
any Netlify tool directly for a normal day's run (see
`references/netlify-deploy.md` for why: this sandbox's network egress can't
reach Netlify's own domains, only GitHub's).

Give the Action a minute or two, then verify it actually went live: use the
Netlify MCP connector's `netlify-project-services-reader` → `get-project` on
site ID `60b0eac1-cc98-4376-9d5a-720eaf799f03` and confirm `currentDeploy`
changed, and `WebFetch` the live `manifest.json` to confirm today's date is
in it. If the connector isn't enabled for this session, `WebFetch` the live
site alone is enough to confirm — don't block delivery on it either way,
but do mention in your final message if you couldn't verify.

## Step 6: Deliver

Call `SendUserFile` on today's rendered briefing HTML (the same file at
`site/public/briefings/2026-07-29.html`) with `status: "proactive"` and a caption
that is exactly one line naming the day's most distinctive story — not a
generic description of the digest as a whole.

In your accompanying message, also share the live archive URL so Ankit can
browse past editions, and note anything unusual about the run (a section that
came up thin, a story you dropped for lack of a verifiable source, deployment
being skipped, etc.) — brief, not a full recap.

## When asked to change the design or add a feature

The CSS/JS design system lives inline inside `scripts/render_briefing.py`
(the `CSS` and `JS` string constants) and in `assets/index_template.html` for
the cover page. Edit those directly rather than hand-writing one-off HTML —
keeping them as the single source of truth is what makes every future edition
(and every past one, since old pages aren't regenerated) consistent. If you
change the per-section accent colors or add a section, update both the
`ACCENT_MAP`/`PILLS` constants in `render_briefing.py` and the corresponding
research-guide/section-order notes so future unattended runs stay in sync.
