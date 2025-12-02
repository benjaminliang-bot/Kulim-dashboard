-- T3/T20 Promotion and Ads Participation (Redefined)
-- Last 6 Months (May 2025 - October 2025)
-- Generated: 2025-11-07 15:27:50


-- ============================================================================
-- Promotion Participation (MFP Campaigns)
-- ============================================================================


-- ============================================================================
-- PROMOTION PARTICIPATION (Redefined)
-- Definition: If promotion spending > 0, then merchant is in promo
-- Track: MFP campaigns (hotdeals, delivery campaigns)
-- Source: ocd_adw.f_food_discount
-- ============================================================================

WITH t20_t3_merchants AS (
    SELECT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN ('1-CZBFC342UA6UGJ','1-C6VAJ2DACJLTVX','1-CZDTC2LJPEM1ET','1-C6WETEAEJ2DEKA','1-CYVFTENEVN5EVJ','1-C3EELCLYG4KTNA','1-C6CGUCEKNK4JEN','1-CYVVJGKZRK6FME','1-C2KKLTWFTNNCLN','1-C23CE6KJAYEEAA','1-C2U3CU3JEE5ATT','1-C2AEAXJAGLDWA2','1-C2WCLVCEVY3DR2','1-C252G4LCR6JUAA','1-C2EWE7WYRCKCGJ','1-C25DMBE3CNAJJX','1-C3WJJUJKEUDTBE','1-C2AEAXE3VUNEGX','1-C62KMFX1GY3JRE','1-C4EGGX3YHE61R2','1-C2DTLGBZGE6YC2','1-C63WAF6XGPJJTN','1-C3XUR2LVETNVEJ','1-C22EPAA2N3V1G2','1-C2MKUFVJCZD2TX','1-C63VAEDVRXVCVN','1-C2MKWBJ3J35DC6','1-C65JE7TXGYAEG6','1-C4MVC8C3JUBELA','1-CYWUJZCUR6UAC2','1-C4MZUBDANRABRN','1-C2MKUFVJAN2WTN','1-C2AVPADYTEECTA','1-C2DYWA5GAVD2CA','1-C2XWN6NACEEBLX','1-C3XFFA3HWBUTKE','1-C63CJ4NCN7WUJX','1-C2BERJNZV2UUE2','1-C6MCTN4WRPCACE','1-C3EBTUTVA7T3V2','1-CZMBCTBUVUC2SE','1-C4NHHFMCGCAKN6','1-C4KYNYC1RLDXPA','1-C3XVRUJWUFJFNA','1-C2NYTRKCN6MZME','1-C6VAME5GNVJWRN','1-C3LFTNAGTTLCCT','1-C4KYNYCVAN5VGX','1-C25TNGMZNK4CRJ','1-C34UGTKZEBKCEA','1-C2NXE7UJG6TDWE','1-CZLKAUNTSCCZNJ','1-C3EXAE3HJ2TWLE','1-C2WEJNKJE4JKC6','1-C2EHTFL1E7DJAX','1-C65JJTMFJXXHCA','1-C2EBRLEJNPJTJX','1-C62HVTKJLENXLJ','1-CYLZJTAHN2WZUA','1-C65DC66ZTN3XA2','1-C4LVTLAGTEBAPA','1-CY6AGLATCBC2A2','1-C4DJEPC3AGA3BA','1-C3CJFE4AAA2BJN','1-C32FCANZT2KACN','1-C3JEJTK1TYABJE','1-C62BV62FC7NVEE','1-CZDTC2LHV7KTVT','1-C24CTADDCELCDE','1-C2D3JTLDWFDWL2','1-C25KKCMEUGBCJ6','1-C2DXBFMWEJVKN6','1-CZEHHAEXEPNKEA','1-CY4JE8JYRFXZAN','1-CY61NKMVBCEAJX','1-CZLKTLEHC7VUEX','1-C2LWNALGVFEXN2','1-CYTYGGABLBBGGX','1-C3BWN3EVHACYG6','1-C4LVRBJDJLKUT6','1-C6T2CYCWNAXCCA','1-C3NCACEXPCAHAN','1-C6CEFCM3GLKDVT','1-C6VDCRCEALAZR2','1-C3JKJUEBDGN2GT','1-C4KWVEA1E8LWFA','1-C6DATPD1WB41AA','1-C2TAV4CZJBMBPE','1-C2DYTRCJEPL1CT','1-C7BDTABYCLDVKE','1-C3W3VTEVNU4JRN','1-C3KCJX2BLE4VCX','1-C3TXT3V2RKWBET','1-C4LWN72JLBEWLN','1-C242EUEETXU1LN','1-C66KTVJWN4EHL6','1-C6VEA7CEGUAGLX','1-C34XCXAWT3XKT2','1-CYWUJLNYL8CFT6','1-C24ULE2TGUTDGN')  -- Sample first 100 for testing
),
promo_spending_by_month AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        merchant_id,
        -- MEX-funded promo spending
        SUM(CASE WHEN total_mex_promo_spend > 0 THEN total_mex_promo_spend ELSE 0 END) as mex_promo_spend,
        -- Grab-funded promo spending
        SUM(CASE WHEN total_grab_promo_spend > 0 THEN total_grab_promo_spend ELSE 0 END) as grab_promo_spend,
        -- Total promo spending
        SUM(COALESCE(total_mex_promo_spend, 0) + COALESCE(total_grab_promo_spend, 0)) as total_promo_spend,
        -- Campaign type breakdown (for hotdeals, delivery campaigns)
        COUNT(DISTINCT CASE WHEN is_mfp = TRUE THEN mfc_campaign_id END) as mfp_campaigns,
        COUNT(DISTINCT CASE WHEN is_mfc = TRUE THEN mfc_campaign_id END) as mfc_campaigns,
        COUNT(DISTINCT order_id) as promo_orders
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
    total_mfp_campaigns,
    total_promo_orders,
    -- Calculate participation rate (need total T20/T3 count)
    ROUND(merchants_in_promo * 100.0 / NULLIF((SELECT COUNT(*) FROM t20_t3_merchants), 0), 2) as participation_rate_pct,
    LAG(merchants_in_promo) OVER (ORDER BY month_id) as prev_month_merchants,
    merchants_in_promo - LAG(merchants_in_promo) OVER (ORDER BY month_id) as merchant_change,
    ROUND((merchants_in_promo - LAG(merchants_in_promo) OVER (ORDER BY month_id)) * 100.0 / 
          NULLIF(LAG(merchants_in_promo) OVER (ORDER BY month_id), 0), 2) as merchant_change_pct
