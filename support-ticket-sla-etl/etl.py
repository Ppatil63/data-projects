"""
Support Ticket SLA — ETL + Dashboard
=====================================
Loads the (synthetic, seeded) ticket dataset produced by generate_data.py,
validates it, builds a SQLite warehouse, runs SLA analysis in SQL, and
renders a 4-panel dashboard.

Run:  python3 generate_data.py && python3 etl.py
Outputs (in ./outputs): tickets.db, dashboard.png, kpis.txt
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent
RAW = BASE / "data" / "tickets_raw.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
DB = OUT / "tickets.db"


def extract() -> pd.DataFrame:
    df = pd.read_csv(RAW)
    print(f"[extract] raw tickets: {len(df):,}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and enrich: parse timestamps, derive resolution/breach."""
    df = df.copy()
    rows_in = len(df)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["resolved_at"] = pd.to_datetime(df["resolved_at"], errors="coerce")
    # Validation: drop unparseable creations and impossible resolutions
    df = df.dropna(subset=["created_at"])
    bad = (df["resolved_at"].notna()) & (df["resolved_at"] < df["created_at"])
    df = df[~bad]
    df = df.drop_duplicates(subset=["ticket_id"])

    df["resolution_hours"] = (
        df["resolved_at"] - df["created_at"]).dt.total_seconds() / 3600
    df["sla_breached"] = (
        (df["resolution_hours"] > df["sla_target_hours"]).astype("Int64"))
    df.loc[df["resolved_at"].isna(), "sla_breached"] = pd.NA
    df["reopened_flag"] = (df["reopened"] == "Yes").astype(int)

    # Backlog aging is measured at a snapshot = day after the last ticket
    snapshot = df["created_at"].max().normalize() + pd.Timedelta(days=1)
    df["age_days"] = (snapshot - df["created_at"]).dt.total_seconds() / 86400
    df["age_days"] = df["age_days"].where(df["resolved_at"].isna())
    print(f"[transform] rows in: {rows_in:,} -> clean rows: {len(df):,} | "
          f"snapshot date: {snapshot.date()}")
    df.attrs["snapshot"] = snapshot
    return df


def load(df: pd.DataFrame) -> sqlite3.Connection:
    """Star-ish schema: fact_tickets + one dim per categorical attribute."""
    dims = {}
    for col in ("priority", "category", "channel", "assignment_group", "status"):
        d = pd.DataFrame({col: sorted(df[col].unique())})
        d[f"{col}_key"] = d.index + 1
        dims[col] = d

    fact = df.copy()
    for col, d in dims.items():
        fact = fact.merge(d, on=col, how="left").drop(columns=[col])
    fact["created_at"] = fact["created_at"].dt.strftime("%Y-%m-%d %H:%M")
    fact["resolved_at"] = fact["resolved_at"].dt.strftime("%Y-%m-%d %H:%M")
    fact = fact[["ticket_id", "created_at", "resolved_at", "priority_key",
                 "category_key", "channel_key", "assignment_group_key",
                 "status_key", "sla_target_hours", "resolution_hours",
                 "sla_breached", "reopened_flag", "age_days"]]

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    for col, d in dims.items():
        d.to_sql(f"dim_{col}", con, index=False)
    fact.to_sql("fact_tickets", con, index=False)
    con.commit()
    print(f"[load] fact_tickets rows: {len(fact):,} | dims: "
          + ", ".join(f"{c}={len(d)}" for c, d in dims.items()))
    return con


