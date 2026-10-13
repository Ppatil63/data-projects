"""
Logistics Delivery ETL + Dashboard
===================================
Loads the (synthetic, seeded) shipment dataset from generate_data.py,
validates it, builds a SQLite warehouse, runs delivery-performance SQL,
and renders a 4-panel dashboard.

Run:  python3 generate_data.py && python3 etl.py
Outputs (in ./outputs): logistics.db, dashboard.png, kpis.txt
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent
RAW = BASE / "data" / "shipments_raw.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
DB = OUT / "logistics.db"


def extract() -> pd.DataFrame:
    df = pd.read_csv(RAW)
    print(f"[extract] raw shipments: {len(df):,}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Validate dates and derive delay / on-time / cost-per-kg measures."""
    df = df.copy()
    rows_in = len(df)
    for c in ("ship_date", "promised_date", "delivered_date"):
        df[c] = pd.to_datetime(df[c], errors="coerce")
    df = df.dropna(subset=["ship_date", "promised_date"])
    bad = (df["delivered_date"].notna()) & (df["delivered_date"] < df["ship_date"])
    df = df[~bad].drop_duplicates(subset=["shipment_id"])

    delivered = df["status"] == "Delivered"
    df["delay_days"] = (df["delivered_date"] - df["promised_date"]).dt.days
    df["delay_days"] = df["delay_days"].where(delivered)
    df["on_time"] = (df["delay_days"] <= 0).astype("Int64")
    df["on_time"] = df["on_time"].where(delivered, pd.NA)
    df["cost_per_kg"] = df["shipping_cost"] / df["weight_kg"]
    print(f"[transform] rows in: {rows_in:,} -> clean rows: {len(df):,} | "
          f"delivered: {int(delivered.sum()):,}")
    return df


def load(df: pd.DataFrame) -> sqlite3.Connection:
    dim_carrier = pd.DataFrame({"carrier": sorted(df["carrier"].unique())})
    dim_carrier["carrier_key"] = dim_carrier.index + 1
    dim_zone = pd.DataFrame({"zone": sorted(df["destination_zone"].unique())})
    dim_zone["zone_key"] = dim_zone.index + 1

    fact = df.merge(dim_carrier, on="carrier").merge(
        dim_zone, left_on="destination_zone", right_on="zone")
    for c in ("ship_date", "promised_date", "delivered_date"):
        fact[c] = fact[c].dt.strftime("%Y-%m-%d")
    fact = fact[["shipment_id", "ship_date", "promised_date", "delivered_date",
                 "origin", "zone_key", "carrier_key", "weight_kg",
                 "shipping_cost", "cost_per_kg", "status", "delay_days",
                 "on_time"]]
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    dim_carrier.to_sql("dim_carrier", con, index=False)
    dim_zone.to_sql("dim_destination_zone", con, index=False)
    fact.to_sql("fact_shipments", con, index=False)
    con.commit()
    print(f"[load] fact_shipments rows: {len(fact):,} | carriers: "
          f"{len(dim_carrier)} | zones: {len(dim_zone)}")
    return con


def analyze(con: sqlite3.Connection) -> dict:
    q = lambda sql: pd.read_sql(sql, con)
    k = {}
    k["overall"] = q("""
        SELECT COUNT(*) total, SUM(status = 'Delivered') delivered,
               ROUND(100.0 * AVG(on_time), 2) on_time_pct,
               ROUND(AVG(delay_days), 2) avg_delay,
               ROUND(SUM(shipping_cost), 2) total_cost
        FROM fact_shipments""").iloc[0]
    k["by_carrier"] = q("""
        SELECT c.carrier, COUNT(*) shipments,
               ROUND(100.0 * AVG(f.on_time), 1) on_time_pct,
               ROUND(AVG(f.delay_days), 2) avg_delay,
               ROUND(AVG(f.cost_per_kg), 2) cost_per_kg
        FROM fact_shipments f JOIN dim_carrier c USING (carrier_key)
        GROUP BY c.carrier ORDER BY on_time_pct DESC""")
    k["by_zone"] = q("""
        SELECT z.zone, COUNT(*) shipments,
               ROUND(100.0 * AVG(f.on_time), 1) on_time_pct,
               ROUND(AVG(f.delay_days), 2) avg_delay
        FROM fact_shipments f JOIN dim_destination_zone z USING (zone_key)
        GROUP BY z.zone ORDER BY on_time_pct""")
    k["late_cost"] = q("""
        SELECT COUNT(*) late_shipments, ROUND(SUM(shipping_cost), 2) late_cost,
               ROUND(AVG(shipping_cost), 2) avg_late_cost,
               ROUND(AVG(delay_days), 2) avg_late_delay
        FROM fact_shipments WHERE on_time = 0""").iloc[0]
    k["monthly"] = q("""
        SELECT substr(ship_date, 1, 7) month,
               ROUND(100.0 * AVG(on_time), 1) on_time_pct, COUNT(*) shipments
        FROM fact_shipments WHERE status = 'Delivered'
        GROUP BY month ORDER BY month""")
    return k


def dashboard(k: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Logistics Delivery Dashboard — synthetic sample data "
                 "(Apr–Sep 2026)", fontsize=13, fontweight="bold")

    ax = axes[0, 0]
    c = k["by_carrier"].iloc[::-1]
    ax.barh(c["carrier"], c["on_time_pct"], color="#2f855a")
    ax.set_title("On-time % by carrier"); ax.set_xlabel("% on time")

    ax = axes[0, 1]
    z = k["by_zone"]
    ax.bar(z["zone"], z["avg_delay"], color="#c53030")
    ax.set_title("Avg delay (days) by destination zone")
    ax.tick_params(axis="x", rotation=25)

    ax = axes[1, 0]
    ax.bar(k["by_carrier"]["carrier"], k["by_carrier"]["cost_per_kg"],
           color="#6b46c1")
    ax.set_title("Cost per kg by carrier"); ax.set_ylabel("$ / kg")
    ax.tick_params(axis="x", rotation=15)

    ax = axes[1, 1]
    m = k["monthly"].copy()
    m["month"] = pd.to_datetime(m["month"])
    ax.plot(m["month"], m["on_time_pct"], marker="o", color="#2b6cb0")
    ax.set_title("On-time % by month"); ax.set_ylabel("% on time")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "dashboard.png", dpi=130)
    print(f"[dashboard] wrote {OUT / 'dashboard.png'}")


def main() -> None:
    df = transform(extract())
    con = load(df)
    k = analyze(con)
    o, lc = k["overall"], k["late_cost"]
    lines = [
        f"Shipments: {int(o.total):,} | delivered: {int(o.delivered):,} | "
        f"total shipping cost: ${o.total_cost:,.2f}",
        f"Overall on-time: {o.on_time_pct:.2f}% | avg delay: {o.avg_delay:.2f} days",
        f"Late shipments: {int(lc.late_shipments):,} costing "
        f"${lc.late_cost:,.2f} (avg ${lc.avg_late_cost:.2f} each, "
        f"avg delay {lc.avg_late_delay:.2f} days)",
        "By carrier:\n" + k["by_carrier"].to_string(index=False),
        "By destination zone:\n" + k["by_zone"].to_string(index=False),
        "Monthly on-time:\n" + k["monthly"].to_string(index=False),
    ]
    (OUT / "kpis.txt").write_text("\n\n".join(lines))
    print("\n\n".join(lines))
    dashboard(k)
    con.close()
    print("[done] logistics-delivery-etl complete")


if __name__ == "__main__":
    main()
