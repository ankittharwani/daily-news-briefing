# Researching the Market Watch section

Read `watchlist.md` first — it holds the 46 tickers and, more importantly, the
hard rule that no price or position numbers may reach the page.

## Why the scan is movement-first

46 companies is far too many to write about daily, and on any given day most of
them have no story. Rather than picking favourites, let the market tell you
where to look: scan everything, then investigate only what actually moved. This
keeps the section honest — it surfaces the small holding that dropped 8% on real
news instead of dutifully reporting that Apple was flat again.

## Step 1: scan for movement (cheap, ~6 fetches)

**US tickers** — stockanalysis.com's compare page takes up to 12 symbols in one
fetch and returns current price and day change for each:

```
https://stockanalysis.com/stocks/compare/AAPL-vs-INTC-vs-AMZN-vs-BA-vs-NVDA-vs-MSFT-vs-SBUX-vs-PYPL-vs-CRWD-vs-ORCL-vs-GOOGL-vs-META/
```

Ask the fetch: *"For each ticker on this comparison page, list the ticker symbol,
current price, and today's percentage change. Give exact figures for every ticker
shown."* Four batches covers the US names.

**Non-US tickers** — use Google Finance individually
(`https://www.google.com/finance/quote/BP:LON`). Two cautions learned the hard
way: stockanalysis.com's international quote pages returned data weeks stale,
and even Google Finance sometimes serves a cached page from months back. **Always
ask for the quote timestamp and discard anything not from today** — reporting a
stale move as today's news is worse than omitting the company.

## Step 2: pick what to investigate

Roughly ±3% is a sensible threshold for a large-cap and a reasonable floor
generally, but treat it as a starting point rather than a rule. A 2% move in a
mega-cap on the day it reports earnings is a story; a 15% move in a sub-penny
stock usually is not. Aim to end up investigating 8-12 names and publishing
6-9 — enough that the section feels substantial, few enough that it doesn't
swamp the briefing.

## Step 3: find the actual cause

For each candidate, search for the company name plus a keyword like earnings,
guidance, contract, analyst or news, then fetch a specific article. Look for:
earnings or guidance, product and contract announcements, analyst rating and
price-target changes, regulatory or legal decisions, M&A, index inclusion, and
sector-wide drivers.

Three things make this section good rather than merely present:

**Say when there is no company-specific cause.** Frequently the honest finding
is that a stock rode a sector move. Write that — "Ring Energy is a small-cap
Permian producer with high sensitivity to spot crude, and no company-specific
announcement was found for the session" — rather than manufacturing a narrative.

**Notice when one event explains several names.** On 2026-07-28 a single report
about Nvidia backstopping OpenAI's data-centre leases drove Nvidia down and
rotated money into Oracle, Figma and C3.ai. Writing those as one connected story
across four cards is far more useful than four unconnected ones.

**Cross-check against the rest of the briefing.** If the Business & Markets
section already covers the oil price falling on the Iran ceasefire, and that is
what moved Ring Energy, mark the Market Watch card `"continues": true` and let
the two sections speak to each other.

## Step 4: write it

Each entry becomes an object in the `portfolio` array of `content.json`:

```json
{
  "ticker": "BARC.L",
  "headline": "Barclays Q2 profit jumps 31% and buyback raised to £1bn, but costs overshoot",
  "body": "2-3 sentences on the company event, with figures from the event itself. Cite source and date in prose, e.g. 'per MarketScreener (Jul 28)'. No share price, no percentage move.",
  "img": "https://... or null",
  "url": "https://exact-article-url",
  "continues": true
}
```

The `ticker` renders as a small chip on the card. Order the array by how much the
story matters to a reader, not alphabetically and not by move size — a major
holding with a real corporate event outranks a micro-cap that drifted.

Before you finish, reread every `body` string and check it contains no share
price and no percentage move. That check is the one thing in this section that
is not a matter of judgement.
