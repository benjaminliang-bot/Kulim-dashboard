"""
Execute Promotion and Ads Participation Queries
"""

import json
import re

# Load merchant IDs
with open('t20_merchant_ids.json', 'r') as f:
    t20_merchant_ids = json.load(f)

print(f"Loaded {len(t20_merchant_ids)} T20/T3 merchant IDs")

# Read the SQL file
with open('query_promo_ads_redefined_final.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Extract Part 1: Promotion Participation
# Find the section between "-- PART 1:" and "-- PART 2:"
part1_match = re.search(r'-- PART 1:.*?(?=-- PART 2:)', sql_content, re.DOTALL)
if part1_match:
    part1_query = part1_match.group(0).replace('-- PART 1:', '').strip()
    # Remove the comment lines
    part1_query = re.sub(r'^--.*$', '', part1_query, flags=re.MULTILINE)
    part1_query = '\n'.join([line for line in part1_query.split('\n') if line.strip()])
    
    print("\n" + "="*80)
    print("PART 1: PROMOTION PARTICIPATION QUERY")
    print("="*80)
    print(part1_query[:500] + "...")
    print("\n[INFO] Query ready to execute")
    print("[INFO] This query analyzes MFP campaigns (hotdeals, delivery campaigns)")
    print("[INFO] With Grab-funded vs MEX-funded breakdown")
    
    # Save Part 1 query
    with open('query_part1_promo_participation.sql', 'w', encoding='utf-8') as f:
        f.write(part1_query)
    print(f"\n[OK] Saved to: query_part1_promo_participation.sql")

# Extract Part 2: Ads Revenue Participation
part2_match = re.search(r'-- PART 2:.*?(?=-- PART 3:)', sql_content, re.DOTALL)
if part2_match:
    part2_query = part2_match.group(0).replace('-- PART 2:', '').strip()
    part2_query = re.sub(r'^--.*$', '', part2_query, flags=re.MULTILINE)
    part2_query = '\n'.join([line for line in part2_query.split('\n') if line.strip()])
    
    print("\n" + "="*80)
    print("PART 2: ADS REVENUE PARTICIPATION QUERY")
    print("="*80)
    print(part2_query[:500] + "...")
    print("\n[INFO] Query ready to execute")
    print("[INFO] This query analyzes ads revenue with Grab-funded vs MEX-funded breakdown")
    
    with open('query_part2_ads_participation.sql', 'w', encoding='utf-8') as f:
        f.write(part2_query)
    print(f"\n[OK] Saved to: query_part2_ads_participation.sql")

# Extract Part 3: Combined
part3_match = re.search(r'-- PART 3:.*?(?=-- PART 4:)', sql_content, re.DOTALL)
if part3_match:
    part3_query = part3_match.group(0).replace('-- PART 3:', '').strip()
    part3_query = re.sub(r'^--.*$', '', part3_query, flags=re.MULTILINE)
    part3_query = '\n'.join([line for line in part3_query.split('\n') if line.strip()])
    
    print("\n" + "="*80)
    print("PART 3: COMBINED PROMO + ADS PARTICIPATION QUERY")
    print("="*80)
    print(part3_query[:500] + "...")
    
    with open('query_part3_combined.sql', 'w', encoding='utf-8') as f:
        f.write(part3_query)
    print(f"\n[OK] Saved to: query_part3_combined.sql")

# Extract Part 4: Campaign Type Breakdown
part4_match = re.search(r'-- PART 4:.*?$', sql_content, re.DOTALL)
if part4_match:
    part4_query = part4_match.group(0).replace('-- PART 4:', '').strip()
    part4_query = re.sub(r'^--.*$', '', part4_query, flags=re.MULTILINE)
    part4_query = '\n'.join([line for line in part4_query.split('\n') if line.strip()])
    
    print("\n" + "="*80)
    print("PART 4: CAMPAIGN TYPE BREAKDOWN QUERY")
    print("="*80)
    print(part4_query)
    
    with open('query_part4_campaign_types.sql', 'w', encoding='utf-8') as f:
        f.write(part4_query)
    print(f"\n[OK] Saved to: query_part4_campaign_types.sql")

print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("1. Execute query_part1_promo_participation.sql in Presto/Hubble")
print("2. Execute query_part2_ads_participation.sql in Presto/Hubble")
print("3. Execute query_part3_combined.sql in Presto/Hubble")
print("4. Execute query_part4_campaign_types.sql in Presto/Hubble")
print("\nOr use the MCP Presto query tool to execute them directly.")


