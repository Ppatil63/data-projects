# Insights — HR Attrition (IBM HR Analytics, 1,470 employees)

Every number below is computed by `etl.py` / `analysis.sql` from the actual
dataset and stored in `outputs/kpis.txt`.

- **Overall attrition is 16.12%** — 237 of 1,470 employees left. That's the
  baseline every segment below is compared against.
- **Overtime is the single strongest signal.** Employees working overtime
  left at 30.5% (127 of 416), versus 10.4% for everyone else — nearly 3×
  the rate. Overtime policy is the first lever to pull.
- **People leave early or not at all.** Attrition is 36.4% in year 0 and
  28.9% in years 1–2, then drops to 13.8% (3–5 yrs), 12.3% (6–10 yrs), and
  just 8.1% after 10 years. Onboarding and the first-two-years experience
  decide retention.
- **Pay matters, measurably.** Employees earning under $3k/month left at
  28.6%, versus 8.9% for the $10k+ band. Leavers earned $4,787/month on
  average versus $6,833 for stayers — a $2,046 gap.
- **Sales is the leakiest department** at 20.6% attrition (446 employees),
  ahead of HR at 19.0%; Research & Development is the most stable at 13.8%.
- **One role is an outlier:** Sales Representatives left at 39.8% — almost
  2.5× the company rate and the highest of all 9 roles — while Research
  Directors left at only 2.5% and Managers at 4.9%.
- **Satisfaction tracks attrition but weakly:** employees with the lowest
  job satisfaction (1 of 4) left at 22.8% versus 11.3% at the highest
  level. It matters, but overtime and pay separate leavers more sharply.
