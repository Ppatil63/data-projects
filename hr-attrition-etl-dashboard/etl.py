"""
HR Attrition ETL + Dashboard
============================
Cleans the IBM HR Analytics employee attrition dataset, loads it into a
SQLite star-ish schema, runs SQL analysis (department, overtime, tenure,
income), and renders a 4-panel dashboard.

Run:  python3 etl.py
Outputs (in ./outputs): hr.db, dashboard.png, kpis.txt
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent
RAW = BASE / "data" / "hr_attrition.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
DB = OUT / "hr.db"


def extract() -> pd.DataFrame:
    df = pd.read_csv(RAW, encoding="utf-8-sig")
    print(f"[extract] raw employees: {len(df):,}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean: snake_case columns, attrition flag, drop constant columns."""
    import re
    df = df.copy()
    rows_in = len(df)
    # CamelCase -> snake_case for every column, then one friendly rename
    df.columns = [re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", c.strip()).lower()
                  for c in df.columns]
    df = df.rename(columns={"employee_number": "employee_id"})
    df = df.drop_duplicates(subset=["employee_id"])
    # Constant / non-informative columns in this dataset
    df = df.drop(columns=[c for c in ("employee_count", "standard_hours",
                                      "over_18", "over18") if c in df.columns])
    df["left"] = (df["attrition"].str.strip().str.lower() == "yes").astype(int)
    df = df.dropna(subset=["employee_id", "department", "monthly_income"])
    print(f"[transform] rows in: {rows_in:,} -> clean rows: {len(df):,}")
    return df


def load(df: pd.DataFrame) -> sqlite3.Connection:
    dim_dept = pd.DataFrame({"department": sorted(df["department"].unique())})
    dim_dept["department_key"] = dim_dept.index + 1
    dim_role = pd.DataFrame({"job_role": sorted(df["job_role"].unique())})
    dim_role["job_role_key"] = dim_role.index + 1

    fact = df.merge(dim_dept, on="department").merge(dim_role, on="job_role")
    fact = fact[["employee_id", "department_key", "job_role_key", "age",
                 "gender", "monthly_income", "over_time", "years_at_company",
                 "total_working_years", "years_since_last_promotion",
                 "job_satisfaction", "environment_satisfaction",
                 "work_life_balance", "distance_from_home", "left"]]
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    dim_dept.to_sql("dim_department", con, index=False)
    dim_role.to_sql("dim_job_role", con, index=False)
    fact.to_sql("fact_employee", con, index=False)
    con.commit()
    print(f"[load] fact_employee rows: {len(fact):,} | departments: "
          f"{len(dim_dept)} | job roles: {len(dim_role)}")
    return con


