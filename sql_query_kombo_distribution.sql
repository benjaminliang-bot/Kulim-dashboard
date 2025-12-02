-- SQL Query to analyze Kombo Jimat order distribution across last 4 days of each month
-- This query analyzes how orders are distributed across the 4 campaign days historically
-- Use this to identify distribution patterns (e.g., which day has most orders)

-- Replace table names and column names based on your actual schema
-- Based on user's previous query pattern, this should identify Kombo Jimat orders

SELECT 
    DATE_TRUNC('month', order_date) as month,
    EXTRACT(DAY FROM order_date) as day_of_month,
    COUNT(DISTINCT order_id) as kombo_jimat_orders,
    SUM(order_value) as kombo_jimat_gmv,
    -- Day position: 1 = 4th last day, 2 = 3rd last, 3 = 2nd last, 4 = last day
    EXTRACT(DAY FROM (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '1 day')) 
        - EXTRACT(DAY FROM order_date) + 1 as day_position,
    -- Day name for reference
    TO_CHAR(order_date, 'Day') as day_name
FROM 
    orders  -- Replace with actual table name
WHERE 
    -- Filter for Kombo Jimat promotion
    -- Adjust this filter based on how Kombo Jimat is identified in your system
    (
        promo_name ILIKE '%Kombo Jimat%' 
        OR promo_name ILIKE '%kombo jimat%'
        OR promo_name ILIKE '%Buy 1 Free 1%'
        OR promo_name ILIKE '%Buy 1 Get 2nd%'
        OR promo_id IN (
            SELECT promo_id 
            FROM promotions 
            WHERE promo_name ILIKE '%Kombo Jimat%'
        )
    )
    
    -- Filter for Penang
    AND city_id = 13  -- Penang city ID
    
    -- Filter for completed orders only
    AND booking_simple_state = 'COMPLETED'
    
    -- Filter for last 4 days of each month
    AND EXTRACT(DAY FROM order_date) > (
        EXTRACT(DAY FROM (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '1 day')) - 4
    )
    
    -- Historical data range (adjust as needed)
    AND order_date >= '2024-01-01'
    AND order_date < '2025-11-01'  -- Up to current date

GROUP BY 
    DATE_TRUNC('month', order_date),
    EXTRACT(DAY FROM order_date),
    order_date

ORDER BY 
    month DESC,
    day_of_month DESC

-- Expected output:
-- month       | day_of_month | kombo_jimat_orders | kombo_jimat_gmv | day_position | day_name
-- 2025-10-01  | 31           | 5,234              | 251,232         | 1            | Thursday
-- 2025-10-01  | 30           | 6,891              | 330,768         | 2            | Wednesday
-- 2025-10-01  | 29           | 7,123              | 341,904         | 3            | Tuesday
-- 2025-10-01  | 28           | 8,456              | 405,888         | 4            | Monday
-- ... (more months)


