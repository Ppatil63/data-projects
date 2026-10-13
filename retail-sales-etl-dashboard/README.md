# Retail Sales ETL + Dashboard

Turns 9,994 raw retail order lines into a SQLite star-schema warehouse, SQL
analysis, and a 4-panel dashboard — answering where the money is made and
where it leaks.

**Business question:** Which categories, regions, products, and discount
practices actually drive profit — and which ones quietly destroy it?

**Stack:** Python (pandas) · SQLite · SQL · matplotlib

**Data source:** "Sample Superstore" — Tableau's classic public sample
dataset (US retail orders, 2014–2017). Downloaded from a GitHub mirror of
the dataset (the plotly/datasets copy has been removed):
`raw.githubusercontent.com/And3m/superstore-sales-analysis-eda` —
`data/superstore.csv` in this folder.

## Pipeline (`python3 etl.py`)

1. **Extract** — read `data/superstore.csv` (9,994 rows).
2. **Transform** — normalize column names, parse order/ship dates, coerce
   numeric types, standardize postal codes, drop duplicates and rows
   missing key fields (9,994 rows in → 9,994 clean rows; this dataset is
   already tidy, so the checks act as validation).
3. **Load** — SQLite star schema in `outputs/superstore.db`:
   - `fact_sales` (9,994 rows): sales, quantity, discount, profit + FKs
   - `dim_product` (1,862), `dim_customer` (793), `dim_region` (632),
     `dim_date` (1,434)
4. **Analyze** — the queries in `analysis.sql` (category/region profit,
   monthly trend, top/bottom products, discount buckets, YoY).
5. **Present** — `outputs/dashboard.png`: sales by category, monthly trend,
   profit by region, top 10 products by profit.

## Key findings

- Furniture sells $742K but keeps only a 2.49% margin (Technology: 17.40%).
- Discounts above 20% flip order lines to losses on average (−$77.86 at
  21–40% off, −$106.71 above 40%).
- Sales grew 51% from 2014 to 2017; the West region is the profit engine.

See `INSIGHTS.md` for the full findings with numbers.