def analyze(con: sqlite3.Connection) -> dict:
    q = lambda sql: pd.read_sql(sql, con)
    k = {}
    k["overall"] = q("""
        SELECT COUNT(*) n, SUM("left") leavers,
               ROUND(100.0 * AVG("left"), 2) attrition_pct FROM fact_employee
        """).iloc[0]
    k["by_dept"] = q("""
        SELECT d.department, COUNT(*) n,
               ROUND(100.0 * AVG(f."left"), 1) attrition_pct
        FROM fact_employee f JOIN dim_department d USING (department_key)
        GROUP BY d.department ORDER BY attrition_pct DESC""")
    k["overtime"] = q("""
        SELECT over_time, COUNT(*) n,
               ROUND(100.0 * AVG("left"), 1) attrition_pct
        FROM fact_employee GROUP BY over_time ORDER BY attrition_pct DESC""")
    k["tenure"] = q("""
        SELECT CASE WHEN years_at_company = 0 THEN '0 yrs'
                    WHEN years_at_company <= 2 THEN '1-2 yrs'
                    WHEN years_at_company <= 5 THEN '3-5 yrs'
                    WHEN years_at_company <= 10 THEN '6-10 yrs'
                    ELSE '10+ yrs' END band, COUNT(*) n,
               ROUND(100.0 * AVG("left"), 1) attrition_pct
        FROM fact_employee GROUP BY band""")
    k["income"] = q("""
        SELECT CASE WHEN monthly_income < 3000 THEN 'Under $3k'
                    WHEN monthly_income < 5000 THEN '$3k-5k'
                    WHEN monthly_income < 10000 THEN '$5k-10k'
                    ELSE '$10k+' END band, COUNT(*) n,
               ROUND(100.0 * AVG("left"), 1) attrition_pct,
               ROUND(AVG(monthly_income)) avg_income
        FROM fact_employee GROUP BY band""")
    k["by_role"] = q("""
        SELECT r.job_role, COUNT(*) n,
               ROUND(100.0 * AVG(f."left"), 1) attrition_pct
        FROM fact_employee f JOIN dim_job_role r USING (job_role_key)
        GROUP BY r.job_role ORDER BY attrition_pct DESC""")
    k["satisfaction"] = q("""
        SELECT job_satisfaction, ROUND(100.0 * AVG("left"), 1) attrition_pct
        FROM fact_employee GROUP BY job_satisfaction ORDER BY job_satisfaction""")
    k["income_gap"] = q("""
        SELECT ROUND(AVG(CASE WHEN "left" = 1 THEN monthly_income END)) leaver_income,
               ROUND(AVG(CASE WHEN "left" = 0 THEN monthly_income END)) stayer_income
        FROM fact_employee""").iloc[0]
    order = {"0 yrs": 0, "1-2 yrs": 1, "3-5 yrs": 2, "6-10 yrs": 3, "10+ yrs": 4}
    k["tenure"]["_o"] = k["tenure"]["band"].map(order)
    k["tenure"] = k["tenure"].sort_values("_o").drop(columns="_o")
    iorder = {"Under $3k": 0, "$3k-5k": 1, "$5k-10k": 2, "$10k+": 3}
    k["income"]["_o"] = k["income"]["band"].map(iorder)
    k["income"] = k["income"].sort_values("_o").drop(columns="_o")
    return k


def dashboard(k: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("HR Attrition Dashboard — IBM HR Analytics dataset",
                 fontsize=14, fontweight="bold")

    ax = axes[0, 0]
    d = k["by_dept"].iloc[::-1]
    ax.barh(d["department"], d["attrition_pct"], color="#c53030")
    ax.set_title("Attrition % by department"); ax.set_xlabel("% left")

    ax = axes[0, 1]
    ax.bar(k["overtime"]["over_time"], k["overtime"]["attrition_pct"],
           color=["#2f855a", "#c53030"])
    ax.set_title("Attrition % — overtime vs not"); ax.set_ylabel("% left")

    ax = axes[1, 0]
    ax.bar(k["tenure"]["band"], k["tenure"]["attrition_pct"], color="#2b6cb0")
    ax.set_title("Attrition % by tenure band"); ax.set_ylabel("% left")

    ax = axes[1, 1]
    ax.bar(k["income"]["band"], k["income"]["attrition_pct"], color="#6b46c1")
    ax.set_title("Attrition % by monthly income band"); ax.set_ylabel("% left")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT / "dashboard.png", dpi=130)
    print(f"[dashboard] wrote {OUT / 'dashboard.png'}")


def main() -> None:
    df = transform(extract())
    con = load(df)
    k = analyze(con)
    o = k["overall"]
    lines = [
        f"Employees: {int(o.n):,} | leavers: {int(o.leavers):,} | "
        f"overall attrition: {o.attrition_pct:.2f}%",
        f"Avg monthly income — leavers: ${k['income_gap'].leaver_income:,.0f} "
        f"vs stayers: ${k['income_gap'].stayer_income:,.0f}",
        "By department:\n" + k["by_dept"].to_string(index=False),
        "Overtime effect:\n" + k["overtime"].to_string(index=False),
        "Tenure bands:\n" + k["tenure"].to_string(index=False),
        "Income bands:\n" + k["income"].to_string(index=False),
        "By job role:\n" + k["by_role"].to_string(index=False),
        "Job satisfaction vs attrition:\n" + k["satisfaction"].to_string(index=False),
    ]
    (OUT / "kpis.txt").write_text("\n\n".join(lines))
    print("\n\n".join(lines))
    dashboard(k)
    con.close()
    print("[done] hr-attrition-etl-dashboard complete")


if __name__ == "__main__":
    main()
