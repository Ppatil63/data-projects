"""
Retail Sales ETL + Dashboard
============================
Extracts the classic "Sample Superstore" retail dataset (Tableau's public
sample data, mirrored on GitHub), cleans it, loads it into a SQLite star
schema, runs SQL analysis, and renders a 4-panel dashboard PNG.

Run:  python3 etl.py
Outputs (in ./outputs):
  - superstore.db   SQLite star-schema warehouse
  - dashboard.png   4-panel matplotlib dashboard
  - kpis.txt        headline numbers used for INSIGHTS.md
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent
RAW = BASE / "data" / "superstore.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
DB = OUT / "superstore.db"


def extract() -> pd.DataFrame:
    """Read the raw CSV (the mirror file is UTF-8 with a few special chars)."""
    try:
        df = pd.read_csv(RAW, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(RAW, encoding="latin1")
    print(f"[extract] raw rows: {len(df):,}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean: tidy column names, parse dates, fix types, drop bad rows."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_")
                  for c in df.columns]
    rows_in = len(df)

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
    df["postal_code"] = df["postal_code"].astype(str).str.zfill(5)
    for col in ("sales", "profit", "discount", "quantity"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates()
    df = df.dropna(subset=["order_date", "sales", "profit", "product_id",
                           "customer_id", "region"])
    df = df[df["sales"] >= 0]
    print(f"[transform] rows in: {rows_in:,} -> clean rows: {len(df):,} "
          f"(removed {rows_in - len(df):,})")
    return df.reset_index(drop=True)


def load(df: pd.DataFrame) -> sqlite3.Connection:
    """Load a star schema: fact_sales + dim_product/customer/region/date."""
    # --- dimensions -------------------------------------------------------
    dim_product = (df[["product_id", "product_name", "category", "sub_category"]]
                   .drop_duplicates("product_id").reset_index(drop=True))
    dim_customer = (df[["customer_id", "customer_name", "segment"]]
                    .drop_duplicates("customer_id").reset_index(drop=True))
    dim_region = (df[["region", "state", "city", "postal_code", "country"]]
                  .drop_duplicates().reset_index(drop=True))
    dim_region["region_key"] = dim_region.index + 1

    dates = pd.DataFrame({"date": pd.unique(
        pd.concat([df["order_date"], df["ship_date"]]))}).dropna()
    dates["date_key"] = dates["date"].dt.strftime("%Y%m%d").astype(int)
    dates["year"] = dates["date"].dt.year
    dates["month"] = dates["date"].dt.month
    dates["month_name"] = dates["date"].dt.strftime("%b")
    dates["quarter"] = dates["date"].dt.quarter
    dim_date = dates.sort_values("date_key")

    # --- fact -------------------------------------------------------------
    f = df.merge(dim_region, on=["region", "state", "city", "postal_code",
                                  "country"], how="left")
    fact = pd.DataFrame({
        "row_id": f["row_id"],
        "order_id": f["order_id"],
        "product_id": f["product_id"],
        "customer_id": f["customer_id"],
        "region_key": f["region_key"],
        "order_date_key": f["order_date"].dt.strftime("%Y%m%d").astype(int),
        "ship_date_key": f["ship_date"].dt.strftime("%Y%m%d").astype(int),
        "ship_mode": f["ship_mode"],
        "sales": f["sales"],
        "quantity": f["quantity"],
        "discount": f["discount"],
        "profit": f["profit"],
    })

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    dim_product.to_sql("dim_product", con, index=False)
    dim_customer.to_sql("dim_customer", con, index=False)
    dim_region.to_sql("dim_region", con, index=False)
    dim_date.assign(date=dim_date["date"].dt.strftime("%Y-%m-%d")) \
        .to_sql("dim_date", con, index=False)
    fact.to_sql("fact_sales", con, index=False)
    con.executescript("""
        CREATE INDEX idx_fact_product ON fact_sales(product_id);
        CREATE INDEX idx_fact_order_date ON fact_sales(order_date_key);
    """)
    con.commit()
    print(f"[load] fact_sales rows: {len(fact):,} | dim_product: "
          f"{len(dim_product):,} | dim_customer: {len(dim_customer):,} | "
          f"dim_region: {len(dim_region):,} | dim_date: {len(dim_date):,}")
    return con


def analyze(con: sqlite3.Connection) -> dict:
    """Run the analysis queries (same SQL as analysis.sql) and collect KPIs."""
    q = lambda sql: pd.read_sql(sql, con)
    k = {}
    tot = q("SELECT SUM(sales) s, SUM(profit) p, COUNT(*) n, "
            "COUNT(DISTINCT order_id) o FROM fact_sales").iloc[0]
    k["total_sales"], k["total_profit"] = tot.s, tot.p
    k["rows"], k["orders"] = int(tot.n), int(tot.o)
    k["margin"] = 100 * tot.p / tot.s

    k["by_category"] = q("""
        SELECT p.category, SUM(f.sales) sales, SUM(f.profit) profit
        FROM fact_sales f JOIN dim_product p USING(product_id)
        GROUP BY p.category ORDER BY sales DESC""")
    k["by_region"] = q("""
        SELECT r.region, SUM(f.sales) sales, SUM(f.profit) profit
        FROM fact_sales f JOIN dim_region r USING(region_key)
        GROUP BY r.region ORDER BY profit DESC""")
    k["monthly"] = q("""
        SELECT d.year, d.month, SUM(f.sales) sales
        FROM fact_sales f JOIN dim_date d ON f.order_date_key = d.date_key
        GROUP BY d.year, d.month ORDER BY d.year, d.month""")
    k["top_products"] = q("""
        SELECT p.product_name, SUM(f.profit) profit, SUM(f.sales) sales
        FROM fact_sales f JOIN dim_product p USING(product_id)
        GROUP BY p.product_name ORDER BY profit DESC LIMIT 10""")
    k["worst_products"] = q("""
        SELECT p.product_name, SUM(f.profit) profit
        FROM fact_sales f JOIN dim_product p USING(product_id)
        GROUP BY p.product_name ORDER BY profit ASC LIMIT 5""")
    k["discount"] = q("""
        SELECT CASE WHEN discount = 0 THEN 'No discount'
                    WHEN discount <= 0.2 THEN '1-20%'
                    WHEN discount <= 0.4 THEN '21-40%'
                    ELSE 'Over 40%' END bucket,
               COUNT(*) lines, ROUND(AVG(profit),2) avg_profit
        FROM fact_sales GROUP BY bucket""")
    k["by_year"] = q("""
        SELECT d.year, SUM(f.sales) sales, SUM(f.profit) profit
        FROM fact_sales f JOIN dim_date d ON f.order_date_key = d.date_key
        GROUP BY d.year ORDER BY d.year""")
    furn = k["by_category"].set_index("category")
    k["furniture_margin"] = 100 * furn.loc["Furniture", "profit"] / furn.loc["Furniture", "sales"]
    k["tech_margin"] = 100 * furn.loc["Technology", "profit"] / furn.loc["Technology", "sales"]
    return k


def dashboard(k: dict) -> None:
    """Render the 4-panel dashboard PNG."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Retail Sales Dashboard — Sample Superstore (2014–2017)",
                 fontsize=14, fontweight="bold")

    ax = axes[0, 0]
    ax.bar(k["by_category"]["category"], k["by_category"]["sales"] / 1000,
           color="#2b6cb0")
    ax.set_title("Sales by Category"); ax.set_ylabel("$ thousands")

    ax = axes[0, 1]
    m = k["monthly"].copy()
    m["ym"] = pd.to_datetime(dict(year=m.year, month=m.month, day=1))
    ax.plot(m["ym"], m["sales"] / 1000, color="#2b6cb0", lw=1.6)
    ax.set_title("Monthly Sales Trend"); ax.set_ylabel("$ thousands")
    ax.tick_params(axis="x", rotation=30)

    ax = axes[1, 0]
    r = k["by_region"]
    ax.bar(r["region"], r["profit"] / 1000,
           color=["#c53030" if v < 47000 else "#2f855a" for v in r["profit"]])
    ax.set_title("Profit by Region"); ax.set_ylabel("$ thousands")

    ax = axes[1, 1]
    t = k["top_products"].iloc[::-1]
    ax.barh(t["product_name"].str.slice(0, 34), t["profit"] / 1000,
            color="#2f855a")
    ax.set_title("Top 10 Products by Profit"); ax.set_xlabel("$ thousands")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "dashboard.png", dpi=130)
    print(f"[dashboard] wrote {OUT / 'dashboard.png'}")