FROM merchant_promo_participation
ORDER BY month_id;



-- ============================================================================
-- Campaign Type Breakdown
-- ============================================================================


-- ============================================================================
-- CAMPAIGN TYPE BREAKDOWN
-- Identify hotdeals and delivery campaigns
-- Source: ocd_adw.d_merchant_funded_campaign (campaign_type, merchant_campaign_name)
-- ============================================================================

SELECT DISTINCT
    campaign_type,
    COUNT(*) as campaign_count,
    COUNT(DISTINCT merchant_id) as merchant_count
FROM ocd_adw.d_merchant_funded_campaign
WHERE city_id = 13
    AND CAST(start_time AS DATE) >= DATE '2025-05-01'
    AND CAST(start_time AS DATE) < DATE '2025-11-01'
GROUP BY campaign_type
ORDER BY campaign_count DESC
LIMIT 20;



-- ============================================================================
-- Ads Revenue Participation (TODO)
-- ============================================================================


-- ============================================================================
-- ADS REVENUE PARTICIPATION (Placeholder)
-- Definition: If ads revenue > 0, then merchant is in ads
-- TODO: Identify correct table for ads revenue
-- Potential sources:
--   - ocd_adw.f_food_metrics (check for ads-related metrics)
--   - Merchant advertising/spending tables
-- ============================================================================

-- This query structure will be updated once ads revenue table is identified
SELECT 
    'Ads revenue table needs to be identified' as note;



-- ============================================================================
-- Combined Promo + Ads
-- ============================================================================


-- ============================================================================
-- COMBINED PROMO + ADS PARTICIPATION
-- Merchants participating in either promo or ads
-- ============================================================================

-- Will be completed once ads revenue table is identified
SELECT 
    'Combined analysis pending ads revenue table identification' as note;


