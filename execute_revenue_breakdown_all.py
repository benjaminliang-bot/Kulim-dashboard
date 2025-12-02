"""
Execute Revenue Breakdown for All Individuals
Uses am_name filtering for AMs (more efficient than merchant ID lists)
"""

import json
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load MGS assignments
print("Loading MGS assignments...")
with open('mgs_merchant_assignments.json', 'r', encoding='utf-8') as f:
    mgs_assignments = json.load(f)

# AM email mappings (actual emails found in database)
am_mappings = {
    'Darren': 'darren.ng@grabtaxi.com',
    'Suki': 'suki.teoh@grabtaxi.com',
    'Chia Yee': 'chiayee.leong@grabtaxi.com',
    'Hsin Tsi Lim': None  # Not found in database - will need manual check
}

print("\nAM Mappings:")
for am_name, email in am_mappings.items():
    if email:
        print(f"  {am_name}: {email}")
    else:
        print(f"  {am_name}: NOT FOUND in database")

# Generate revenue breakdown query using am_name filter (more efficient)
def generate_am_revenue_query(am_name, am_email):
    """Generate revenue breakdown query for AM using am_name filter"""
    
    if not am_email:
        return None
    
    person_var = am_name.lower().replace(' ', '_').replace('.', '_')
    
    query = f"""
-- ============================================================================
-- REVENUE BREAKDOWN: {am_name} (AM)
-- Last 6 Months (May 2025 - October 2025)
-- Filtered by: am_name = '{am_email}'
-- ============================================================================

WITH {person_var}_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND am_name = '{am_email}'
),
-- 1. COMMISSION REVENUE (Gross billing from deliveries/dine out)
commission_revenue AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.commission_from_merchant, 0) 
            ELSE 0 
        END) as commission_revenue,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as gmv,
        COUNT(DISTINCT CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN f.order_id 
        END) as orders,
        COUNT(DISTINCT CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN f.merchant_id 
        END) as active_merchants
    FROM ocd_adw.f_food_metrics f
    INNER JOIN {person_var}_merchants m ON f.merchant_id = m.merchant_id_nk
    WHERE f.city_id = 13
        AND f.business_type = 0
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- 2. ADS/SPOTLIGHT REVENUE (Grab's revenue from ads)
ads_revenue AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(COALESCE(accrued_amount_before_tax_local, 0)) as ads_revenue,
        SUM(COALESCE(billable_ad_spend_local, 0)) as total_ads_spend,
        SUM(COALESCE(mex_prorated_billable_ad_spend_local, 0)) as mex_ads_spend,
        COUNT(DISTINCT merchant_id) as merchants_in_ads
    FROM ocd_adw.agg_ads_merchant a
    INNER JOIN {person_var}_merchants m ON a.merchant_id = m.merchant_id_nk
    WHERE date_id >= 20250501
        AND date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- 3. MEX FUNDED CAMPAIGN SPENDING (MEX-funded promotional campaigns)
mex_campaign_spend AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(COALESCE(total_mex_promo_spend, 0)) as mex_campaign_spend,
        SUM(COALESCE(total_grab_promo_spend, 0)) as grab_campaign_spend,
        COUNT(DISTINCT merchant_id) as merchants_with_campaigns,
        COUNT(DISTINCT order_id) as campaign_orders,
        COUNT(DISTINCT mfc_campaign_id) as unique_campaigns
    FROM ocd_adw.f_food_discount d
    INNER JOIN {person_var}_merchants m ON d.merchant_id = m.merchant_id_nk
    WHERE d.city_id = 13
        AND d.date_id >= 20250501
        AND d.date_id < 20251101
        AND d.booking_state_simple = 'COMPLETED'
        AND d.is_mfp = TRUE
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- Combine all revenue sources
combined_revenue AS (
    SELECT 
        COALESCE(c.month_id, a.month_id, m.month_id) as month_id,
        COALESCE(c.commission_revenue, 0) as commission_revenue,
        COALESCE(c.gmv, 0) as gmv,
        COALESCE(c.orders, 0) as orders,
        COALESCE(c.active_merchants, 0) as active_merchants,
        COALESCE(a.ads_revenue, 0) as ads_revenue,
        COALESCE(a.total_ads_spend, 0) as total_ads_spend,
        COALESCE(a.mex_ads_spend, 0) as mex_ads_spend,
        COALESCE(a.merchants_in_ads, 0) as merchants_in_ads,
        COALESCE(m.mex_campaign_spend, 0) as mex_campaign_spend,
        COALESCE(m.grab_campaign_spend, 0) as grab_campaign_spend,
        COALESCE(m.merchants_with_campaigns, 0) as merchants_with_campaigns,
        COALESCE(m.campaign_orders, 0) as campaign_orders,
        COALESCE(m.unique_campaigns, 0) as unique_campaigns
    FROM commission_revenue c
    FULL OUTER JOIN ads_revenue a ON c.month_id = a.month_id
    FULL OUTER JOIN mex_campaign_spend m ON COALESCE(c.month_id, a.month_id) = m.month_id
)
SELECT 
    month_id,
    '{am_name}' as person_name,
    'AM' as role,
    commission_revenue,
    ads_revenue,
    mex_campaign_spend,
    (commission_revenue + ads_revenue) as total_revenue,
    gmv,
    orders,
    active_merchants,
    -- Calculate percentages of total revenue
    ROUND(commission_revenue * 100.0 / NULLIF((commission_revenue + ads_revenue), 0), 2) as commission_revenue_pct,
    ROUND(ads_revenue * 100.0 / NULLIF((commission_revenue + ads_revenue), 0), 2) as ads_revenue_pct,
    -- Additional metrics
    total_ads_spend,
    mex_ads_spend,
    grab_campaign_spend,
    merchants_in_ads,
    merchants_with_campaigns,
    campaign_orders,
    unique_campaigns
FROM combined_revenue
ORDER BY month_id;
"""
    return query

