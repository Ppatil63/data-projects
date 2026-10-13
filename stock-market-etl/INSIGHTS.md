# Insights — Stock Market ETL (Oct 14, 2021 – Oct 13, 2026)

Every number below is computed by `etl.py` from the actual downloaded data
(1,254 trading days per ticker, 6,270 rows) and stored in `outputs/kpis.txt`.

- **NVIDIA ran away with the period.** NVDA rose from $21.75 to $228.52 —
  a **+950.86%** total return, roughly 6× the next best performer. The
  other four are not close: GOOG +147.16%, AAPL +137.39%, MSFT +79.50%,
  AMZN +56.72%.
- **That return came with the wildest ride.** NVDA's annualized volatility
  is 51.91% — far above AAPL (28.03%) and MSFT (28.19%) — with a best day
  of +24.37% and a worst day of −16.97%. Highest return, highest risk.
- **The last year reshuffled the order.** Over the most recent ~252 trading
  days, Alphabet led with +42.87% and Apple returned +37.80%, while
  Microsoft managed only +5.72% despite its solid 5-year gain — recent
  momentum and long-term performance tell different stories.
- **Amazon is the quiet laggard with a temper.** AMZN has the weakest
  5-year return (+56.72%) but the second-highest volatility (36.53%) and a
  −14.05% worst day — more risk than MSFT/AAPL for less return over this
  window.
- **Latest closes (Oct 13, 2026):** MSFT $543.45, GOOG $349.52, AAPL
  $341.27, AMZN $258.58, NVDA $228.52 — absolute price levels say nothing
  about performance, which is why the dashboard indexes every series to
  100 at the start date.
