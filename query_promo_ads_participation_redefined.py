"""
Query T3/T20 Promotion and Ads Participation (Redefined)
Last 6 Months (May 2025 - October 2025)

Redefinition:
1. Promotion: If promotion spending > 0, then merchant is in promo
   - Track MFP campaigns (hotdeals and delivery campaigns)
   - Identify Grab-funded vs MEX-funded

2. Ads: If ads revenue > 0, then merchant is in ads
   - Identify Grab-funded vs MEX-funded
"""

import json
from datetime import datetime

# Load T20/T3 merchant IDs
with open('t20_merchant_ids.json', 'r') as f:
    t20_merchant_ids = json.load(f)

with open('t3_merchant_ids.json', 'r') as f:
    t3_merchant_ids = json.load(f)

# Combine and deduplicate (T3 is subset of T20)
all_t20_t3_ids = list(set(t20_merchant_ids))
print(f"Total T20/T3 merchants: {len(all_t20_t3_ids)}")

# Generate SQL queries
sql_queries = []

# ============================================================================
# PART 1: PROMOTION PARTICIPATION
# Based on: total_mex_promo_spend > 0 OR total_grab_promo_spend > 0
# Filter: is_mfp = TRUE (MFP campaigns - hotdeals, delivery campaigns)
# ============================================================================

promo_participation_query = f"""
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
        AND merchant_id_nk IN ({','.join([f"'{mid}'" for mid in all_t20_t3_ids[:100]])})  -- Sample first 100 for testing
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
"""

sql_queries.append(("Promotion Participation (MFP Campaigns)", promo_participation_query))

# ============================================================================
# PART 2: CAMPAIGN TYPE BREAKDOWN (Hotdeals, Delivery Campaigns)
# Need to identify campaign types from d_merchant_funded_campaign or f_food_discount
# ============================================================================

campaign_type_query = """
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
"""

sql_queries.append(("Campaign Type Breakdown", campaign_type_query))

# ============================================================================
# PART 3: ADS REVENUE PARTICIPATION
# Definition: If ads revenue > 0, then merchant is in ads
# Need to identify the correct table for ads revenue
# ============================================================================

# Note: Ads revenue table needs to be identified
# Potential tables: f_food_metrics, merchant advertising tables
ads_revenue_query = """
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
"""

sql_queries.append(("Ads Revenue Participation (TODO)", ads_revenue_query))

# ============================================================================
# PART 4: COMBINED PROMO + ADS PARTICIPATION
# ============================================================================

combined_query = """
-- ============================================================================
-- COMBINED PROMO + ADS PARTICIPATION
-- Merchants participating in either promo or ads
-- ============================================================================

-- Will be completed once ads revenue table is identified
SELECT 
    'Combined analysis pending ads revenue table identification' as note;
"""

sql_queries.append(("Combined Promo + Ads", combined_query))

# Save queries to file
with open('query_promo_ads_redefined.sql', 'w', encoding='utf-8') as f:
    f.write("-- T3/T20 Promotion and Ads Participation (Redefined)\n")
    f.write("-- Last 6 Months (May 2025 - October 2025)\n")
    f.write("-- Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    
    for title, query in sql_queries:
        f.write(f"\n-- ============================================================================\n")
        f.write(f"-- {title}\n")
        f.write(f"-- ============================================================================\n\n")
        f.write(query)
        f.write("\n\n")

print(f"\n[OK] Generated SQL queries saved to: query_promo_ads_redefined.sql")
print(f"\n[INFO] Query Summary:")
for i, (title, _) in enumerate(sql_queries, 1):
    print(f"   {i}. {title}")

print(f"\n[WARNING] Next Steps:")
print(f"   1. Identify ads revenue table")
print(f"   2. Identify campaign types for hotdeals and delivery campaigns")
print(f"   3. Update queries with full T20/T3 merchant list (currently using sample of 100)")

