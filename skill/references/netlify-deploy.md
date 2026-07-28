# Deploying the archive: GitHub → GitHub Actions → Netlify

The archive is a git repository, and the repository itself is the durable
source of truth for every past edition — not the live Netlify site. This
matters because each morning's run is a **brand-new session** with no local
memory of prior days; cloning the repo is how you get that history back.

## Repo layout — and what is deliberately not published

```
public/          <-- the ONLY directory served at db.labs.tocn.ai
  index.html
  manifest.json
  search-index.json
  briefings/YYYY-MM-DD.html
data/            <-- structured content JSON per edition (not published)
skill/           <-- durable copy of this skill (not published)
netlify.toml     <-- publish = "public"
.github/workflows/deploy.yml
```

`netlify.toml` sets `publish = "public"` and the workflow deploys `--dir=public`,
so anything outside `public/` stays in the repo but never reaches the internet.
That separation exists for a specific reason: `skill/references/watchlist.md`
holds Ankit's stock watchlist, and the site is public and unauthenticated. If
you ever flatten this structure or change the publish directory, you will
silently expose it. Don't.

`data/YYYY-MM-DD.json` is the structured content each edition was rendered from.
Commit it alongside the HTML — it costs nothing and means any future rebuild,
redesign or migration can regenerate every past edition from clean data instead
of scraping its own HTML back out.

`skill/` is a copy of this skill committed into the repo because the sandbox
each scheduled run gets is ephemeral — if the container is ever recycled, the
installed skill goes with it. Whoever runs next can restore the whole pipeline
from `skill/SKILL.md` in the clone. Keep it in sync when you change the skill.

**Repo:** `https://github.com/ankittharwani/daily-news-briefing`
**Netlify site:** `ankit-morning-briefing` (site ID `60b0eac1-cc98-4376-9d5a-720eaf799f03`)
**Live URL:** `https://db.labs.tocn.ai/` — this is the canonical URL Ankit
uses (custom domain on Netlify DNS, configured 2026-07-28). The site's
original `http://ankit-morning-briefing.netlify.app` still works too, but
always share the `db.labs.tocn.ai` link with Ankit. If it ever stops
resolving, double check via `get-project` on the site ID rather than assuming
— but don't switch back to the netlify.app link without a clear reason.

## Why GitHub Actions, not a direct Netlify deploy

Two things were tried and ruled out while first building this (2026-07-28) —
don't re-attempt them, they're dead ends specific to this sandboxed
environment:

- **The Netlify MCP connector's `deploy-site` tool** doesn't upload files
  itself — it only returns a `npx @netlify/mcp ... --proxy-path ...` shell
  command to run. That command fails with a 403 from this sandbox every
  time: this environment's network egress is allowlisted to specific hosts,
  and neither `api.netlify.com` nor `netlify-mcp.netlify.app` are on it (nor
  is a personal Claude.ai account able to change that allowlist — it's an
  admin-console setting for Team/Enterprise orgs only).
- **A direct `curl`/API call to `api.netlify.com` with a Netlify personal
  access token** hits the exact same egress block — confirmed via
  `Host not in allowlist: api.netlify.com` errors from both `curl` and Node's
  `fetch`.

**What does work:** plain `git` operations against `github.com` (clone, push)
are not blocked by that allowlist. So the deploy path that actually functions
from this sandbox is: push to GitHub, and let a GitHub Actions runner (which
has full, unrestricted internet access) do the actual Netlify upload.

If a future run finds Netlify's own domains ARE reachable (e.g. this skill is
invoked from a different, less restricted environment), the GitHub Actions
path still works fine and there's no need to switch — it's not a workaround
you should try to "upgrade" away from.

## The daily sequence

1. **Clone the repo** to get the full prior archive:
   ```bash
   git clone https://<GITHUB_TOKEN>@github.com/ankittharwani/daily-news-briefing.git site
   cd site
   ```
   You'll need a GitHub token with `Contents: Read and write` (and
   `Workflows: Read and write` if you ever need to touch
   `.github/workflows/deploy.yml` again) scoped to this repo. If you don't
   have one cached anywhere, ask Ankit for a fresh fine-grained personal
   access token — same as the first setup.

2. **Render today's briefing and update the manifest** exactly as described
   in `SKILL.md` steps 1-3, writing into this cloned `site/` directory.

3. **Render-check** (SKILL.md step 4) before committing anything.

4. **Commit and push:**
   ```bash
   git add -A
   git commit -m "Add YYYY-MM-DD edition"
   git push origin main
   ```
   Pushing to `main` triggers `.github/workflows/deploy.yml`, which installs
   `netlify-cli` on GitHub's runner and deploys this exact directory to the
   Netlify site above using two repo secrets that already exist —
   `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID`. You don't need to touch Netlify
   directly at all on a normal day.

5. **Verify the deploy actually went live** — this sandbox can't reach GitHub's
   API (`api.github.com`) or Netlify's site directly via `curl`, but the
   Netlify MCP connector's `get-project` read operation works (it's proxied
   through Anthropic's infrastructure, not raw sandbox egress), and so does
   `WebFetch` against the public site URL. Use both:
   - `netlify-project-services-reader` → `get-project` with the site ID above;
     check `currentDeploy.state == "ready"` and that `currentDeploy.id` is new
     (changed since before you pushed).
   - `WebFetch` the live URL's `manifest.json` and confirm today's date is in
     it, and `WebFetch` today's `briefings/YYYY-MM-DD.html` and confirm the
     section headings are all present.
   Give the GitHub Actions run a minute or two to finish (checkout + npm
   install + netlify-cli deploy) before checking.

## If the workflow or secrets are ever missing

`.github/workflows/deploy.yml` and the two repo secrets
(`NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID`) should already exist in the repo
from initial setup. If a push doesn't trigger a deploy and you suspect they're
missing or broken, don't try to fix GitHub Actions secrets yourself (setting
secrets requires the GitHub API, which this sandbox can't reach) — flag it to
Ankit plainly rather than guessing.

## Custom domain

No tool available to this skill can manage Netlify custom domains or DNS —
that's a one-time manual step in the Netlify dashboard (Site → Domain
management → Add a domain) if Ankit wants a custom subdomain instead of the
default `*.netlify.app` URL. Don't attempt to script this; point him at the
dashboard if it ever comes up.
