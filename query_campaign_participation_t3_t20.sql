-- Question 1: Do we increase T3/T20 Campaigns/Ads Participation %?
-- Last 6 months (May 2025 - October 2025)
-- Using: ocd_adw.d_merchant_funded_campaign (campaign setup)
-- Using: ocd_adw.f_food_discount (campaign usage/redemption)

-- ============================================================================
-- PART 1: Campaign Participation from d_merchant_funded_campaign
-- Tracks which merchants have created/participated in campaigns
-- ============================================================================

WITH t20_t3_merchants AS (
    -- Get T20/T3 merchant IDs (1474 merchants from Main Tracker V2)
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
    LIMIT 1474  -- Approximate T20/T3 count
),
campaign_participation_by_month AS (
    SELECT 
        DATE_TRUNC('month', CAST(start_time AS DATE)) as month,
        COUNT(DISTINCT mfc.merchant_id) as participating_merchants,
        COUNT(DISTINCT mfc.campaign_id) as total_campaigns
    FROM ocd_adw.d_merchant_funded_campaign mfc
    WHERE mfc.city_id = 13
        AND CAST(mfc.start_time AS DATE) >= DATE '2025-05-01'
        AND CAST(mfc.start_time AS DATE) < DATE '2025-11-01'
        AND mfc.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
    GROUP BY DATE_TRUNC('month', CAST(start_time AS DATE))
)
SELECT 
    month,
    participating_merchants,
    total_campaigns,
    LAG(participating_merchants) OVER (ORDER BY month) as prev_month_participants,
    participating_merchants - LAG(participating_merchants) OVER (ORDER BY month) as change,
    ROUND((participating_merchants - LAG(participating_merchants) OVER (ORDER BY month)) * 100.0 / 
          NULLIF(LAG(participating_merchants) OVER (ORDER BY month), 0), 2) as change_pct
FROM campaign_participation_by_month
ORDER BY month;

-- ============================================================================
-- PART 2: Campaign Usage from f_food_discount
-- Tracks actual campaign redemptions (is_mfc = TRUE)
-- ============================================================================

WITH campaign_usage_by_month AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        COUNT(DISTINCT merchant_id) as merchants_with_campaign_usage,
        COUNT(DISTINCT order_id) as orders_with_campaigns,
        COUNT(DISTINCT mfc_campaign_id) as unique_campaigns_used,
        SUM(total_deducted_amount) as total_campaign_discount
    FROM ocd_adw.f_food_discount
    WHERE city_id = 13
        AND date_id >= 20250501  -- May 2025
        AND date_id < 20251101   -- Nov 2025
        AND booking_state_simple = 'COMPLETED'
        AND is_mfc = TRUE  -- Merchant-funded campaigns only
        AND merchant_id IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant 
            WHERE city_id = 13 LIMIT 1474  -- T20/T3 merchants
        )
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    month_id,
    merchants_with_campaign_usage,
    orders_with_campaigns,
    unique_campaigns_used,
    total_campaign_discount,
    LAG(merchants_with_campaign_usage) OVER (ORDER BY month_id) as prev_month_merchants,
    merchants_with_campaign_usage - LAG(merchants_with_campaign_usage) OVER (ORDER BY month_id) as merchant_change,
    ROUND((merchants_with_campaign_usage - LAG(merchants_with_campaign_usage) OVER (ORDER BY month_id)) * 100.0 / 
          NULLIF(LAG(merchants_with_campaign_usage) OVER (ORDER BY month_id), 0), 2) as merchant_change_pct
FROM campaign_usage_by_month
ORDER BY month_id;

-- ============================================================================
-- PART 3: Participation Rate Calculation
-- % of T20/T3 merchants participating in campaigns
-- ============================================================================

WITH t20_t3_total AS (
    SELECT COUNT(DISTINCT merchant_id_nk) as total_merchants
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
    LIMIT 1474
),
campaign_participants AS (
    SELECT 
        DATE_TRUNC('month', CAST(start_time AS DATE)) as month,
        COUNT(DISTINCT merchant_id) as participating_merchants
    FROM ocd_adw.d_merchant_funded_campaign
    WHERE city_id = 13
        AND CAST(start_time AS DATE) >= DATE '2025-05-01'
        AND CAST(start_time AS DATE) < DATE '2025-11-01'
        AND merchant_id IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant 
            WHERE city_id = 13 LIMIT 1474
        )
    GROUP BY DATE_TRUNC('month', CAST(start_time AS DATE))
)
SELECT 
    cp.month,
    cp.participating_merchants,
    tt.total_merchants,
    ROUND(cp.participating_merchants * 100.0 / NULLIF(tt.total_merchants, 0), 2) as participation_rate_pct,
    LAG(ROUND(cp.participating_merchants * 100.0 / NULLIF(tt.total_merchants, 0), 2)) OVER (ORDER BY cp.month) as prev_month_rate,
    ROUND(cp.participating_merchants * 100.0 / NULLIF(tt.total_merchants, 0), 2) - 
    LAG(ROUND(cp.participating_merchants * 100.0 / NULLIF(tt.total_merchants, 0), 2)) OVER (ORDER BY cp.month) as rate_change_pp
FROM campaign_participants cp
CROSS JOIN t20_t3_total tt
ORDER BY cp.month;


