
-- 1. Overall business performance
SELECT
    COUNT(DISTINCT Order_ID) AS total_orders,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(
        100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0),
        2
    ) AS profit_margin
FROM orders;


-- 2. Regional performance
SELECT
    Region,
    COUNT(DISTINCT Order_ID) AS orders,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM orders
GROUP BY Region
ORDER BY revenue DESC;


-- 3. Monthly sales trends
SELECT
    Order_Month,
    SUM(Sales) AS monthly_sales,
    SUM(Profit) AS monthly_profit
FROM orders
GROUP BY Order_Month
ORDER BY Order_Month;


-- 4. Least profitable products
SELECT
    Sub_Category,
    SUM(Sales) AS sales,
    SUM(Profit) AS profit
FROM orders
GROUP BY Sub_Category
ORDER BY profit ASC;


-- 5. Discount impact analysis
SELECT
    discount_band,
    COUNT(*) AS order_lines,
    COUNT(DISTINCT Order_ID) AS distinct_orders_touched,
    ROUND(AVG(Discount) * 100, 2) AS average_discount_pct,
    ROUND(SUM(Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0),
        2
    ) AS profit_margin_pct

FROM (
    SELECT
        *,
        CASE
            WHEN Discount = 0 THEN 'No Discount'
            WHEN Discount <= 0.20 THEN '1-20%'
            WHEN Discount <= 0.40 THEN '21-40%'
            ELSE 'Above 40%'
        END AS discount_band
    FROM orders
) AS discount_analysis

GROUP BY discount_band
ORDER BY average_discount_pct;
