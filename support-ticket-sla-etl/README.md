# Support Ticket SLA — ETL + Dashboard

An end-to-end pipeline that generates, cleans, warehouses, and analyzes IT
support tickets to find where SLAs breach and why.

**Business question:** Which priorities, categories, and teams miss SLA —
and what should a support manager fix first?

**Stack:** Python (pandas) · SQLite · SQL · matplotlib

**Data:** *Synthetic sample data.* `generate_data.py` creates 3,000 seeded,
reproducible tickets (Jun–Aug 2026) with priorities P1–P4, 9 categories,
4 channels, 3 assignment groups, SLA targets, resolution timestamps, and
reopen flags. It is generated demo data — not from any real ticketing
system — and exists so the pipeline can be shown and re-run anywhere.

## Pipeline

```bash
python3 generate_data.py   # -> data/tickets_raw.csv (3,000 rows)
python3 etl.py             # -> outputs/tickets.db, dashboard.png, kpis.txt
```

1. **Generate** — seeded synthetic tickets with realistic patterns baked in
   (integration/bug tickets slower, weekend slowdowns, ~12% left open).
2. **Transform** — parse timestamps, drop impossible records
   (resolved before created), derive resolution hours, SLA breach flag,
   and backlog age at a snapshot date. 3,000 in → 3,000 clean.
3. **Load** — SQLite schema in `outputs/tickets.db`:
   `fact_tickets` (3,000 rows) + `dim_priority`, `dim_category`,
   `dim_channel`, `dim_assignment_group`, `dim_status`.
4. **Analyze** — `analysis.sql`: breach % overall/by priority/by category/
   by team, average resolution, reopen rate, backlog aging, weekend effect.
5. **Present** — `outputs/dashboard.png`: breach % by priority, average
   resolution by priority, volume by category, daily ticket trend.

## Key findings

- 26.96% of resolved tickets breached SLA; P1/P2 breach most (41–43%).
- Software Bug (70.7%) and Integration / API (69.9%) tickets are the breach
  drivers; App Support L2 breaches 54.5% vs 5.7% at Service Desk L1.
- 86.8% of the open backlog is 15+ days old — a hygiene problem, not a
  volume problem.

See `INSIGHTS.md` for the full findings with numbers.
