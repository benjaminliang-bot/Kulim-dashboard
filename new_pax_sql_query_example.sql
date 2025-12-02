-- New Pax SQL Query Example
-- Definition: Unique passenger_id where:
--   - Last transaction was more than a year ago, OR
--   - First order was within the week

-- For OC Overall (This Week)
WITH this_week_new_pax AS (
    SELECT 
        COUNT(DISTINCT f.passenger_id) as new_pax_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {THIS_WEEK_START} 
      AND f.date_id <= {THIS_WEEK_END}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.passenger_id IN (
          -- Passengers whose last transaction was more than a year ago
          SELECT DISTINCT passenger_id
          FROM ocd_adw.f_food_metrics
          WHERE country_id = 1
            AND city_id != 1
            AND business_type = 0
            AND booking_state_simple = 'COMPLETED'
            AND date_id < {THIS_WEEK_START} - 36500  -- More than a year ago (365 days * 100 for date_id format)
            AND passenger_id NOT IN (
                -- Exclude passengers who ordered in the last year (before this week)
                SELECT DISTINCT passenger_id
                FROM ocd_adw.f_food_metrics
                WHERE country_id = 1
                  AND city_id != 1
                  AND business_type = 0
                  AND booking_state_simple = 'COMPLETED'
                  AND date_id >= {THIS_WEEK_START} - 36500
                  AND date_id < {THIS_WEEK_START}
            )
      )
      OR f.passenger_id IN (
          -- Passengers whose first order was within this week
          SELECT passenger_id
          FROM (
              SELECT 
                  passenger_id,
                  MIN(date_id) as first_order_date
              FROM ocd_adw.f_food_metrics
              WHERE country_id = 1
                AND city_id != 1
                AND business_type = 0
                AND booking_state_simple = 'COMPLETED'
              GROUP BY passenger_id
          ) first_orders
          WHERE first_order_date >= {THIS_WEEK_START}
            AND first_order_date <= {THIS_WEEK_END}
      )
)
SELECT new_pax_count as this_week_new_pax
FROM this_week_new_pax;

-- Alternative simpler approach using window functions:
-- This counts passengers who either:
-- 1. Have their first order in this week, OR
-- 2. Have their last order before this week but more than 365 days ago

WITH passenger_history AS (
    SELECT 
        passenger_id,
        MIN(date_id) as first_order_date,
        MAX(date_id) as last_order_date
    FROM ocd_adw.f_food_metrics
    WHERE country_id = 1
      AND city_id != 1
      AND business_type = 0
      AND booking_state_simple = 'COMPLETED'
    GROUP BY passenger_id
),
this_week_orders AS (
    SELECT DISTINCT passenger_id
    FROM ocd_adw.f_food_metrics
    WHERE country_id = 1
      AND city_id != 1
      AND business_type = 0
      AND booking_state_simple = 'COMPLETED'
      AND date_id >= {THIS_WEEK_START}
      AND date_id <= {THIS_WEEK_END}
)
SELECT 
    COUNT(DISTINCT t.passenger_id) as this_week_new_pax
FROM this_week_orders t
INNER JOIN passenger_history p ON t.passenger_id = p.passenger_id
WHERE 
    -- First order was within this week
    (p.first_order_date >= {THIS_WEEK_START} AND p.first_order_date <= {THIS_WEEK_END})
    OR
    -- Last order before this week was more than a year ago
    (p.last_order_date < {THIS_WEEK_START} - 36500);

-- For Same Week Last Month comparison:
-- Replace {THIS_WEEK_START} and {THIS_WEEK_END} with {SAME_WEEK_LAST_MONTH_START} and {SAME_WEEK_LAST_MONTH_END}
-- And adjust the date comparisons accordingly

-- For YoY comparison:
-- Replace {THIS_WEEK_START} and {THIS_WEEK_END} with {SAME_WEEK_LAST_YEAR_START} and {SAME_WEEK_LAST_YEAR_END}
-- And adjust the date comparisons accordingly

