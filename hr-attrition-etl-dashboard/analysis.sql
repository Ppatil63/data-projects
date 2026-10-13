-- HR Attrition — analysis queries (SQLite, run against outputs/hr.db)
-- Schema: fact_employee + dim_department, dim_job_role  ("left" = 1 if left)

-- 1. Overall attrition
SELECT COUNT(*) AS employees, SUM("left") AS leavers,
       ROUND(100.0 * AVG("left"), 2) AS attrition_pct
FROM fact_employee;

-- 2. Attrition by department
SELECT d.department, COUNT(*) AS employees,
       ROUND(100.0 * AVG(f."left"), 1) AS attrition_pct
FROM fact_employee f JOIN dim_department d USING (department_key)
GROUP BY d.department ORDER BY attrition_pct DESC;

-- 3. Overtime effect
SELECT over_time, COUNT(*) AS employees,
       ROUND(100.0 * AVG("left"), 1) AS attrition_pct
FROM fact_employee GROUP BY over_time ORDER BY attrition_pct DESC;

-- 4. Attrition by tenure band (years at company)
SELECT CASE WHEN years_at_company = 0 THEN '0 yrs'
            WHEN years_at_company <= 2 THEN '1-2 yrs'
            WHEN years_at_company <= 5 THEN '3-5 yrs'
            WHEN years_at_company <= 10 THEN '6-10 yrs'
            ELSE '10+ yrs' END AS tenure_band,
       COUNT(*) AS employees,
       ROUND(100.0 * AVG("left"), 1) AS attrition_pct
FROM fact_employee GROUP BY tenure_band;

-- 5. Attrition by monthly income band
SELECT CASE WHEN monthly_income < 3000 THEN 'Under $3k'
            WHEN monthly_income < 5000 THEN '$3k-5k'
            WHEN monthly_income < 10000 THEN '$5k-10k'
            ELSE '$10k+' END AS income_band,
       COUNT(*) AS employees,
       ROUND(100.0 * AVG("left"), 1) AS attrition_pct
FROM fact_employee GROUP BY income_band;

-- 6. Attrition by job role
SELECT r.job_role, COUNT(*) AS employees,
       ROUND(100.0 * AVG(f."left"), 1) AS attrition_pct
FROM fact_employee f JOIN dim_job_role r USING (job_role_key)
GROUP BY r.job_role ORDER BY attrition_pct DESC;

-- 7. Leavers vs stayers — average monthly income
SELECT ROUND(AVG(CASE WHEN "left" = 1 THEN monthly_income END)) AS leaver_income,
       ROUND(AVG(CASE WHEN "left" = 0 THEN monthly_income END)) AS stayer_income
FROM fact_employee;
