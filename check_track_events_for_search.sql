-- ============================================================================
-- CHECK track_events_v2 FOR SEARCH DATA
-- ============================================================================
-- Purpose: Verify if grab_x.track_events_v2 contains search query events
-- Note: This table requires scope filter - adjust scope as needed
-- ============================================================================

-- Step 1: Check what event types exist related to search
SELECT DISTINCT
    event_name,
    COUNT(*) as event_count
FROM grab_x.track_events_v2
WHERE scope = 'grab_food'  -- ADJUST SCOPE AS NEEDED (e.g., 'grab_food_my', 'grab_food_penang')
    AND ingestion_date >= CURRENT_DATE - INTERVAL '7' DAY
    AND (
        event_name LIKE '%search%'
        OR event_name LIKE '%query%'
        OR event_name LIKE '%browse%'
        OR event_name LIKE '%filter%'
    )
GROUP BY event_name
ORDER BY event_count DESC
LIMIT 20;


-- Step 2: Sample search events to see structure
SELECT 
    event_name,
    event_properties,
    area_id,
    date_id,
    user_id,
    ingestion_date
FROM grab_x.track_events_v2
WHERE scope = 'grab_food'  -- ADJUST SCOPE AS NEEDED
    AND event_name LIKE '%search%'
    AND ingestion_date >= CURRENT_DATE - INTERVAL '7' DAY
LIMIT 10;


-- Step 3: Check if event_properties contains search_query field
SELECT 
    event_name,
    event_properties['search_query'] as search_query,
    event_properties['has_results'] as has_results,
    event_properties['result_count'] as result_count,
    event_properties['query_type'] as query_type,
    COUNT(*) as count
FROM grab_x.track_events_v2
WHERE scope = 'grab_food'  -- ADJUST SCOPE AS NEEDED
    AND event_name LIKE '%search%'
    AND ingestion_date >= CURRENT_DATE - INTERVAL '7' DAY
    AND event_properties['search_query'] IS NOT NULL
GROUP BY 
    event_name,
    event_properties['search_query'],
    event_properties['has_results'],
    event_properties['result_count'],
    event_properties['query_type']
ORDER BY count DESC
LIMIT 20;


-- Step 4: If search data exists, check Mainland coverage
WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
)
SELECT 
    event_name,
    COUNT(DISTINCT user_id) as unique_searchers,
    COUNT(*) as total_search_events,
    COUNT(DISTINCT CASE WHEN event_properties['has_results'] = 'false' THEN user_id END) as searches_with_no_results,
    COUNT(DISTINCT area_id) as areas_with_searches
FROM grab_x.track_events_v2
WHERE scope = 'grab_food'  -- ADJUST SCOPE AS NEEDED
    AND event_name LIKE '%search%'
    AND ingestion_date >= CURRENT_DATE - INTERVAL '30' DAY
    AND area_id IN (SELECT area_id FROM mainland_areas)
GROUP BY event_name
ORDER BY total_search_events DESC;


-- ============================================================================
-- NOTES
-- ============================================================================
-- 
-- 1. SCOPE FILTER IS REQUIRED for track_events_v2
--    - Common scopes: 'grab_food', 'grab_food_my', 'grab_food_penang'
--    - If query fails, try different scope values
--    - Check with data team for correct scope for Penang
--
-- 2. If search events are found:
--    - Use the template in Query 7 (commented section)
--    - Adjust event_name filter based on actual event names
--    - Map event_properties fields to search_query, has_results, etc.
--
-- 3. If no search events found:
--    - Search data may not be tracked in track_events_v2
--    - Use Query 7 session-based approach instead
--    - Contact data team for search analytics location
--
-- ============================================================================

