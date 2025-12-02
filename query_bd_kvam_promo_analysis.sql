-- ============================================================================
-- BD, KVAM, and SD PROMO CODE ANALYSIS - PENANG
-- Last 6 Months (May 2025 - October 2025)
-- ============================================================================


================================================================================
QUESTION 1: BD GMV % Trends
================================================================================


-- ============================================================================
-- QUESTION 1: BD GMV % TRENDS IN PENANG
-- Last 6 Months (May 2025 - October 2025)
-- How T3/T20 growth changes the distribution
-- ============================================================================

WITH t20_t3_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )
),
bd_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND (is_bd_account = TRUE OR is_bd_partner = TRUE)
),
monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        -- Total Penang GMV
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv,
        -- BD GMV (from BD merchants)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM bd_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as bd_gmv,
        -- Non-BD GMV
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id NOT IN (SELECT merchant_id_nk FROM bd_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as non_bd_gmv,
        -- T20/T3 GMV (total)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as t20_t3_gmv,
        -- BD + T20/T3 GMV (overlap)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM bd_merchants)
            AND f.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as bd_t20_t3_gmv,
        -- BD but not T20/T3 GMV
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM bd_merchants)
            AND f.merchant_id NOT IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as bd_non_t20_t3_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    month_id,
    total_penang_gmv,
    bd_gmv,
    non_bd_gmv,
    t20_t3_gmv,
    bd_t20_t3_gmv,
    bd_non_t20_t3_gmv,
    -- BD GMV as % of total Penang GMV
    ROUND(bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0), 2) as bd_gmv_pct,
    -- T20/T3 GMV as % of total Penang GMV
    ROUND(t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0), 2) as t20_t3_gmv_pct,
    -- BD + T20/T3 overlap as % of total Penang GMV
    ROUND(bd_t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0), 2) as bd_t20_t3_overlap_pct,
    -- BD but not T20/T3 as % of total Penang GMV
    ROUND(bd_non_t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0), 2) as bd_non_t20_t3_pct,
    -- MoM changes
    LAG(bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) OVER (ORDER BY month_id) as prev_bd_gmv_pct,
    ROUND((bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) - 
          LAG(bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) OVER (ORDER BY month_id), 2) as bd_gmv_pct_change,
    LAG(t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) OVER (ORDER BY month_id) as prev_t20_t3_gmv_pct,
    ROUND((t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) - 
          LAG(t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) OVER (ORDER BY month_id), 2) as t20_t3_gmv_pct_change
FROM monthly_gmv
ORDER BY month_id;



================================================================================
QUESTION 2: KVAM GMV % Trends
================================================================================


-- ============================================================================
-- QUESTION 2: KVAM GMV % TRENDS IN PENANG
-- Last 6 Months (May 2025 - October 2025)
-- KVAM: Darren, Suki, Chia Yee, MGS
-- How T3/T20 growth changes the distribution
-- ============================================================================

WITH t20_t3_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )
),
kvam_merchants AS (
    SELECT DISTINCT merchant_id_nk, am_name
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND am_name IN ('Darren', 'Suki', 'Chia Yee', 'MGS')
),
monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        -- Total Penang GMV
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv,
        -- KVAM GMV (total from all KVAMs)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kvam_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as kvam_total_gmv,
        -- T20/T3 GMV (total)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as t20_t3_gmv,
        -- KVAM + T20/T3 GMV (overlap)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kvam_merchants)
            AND f.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as kvam_t20_t3_gmv,
        -- KVAM but not T20/T3 GMV
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kvam_merchants)
            AND f.merchant_id NOT IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as kvam_non_t20_t3_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
