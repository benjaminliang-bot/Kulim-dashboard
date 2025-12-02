"""
Query Revenue Breakdown by Individual (AM & MGS)
Last 6 Months (May 2025 - October 2025)

Revenue Sources:
1. Gross billing revenue from commission (deliveries, or dine out)
2. Revenue from ads or spotlight
3. MEX funded campaign

Includes: All ranked individuals + Hsin Tsi Lim
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

# AM assignments (from previous analysis - need to query from d_merchant)
# We'll query these from d_merchant by am_name
am_names = {
    'Darren': 'darren@grabtaxi.com',  # Need to verify actual email
    'Suki': 'suki@grabtaxi.com',      # Need to verify actual email
    'Chia Yee': 'chiayee@grabtaxi.com', # Need to verify actual email
    'Hsin Tsi Lim': 'hsintsi.lim@grabtaxi.com'
}

print("\nGenerating revenue breakdown queries...")

# Generate SQL query for each individual
sql_queries = []

# ============================================================================
# PART 1: Get merchant IDs for AMs (including Hsin Tsi Lim)
# ============================================================================

am_merchant_query = """
-- ============================================================================
-- GET MERCHANT IDs FOR AMs (including Hsin Tsi Lim)
-- ============================================================================

SELECT 
    am_name,
    COUNT(DISTINCT merchant_id_nk) as merchant_count,
    LISTAGG(DISTINCT merchant_id_nk, ', ') WITHIN GROUP (ORDER BY merchant_id_nk) as merchant_ids
FROM ocd_adw.d_merchant
WHERE city_id = 13
    AND country_id = 1
    AND am_name IN (
        'darren@grabtaxi.com',
        'suki@grabtaxi.com', 
        'chiayee@grabtaxi.com',
        'hsintsi.lim@grabtaxi.com'
    )
GROUP BY am_name
ORDER BY merchant_count DESC;
"""

sql_queries.append(("Get AM Merchant IDs", am_merchant_query))

# ============================================================================
# PART 2: Revenue Breakdown Query Template
# ============================================================================

def generate_revenue_breakdown_query(person_name, merchant_ids, role):
    """Generate revenue breakdown query for a person"""
    
    # Format merchant IDs for IN clause
    merchant_id_list = ",\n        ".join([f"'{mid}'" for mid in merchant_ids[:1000]])  # Limit to avoid query size
    
    query = f"""
-- ============================================================================
-- REVENUE BREAKDOWN: {person_name} ({role})
-- Last 6 Months (May 2025 - October 2025)
-- ============================================================================

