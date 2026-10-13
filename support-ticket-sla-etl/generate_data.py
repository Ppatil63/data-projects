"""
Synthetic support-ticket data generator
========================================
Creates a realistic sample dataset of 3,000 IT support tickets so the ETL /
SLA pipeline can be demonstrated end to end. The data is SYNTHETIC — it is
generated here with a fixed seed (fully reproducible) and does not come from
any real company or ticketing system.

Patterns baked in on purpose (so the analysis has something real to find):
  - Integration/API and Software Bug tickets resolve slower and breach more.
  - P1s are rare and fast; P3s are the volume bulk.
  - Tickets created on Friday/weekend resolve slower.
  - Some tickets get reopened (~8%).

Run:  python3 generate_data.py   ->  data/tickets_raw.csv
"""
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)
N = 3000
START = datetime(2026, 6, 1, 0, 0)
WINDOW_DAYS = 92  # Jun 1 - Aug 31 2026

SLA_HOURS = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
PRIORITY_W = [("P1", 0.04), ("P2", 0.21), ("P3", 0.50), ("P4", 0.25)]

# category -> (weight, base resolution hours, breach tendency multiplier)
CATEGORIES = {
    "Password Reset":     (0.16, 1.2, 0.5),
    "Access / Login":     (0.16, 3.0, 0.8),
    "Data Issue":         (0.12, 9.0, 1.4),
    "Integration / API":  (0.12, 14.0, 2.1),
    "Software Bug":       (0.14, 16.0, 1.9),
    "Network":            (0.08, 6.0, 1.1),
    "Hardware":           (0.10, 11.0, 1.2),
    "Performance":        (0.07, 12.0, 1.6),
    "How-To / Request":   (0.05, 2.5, 0.6),
}
CHANNELS = [("Portal", 0.38), ("Email", 0.27), ("Phone", 0.20), ("Chat", 0.15)]
GROUPS = {
    "Password Reset": "Service Desk L1", "Access / Login": "Service Desk L1",
    "How-To / Request": "Service Desk L1", "Hardware": "Service Desk L1",
    "Data Issue": "App Support L2", "Integration / API": "App Support L2",
    "Software Bug": "App Support L2", "Performance": "App Support L2",
    "Network": "Infrastructure",
}


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
        created = START + timedelta(days=random.uniform(0, WINDOW_DAYS),
                                    hours=random.uniform(0, 24))
        priority = pick(PRIORITY_W)
        category = pick([(k, v[0]) for k, v in CATEGORIES.items()])
        _, base_hours, breach_mult = CATEGORIES[category]
        channel = pick(CHANNELS)
        group = GROUPS[category]

        # ~12% of tickets are still open at the snapshot date
        is_open = random.random() < 0.12
        # Resolution time: lognormal around the category base, stretched by
        # the priority SLA (P1s get worked faster) and the weekend effect.
        sla_factor = {"P1": 0.35, "P2": 0.6, "P3": 1.0, "P4": 1.6}[priority]
        weekend_factor = 1.45 if created.weekday() >= 4 else 1.0
        mu = base_hours * sla_factor * breach_mult * weekend_factor
        resolution_hours = max(0.1, random.lognormvariate(
            __import__("math").log(max(mu, 0.2)), 0.55))

        resolved = None if is_open else created + timedelta(hours=resolution_hours)
        status = random.choice(["Open", "In Progress"]) if is_open else \
            random.choice(["Resolved", "Closed"])
        reopened = (not is_open) and random.random() < (
            0.05 + 0.05 * (breach_mult - 0.5))

        rows.append({
            "ticket_id": f"INC{1000000 + i}",
            "created_at": created.strftime("%Y-%m-%d %H:%M"),
            "resolved_at": "" if resolved is None else resolved.strftime("%Y-%m-%d %H:%M"),
            "priority": priority,
            "category": category,
            "channel": channel,
            "assignment_group": group,
            "sla_target_hours": SLA_HOURS[priority],
            "status": status,
            "reopened": "Yes" if reopened else "No",
        })

    df = pd.DataFrame(rows)
    out = Path(__file__).parent / "data" / "tickets_raw.csv"
    out.parent.mkdir(exist_ok=True)
    df.to_csv(out, index=False)
    print(f"[generate] wrote {len(df):,} synthetic tickets -> {out}")


if __name__ == "__main__":
    main()
