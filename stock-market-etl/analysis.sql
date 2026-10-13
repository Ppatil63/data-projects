-- Stock Market — analysis queries (SQLite, run against outputs/stocks.db)
-- Schema: fact_prices (ticker, date, open, high, low, close, volume)
--         + dim_ticker

-- 1. Latest close per ticker
SELECT f.ticker, f.date, ROUND(f.close, 2) AS latest_close
FROM fact_prices f
JOIN (SELECT ticker, MAX(date) AS d FROM fact_prices GROUP BY ticker) m
  ON f.ticker = m.ticker AND f.date = m.d
ORDER BY f.ticker;

-- 2. 30-day and 90-day moving averages (window functions)
SELECT ticker, date, ROUND(close, 2) AS close,
       ROUND(AVG(close) OVER (PARTITION BY ticker ORDER BY date
              ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 2) AS ma30,
       ROUND(AVG(close) OVER (PARTITION BY ticker ORDER BY date
              ROWS BETWEEN 89 PRECEDING AND CURRENT ROW), 2) AS ma90
FROM fact_prices
ORDER BY ticker, date DESC
LIMIT 20;

-- 3. Daily returns per ticker (LAG window function)
SELECT ticker, date, ROUND(close, 2) AS close,
       ROUND(100.0 * (close - LAG(close) OVER w) / LAG(close) OVER w, 2)
           AS daily_return_pct
FROM fact_prices
WINDOW w AS (PARTITION BY ticker ORDER BY date)
ORDER BY ticker, date DESC
LIMIT 20;

-- 4. Average daily volume and price range per ticker
SELECT ticker, COUNT(*) AS trading_days,
       ROUND(AVG(volume)) AS avg_daily_volume,
       ROUND(MIN(close), 2) AS period_low, ROUND(MAX(close), 2) AS period_high
FROM fact_prices GROUP BY ticker ORDER BY ticker;

-- Volatility and total return are aggregated in etl.py from the daily-return
-- series above (SQLite has no built-in STDEV aggregate); see outputs/kpis.txt.