WITH {person_name.lower().replace(' ', '_')}_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES {merchant_id_list}
    ) AS t(merchant_id_nk)
),
-- 1. COMMISSION REVENUE (from deliveries/dine out)
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
        END) as orders
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.merchant_id IN (SELECT merchant_id_nk FROM {person_name.lower().replace(' ', '_')}_merchants)
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- 2. ADS/SPOTLIGHT REVENUE
ads_revenue AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(COALESCE(accrued_amount_before_tax_local, 0)) as ads_revenue,
        SUM(COALESCE(billable_ad_spend_local, 0)) as total_ads_spend,
        SUM(COALESCE(mex_prorated_billable_ad_spend_local, 0)) as mex_ads_spend
    FROM ocd_adw.agg_ads_merchant
    WHERE date_id >= 20250501
        AND date_id < 20251101
        AND merchant_id IN (SELECT merchant_id_nk FROM {person_name.lower().replace(' ', '_')}_merchants)
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- 3. MEX FUNDED CAMPAIGN REVENUE (spending)
mex_campaign_spend AS (
    SELECT 
        CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(COALESCE(total_mex_promo_spend, 0)) as mex_campaign_spend,
        SUM(COALESCE(total_grab_promo_spend, 0)) as grab_campaign_spend,
        COUNT(DISTINCT merchant_id) as merchants_with_campaigns,
        COUNT(DISTINCT order_id) as campaign_orders
    FROM ocd_adw.f_food_discount
    WHERE city_id = 13
        AND date_id >= 20250501
        AND date_id < 20251101
        AND booking_state_simple = 'COMPLETED'
        AND is_mfp = TRUE
        AND merchant_id IN (SELECT merchant_id_nk FROM {person_name.lower().replace(' ', '_')}_merchants)
    GROUP BY CAST(SUBSTRING(CAST(date_id AS VARCHAR), 1, 6) AS INTEGER)
),
-- Combine all revenue sources
combined_revenue AS (
    SELECT 
        COALESCE(c.month_id, a.month_id, m.month_id) as month_id,
        COALESCE(c.commission_revenue, 0) as commission_revenue,
        COALESCE(c.gmv, 0) as gmv,
        COALESCE(c.orders, 0) as orders,
        COALESCE(a.ads_revenue, 0) as ads_revenue,
        COALESCE(a.total_ads_spend, 0) as total_ads_spend,
        COALESCE(a.mex_ads_spend, 0) as mex_ads_spend,
        COALESCE(m.mex_campaign_spend, 0) as mex_campaign_spend,
        COALESCE(m.grab_campaign_spend, 0) as grab_campaign_spend,
        COALESCE(m.merchants_with_campaigns, 0) as merchants_with_campaigns,
        COALESCE(m.campaign_orders, 0) as campaign_orders
    FROM commission_revenue c
    FULL OUTER JOIN ads_revenue a ON c.month_id = a.month_id
    FULL OUTER JOIN mex_campaign_spend m ON COALESCE(c.month_id, a.month_id) = m.month_id
)
SELECT 
    month_id,
    '{person_name}' as person_name,
    '{role}' as role,
    commission_revenue,
    ads_revenue,
    mex_campaign_spend,
    (commission_revenue + ads_revenue) as total_revenue,
    gmv,
    orders,
    -- Calculate percentages
    ROUND(commission_revenue * 100.0 / NULLIF((commission_revenue + ads_revenue), 0), 2) as commission_revenue_pct,
    ROUND(ads_revenue * 100.0 / NULLIF((commission_revenue + ads_revenue), 0), 2) as ads_revenue_pct,
    -- Additional metrics
    total_ads_spend,
    mex_ads_spend,
    grab_campaign_spend,
    merchants_with_campaigns,
    campaign_orders
FROM combined_revenue
ORDER BY month_id;
"""
    return query

# Generate queries for MGSs
for mgs_name, merchant_ids in mgs_assignments.items():
    query = generate_revenue_breakdown_query(mgs_name, merchant_ids, 'MGS')
    sql_queries.append((f"Revenue Breakdown: {mgs_name}", query))

# Generate queries for AMs (will need merchant IDs from query)
for am_name, email in am_names.items():
    # Placeholder - will be filled after getting merchant IDs
    query = f"""
-- ============================================================================
-- REVENUE BREAKDOWN: {am_name} (AM)
-- Note: Run Part 1 query first to get merchant IDs, then update this query
-- ============================================================================

-- TODO: Replace merchant_ids with actual IDs from Part 1 query
SELECT 
    'Run Part 1 query first to get merchant IDs for {am_name}' as note;
"""
    sql_queries.append((f"Revenue Breakdown: {am_name} (Template)", query))

# ============================================================================
# PART 3: Combined Summary Query
# ============================================================================

summary_query = """
-- ============================================================================
-- COMBINED REVENUE SUMMARY (All Individuals)
-- ============================================================================

-- This will combine results from all individual queries
-- Run all individual queries first, then combine results

SELECT 
    'Run individual queries first, then combine results' as note;
"""

sql_queries.append(("Combined Summary", summary_query))

# Save all queries to file
output_file = 'query_revenue_breakdown_all_individuals.sql'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("-- ============================================================================\n")
    f.write("-- REVENUE BREAKDOWN BY INDIVIDUAL (AM & MGS)\n")
    f.write("-- Last 6 Months (May 2025 - October 2025)\n")
    f.write("-- ============================================================================\n\n")
    
    for i, (query_name, query) in enumerate(sql_queries, 1):
        f.write(f"\n-- ============================================================================\n")
        f.write(f"-- QUERY {i}: {query_name}\n")
        f.write(f"-- ============================================================================\n\n")
        f.write(query)
        f.write("\n\n")

print(f"\n[OK] Generated {len(sql_queries)} queries")
print(f"[OK] Saved to: {output_file}")
print("\n[INFO] Next steps:")
print("  1. Run Part 1 query to get AM merchant IDs")
print("  2. Update AM revenue queries with actual merchant IDs")
print("  3. Run all individual revenue breakdown queries")
print("  4. Combine results for final summary")



