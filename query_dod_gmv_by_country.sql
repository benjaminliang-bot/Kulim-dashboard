-- SQL Query: DoD (Dine on Demand) GMV by Country - Last 90 Days
-- Using Presto/Trino syntax compatible with Grab DataLake
-- 
-- ASSUMPTIONS:
-- 1. DoD orders are identified by service_type, booking_type, or order_type field
-- 2. GMV is captured in f_food_order or f_food_metrics table
-- 3. Country code is available in d_area or directly in order table
-- 4. Date range: last 90 days from current date

WITH date_range AS (
  SELECT 
    date_id,
    DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d') as order_date,
    country_code
  FROM gt_aws_hive.ocd_adw.d_date d
  CROSS JOIN (
    -- Get all active countries
    SELECT DISTINCT country_code 
    FROM gt_aws_hive.ocd_adw.d_area 
    WHERE country_code IS NOT NULL
  ) c
  WHERE date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -90, CURRENT_DATE), '%Y%m%d') AS INT)
    AND date_id < CAST(DATE_FORMAT(CURRENT_DATE, '%Y%m%d') AS INT)
)

SELECT 
  COALESCE(a.country_code, 'UNKNOWN') as country_code,
  COUNT(DISTINCT f.order_id) as dod_orders,
  SUM(COALESCE(fm.gross_merchandise_value, f.receipt_total_fare, 0)) as dod_gmv_local_currency,
  -- Convert to USD if needed (adjust exchange rates as required)
  -- SUM(COALESCE(fm.gross_merchandise_value, f.receipt_total_fare, 0) / exchange_rate) as dod_gmv_usd,
  COUNT(DISTINCT f.merchant_id_nk) as active_merchants,
  COUNT(DISTINCT f.consumer_id) as active_consumers,
  -- Average order value
  SUM(COALESCE(fm.gross_merchandise_value, f.receipt_total_fare, 0)) / 
    NULLIF(COUNT(DISTINCT f.order_id), 0) as avg_order_value
FROM 
  gt_aws_hive.ocd_adw.f_food_order f
  INNER JOIN date_range dr ON f.date_id = dr.date_id
  LEFT JOIN gt_aws_hive.ocd_adw.f_food_metrics fm ON f.order_id = fm.order_id
  LEFT JOIN gt_aws_hive.ocd_adw.d_area a ON COALESCE(fm.area_id, f.area_id) = a.area_id

WHERE 
  -- Filter for completed orders only
  f.booking_state_simple = 'COMPLETED'
  
  -- OPTION 1: If DoD is identified by service_type
  -- AND f.service_type = 'DINE_ON_DEMAND'  -- or 'DOD' or similar
  
  -- OPTION 2: If DoD is identified by booking_type
  -- AND f.booking_type = 'DINE_IN'  -- or 'DOD' or similar
  
  -- OPTION 3: If DoD is identified by order_type field
  -- AND f.order_type = 'DINE_ON_DEMAND'
  
  -- OPTION 4: If DoD is identified by a flag
  -- AND f.is_dine_in = TRUE  -- or f.is_dod = TRUE
  
  -- OPTION 5: If DoD is identified via service dimension table
  -- INNER JOIN gt_aws_hive.ocd_adw.d_service s ON f.service_id = s.service_id
  -- AND s.service_name = 'Dine on Demand'  -- or similar
  
  -- OPTION 6: If DoD is identified by merchant business type or service category
  -- INNER JOIN gt_aws_hive.ocd_adw.d_merchant m ON f.merchant_id_nk = m.merchant_id_nk
  -- AND m.business_type = X  -- Replace X with DoD business type code if applicable
  
  -- Date filter (already in CTE, but adding as safety)
  AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -90, CURRENT_DATE), '%Y%m%d') AS INT)
  AND f.date_id < CAST(DATE_FORMAT(CURRENT_DATE, '%Y%m%d') AS INT)

GROUP BY 
  COALESCE(a.country_code, 'UNKNOWN')

ORDER BY 
  dod_gmv_local_currency DESC

-- Remove LIMIT to see all countries
LIMIT 100

-- ============================================================================
-- VALIDATION QUERIES (Run separately to verify DoD identification logic)
-- ============================================================================

-- Query 1: Check available service types / booking types
-- SELECT DISTINCT service_type, booking_type, order_type
-- FROM gt_aws_hive.ocd_adw.f_food_order
-- WHERE date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -7, CURRENT_DATE), '%Y%m%d') AS INT)
-- LIMIT 1000

-- Query 2: Check service dimension for DoD-related services
-- SELECT DISTINCT service_id, service_name, service_type
-- FROM gt_aws_hive.ocd_adw.d_service
-- WHERE LOWER(service_name) LIKE '%dine%' 
--    OR LOWER(service_name) LIKE '%dod%'
--    OR LOWER(service_name) LIKE '%dine%in%'

-- Query 3: Sample DoD orders to verify GMV field
-- SELECT 
--   f.order_id,
--   f.date_id,
--   f.service_type,
--   f.booking_type,
--   f.receipt_total_fare,
--   fm.gross_merchandise_value,
--   a.country_code
-- FROM gt_aws_hive.ocd_adw.f_food_order f
-- LEFT JOIN gt_aws_hive.ocd_adw.f_food_metrics fm ON f.order_id = fm.order_id
-- LEFT JOIN gt_aws_hive.ocd_adw.d_area a ON COALESCE(fm.area_id, f.area_id) = a.area_id
-- WHERE f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -7, CURRENT_DATE), '%Y%m%d') AS INT)
--   AND f.booking_state_simple = 'COMPLETED'
--   -- Add your DoD filter here
-- LIMIT 100