# Generate MGS revenue query (using merchant IDs)
def generate_mgs_revenue_query(mgs_name, merchant_ids):
    """Generate revenue breakdown query for MGS using merchant IDs"""
    
    if not merchant_ids:
        return None
    
    # Format merchant IDs (limit to avoid query size issues)
    merchant_id_values = ",\n        ".join([f"('{mid}')" for mid in merchant_ids[:1000]])
    person_var = mgs_name.lower().replace(' ', '_').replace('.', '_')
    
    query = f"""
-- ============================================================================
-- REVENUE BREAKDOWN: {mgs_name} (MGS)
-- Last 6 Months (May 2025 - October 2025)
-- Portfolio: {len(merchant_ids)} merchants
-- ============================================================================

WITH {person_var}_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES {merchant_id_values}
    ) AS t(merchant_id_nk)
),
-- 1. COMMISSION REVENUE (Gross billing from deliveries/dine out)
commission_revenue AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.commission_from_merchant, 0) 
            ELSE 0 
        END) as commission_revenue,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as gmv,
        COUNT(DISTINCT CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN f.order_id 
        END) as orders,
        COUNT(DISTINCT CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN f.merchant_id 
        END) as active_merchants
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.business_type = 0
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.merchant_id IN (SELECT merchant_id_nk FROM {person_var}_merchants)
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- 2. ADS/SPOTLIGHT REVENUE (Grab's revenue from ads)
ads_revenue AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(COALESCE(accrued_amount_before_tax_local, 0)) as ads_revenue,
        SUM(COALESCE(billable_ad_spend_local, 0)) as total_ads_spend,
        SUM(COALESCE(mex_prorated_billable_ad_spend_local, 0)) as mex_ads_spend,
        COUNT(DISTINCT merchant_id) as merchants_in_ads
    FROM ocd_adw.agg_ads_merchant
    WHERE date_id >= 20250501
        AND date_id < 20251101
        AND merchant_id IN (SELECT merchant_id_nk FROM {person_var}_merchants)
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- 3. MEX FUNDED CAMPAIGN SPENDING (MEX-funded promotional campaigns)
mex_campaign_spend AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(COALESCE(total_mex_promo_spend, 0)) as mex_campaign_spend,
        SUM(COALESCE(total_grab_promo_spend, 0)) as grab_campaign_spend,
        COUNT(DISTINCT merchant_id) as merchants_with_campaigns,
        COUNT(DISTINCT order_id) as campaign_orders,
        COUNT(DISTINCT mfc_campaign_id) as unique_campaigns
    FROM ocd_adw.f_food_discount
    WHERE city_id = 13
        AND date_id >= 20250501
        AND date_id < 20251101
        AND booking_state_simple = 'COMPLETED'
        AND is_mfp = TRUE
        AND merchant_id IN (SELECT merchant_id_nk FROM {person_var}_merchants)
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- Combine all revenue sources
combined_revenue AS (
    SELECT 
        COALESCE(c.month_id, a.month_id, m.month_id) as month_id,
        COALESCE(c.commission_revenue, 0) as commission_revenue,
        COALESCE(c.gmv, 0) as gmv,
        COALESCE(c.orders, 0) as orders,
        COALESCE(c.active_merchants, 0) as active_merchants,
        COALESCE(a.ads_revenue, 0) as ads_revenue,
        COALESCE(a.total_ads_spend, 0) as total_ads_spend,
        COALESCE(a.mex_ads_spend, 0) as mex_ads_spend,
        COALESCE(a.merchants_in_ads, 0) as merchants_in_ads,
        COALESCE(m.mex_campaign_spend, 0) as mex_campaign_spend,
        COALESCE(m.grab_campaign_spend, 0) as grab_campaign_spend,
        COALESCE(m.merchants_with_campaigns, 0) as merchants_with_campaigns,
        COALESCE(m.campaign_orders, 0) as campaign_orders,
        COALESCE(m.unique_campaigns, 0) as unique_campaigns
    FROM commission_revenue c
    FULL OUTER JOIN ads_revenue a ON c.month_id = a.month_id
    FULL OUTER JOIN mex_campaign_spend m ON COALESCE(c.month_id, a.month_id) = m.month_id
)
SELECT 
    month_id,
    '{mgs_name}' as person_name,
    'MGS' as role,
    commission_revenue,
    ads_revenue,
    mex_campaign_spend,
    (commission_revenue + ads_revenue) as total_revenue,
    gmv,
    orders,
    active_merchants,
    -- Calculate percentages of total revenue
    ROUND(commission_revenue * 100.0 / NULLIF((commission_revenue + ads_revenue), 0), 2) as commission_revenue_pct,
    ROUND(ads_revenue * 100.0 / NULLIF((commission_revenue + ads_revenue), 0), 2) as ads_revenue_pct,
    -- Additional metrics
    total_ads_spend,
    mex_ads_spend,
    grab_campaign_spend,
    merchants_in_ads,
    merchants_with_campaigns,
    campaign_orders,
    unique_campaigns
FROM combined_revenue
ORDER BY month_id;
"""
    return query

