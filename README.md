# Ankit's Morning Briefing — Archive

A daily news digest for Ankit, researched and published automatically each
morning (7am Asia/Qatar). Live at **https://db.labs.tocn.ai**

## Layout

| Path | Published? | What it is |
|---|---|---|
| `public/` | **yes** | Everything served at db.labs.tocn.ai |
| `public/index.html` | yes | Archive home — hero, topic tiles, cross-edition search |
| `public/briefings/*.html` | yes | One self-contained page per edition |
| `public/manifest.json` | yes | Edition index driving the home page |
| `public/search-index.json` | yes | Full-text index across every edition |
| `data/*.json` | no | Structured content each edition was built from |
| `skill/` | no | Durable copy of the automation skill |

`netlify.toml` sets `publish = "public"`, so `data/` and `skill/` stay private.
This matters: `skill/references/watchlist.md` contains a personal stock
watchlist and the site is public. Do not flatten this structure.

## Deployment

Every push to `main` runs `.github/workflows/deploy.yml`, which deploys
`public/` to Netlify using the `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID`
repository secrets.

## Rebuilding

`skill/SKILL.md` documents the full pipeline: research → render → update
manifest and search index → render-check → push. The scripts in `skill/scripts/`
are the same ones the daily run uses.
