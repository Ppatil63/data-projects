# HR Attrition ETL + Dashboard

Cleans the IBM HR Analytics attrition dataset into a SQLite warehouse and
quantifies which factors actually separate leavers from stayers.

**Business question:** Who leaves, from where, and which factors — overtime,
tenure, pay, department, role — predict it best?

**Stack:** Python (pandas) · SQLite · SQL · matplotlib

**Data source:** IBM HR Analytics Employee Attrition dataset (1,470
employees, fictional data created by IBM data scientists for education),
from IBM's GitHub: `raw.githubusercontent.com/IBM/employee-attrition-aif360`
— `data/hr_attrition.csv` in this folder.

## Pipeline (`python3 etl.py`)

1. **Extract** — read `data/hr_attrition.csv` (1,470 rows, 35 columns).
2. **Transform** — CamelCase → snake_case columns, drop constant columns
   (EmployeeCount, StandardHours, Over18), dedupe on employee ID, convert
   Attrition Yes/No to a 0/1 `left` flag. 1,470 in → 1,470 clean.
3. **Load** — SQLite star-ish schema in `outputs/hr.db`:
   `fact_employee` (1,470 rows, one per employee) + `dim_department` (3) +
   `dim_job_role` (9).
4. **Analyze** — `analysis.sql`: attrition by department, overtime effect,
   tenure bands, income bands, job role, satisfaction, leaver/stayer pay.
5. **Present** — `outputs/dashboard.png`: attrition by department, overtime
   comparison, tenure bands, income bands.

## Key findings

- Overtime workers leave at 30.5% vs 10.4% without — the strongest signal.
- Attrition concentrates in the first 2 years (36.4% in year 0) and in the
  lowest pay band (28.6% under $3k/month).
- Sales Representatives are the outlier role at 39.8% attrition.

See `INSIGHTS.md` for the full findings with numbers.