kvam_by_am AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        km.am_name,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as am_gmv,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as am_t20_t3_gmv
    FROM ocd_adw.f_food_metrics f
    INNER JOIN kvam_merchants km ON f.merchant_id = km.merchant_id_nk
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER), km.am_name
)
SELECT 
    mg.month_id,
    mg.total_penang_gmv,
    mg.kvam_total_gmv,
    mg.t20_t3_gmv,
    mg.kvam_t20_t3_gmv,
    mg.kvam_non_t20_t3_gmv,
    -- KVAM GMV as % of total Penang GMV
    ROUND(mg.kvam_total_gmv * 100.0 / NULLIF(mg.total_penang_gmv, 0), 2) as kvam_gmv_pct,
    -- T20/T3 GMV as % of total Penang GMV
    ROUND(mg.t20_t3_gmv * 100.0 / NULLIF(mg.total_penang_gmv, 0), 2) as t20_t3_gmv_pct,
    -- KVAM + T20/T3 overlap as % of total Penang GMV
    ROUND(mg.kvam_t20_t3_gmv * 100.0 / NULLIF(mg.total_penang_gmv, 0), 2) as kvam_t20_t3_overlap_pct,
    -- KVAM but not T20/T3 as % of total Penang GMV
    ROUND(mg.kvam_non_t20_t3_gmv * 100.0 / NULLIF(mg.total_penang_gmv, 0), 2) as kvam_non_t20_t3_pct,
    -- MoM changes
    LAG(mg.kvam_total_gmv * 100.0 / NULLIF(mg.total_penang_gmv, 0)) OVER (ORDER BY mg.month_id) as prev_kvam_gmv_pct,
    ROUND((mg.kvam_total_gmv * 100.0 / NULLIF(mg.total_penang_gmv, 0)) - 
          LAG(mg.kvam_total_gmv * 100.0 / NULLIF(mg.total_penang_gmv, 0)) OVER (ORDER BY mg.month_id), 2) as kvam_gmv_pct_change
FROM monthly_gmv mg
ORDER BY mg.month_id;

-- KVAM Breakdown by AM
SELECT 
    month_id,
    am_name,
    am_gmv,
    am_t20_t3_gmv,
    ROUND(am_t20_t3_gmv * 100.0 / NULLIF(am_gmv, 0), 2) as t20_t3_pct_of_am_gmv,
    LAG(am_gmv) OVER (PARTITION BY am_name ORDER BY month_id) as prev_am_gmv,
    ROUND((am_gmv - LAG(am_gmv) OVER (PARTITION BY am_name ORDER BY month_id)) * 100.0 / 
          NULLIF(LAG(am_gmv) OVER (PARTITION BY am_name ORDER BY month_id), 0), 2) as am_gmv_growth_pct
FROM kvam_by_am
ORDER BY month_id, am_name;



================================================================================
QUESTION 3: SD Promo Code Contribution
================================================================================


-- ============================================================================
-- QUESTION 3: SD PROMO CODE CONTRIBUTION TO PENANG GROWTH
-- Last 6 Months (May 2025 - October 2025)
-- Promo Codes: Voucher, Hairstory, GPFF5, PSDC5, SMEC, INNPLX, GBSMH, GBSMY, GBSEA, GBTECH... (total 50 codes)
-- ============================================================================

