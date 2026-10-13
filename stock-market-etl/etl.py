"""
Stock Market ETL + Dashboard
============================
Extracts 5 years of daily OHLCV data for 5 large-cap US stocks, normalizes
it into one warehouse table, and analyzes trend, returns, and volatility.

Data source note: the original plan was Stooq's free daily CSVs, but Stooq
serves a JavaScript browser-check page to this machine, so extraction uses
Yahoo Finance's public chart API instead (same daily OHLCV data). The raw
per-ticker CSVs are cached in data/, so re-runs work offline too.

Tickers: AAPL, MSFT, AMZN, NVDA, GOOG (Alphabet Class C)

Run:  python3 etl.py
Outputs (in ./outputs): stocks.db, dashboard.png, kpis.txt
"""
import json
import sqlite3
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
DB = OUT / "stocks.db"
TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOG"]
NAMES = {"AAPL": "Apple", "MSFT": "Microsoft", "AMZN": "Amazon",
         "NVDA": "NVIDIA", "GOOG": "Alphabet"}


def extract() -> None:
    """Fetch daily bars from Yahoo's chart API; cache one CSV per ticker."""
    for t in TICKERS:
        cache = DATA / f"{t.lower()}.csv"
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{t}"
               "?range=5y&interval=1d")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read())
            result = payload["chart"]["result"][0]
            quote = result["indicators"]["quote"][0]
            df = pd.DataFrame({
                "Date": pd.to_datetime(result["timestamp"], unit="s",
                                       utc=True).tz_convert("America/New_York").date,
                "Open": quote["open"], "High": quote["high"],
                "Low": quote["low"], "Close": quote["close"],
                "Volume": quote["volume"],
            })
            df.to_csv(cache, index=False)
            print(f"[extract] {t}: downloaded {len(df):,} rows -> {cache.name}")
        except Exception as e:  # fall back to the cached CSV if present
            if cache.exists():
                print(f"[extract] {t}: download failed ({e}); using cached CSV")
            else:
                raise


def transform() -> pd.DataFrame:
    """Combine per-ticker CSVs into one clean, normalized table."""
    frames = []
    for t in TICKERS:
        d = pd.read_csv(DATA / f"{t.lower()}.csv", parse_dates=["Date"])
        d["ticker"] = t
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    rows_in = len(df)
    df = df.dropna(subset=["Close"])           # holidays return null bars
    df = df.drop_duplicates(subset=["ticker", "Date"])
    df = df.sort_values(["ticker", "Date"]).reset_index(drop=True)
    df.columns = [c.lower() for c in df.columns]
    print(f"[transform] rows in: {rows_in:,} -> clean rows: {len(df):,} "
          f"({df['date'].min().date()} to {df['date'].max().date()})")
    return df


def load(df: pd.DataFrame) -> sqlite3.Connection:
    dim = pd.DataFrame({"ticker": TICKERS,
                        "company": [NAMES[t] for t in TICKERS]})
    fact = df.copy()
    fact["date"] = fact["date"].dt.strftime("%Y-%m-%d")
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    dim.to_sql("dim_ticker", con, index=False)
    fact.to_sql("fact_prices", con, index=False)
    con.execute("CREATE INDEX idx_prices ON fact_prices(ticker, date)")
    con.commit()
    print(f"[load] fact_prices rows: {len(fact):,} | tickers: {len(dim)}")
    return con


def analyze(con: sqlite3.Connection, df: pd.DataFrame) -> dict:
    q = lambda sql: pd.read_sql(sql, con)
    k = {}
    k["latest"] = q("""
        SELECT f.ticker, f.date, ROUND(f.close, 2) latest_close
        FROM fact_prices f
        JOIN (SELECT ticker, MAX(date) d FROM fact_prices GROUP BY ticker) m
          ON f.ticker = m.ticker AND f.date = m.d
        ORDER BY f.ticker""")
    k["ma"] = q("""
        SELECT ticker, date, close,
               AVG(close) OVER (PARTITION BY ticker ORDER BY date
                   ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) ma30,
               AVG(close) OVER (PARTITION BY ticker ORDER BY date
                   ROWS BETWEEN 89 PRECEDING AND CURRENT ROW) ma90
        FROM fact_prices""")
    # Period + 1-year returns and volatility from daily returns (pandas
    # aggregates the SQL-shaped series; SQLite has no STDEV aggregate).
    stats = []
    for t, g in df.groupby("ticker"):
        g = g.sort_values("date")
        rets = g["close"].pct_change().dropna()
        stats.append({
            "ticker": t,
            "start_close": g["close"].iloc[0],
            "latest_close": g["close"].iloc[-1],
            "period_return_pct": 100 * (g["close"].iloc[-1] / g["close"].iloc[0] - 1),
            "one_year_return_pct": 100 * (g["close"].iloc[-1] / g["close"].iloc[-252] - 1)
                if len(g) > 252 else float("nan"),
            "volatility_pct": 100 * rets.std() * (252 ** 0.5),  # annualized
            "best_day_pct": 100 * rets.max(),
            "worst_day_pct": 100 * rets.min(),
            "trading_days": len(g),
        })
    k["stats"] = pd.DataFrame(stats)
    return k


def dashboard(k: dict, df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Stock Market Dashboard — 5 years of daily prices "
                 "(AAPL, MSFT, AMZN, NVDA, GOOG)", fontsize=13, fontweight="bold")

    ax = axes[0, 0]
    for t, g in df.groupby("ticker"):
        g = g.sort_values("date")
        ax.plot(g["date"], 100 * g["close"] / g["close"].iloc[0], label=t, lw=1.2)
    ax.set_title("Indexed price (start = 100)"); ax.legend(fontsize=8)

    ax = axes[0, 1]
    top = k["stats"].sort_values("period_return_pct").iloc[-1]["ticker"]
    ma = k["ma"][k["ma"]["ticker"] == top].copy()
    ma["date"] = pd.to_datetime(ma["date"])
    ax.plot(ma["date"], ma["close"], label="Close", lw=1.1)
    ax.plot(ma["date"], ma["ma30"], label="MA 30", lw=1.1)
    ax.plot(ma["date"], ma["ma90"], label="MA 90", lw=1.1)
    ax.set_title(f"{top} close with 30/90-day moving averages"); ax.legend(fontsize=8)

    ax = axes[1, 0]
    s = k["stats"].sort_values("volatility_pct")
    ax.barh(s["ticker"], s["volatility_pct"], color="#c53030")
    ax.set_title("Annualized volatility % (daily returns)"); ax.set_xlabel("%")

    ax = axes[1, 1]
    s = k["stats"].sort_values("period_return_pct")
    ax.barh(s["ticker"], s["period_return_pct"], color="#2f855a")
    ax.set_title("Total return over the period %"); ax.set_xlabel("%")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "dashboard.png", dpi=130)
    print(f"[dashboard] wrote {OUT / 'dashboard.png'}")


def main() -> None:
    extract()
    df = transform()
    con = load(df)
    k = analyze(con, df)
    s = k["stats"].sort_values("period_return_pct", ascending=False)
    lines = [
        "Latest closes:\n" + k["latest"].to_string(index=False),
        "Per-ticker stats:\n" + s.round(2).to_string(index=False),
    ]
    (OUT / "kpis.txt").write_text("\n\n".join(lines))
    print("\n\n".join(lines))
    dashboard(k, df)
    con.close()
    print("[done] stock-market-etl complete")


if __name__ == "__main__":
    main()
