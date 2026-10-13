-- Retail Sales — analysis queries (SQLite, run against outputs/superstore.db)
-- Star schema: fact_sales + dim_product, dim_customer, dim_region, dim_date

-- 1. Headline totals
SELECT SUM(sales) AS total_sales, SUM(profit) AS total_profit,
       ROUND(100.0 * SUM(profit) / SUM(sales), 2) AS margin_pct,
       COUNT(*) AS fact_rows, COUNT(DISTINCT order_id) AS orders
FROM fact_sales;

-- 2. Sales and profit by product category
SELECT p.category, SUM(f.sales) AS sales, SUM(f.profit) AS profit,
       ROUND(100.0 * SUM(f.profit) / SUM(f.sales), 2) AS margin_pct
FROM fact_sales f JOIN dim_product p USING (product_id)
GROUP BY p.category ORDER BY sales DESC;

-- 3. Monthly sales trend
SELECT d.year, d.month, SUM(f.sales) AS sales
FROM fact_sales f JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY d.year, d.month ORDER BY d.year, d.month;

-- 4. Profit by region
SELECT r.region, SUM(f.sales) AS sales, SUM(f.profit) AS profit
FROM fact_sales f JOIN dim_region r USING (region_key)
GROUP BY r.region ORDER BY profit DESC;

-- 5. Top 10 products by profit (and the 5 biggest loss-makers)
SELECT p.product_name, SUM(f.sales) AS sales, SUM(f.profit) AS profit
FROM fact_sales f JOIN dim_product p USING (product_id)
GROUP BY p.product_name ORDER BY profit DESC LIMIT 10;

SELECT p.product_name, SUM(f.profit) AS profit
FROM fact_sales f JOIN dim_product p USING (product_id)
GROUP BY p.product_name ORDER BY profit ASC LIMIT 5;

-- 6. Discount depth vs average profit per order line
SELECT CASE WHEN discount = 0 THEN 'No discount'
            WHEN discount <= 0.2 THEN '1-20%'
            WHEN discount <= 0.4 THEN '21-40%'
            ELSE 'Over 40%' END AS discount_bucket,
       COUNT(*) AS lines, ROUND(AVG(profit), 2) AS avg_profit
FROM fact_sales GROUP BY discount_bucket;

-- 7. Year-over-year sales and profit
SELECT d.year, SUM(f.sales) AS sales, SUM(f.profit) AS profit
FROM fact_sales f JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY d.year ORDER BY d.year;