WITH monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        -- Total Penang GMV
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as total_penang_orders
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
sd_promo_orders AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        -- Check promo_code_os from f_food_order_detail
        COALESCE(fod.promo_code_os, '') as promo_code,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as orders_with_promo,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv_with_promo,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters_with_promo
    FROM ocd_adw.f_food_metrics f
    LEFT JOIN ocd_adw.f_food_order_detail fod ON f.order_id = fod.order_id AND f.date_id = fod.date_id
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
        AND COALESCE(fod.promo_code_os, '') IN ('Voucher', 'Hairstory', 'GPFF5', 'PSDC5', 'SMEC', 'INNPLX', 'GBSMH', 'GBSMY', 'GBSEA', 'GBTECH', 'GPDC', 'TARPNG', 'PSULA', 'UOWPG', 'BDOPG', 'WOUPG', 'QBPG2', 'PERKESO', 'INFINITY8PG', 'O2PG', 'TUG20', 'PRITECH', 'MALVEST', 'ART20', 'PENTA', 'MBPP20', 'GSDL', 'GIMM20', 'JAZZ20', 'QANOVA', 'ICONIC', 'IQI20', 'SHERYN', 'RFS20', 'CTG20', 'HOSPRAI', 'AKV2', 'UNITAR2', 'UITM', 'MEA20', 'LCOPG', 'IHOS', 'MAINPG', 'ORANGE', 'XILNEX', 'GWM2', 'BELL20', 'KAMI20', 'E2P', 'ASPEN')
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER), COALESCE(fod.promo_code_os, '')
),
sd_promo_summary AS (
    SELECT 
        month_id,
        SUM(orders_with_promo) as total_sd_promo_orders,
        SUM(gmv_with_promo) as total_sd_promo_gmv,
        SUM(unique_eaters_with_promo) as total_sd_promo_eaters
    FROM sd_promo_orders
    GROUP BY month_id
)
SELECT 
    mg.month_id,
    mg.total_penang_gmv,
    mg.total_penang_orders,
    COALESCE(sp.total_sd_promo_gmv, 0) as sd_promo_gmv,
    COALESCE(sp.total_sd_promo_orders, 0) as sd_promo_orders,
    COALESCE(sp.total_sd_promo_eaters, 0) as sd_promo_eaters,
    -- SD Promo GMV as % of total Penang GMV
    ROUND(COALESCE(sp.total_sd_promo_gmv, 0) * 100.0 / NULLIF(mg.total_penang_gmv, 0), 2) as sd_promo_gmv_pct,
    -- SD Promo Orders as % of total Penang Orders
    ROUND(COALESCE(sp.total_sd_promo_orders, 0) * 100.0 / NULLIF(mg.total_penang_orders, 0), 2) as sd_promo_orders_pct,
    -- MoM changes
    LAG(COALESCE(sp.total_sd_promo_gmv, 0) * 100.0 / NULLIF(mg.total_penang_gmv, 0)) OVER (ORDER BY mg.month_id) as prev_sd_promo_gmv_pct,
    ROUND((COALESCE(sp.total_sd_promo_gmv, 0) * 100.0 / NULLIF(mg.total_penang_gmv, 0)) - 
          LAG(COALESCE(sp.total_sd_promo_gmv, 0) * 100.0 / NULLIF(mg.total_penang_gmv, 0)) OVER (ORDER BY mg.month_id), 2) as sd_promo_gmv_pct_change,
    -- GMV growth contribution
    mg.total_penang_gmv - LAG(mg.total_penang_gmv) OVER (ORDER BY mg.month_id) as total_gmv_growth,
    COALESCE(sp.total_sd_promo_gmv, 0) - LAG(COALESCE(sp.total_sd_promo_gmv, 0)) OVER (ORDER BY mg.month_id) as sd_promo_gmv_growth,
    ROUND((COALESCE(sp.total_sd_promo_gmv, 0) - LAG(COALESCE(sp.total_sd_promo_gmv, 0)) OVER (ORDER BY mg.month_id)) * 100.0 / 
          NULLIF(mg.total_penang_gmv - LAG(mg.total_penang_gmv) OVER (ORDER BY mg.month_id), 0), 2) as sd_promo_contribution_to_growth_pct
FROM monthly_gmv mg
LEFT JOIN sd_promo_summary sp ON mg.month_id = sp.month_id
ORDER BY mg.month_id;

-- SD Promo Code Breakdown by Code
SELECT 
    month_id,
    promo_code,
    orders_with_promo,
    gmv_with_promo,
    unique_eaters_with_promo,
    ROUND(gmv_with_promo * 100.0 / NULLIF(SUM(gmv_with_promo) OVER (PARTITION BY month_id), 0), 2) as promo_code_share_pct,
    LAG(gmv_with_promo) OVER (PARTITION BY promo_code ORDER BY month_id) as prev_gmv,
    ROUND((gmv_with_promo - LAG(gmv_with_promo) OVER (PARTITION BY promo_code ORDER BY month_id)) * 100.0 / 
          NULLIF(LAG(gmv_with_promo) OVER (PARTITION BY promo_code ORDER BY month_id), 0), 2) as promo_code_gmv_growth_pct
FROM sd_promo_orders
ORDER BY month_id, gmv_with_promo DESC;


