-- ============================================================================
-- MGS INDIVIDUAL IMPACT ANALYSIS - PENANG
-- Last 6 Months (May 2025 - October 2025)
-- ============================================================================


================================================================================
MGS: Low Jia Ying (1 merchants)
================================================================================


-- ============================================================================
-- Low Jia Ying - Individual Impact Analysis
-- Last 6 Months (May 2025 - October 2025)
-- ============================================================================

WITH low_jia_ying_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES ('1-C2C2MBA2NKW3C6')) AS t(merchant_id_nk)
),
monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        COUNT(DISTINCT f.merchant_id) as unique_merchants,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
        AND f.merchant_id IN (SELECT merchant_id_nk FROM low_jia_ying_merchants)
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
total_penang_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    mg.month_id,
    mg.unique_merchants,
    mg.orders,
    mg.unique_eaters,
    mg.gmv,
    tp.total_penang_gmv,
    ROUND(mg.gmv * 100.0 / NULLIF(tp.total_penang_gmv, 0), 2) as gmv_pct_of_penang,
    ROUND(mg.gmv / NULLIF(mg.unique_merchants, 0), 2) as avg_gmv_per_merchant,
    ROUND(mg.gmv / NULLIF(mg.orders, 0), 2) as avg_gmv_per_order,
    ROUND(mg.gmv / NULLIF(mg.unique_eaters, 0), 2) as avg_gmv_per_eater
FROM monthly_gmv mg
INNER JOIN total_penang_gmv tp ON mg.month_id = tp.month_id
ORDER BY mg.month_id;



================================================================================
MGS: Teoh Jun Ling (2 merchants)
================================================================================


-- ============================================================================
-- Teoh Jun Ling - Individual Impact Analysis
-- Last 6 Months (May 2025 - October 2025)
-- ============================================================================

WITH teoh_jun_ling_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES ('1-C2AKJFAYT7MVTA'), ('1-C2UHGA3HLYXJTA')) AS t(merchant_id_nk)
),
monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        COUNT(DISTINCT f.merchant_id) as unique_merchants,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
        AND f.merchant_id IN (SELECT merchant_id_nk FROM teoh_jun_ling_merchants)
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
total_penang_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    mg.month_id,
    mg.unique_merchants,
    mg.orders,
    mg.unique_eaters,
    mg.gmv,
    tp.total_penang_gmv,
    ROUND(mg.gmv * 100.0 / NULLIF(tp.total_penang_gmv, 0), 2) as gmv_pct_of_penang,
    ROUND(mg.gmv / NULLIF(mg.unique_merchants, 0), 2) as avg_gmv_per_merchant,
    ROUND(mg.gmv / NULLIF(mg.orders, 0), 2) as avg_gmv_per_order,
    ROUND(mg.gmv / NULLIF(mg.unique_eaters, 0), 2) as avg_gmv_per_eater
FROM monthly_gmv mg
INNER JOIN total_penang_gmv tp ON mg.month_id = tp.month_id
ORDER BY mg.month_id;



================================================================================
MGS: Hon Yi Ni (4 merchants)
================================================================================


-- ============================================================================
-- Hon Yi Ni - Individual Impact Analysis
-- Last 6 Months (May 2025 - October 2025)
-- ============================================================================

WITH hon_yi_ni_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES ('1-C3XAT7WHCKMYVE'), ('1-C6AGEN4BLZBTJJ'), ('1-C3U3WADTGECARN'), ('1-C33HCVLUMEN1AA')) AS t(merchant_id_nk)
),
monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        COUNT(DISTINCT f.merchant_id) as unique_merchants,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
        AND f.merchant_id IN (SELECT merchant_id_nk FROM hon_yi_ni_merchants)
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
total_penang_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    mg.month_id,
    mg.unique_merchants,
    mg.orders,
    mg.unique_eaters,
    mg.gmv,
    tp.total_penang_gmv,
    ROUND(mg.gmv * 100.0 / NULLIF(tp.total_penang_gmv, 0), 2) as gmv_pct_of_penang,
    ROUND(mg.gmv / NULLIF(mg.unique_merchants, 0), 2) as avg_gmv_per_merchant,
    ROUND(mg.gmv / NULLIF(mg.orders, 0), 2) as avg_gmv_per_order,
    ROUND(mg.gmv / NULLIF(mg.unique_eaters, 0), 2) as avg_gmv_per_eater
FROM monthly_gmv mg
INNER JOIN total_penang_gmv tp ON mg.month_id = tp.month_id
ORDER BY mg.month_id;


