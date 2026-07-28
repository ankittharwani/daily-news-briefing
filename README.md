# Ankit's Morning Briefing — Archive

A daily news digest for Ankit, automatically researched and published each
morning (Asia/Qatar time). This repo is the source of truth for the archive:

- `index.html` — cover/archive page (lists every edition, searchable)
- `manifest.json` — one entry per day (date, caption, file path)
- `briefings/YYYY-MM-DD.html` — each day's full single-file digest

Every push to `main` triggers `.github/workflows/deploy.yml`, which deploys
this directory to Netlify as a production build. See the
`ankit-morning-briefing` skill (in the automation session that maintains this
repo) for the full research → build → publish pipeline.
