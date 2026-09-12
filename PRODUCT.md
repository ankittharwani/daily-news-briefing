# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary user is Ankit, who reads this every morning (usually on his phone,
in Doha, Qatar) before the day starts. Confirmed: the site is sometimes
shared with a few other people too, so it should read reasonably well to
someone unfamiliar with the format — not purely personal shorthand only
Ankit could decode.

## Product Purpose

A fully-automated daily news digest, researched and rendered unattended by a
scheduled task every morning, then published to a public (unauthenticated,
but unlisted/unadvertised) archive site. It exists to give Ankit one
considered pass over the news that actually matters to him — world events,
sport, business/markets, AI, geopolitics, his personal stock watchlist
(content only, never numbers — see Capabilities and Constraints), country
updates for the places he cares about, and local Doha events — without
having to assemble that himself from a dozen sources every day.

Confirmed: fast skim matters most. Most mornings this is skimmed quickly,
not read deeply — scanability should be prioritized over rich detail or
density. The existing "30-Second Skim" block at the top of every edition is
a direct expression of this and should stay central, not be treated as a
minor feature.

## Positioning

Not a general news aggregator or reader (Feedly, Google News, Axios) — it is
a single-recipient personal briefing with editorial continuity: it tracks
what Ankit has already read and explicitly marks follow-up stories as
"Continuing" rather than re-explaining background he already has. No other
product does that for one specific reader's ongoing story threads. The
archive itself (every past edition, searchable) is also part of the product,
not just today's page.

## Operating Context

- Researched and rendered by an unattended scheduled agent once a day
  (~7am Asia/Qatar), with no human in the loop for a normal day's run.
- Read overwhelmingly on a phone, first thing in the morning.
- Occasionally the link is shared with a few other people.
- The whole pipeline (research → render → archive → deploy) is documented
  in `skill/SKILL.md`; this PRODUCT.md is scoped to product truth, not that
  operational detail.

## Capabilities and Constraints

- **Eight sections in a fixed order**, every edition: World, Sports (with a
  Fixtures Ahead sub-block), Business & Markets, AI & Technology,
  Geopolitics, Market Watch, Country Updates (India / United Kingdom /
  Qatar & the GCC sub-groups), Doha Events — topped by the 30-Second Skim.
  This order and the section set are a hard constraint the daily automation
  depends on (`ACCENT_MAP`/`PILLS` in `skill/scripts/render_briefing.py` and
  `skill/references/research-guide.md` must stay in sync with each other).
- **Market Watch must never render a share price, percentage move, position
  size, or share count** — a hard privacy rule from Ankit about his own
  holdings. The section may describe company events (earnings, guidance,
  contract values, analyst targets) but never his position or the stock's
  move. This is a content/rendering rule, not primarily a visual one, but no
  new visual element (sparkline, numeric badge, etc.) may leak it either.
- **Each briefing page must stay a single self-contained HTML file** — no
  external CSS/JS files, no web fonts, no build pipeline. Hotlinked images
  from the original article's CDN are the one exception. This is what makes
  every past edition a durable, independent artifact and is why the "design
  system" is literally CSS/JS string constants inside
  `skill/scripts/render_briefing.py` plus `skill/assets/index_template.html`
  — there is nowhere else for shared styles or scripts to live.
- **Past editions under `public/briefings/*.html` are frozen snapshots** —
  changing the design does not retroactively re-render them; that is a
  deliberate, separate, optional batch step done later and only on request.
- Mobile must keep working — it's read on a phone most mornings.
- Terminology: "edition" = one day's page; "Market Watch" = the
  watchlist-event section (not "portfolio" in any user-facing copy, even
  though the internal data key is `portfolio`).

## Brand Commitments

- Name: "Ankit's Morning Briefing" — confirmed to keep for now (no request
  to rename came up), but the user is **open to reframing** the product's
  visual/conceptual identity beyond a strict "personal newspaper" pastiche
  if a different frame serves fast-skim reading better — this is not
  locked to a broadsheet/editorial treatment by mandate, just by default.
- The previous logo mark (a sunrise-over-horizon icon) was explicitly
  rejected by the user ("not very fond of the logo, can't trust the design
  outcome") — treat it as anti-reference, not a direction to refine. No
  replacement direction has been mandated; new-work should propose one.
- Section accent colors (`ACCENT_MAP` in `render_briefing.py`) and the
  existing ink/wash palette are incumbent implementation, not confirmed
  brand commitments — evidence to weigh, not a constraint to preserve.

## Evidence on Hand

- `data/YYYY-MM-DD.json` — every past edition's structured content (real
  production content, not placeholder).
- `public/briefings/*.html`, `public/index.html` — the live, shipped
  incumbent implementation (currently mid-redesign; the most recent
  `public/index.html` and `public/briefings/2026-09-12.html` are an
  unapproved first-pass draft, not the confirmed incumbent to preserve).
- `skill/SKILL.md`, `skill/references/*.md` — the full daily research/render
  pipeline and its editorial rules (sourcing per section, the Market Watch
  privacy rule, fixture-ahead framing).
- `README.md` — repo/deploy layout.
- No user research, testimonials, or analytics exist beyond Ankit's own
  stated preferences; do not fabricate any.

## Product Principles

1. Skim first. The reader's default mode is fast scanning, not deep
   reading — hierarchy, the 30-Second Skim, and navigation should all
   optimize for "what do I need to know in the next 30 seconds," with depth
   available but never required.
2. One recipient, continuity-aware. Every design and copy decision can
   assume a returning daily reader who has seen yesterday's edition —
   lean into that (the "Continuing" tag, an archive that's actually
   browsable) rather than re-explaining from zero each day.
3. Self-contained by necessity, not by taste. The single-file-per-page,
   no-build-step, system-font-only constraint is permanent infrastructure,
   not a temporary limitation — design within it rather than around it.
4. Never leak the watchlist numbers. The Market Watch privacy rule is
   absolute and takes priority over any visual idea that would require a
   number, price, or percentage to render.
5. A public URL, a private readership. It's unauthenticated and occasionally
   shared, so it must stand on its own to a first-time viewer — but it is
   not trying to acquire an audience or compete with a public news product.

## Accessibility & Inclusion

No formally required standard confirmed. Reading context is a real product
signal: mostly phone, often early morning/low light — a genuine dark mode is
worth building, not a decorative extra (see Product Principles).
