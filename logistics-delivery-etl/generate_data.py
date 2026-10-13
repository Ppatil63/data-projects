"""
Synthetic shipment data generator
==================================
Creates a realistic sample dataset of 2,500 shipments so the logistics ETL
pipeline can be demonstrated end to end. The data is SYNTHETIC — generated
here with a fixed seed (fully reproducible), not from any real carrier or
company.

Patterns baked in on purpose (so the analysis has something real to find):
  - Carriers differ: SwiftLine is fast/reliable, BlueRail is cheap but slow
    and delay-prone, Apex Freight is mid-pack, National Parcel is steady.
  - Long-haul destination zones (Northwest, Northeast) run later.
  - Heavy shipments cost more per kg on some carriers.

Run:  python3 generate_data.py   ->  data/shipments_raw.csv
"""
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

random.seed(7)
N = 2500
START = datetime(2026, 4, 1)
WINDOW_DAYS = 182  # Apr 1 - Sep 29 2026

ORIGINS = ["Phoenix, AZ", "Dallas, TX", "Chicago, IL", "Atlanta, GA",
           "Seattle, WA"]
ZONES = ["Southwest", "South Central", "Midwest", "Southeast", "Northwest",
         "Northeast"]
# carrier -> (weight, base days, delay tendency, $ per kg, reliability noise)
CARRIERS = {
    "SwiftLine":        (0.30, 2.0, 0.10, 1.85),
    "Apex Freight":     (0.28, 3.2, 0.30, 1.45),
    "BlueRail Logistics": (0.22, 4.5, 0.62, 0.95),
    "National Parcel Co": (0.20, 3.0, 0.22, 1.60),
}
ZONE_EXTRA_DAYS = {"Southwest": 0.0, "South Central": 0.4, "Midwest": 0.8,
                   "Southeast": 0.9, "Northwest": 1.6, "Northeast": 1.4}


def pick(weighted):
    r, acc = random.random(), 0.0
    for name, w in weighted:
        acc += w
        if r <= acc:
            return name
    return weighted[-1][0]


def main() -> None:
    rows = []
    for i in range(1, N + 1):
        ship_date = START + timedelta(days=random.uniform(0, WINDOW_DAYS))
        origin = random.choice(ORIGINS)
        dest_zone = random.choice(ZONES)
        carrier = pick([(k, v[0]) for k, v in CARRIERS.items()])
        _, base_days, delay_p, rate = CARRIERS[carrier]
        weight = round(max(0.5, random.lognormvariate(math.log(18), 0.8)), 1)

        promised_days = base_days + ZONE_EXTRA_DAYS[dest_zone] + random.uniform(0, 1)
        promised = ship_date + timedelta(days=promised_days)
        # Actual: promised transit + noise; delay-prone carriers slip more
        slip = random.lognormvariate(math.log(0.6 + 2.2 * delay_p), 0.7) - 0.7
        actual_days = max(0.5, promised_days + slip - 0.55)

        is_open = random.random() < 0.06  # still in transit at snapshot
        delivered = None if is_open else ship_date + timedelta(days=actual_days)
        status = "In Transit" if is_open else (
            "Returned" if random.random() < 0.02 else "Delivered")
        if status == "Returned":
            delivered = ship_date + timedelta(days=actual_days)

        cost = round(weight * rate * (1 + 0.25 * ZONE_EXTRA_DAYS[dest_zone])
                     + random.uniform(4, 12), 2)
        rows.append({
            "shipment_id": f"SHP{500000 + i}",
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "promised_date": promised.strftime("%Y-%m-%d"),
            "delivered_date": "" if delivered is None else delivered.strftime("%Y-%m-%d"),
            "origin": origin,
            "destination_zone": dest_zone,
            "carrier": carrier,
            "weight_kg": weight,
            "shipping_cost": cost,
            "status": status,
        })

    df = pd.DataFrame(rows)
    out = Path(__file__).parent / "data" / "shipments_raw.csv"
    out.parent.mkdir(exist_ok=True)
    df.to_csv(out, index=False)
    print(f"[generate] wrote {len(df):,} synthetic shipments -> {out}")


if __name__ == "__main__":
    main()
