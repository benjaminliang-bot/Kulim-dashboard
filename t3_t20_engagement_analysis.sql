-- T3/T20 Engagement Analysis - Last 6 Months
-- Period: May 2025 to October 2025

-- ============================================================================
-- QUESTION 1: Do we increase T3/T20 Campaigns/Ads Participation %?
-- ============================================================================
-- Note: Need to identify campaign/ads participation tables
-- This may require querying campaign management systems or promo tables

-- ============================================================================
-- QUESTION 2: Do we Increase T3/T20 DoD Mex Participation %?
-- ============================================================================

-- 2a. DoD Participation from pre_purchased_deals_base (campaign setup)
WITH t20_t3_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN (
            -- T20/T3 merchant IDs from Main Tracker V2
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )
),
dod_participation_by_month AS (
    SELECT 
        DATE_TRUNC('month', CAST(campaign_upload_date AS DATE)) as month,
        COUNT(DISTINCT merchant_id) as participating_merchants,
        COUNT(DISTINCT campaign_id) as total_campaigns
    FROM analytics_food.pre_purchased_deals_base
    WHERE city_name = 'Penang'
        AND campaign_upload_date >= DATE '2025-05-01'
        AND campaign_upload_date < DATE '2025-11-01'
        AND merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
    GROUP BY DATE_TRUNC('month', CAST(campaign_upload_date AS DATE))
)
SELECT 
    month,
    participating_merchants,
    total_campaigns,
    LAG(participating_merchants) OVER (ORDER BY month) as prev_month_participants,
    participating_merchants - LAG(participating_merchants) OVER (ORDER BY month) as change
FROM dod_participation_by_month
ORDER BY month;

-- 2b. DoD Participation from f_food_prepurchased_deals (actual orders)
WITH dod_orders_by_month AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        COUNT(DISTINCT merchant_id) as participating_merchants,
        COUNT(DISTINCT order_id) as total_orders,
        SUM(gmv_local) as total_gmv
    FROM ocd_adw.f_food_prepurchased_deals
    WHERE city_id = 13
        AND date_id >= 20250501  -- May 2025
        AND date_id < 20251101   -- Nov 2025
        AND order_state_simple = 'COMPLETED'
        AND merchant_id IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant 
            WHERE city_id = 13 LIMIT 1474  -- T20/T3 merchants
        )
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    month_id,
    participating_merchants,
    total_orders,
    total_gmv,
    LAG(participating_merchants) OVER (ORDER BY month_id) as prev_month_participants,
    participating_merchants - LAG(participating_merchants) OVER (ORDER BY month_id) as change
FROM dod_orders_by_month
ORDER BY month_id;

-- ============================================================================
-- QUESTION 3: Is all T20/T3 merchant being tagged to someone? (engagement rate)
-- ============================================================================
SELECT 
    COUNT(DISTINCT merchant_id_nk) as total_t20_t3_merchants,
    COUNT(DISTINCT CASE WHEN am_name IS NOT NULL AND am_name != '' THEN merchant_id_nk END) as with_am_assigned,
    COUNT(DISTINCT CASE WHEN am_name IS NULL OR am_name = '' THEN merchant_id_nk END) as without_am_assigned,
    ROUND(COUNT(DISTINCT CASE WHEN am_name IS NOT NULL AND am_name != '' THEN merchant_id_nk END) * 100.0 / 
          NULLIF(COUNT(DISTINCT merchant_id_nk), 0), 2) as engagement_rate_pct
FROM ocd_adw.d_merchant
WHERE city_id = 13
    AND merchant_id_nk IN (
        -- T20/T3 merchant IDs from Main Tracker V2
        SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
    );


