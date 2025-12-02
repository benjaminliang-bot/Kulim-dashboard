-- ============================================================================
-- T3/T20 PROMOTION AND ADS PARTICIPATION (REDEFINED)
-- Last 6 Months (May 2025 - October 2025)
-- 
-- Redefinition:
-- 1. Promotion: If promotion spending > 0, then merchant is in promo
--    - Track MFP campaigns (hotdeals, delivery campaigns)
--    - Identify Grab-funded vs MEX-funded
--
-- 2. Ads: If ads revenue > 0, then merchant is in ads
--    - Identify Grab-funded vs MEX-funded
-- ============================================================================

-- Load T20/T3 merchant IDs (1474 merchants)
-- Note: Replace with actual merchant_id_nk list from t20_merchant_ids.json

-- ============================================================================
-- PART 1: PROMOTION PARTICIPATION
-- Source: ocd_adw.f_food_discount
-- Definition: total_mex_promo_spend > 0 OR total_grab_promo_spend > 0
-- Filter: is_mfp = TRUE (MFP campaigns - hotdeals, delivery campaigns)
-- ============================================================================

WITH t20_t3_merchants AS (
    -- Get T20/T3 merchant IDs from d_merchant
    -- For full analysis, use actual merchant_id_nk from t20_merchant_ids.json
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN (
            -- Sample: Replace with full list from t20_merchant_ids.json
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )
),
promo_spending_by_month AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        merchant_id,
        -- MEX-funded promo spending
        SUM(COALESCE(total_mex_promo_spend, 0)) as mex_promo_spend,
        -- Grab-funded promo spending
        SUM(COALESCE(total_grab_promo_spend, 0)) as grab_promo_spend,
        -- Total promo spending
        SUM(COALESCE(total_mex_promo_spend, 0) + COALESCE(total_grab_promo_spend, 0)) as total_promo_spend,
        -- MFP campaigns count (hotdeals, delivery campaigns)
        COUNT(DISTINCT CASE WHEN is_mfp = TRUE THEN mfc_campaign_id END) as mfp_campaigns,
        -- MFC campaigns count
        COUNT(DISTINCT CASE WHEN is_mfc = TRUE THEN mfc_campaign_id END) as mfc_campaigns,
        COUNT(DISTINCT order_id) as promo_orders,
        -- Campaign type breakdown (from eater_app_campaign_name or promo_type)
        COUNT(DISTINCT CASE WHEN is_mfp = TRUE AND (LOWER(eater_app_campaign_name) LIKE '%hotdeal%' 
                                                    OR LOWER(eater_app_campaign_name) LIKE '%delivery%') 
                           THEN mfc_campaign_id END) as hotdeal_delivery_campaigns
    FROM ocd_adw.f_food_discount
    WHERE city_id = 13
        AND date_id >= 20250501  -- May 2025
        AND date_id < 20251101   -- Nov 2025
        AND booking_state_simple = 'COMPLETED'
        AND merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
        -- Filter for MFP campaigns (hotdeals, delivery campaigns)
        AND is_mfp = TRUE
    GROUP BY 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER),
        merchant_id
),
merchant_promo_participation AS (
    SELECT 
        month_id,
        COUNT(DISTINCT CASE WHEN total_promo_spend > 0 THEN merchant_id END) as merchants_in_promo,
        COUNT(DISTINCT CASE WHEN mex_promo_spend > 0 THEN merchant_id END) as merchants_mex_funded,
        COUNT(DISTINCT CASE WHEN grab_promo_spend > 0 THEN merchant_id END) as merchants_grab_funded,
        COUNT(DISTINCT CASE WHEN mex_promo_spend > 0 AND grab_promo_spend > 0 THEN merchant_id END) as merchants_both_funded,
        SUM(total_promo_spend) as total_promo_spend_all,
        SUM(mex_promo_spend) as total_mex_promo_spend,
        SUM(grab_promo_spend) as total_grab_promo_spend,
        SUM(mfp_campaigns) as total_mfp_campaigns,
        SUM(hotdeal_delivery_campaigns) as total_hotdeal_delivery_campaigns,
        SUM(promo_orders) as total_promo_orders
    FROM promo_spending_by_month
    GROUP BY month_id
)
SELECT 
    month_id,
    merchants_in_promo,
    merchants_mex_funded,
    merchants_grab_funded,
    merchants_both_funded,
    total_promo_spend_all,
    total_mex_promo_spend,
    total_grab_promo_spend,
    ROUND(total_mex_promo_spend * 100.0 / NULLIF(total_promo_spend_all, 0), 2) as mex_funded_pct,
    ROUND(total_grab_promo_spend * 100.0 / NULLIF(total_promo_spend_all, 0), 2) as grab_funded_pct,
    total_mfp_campaigns,
    total_hotdeal_delivery_campaigns,
    total_promo_orders,
    -- Calculate participation rate
    ROUND(merchants_in_promo * 100.0 / NULLIF((SELECT COUNT(*) FROM t20_t3_merchants), 0), 2) as participation_rate_pct,
    LAG(merchants_in_promo) OVER (ORDER BY month_id) as prev_month_merchants,
    merchants_in_promo - LAG(merchants_in_promo) OVER (ORDER BY month_id) as merchant_change,
    ROUND((merchants_in_promo - LAG(merchants_in_promo) OVER (ORDER BY month_id)) * 100.0 / 
          NULLIF(LAG(merchants_in_promo) OVER (ORDER BY month_id), 0), 2) as merchant_change_pct