def analyze(con: sqlite3.Connection) -> dict:
    q = lambda sql: pd.read_sql(sql, con)
    k = {}
    k["overall"] = q("""
        SELECT COUNT(*) total,
               SUM(resolved_at IS NOT NULL) resolved,
               ROUND(100.0 * SUM(sla_breached) /
                     SUM(resolved_at IS NOT NULL), 2) breach_pct,
               ROUND(100.0 * AVG(reopened_flag), 2) reopen_pct
        FROM fact_tickets""").iloc[0]
    k["by_priority"] = q("""
        SELECT p.priority, COUNT(*) tickets,
               ROUND(AVG(f.resolution_hours), 1) avg_hours,
               ROUND(100.0 * SUM(f.sla_breached) /
                     SUM(f.resolved_at IS NOT NULL), 1) breach_pct
        FROM fact_tickets f JOIN dim_priority p USING (priority_key)
        GROUP BY p.priority ORDER BY p.priority""")
    k["by_category"] = q("""
        SELECT c.category, COUNT(*) tickets,
               ROUND(100.0 * SUM(f.sla_breached) /
                     SUM(f.resolved_at IS NOT NULL), 1) breach_pct,
               ROUND(AVG(f.resolution_hours), 1) avg_hours
        FROM fact_tickets f JOIN dim_category c USING (category_key)
        GROUP BY c.category ORDER BY tickets DESC""")
    k["by_group"] = q("""
        SELECT g.assignment_group, COUNT(*) tickets,
               ROUND(100.0 * SUM(f.sla_breached) /
                     SUM(f.resolved_at IS NOT NULL), 1) breach_pct
        FROM fact_tickets f
        JOIN dim_assignment_group g USING (assignment_group_key)
        GROUP BY g.assignment_group ORDER BY breach_pct DESC""")
    k["aging"] = q("""
        SELECT CASE WHEN age_days <= 3 THEN '0-3 days'
                    WHEN age_days <= 7 THEN '4-7 days'
                    WHEN age_days <= 14 THEN '8-14 days'
                    ELSE '15+ days' END bucket, COUNT(*) tickets
        FROM fact_tickets WHERE resolved_at IS NULL
        GROUP BY bucket""")
    k["daily"] = q("""
        SELECT substr(created_at, 1, 10) day, COUNT(*) tickets
        FROM fact_tickets GROUP BY day ORDER BY day""")
    k["weekend"] = q("""
        SELECT CASE WHEN strftime('%w', created_at) IN ('0','5','6')
                    THEN 'Fri-Sun' ELSE 'Mon-Thu' END period,
               ROUND(AVG(resolution_hours), 1) avg_hours
        FROM fact_tickets WHERE resolved_at IS NOT NULL GROUP BY period""")
    return k


def dashboard(k: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Support Ticket SLA Dashboard — synthetic sample data "
                 "(Jun–Aug 2026)", fontsize=13, fontweight="bold")

    ax = axes[0, 0]
    bp = k["by_priority"]
    ax.bar(bp["priority"], bp["breach_pct"], color="#c53030")
    ax.set_title("SLA breach % by priority"); ax.set_ylabel("% breached")

    ax = axes[0, 1]
    ax.bar(bp["priority"], bp["avg_hours"], color="#2b6cb0")
    ax.set_title("Avg resolution hours by priority"); ax.set_ylabel("hours")

    ax = axes[1, 0]
    c = k["by_category"].iloc[::-1]
    ax.barh(c["category"], c["tickets"], color="#2f855a")
    ax.set_title("Ticket volume by category"); ax.set_xlabel("tickets")

    ax = axes[1, 1]
    d = k["daily"].copy()
    d["day"] = pd.to_datetime(d["day"])
    ax.plot(d["day"], d["tickets"], color="#2b6cb0", lw=1.2)
    ax.set_title("Tickets created per day"); ax.tick_params(axis="x", rotation=30)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "dashboard.png", dpi=130)
    print(f"[dashboard] wrote {OUT / 'dashboard.png'}")


def main() -> None:
    df = transform(extract())
    con = load(df)
    k = analyze(con)
    o = k["overall"]
    lines = [
        f"Total tickets: {int(o.total):,} | resolved: {int(o.resolved):,} | "
        f"open: {int(o.total - o.resolved):,}",
        f"Overall SLA breach rate (resolved tickets): {o.breach_pct:.2f}%",
        f"Overall reopen rate: {o.reopen_pct:.2f}%",
        "By priority:\n" + k["by_priority"].to_string(index=False),
        "By category:\n" + k["by_category"].to_string(index=False),
        "By assignment group:\n" + k["by_group"].to_string(index=False),
        "Open backlog aging:\n" + k["aging"].to_string(index=False),
        "Resolution by creation period:\n" + k["weekend"].to_string(index=False),
    ]
    (OUT / "kpis.txt").write_text("\n\n".join(lines))
    print("\n\n".join(lines))
    dashboard(k)
    con.close()
    print("[done] support-ticket-sla-etl complete")


if __name__ == "__main__":
    main()