# Generate all queries
print("\n" + "="*80)
print("GENERATING REVENUE BREAKDOWN QUERIES")
print("="*80)

queries = []

# Generate AM queries
for am_name, am_email in am_mappings.items():
    if am_email:
        query = generate_am_revenue_query(am_name, am_email)
        if query:
            queries.append((f"Revenue Breakdown: {am_name} (AM)", query))
    else:
        print(f"\n[WARNING] {am_name}: Not found in database - skipping")

# Generate MGS queries
for mgs_name, merchant_ids in mgs_assignments.items():
    query = generate_mgs_revenue_query(mgs_name, merchant_ids)
    if query:
        queries.append((f"Revenue Breakdown: {mgs_name} (MGS)", query))

# Save all queries
output_file = 'query_revenue_breakdown_executable.sql'
print(f"\nSaving {len(queries)} queries to: {output_file}")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("-- ============================================================================\n")
    f.write("-- REVENUE BREAKDOWN BY INDIVIDUAL (AM & MGS) - EXECUTABLE QUERIES\n")
    f.write("-- Last 6 Months (May 2025 - October 2025)\n")
    f.write("-- ============================================================================\n")
    f.write("-- Revenue Sources:\n")
    f.write("--   1. Commission Revenue: Gross billing from commission (deliveries/dine out)\n")
    f.write("--   2. Ads/Spotlight Revenue: Revenue from ads or spotlight\n")
    f.write("--   3. MEX Funded Campaign: MEX-funded promotional campaign spending\n")
    f.write("-- ============================================================================\n\n")
    
    for i, (query_name, query) in enumerate(queries, 1):
        f.write(f"\n-- ============================================================================\n")
        f.write(f"-- QUERY {i}: {query_name}\n")
        f.write(f"-- ============================================================================\n\n")
        f.write(query)
        f.write("\n\n")

print(f"[OK] Generated {len(queries)} executable queries")
print(f"[OK] Saved to: {output_file}")
print("\n[INFO] Ready to execute queries via Presto/Hubble")





