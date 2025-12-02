-- Query to analyze Kombo Jimat order distribution across the last 4 days of each month
-- This will help understand how orders are typically distributed (e.g., higher on certain days)

-- Expected structure based on user's previous SQL query pattern
-- Modify based on actual table structure

SELECT 
    DATE_TRUNC('month', order_date) as month,
    EXTRACT(DAY FROM order_date) as day_of_month,
    COUNT(*) as kombo_jimat_orders,
    SUM(order_value) as kombo_jimat_gmv,
    -- Calculate day position within last 4 days (1 = 4th last day, 4 = last day)
    CASE 
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '1 day')) THEN 4  -- Last day
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '2 day')) THEN 3  -- 2nd last
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '3 day')) THEN 2  -- 3rd last
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '4 day')) THEN 1  -- 4th last
    END as day_position_in_campaign,
    -- Calculate which day is highest (to identify patterns)
    ROW_NUMBER() OVER (PARTITION BY DATE_TRUNC('month', order_date) ORDER BY COUNT(*) DESC) as rank_by_orders
FROM 
    orders_table  -- Replace with actual table name
WHERE 
    -- Filter for Kombo Jimat orders (adjust filter based on actual promo identifier)
    promo_type LIKE '%Kombo Jimat%' 
    OR promo_name LIKE '%Kombo Jimat%'
    OR promo_id IN (SELECT promo_id FROM promos WHERE promo_name LIKE '%Kombo Jimat%')
    
    -- Filter for last 4 days of each month
    AND EXTRACT(DAY FROM order_date) > EXTRACT(DAY FROM (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '5 day'))
    
    -- Filter for Penang
    AND city_id = 13  -- Penang
    
    -- Filter for completed orders
    AND booking_simple_state = 'COMPLETED'
    
    -- Filter for date range (e.g., 2024-2025)
    AND order_date >= '2024-01-01'
    AND order_date < '2025-11-01'

GROUP BY 
    DATE_TRUNC('month', order_date),
    EXTRACT(DAY FROM order_date)

ORDER BY 
    month,
    day_of_month DESC


