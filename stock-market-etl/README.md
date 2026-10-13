# Stock Market ETL + Dashboard

Downloads 5 years of daily prices for five large-cap US stocks, normalizes
them into one SQLite warehouse, and compares trend, return, and risk.

**Business question:** Over the last 5 years, which of these stocks actually
performed — and how much volatility did you have to sit through to get it?

**Stack:** Python (pandas, urllib) · SQLite · SQL (window functions) · matplotlib

**Data source — substitution note:** The original plan was Stooq's free
daily CSVs, but Stooq serves a JavaScript browser-check page to scripted
downloads from this machine, so extraction uses **Yahoo Finance's public
chart API** instead (same daily OHLCV data). Raw per-ticker CSVs are cached
in `data/` (`aapl.csv`, `msft.csv`, `amzn.csv`, `nvda.csv`, `goog.csv`), so
re-runs also work offline.

## Pipeline (`python3 etl.py`)

1. **Extract** — 5 tickers × ~1,254 trading days (Oct 14, 2021 – Oct 13,
   2026) from Yahoo's chart API, cached as per-ticker CSVs.
2. **Transform** — combine into one table, drop null holiday bars, dedupe
   on (ticker, date), sort. 6,270 rows in → 6,270 clean rows.
3. **Load** — `outputs/stocks.db`: `fact_prices` (6,270 rows) + `dim_ticker`.
4. **Analyze** — `analysis.sql`: latest close per ticker, 30/90-day moving
   averages and daily returns with SQL window functions; volatility
   (annualized) and period/1-year returns aggregated in `etl.py` (SQLite
   has no STDEV aggregate).
5. **Present** — `outputs/dashboard.png`: indexed price lines (start = 100),
   top performer with MA30/MA90, volatility ranking, total-return ranking.

## Key findings

- NVDA: +950.86% over 5 years — and the highest volatility at 51.91%.
- In the last year GOOG (+42.87%) and AAPL (+37.80%) led; MSFT returned
  only +5.72% despite a strong 5-year run.

See `INSIGHTS.md` for the full findings with numbers.
