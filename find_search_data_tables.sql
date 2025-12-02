-- ============================================================================
-- DISCOVERY QUERY: Find Search Data Tables
-- ============================================================================
-- Purpose: Identify tables that contain search query data
-- Method: Query information_schema to find potential search/analytics tables
-- ============================================================================

-- Option 1: List all tables in ocd_adw schema that might contain search data
-- Run this in Presto/Trino to see available tables
SELECT 
    table_schema,
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'ocd_adw'
    AND (
        table_name LIKE '%search%' 
        OR table_name LIKE '%query%'
        OR table_name LIKE '%session%'
        OR table_name LIKE '%event%'
        OR table_name LIKE '%analytics%'
        OR table_name LIKE '%scribe%'
        OR table_name LIKE '%user_behavior%'
        OR table_name LIKE '%log%'
    )
ORDER BY table_name;


-- Option 2: Check if there's a scribe_session dimension table
-- This might contain session-level data including searches
SELECT 
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'ocd_adw'
    AND table_name LIKE '%scribe%'
ORDER BY table_name;


-- Option 3: Check for analytics or tracking schemas
SELECT DISTINCT
    table_schema
FROM information_schema.tables
WHERE table_schema LIKE '%analytics%'
    OR table_schema LIKE '%track%'
    OR table_schema LIKE '%event%'
    OR table_schema LIKE '%log%'
ORDER BY table_schema;


-- ============================================================================
-- ALTERNATIVE APPROACH: Infer Search Behavior from Session Data
-- ============================================================================
-- If direct search tables don't exist, we can use scribe_session_id
-- to identify sessions with no orders (potential failed searches)
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
),
-- Get all sessions in Mainland areas
mainland_sessions AS (
    SELECT DISTINCT
        f.scribe_session_id,
        f.dropoff_area_id,
        f.date_id,
        f.passenger_id,
        COUNT(DISTINCT f.order_id) as orders_in_session,
        MAX(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN 1 ELSE 0 END) as has_completed_order
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.dropoff_area_id IN (SELECT area_id FROM mainland_areas)
        AND f.scribe_session_id IS NOT NULL
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -3, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY f.scribe_session_id, f.dropoff_area_id, f.date_id, f.passenger_id
),
-- Sessions with no completed orders (potential failed searches)
failed_sessions AS (
    SELECT 
        ms.scribe_session_id,
        ms.dropoff_area_id,
        a.area_name,
        ms.date_id,
        ms.passenger_id
    FROM mainland_sessions ms
    INNER JOIN mainland_areas a ON ms.dropoff_area_id = a.area_id
    WHERE ms.has_completed_order = 0
        AND ms.orders_in_session = 0
)
SELECT 
    area_name,
    COUNT(DISTINCT scribe_session_id) as sessions_with_no_orders,
    COUNT(DISTINCT passenger_id) as unique_users_with_no_orders,
    COUNT(DISTINCT date_id) as days_with_failed_sessions
FROM failed_sessions
GROUP BY area_name
ORDER BY sessions_with_no_orders DESC;


-- ============================================================================
-- NEXT STEPS AFTER RUNNING DISCOVERY QUERIES
-- ============================================================================
-- 
-- 1. Run Option 1 to find search-related tables
-- 2. If tables found, check their schema:
--    SELECT * FROM information_schema.columns 
--    WHERE table_schema = 'ocd_adw' AND table_name = '[FOUND_TABLE_NAME]'
-- 3. If no direct search tables, use Alternative Approach above
-- 4. Contact data team to identify search analytics table location
--
-- Common table names to look for:
-- - f_food_search_log
-- - d_scribe_session
-- - f_user_search_events
-- - analytics.food_search_queries
-- - track_events_v2 (if search events are tracked there)
-- ============================================================================