def main() -> None:
    df = transform(extract())
    con = load(df)
    k = analyze(con)

    lines = [
        f"Total sales: ${k['total_sales']:,.2f}",
        f"Total profit: ${k['total_profit']:,.2f}",
        f"Overall margin: {k['margin']:.2f}%",
        f"Fact rows: {k['rows']:,} | distinct orders: {k['orders']:,}",
        "Sales by category:\n" + k["by_category"].to_string(index=False),
        "Profit by region:\n" + k["by_region"].to_string(index=False),
        "By year:\n" + k["by_year"].to_string(index=False),
        f"Furniture margin: {k['furniture_margin']:.2f}% | "
        f"Technology margin: {k['tech_margin']:.2f}%",
        "Top 5 products by profit:\n" + k["top_products"].head(5).to_string(index=False),
        "Bottom 5 products by profit:\n" + k["worst_products"].to_string(index=False),
        "Discount buckets:\n" + k["discount"].to_string(index=False),
        "Peak month: " + str(k["monthly"].loc[k["monthly"]["sales"].idxmax()].to_dict()),
    ]
    (OUT / "kpis.txt").write_text("\n\n".join(lines))
    print("\n".join(lines))

    dashboard(k)
    con.close()
    print("[done] retail-sales-etl-dashboard complete")


if __name__ == "__main__":
    main()
