# Data Projects — Portfolio Pack

Five end-to-end ETL + analytics projects. Every one runs with
`python3 etl.py` (synthetic-data projects: `python3 generate_data.py` first)
and regenerates its SQLite warehouse, dashboard PNG, and KPI file.
Every number below comes from an actual run of the pipeline.

**Common stack:** Python (pandas) · SQLite · SQL · matplotlib

---

## 1. Retail Sales ETL + Dashboard — `retail-sales-etl-dashboard/`
**Pitch:** 9,994 real retail orders (Tableau's Sample Superstore) cleaned
into a star schema to find where profit is made — and where it leaks.
**Tools:** pandas ETL · SQLite star schema (fact + 4 dims) · SQL · matplotlib
**Headline insights:**
- Furniture is the #2 category by sales ($741,999.80) but keeps only a
  2.49% margin, vs 17.40% for Technology.
- Discounts over 20% lose money on average: −$77.86 per line at 21–40% off,
  −$106.71 above 40% (vs +$66.90 with no discount).

## 2. Support Ticket SLA ETL + Dashboard — `support-ticket-sla-etl/`
**Pitch:** Ticket pipeline that scores SLA performance by priority,
category, and team. *(Synthetic seeded sample data — labeled as such.)*
**Tools:** Python data generator · pandas ETL · SQLite · SQL · matplotlib
**Headline insights:**
- 26.96% of resolved tickets breached SLA; Software Bug (70.7%) and
  Integration / API (69.9%) categories are the drivers.
- App Support L2 breached 54.5% of tickets vs 5.7% at Service Desk L1;
  86.8% of the open backlog was already 15+ days old.

## 3. HR Attrition ETL + Dashboard — `hr-attrition-etl-dashboard/`
**Pitch:** IBM's HR attrition dataset (1,470 employees) warehoused and
analyzed to quantify what actually separates leavers from stayers.
**Tools:** pandas ETL · SQLite · SQL · matplotlib
**Headline insights:**
- Overtime workers left at 30.5% vs 10.4% for everyone else — the
  strongest single attrition signal.
- Attrition is 36.4% in an employee's first year and 39.8% among Sales
  Representatives, vs 16.12% company-wide.

## 4. Stock Market ETL + Dashboard — `stock-market-etl/`
**Pitch:** Five years of daily prices for AAPL, MSFT, AMZN, NVDA, GOOG
(6,270 rows) normalized into one warehouse for return/volatility analysis.
**Tools:** Yahoo Finance chart API extract · pandas · SQLite · SQL window
functions (moving averages, LAG returns) · matplotlib
**Headline insights:**
- NVDA returned +950.86% over the period ($21.75 → $228.52) — with the
  highest annualized volatility, 51.91%.
- In the last year GOOG (+42.87%) and AAPL (+37.80%) led, while MSFT
  returned only +5.72%.

## 5. Logistics Delivery ETL + Dashboard — `logistics-delivery-etl/`
**Pitch:** Shipment pipeline scoring 4 carriers across 6 zones on the
cost-vs-reliability tradeoff. *(Synthetic seeded sample data — labeled
as such.)*
**Tools:** Python data generator · pandas ETL · SQLite · SQL · matplotlib
**Headline insights:**
- Cheapest carrier BlueRail ($1.81/kg) delivers on time only 42.9% of the
  time; most expensive SwiftLine ($2.88/kg) hits 85.4%.
- 700 late shipments carry $31,929.77 of freight cost — 24.6% of the
  $129,545.42 total spend.


---

# Case Studies — Operations & Product

Twelve scenario case studies (analysis exercises on realistic industry problems, honestly framed — baselines labelled as assumptions, impacts labelled as projections). Full index: [case-studies/INDEX.md](case-studies/INDEX.md)

**Operations:** warehouse fulfillment bottleneck · last-mile delivery on-time performance · inventory stockouts vs overstock · support queue redesign · manufacturing downtime / OEE · hospital outpatient scheduling

**Product:** food delivery late orders · SaaS onboarding drop-off · e-commerce checkout abandonment · subscription churn (month 2–3) · telemedicine accessibility booking · job-matching for freshers
