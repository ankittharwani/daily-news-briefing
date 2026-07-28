# Ankit's market watchlist

**This file deliberately lives in the skill, not in the published repo.** The
site at db.labs.tocn.ai is public and unauthenticated, so this list must never
be written into the `site/` directory — it would become fetchable by anyone.

## The hard privacy rule

Ankit's instruction, verbatim in spirit: *no numbers about his position or the
stock's move may appear on the page.* That means the rendered Market Watch
section must never contain:

- share counts, position values, or portfolio weights
- the day's percentage move or the share price
- market capitalisation framed as a move

What *is* fine, and what the section is actually for: the **company event
itself** — earnings figures, contract values, guidance numbers, analyst price
targets, regulatory decisions. "Barclays reported Q2 pretax profit of £3.25
billion, up 31%" is exactly right. "Barclays fell 5.1%" is not.

Price data is still central to the workflow — it is just a **private detector**.
You scan for movement to decide *which* companies to investigate, then write
only about what happened. Think of the move as the tip-off, never the story.

## The list (46 tickers)

Ankit gave no ordering for most of these and explicitly said to treat holdings
and watchlist names identically — *"independent of invested or watching, we just
focus on stocks where there has been a movement or event."* So do not rank by
position size or split the section into "held" versus "watching".

**US — batch these through stockanalysis.com compare URLs (12 at a time):**

```
NET TSLA AAPL INTC AMZN BA NVDA MSFT SBUX PYPL CRWD ORCL
SONO FIG GOOGL META ARM UBER ZM TWLO PLTR AI RXT FSLY
FUBO BYND JNJ CDE SRTS EDIT CRSP PLX FBIO REI HYFM XCUR
ADTX YOLO MJ
```

**Non-US — fetch individually via Google Finance (`google.com/finance/quote/TICKER:EXCHANGE`):**

```
BP:LON   RR:LON   BARC:LON   ORDS:QA   IRFC:NSE   HDFCBANK:NSE
```

## Known dead or distressed tickers

Verified 2026-07-28 — re-check occasionally rather than trusting this forever:

- **ETTX (Entasis Therapeutics)** — acquired by Innoviva and delisted in July
  2022. Dead. Excluded from the list above; do not reintroduce it.
- **LPTX (Leap Therapeutics)** — returned no data in the compare tool. Likely
  delisted or renamed; excluded pending verification.
- **XCUR (Exicure)** — trading but has had a Nasdaq minimum-equity compliance
  notice. Alive, low signal.
- **ADTX (Aditxt)** — trading at fractions of a cent. Any "news" here is
  realistically delisting or reverse-split mechanics; include only if that is
  genuinely the story.

## Themes, for context when a sector-wide driver is the real cause

Often the honest answer is that nothing company-specific happened and the move
was sector-driven. Say so plainly — "no company-specific announcement was found
for the session" is a perfectly good line, and much better than inventing a
cause. These clusters are where that reasoning usually applies:

- **Cloud, dev-infra and security** — NET, FSLY, RXT, CRWD, PLTR, TWLO, FIG, ZM
- **Semis and AI compute** — NVDA, INTC, ARM, AI. Watch AMD, TSMC, ASML, Micron
  as the read-across names whose news explains moves here.
- **Mega-cap tech** — AAPL, AMZN, GOOGL, META, MSFT, ORCL
- **Gene editing and small-cap biotech** — CRSP, EDIT, PLX, FBIO, SRTS, JNJ.
  Intellia and Beam are the usual read-across.
- **Energy and metals** — BP, REI, CDE. The driver is usually the oil or silver
  price itself rather than any company announcement.
- **Cannabis** — YOLO, MJ, HYFM
- **Consumer and mobility** — TSLA, SBUX, BYND, SONO, PYPL, UBER
- **Aerospace and industrials** — BA, RR. Airbus and GE Aerospace read across.
- **Banking and India/Gulf** — BARC, HDFCBANK, IRFC, ORDS

## Keeping it current

If Ankit adds or drops names, edit this file — it is the single source of truth
for the scan. There is no ticker list anywhere in the repo to keep in sync.
