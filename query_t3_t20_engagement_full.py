"""
Full analysis of T3/T20 engagement metrics for last 6 months
"""

import json
from datetime import datetime

# Load merchant lists
with open('t20_merchant_ids.json', 'r') as f:
    t20_ids = json.load(f)

with open('t3_merchant_ids.json', 'r') as f:
    t3_ids = json.load(f)

# Combine T20 and T3 (T3 is subset of T20)
all_t20_t3_ids = list(set(t20_ids + t3_ids))

print("="*80)
print("T3/T20 ENGAGEMENT ANALYSIS - QUERY STRUCTURE")
print("="*80)
print(f"T20 merchants: {len(t20_ids)}")
print(f"T3 merchants: {len(t3_ids)}")
print(f"Total unique T20/T3: {len(all_t20_t3_ids)}")
print()

# Generate SQL queries
print("="*80)
print("SQL QUERIES FOR ENGAGEMENT ANALYSIS")
print("="*80)

# Query 1: DoD Participation from pre_purchased_deals_base
print("\n1. DoD Participation % (analytics_food.pre_purchased_deals_base):")
print("   - Period: Last 6 months (May 2025 - Oct 2025)")
print("   - Filter: city_name = 'Penang'")
print("   - Filter: merchant_id IN (T20/T3 merchant IDs)")
print()

# Query 2: DoD Participation from f_food_prepurchased_deals
print("2. DoD Participation % (ocd_adw.f_food_prepurchased_deals):")
print("   - Period: Last 6 months (date_id: 20250501 - 20251031)")
print("   - Filter: city_id = 13")
print("   - Filter: merchant_id IN (T20/T3 merchant IDs)")
print("   - Filter: order_state_simple = 'COMPLETED'")
print()

# Query 3: Merchant Tagging
print("3. Merchant Tagging/Engagement Rate:")
print("   - Check: d_merchant.am_name field")
print("   - Filter: city_id = 13")
print("   - Filter: merchant_id_nk IN (T20/T3 merchant IDs)")
print()

# Save merchant IDs for queries (first 100 for testing)
sample_ids = all_t20_t3_ids[:100]
with open('t20_t3_sample_ids.json', 'w') as f:
    json.dump(sample_ids, f, indent=2)

print(f"Sample merchant IDs (first 100) saved for testing")
print(f"Full list: {len(all_t20_t3_ids)} merchants")