FROM merchant_promo_participation
ORDER BY month_id;

-- ============================================================================
-- PART 2: ADS REVENUE PARTICIPATION
-- Source: ocd_adw.agg_ads_merchant
-- Definition: If ads revenue > 0, then merchant is in ads
-- Ads revenue = accrued_amount_before_tax_local (amount Grab earns from ads)
-- ============================================================================

WITH t20_t3_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )
),
ads_revenue_by_month AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        merchant_id,
        -- Total ads revenue (Grab's revenue from ads)
        SUM(COALESCE(accrued_amount_before_tax_local, 0)) as ads_revenue,
        -- MEX-funded ads spend
        SUM(COALESCE(mex_prorated_billable_ad_spend_local, 0)) as mex_ads_spend,
        -- Total ads spend (billable)
        SUM(COALESCE(billable_ad_spend_local, 0)) as total_ads_spend,
        -- Ads performance metrics
        SUM(COALESCE(attributed_orders, 0)) as attributed_orders,
        SUM(COALESCE(attributed_gmv_local, 0)) as attributed_gmv,
        SUM(COALESCE(clicks, 0)) as total_clicks,
        SUM(COALESCE(impressions, 0)) as total_impressions
    FROM ocd_adw.agg_ads_merchant
    WHERE date_id >= 20250501  -- May 2025
        AND date_id < 20251101   -- Nov 2025
        AND merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
    GROUP BY 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER),
        merchant_id
),
merchant_ads_participation AS (
    SELECT 
        month_id,
        COUNT(DISTINCT CASE WHEN ads_revenue > 0 THEN merchant_id END) as merchants_in_ads,
        COUNT(DISTINCT CASE WHEN mex_ads_spend > 0 THEN merchant_id END) as merchants_mex_funded_ads,
        COUNT(DISTINCT CASE WHEN ads_revenue > 0 AND mex_ads_spend = 0 THEN merchant_id END) as merchants_grab_funded_ads_only,
        SUM(ads_revenue) as total_ads_revenue,
        SUM(mex_ads_spend) as total_mex_ads_spend,
        SUM(total_ads_spend) as total_ads_spend_all,
        SUM(attributed_orders) as total_attributed_orders,
        SUM(attributed_gmv) as total_attributed_gmv,
        SUM(total_clicks) as total_clicks,
        SUM(total_impressions) as total_impressions
    FROM ads_revenue_by_month
    GROUP BY month_id
)
SELECT 
    month_id,
    merchants_in_ads,
    merchants_mex_funded_ads,
    merchants_grab_funded_ads_only,
    total_ads_revenue,
    total_mex_ads_spend,
    total_ads_spend_all,
    ROUND(total_mex_ads_spend * 100.0 / NULLIF(total_ads_spend_all, 0), 2) as mex_funded_ads_pct,
    ROUND((total_ads_spend_all - total_mex_ads_spend) * 100.0 / NULLIF(total_ads_spend_all, 0), 2) as grab_funded_ads_pct,
    total_attributed_orders,
    total_attributed_gmv,
    total_clicks,
    total_impressions,
    -- Calculate participation rate
    ROUND(merchants_in_ads * 100.0 / NULLIF((SELECT COUNT(*) FROM t20_t3_merchants), 0), 2) as participation_rate_pct,
    LAG(merchants_in_ads) OVER (ORDER BY month_id) as prev_month_merchants,
    merchants_in_ads - LAG(merchants_in_ads) OVER (ORDER BY month_id) as merchant_change,
    ROUND((merchants_in_ads - LAG(merchants_in_ads) OVER (ORDER BY month_id)) * 100.0 / 
          NULLIF(LAG(merchants_in_ads) OVER (ORDER BY month_id), 0), 2) as merchant_change_pct
