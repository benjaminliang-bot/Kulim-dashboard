-- SQL Query to analyze Kombo Jimat order distribution across last 4 days of each month for Penang
-- Using Presto/Trino syntax compatible with Grab DataLake

WITH last_4_days AS (
  SELECT 
    date_id,
    DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d') as order_date,
    EXTRACT(DAY FROM DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d')) as day_of_month,
    EXTRACT(DAY FROM (DATE_ADD('day', -1, DATE_ADD('month', 1, DATE_TRUNC('month', DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d')))))) as last_day_of_month
  FROM gt_aws_hive.ocd_adw.d_date
  WHERE date_id >= 20240101 AND date_id < 20251101
)
SELECT 
  DATE_FORMAT(DATE_PARSE(CAST(f.date_id AS VARCHAR), '%Y%m%d'), '%Y-%m-01') as month,
  EXTRACT(DAY FROM DATE_PARSE(CAST(f.date_id AS VARCHAR), '%Y%m%d')) as day_of_month,
  COUNT(DISTINCT f.order_id) as kombo_jimat_orders,
  SUM(f.receipt_total_fare) as kombo_jimat_gmv_myr,
  -- Day position: 1 = 4th last day, 2 = 3rd last, 3 = 2nd last, 4 = last day
  (l.last_day_of_month - EXTRACT(DAY FROM DATE_PARSE(CAST(f.date_id AS VARCHAR), '%Y%m%d')) + 1) as day_position
FROM 
  gt_aws_hive.ocd_adw.f_food_order f
  INNER JOIN last_4_days l ON f.date_id = l.date_id
  LEFT JOIN gt_aws_hive.promo.promo_discount pd ON f.order_id = pd.order_id
WHERE 
  -- Filter for Penang
  f.adw_city_id = 13  -- Penang city ID
  
  -- Filter for completed orders only
  AND f.booking_state_simple = 'COMPLETED'
  
  -- Filter for last 4 days of each month
  AND EXTRACT(DAY FROM DATE_PARSE(CAST(f.date_id AS VARCHAR), '%Y%m%d')) > (l.last_day_of_month - 4)
  
  -- Filter for Kombo Jimat promotion (adjust based on actual promo identifier)
  AND (
    LOWER(CAST(pd.promo_name AS VARCHAR)) LIKE '%kombo%jimat%'
    OR LOWER(CAST(pd.promo_name AS VARCHAR)) LIKE '%buy 1 free 1%'
    OR LOWER(CAST(pd.promo_name AS VARCHAR)) LIKE '%buy 1 get 2nd%'
    OR LOWER(CAST(pd.promo_name AS VARCHAR)) LIKE '%signatures buy 1 free 1%'
  )
  
  -- Historical data range
  AND f.date_id >= 20240101
  AND f.date_id < 20251101

GROUP BY 
  DATE_FORMAT(DATE_PARSE(CAST(f.date_id AS VARCHAR), '%Y%m%d'), '%Y-%m-01'),
  EXTRACT(DAY FROM DATE_PARSE(CAST(f.date_id AS VARCHAR), '%Y%m%d')),
  l.last_day_of_month

ORDER BY 
  month DESC,
  day_of_month DESC

LIMIT 100


