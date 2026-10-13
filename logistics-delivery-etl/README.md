# Logistics Delivery ETL + Dashboard

An end-to-end pipeline that generates, cleans, warehouses, and analyzes
shipment data to score carriers on cost vs reliability.

**Business question:** Which carriers and destination zones deliver on
time, what does late delivery cost, and where should volume shift?

**Stack:** Python (pandas) · SQLite · SQL · matplotlib

**Data:** *Synthetic sample data.* `generate_data.py` creates 2,500 seeded,
reproducible shipments (Apr–Sep 2026) from 5 origin cities to 6 destination
zones via 4 carriers, with weight, promised vs actual delivery dates, cost,
and status. It is generated demo data — not from any real carrier — and
exists so the pipeline can be shown and re-run anywhere.

## Pipeline

```bash
python3 generate_data.py   # -> data/shipments_raw.csv (2,500 rows)
python3 etl.py             # -> outputs/logistics.db, dashboard.png, kpis.txt
```

1. **Generate** — seeded synthetic shipments with realistic patterns baked
   in (carrier speed/reliability/cost tradeoffs, long-haul zones slower,
   ~6% still in transit, ~2% returned).
2. **Transform** — parse dates, drop impossible records (delivered before
   shipped), derive delay days, on-time flag, and cost per kg.
   2,500 in → 2,500 clean; 2,294 delivered.
3. **Load** — SQLite schema in `outputs/logistics.db`: `fact_shipments`
   (2,500 rows) + `dim_carrier` (4) + `dim_destination_zone` (6).
4. **Analyze** — `analysis.sql`: on-time % overall/by carrier/by zone,
   average delay, cost per kg, late-shipment cost impact, monthly trend.
5. **Present** — `outputs/dashboard.png`: on-time % by carrier, delay by
   zone, cost per kg by carrier, monthly on-time trend.

## Key findings

- On-time delivery is 69.49%; the cheapest carrier (BlueRail, $1.81/kg)
  is on time only 42.9% vs SwiftLine's 85.4% at $2.88/kg.
- 700 late shipments carry $31,929.77 of freight cost — 24.6% of spend.
- Zones differ by <5 points; carriers differ by 42 points. Allocation is
  the lever.

See `INSIGHTS.md` for the full findings with numbers.