FROM merchant_ads_participation
ORDER BY month_id;

-- ============================================================================
-- PART 3: COMBINED PROMO + ADS PARTICIPATION
-- Merchants participating in either promo or ads
-- ============================================================================

WITH t20_t3_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )
),
promo_merchants AS (
    SELECT DISTINCT
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        merchant_id
    FROM ocd_adw.f_food_discount
    WHERE city_id = 13
        AND date_id >= 20250501
        AND date_id < 20251101
        AND booking_state_simple = 'COMPLETED'
        AND is_mfp = TRUE
        AND (COALESCE(total_mex_promo_spend, 0) + COALESCE(total_grab_promo_spend, 0)) > 0
        AND merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
),
ads_merchants AS (
    SELECT DISTINCT
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        merchant_id
    FROM ocd_adw.agg_ads_merchant
    WHERE date_id >= 20250501
        AND date_id < 20251101
        AND COALESCE(accrued_amount_before_tax_local, 0) > 0
        AND merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
),
combined_participation AS (
    SELECT 
        COALESCE(p.month_id, a.month_id) as month_id,
        COUNT(DISTINCT p.merchant_id) as merchants_in_promo,
        COUNT(DISTINCT a.merchant_id) as merchants_in_ads,
        COUNT(DISTINCT COALESCE(p.merchant_id, a.merchant_id)) as merchants_in_either,
        COUNT(DISTINCT CASE WHEN p.merchant_id IS NOT NULL AND a.merchant_id IS NOT NULL 
                           THEN COALESCE(p.merchant_id, a.merchant_id) END) as merchants_in_both
    FROM promo_merchants p
    FULL OUTER JOIN ads_merchants a
        ON p.month_id = a.month_id AND p.merchant_id = a.merchant_id
    GROUP BY COALESCE(p.month_id, a.month_id)
)
SELECT 
    month_id,
    merchants_in_promo,
    merchants_in_ads,
    merchants_in_either,
    merchants_in_both,
    ROUND(merchants_in_either * 100.0 / NULLIF((SELECT COUNT(*) FROM t20_t3_merchants), 0), 2) as combined_participation_rate_pct,
    ROUND(merchants_in_both * 100.0 / NULLIF((SELECT COUNT(*) FROM t20_t3_merchants), 0), 2) as both_participation_rate_pct,
    LAG(merchants_in_either) OVER (ORDER BY month_id) as prev_month_combined,
    merchants_in_either - LAG(merchants_in_either) OVER (ORDER BY month_id) as combined_change,
    ROUND((merchants_in_either - LAG(merchants_in_either) OVER (ORDER BY month_id)) * 100.0 / 
          NULLIF(LAG(merchants_in_either) OVER (ORDER BY month_id), 0), 2) as combined_change_pct
FROM combined_participation
ORDER BY month_id;

-- ============================================================================
-- PART 4: CAMPAIGN TYPE BREAKDOWN (Hotdeals, Delivery Campaigns)
-- Identify campaign types from d_merchant_funded_campaign
-- ============================================================================

SELECT DISTINCT
    campaign_type,
    COUNT(*) as campaign_count,
    COUNT(DISTINCT merchant_id) as merchant_count,
    COUNT(DISTINCT CASE WHEN mexfunded_ratio > 0 THEN merchant_id END) as mex_funded_merchants,
    COUNT(DISTINCT CASE WHEN mexfunded_ratio = 0 OR mexfunded_ratio IS NULL THEN merchant_id END) as grab_funded_merchants
FROM ocd_adw.d_merchant_funded_campaign
WHERE city_id = 13
    AND CAST(start_time AS DATE) >= DATE '2025-05-01'
    AND CAST(start_time AS DATE) < DATE '2025-11-01'
GROUP BY campaign_type
ORDER BY campaign_count DESC
LIMIT 20;


