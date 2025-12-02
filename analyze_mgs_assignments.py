"""
Analyze MGS Assignments from User List
Count merchants per MGS and prepare for impact analysis
"""

import json
from collections import Counter

# MGS names from user list
mgs_list = [
    'Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Hon Yi Ni',
    'Low Jia Ying', 'Lee Sook Chin', 'Lee Sook Chin', 'Hon Yi Ni', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Lee Sook Chin', 'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Low Jia Ying', 'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Low Jia Ying', 'Low Jia Ying', 'Low Jia Ying',
    'Teoh Jun Ling', 'Low Jia Ying', 'Low Jia Ying', 'Low Jia Ying', 'Lee Sook Chin',
    'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling',
    'Hon Yi Ni', 'Teoh Jun Ling', 'Lee Sook Chin', 'Hon Yi Ni', 'Lee Sook Chin',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Hon Yi Ni', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Low Jia Ying', 'Teoh Jun Ling', 'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Lee Sook Chin', 'Low Jia Ying', 'Teoh Jun Ling', 'Lee Sook Chin',
    'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni',
    'Teoh Jun Ling', 'Lee Sook Chin', 'Teoh Jun Ling', 'Low Jia Ying', 'Lee Sook Chin',
    'Lee Sook Chin', 'Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Hon Yi Ni',
    'Teoh Jun Ling', 'Lee Sook Chin', 'Low Jia Ying', 'Hon Yi Ni', 'Low Jia Ying',
    'Low Jia Ying', 'Low Jia Ying', 'Low Jia Ying', 'Teoh Jun Ling', 'Low Jia Ying',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Low Jia Ying', 'Lee Sook Chin', 'Low Jia Ying',
    'Hon Yi Ni', 'Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Hon Yi Ni',
    'Teoh Jun Ling', 'Low Jia Ying', 'Low Jia Ying', 'Teoh Jun Ling', 'Low Jia Ying',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin',
    'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Low Jia Ying',
    'Teoh Jun Ling', 'Low Jia Ying', 'Lee Sook Chin', 'Hon Yi Ni', 'Low Jia Ying',
    'Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Low Jia Ying', 'Hon Yi Ni',
    'Low Jia Ying', 'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Hon Yi Ni', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni',
    'Low Jia Ying', 'Teoh Jun Ling', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Low Jia Ying', 'Hon Yi Ni',
    'Low Jia Ying', 'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin',
    'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin',
    'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Low Jia Ying', 'Low Jia Ying',
    'Lee Sook Chin', 'Hon Yi Ni', 'Teoh Jun Ling', 'Hon Yi Ni', 'Low Jia Ying',
    'Low Jia Ying', 'Lee Sook Chin', 'Hon Yi Ni', 'Teoh Jun Ling', 'Lee Sook Chin',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Low Jia Ying', 'Lee Sook Chin', 'Lee Sook Chin', 'Hon Yi Ni', 'Hon Yi Ni',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin', 'Hon Yi Ni', 'Lee Sook Chin',
    'Teoh Jun Ling', 'Hon Yi Ni', 'Low Jia Ying', 'Lee Sook Chin', 'Lee Sook Chin',
    'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni', 'Hon Yi Ni',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Lee Sook Chin', 'Hon Yi Ni', 'Lee Sook Chin',
    'Hon Yi Ni', 'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Low Jia Ying',
    'Hon Yi Ni', 'Teoh Jun Ling', 'Low Jia Ying', 'Hon Yi Ni', 'Low Jia Ying',
    'Lee Sook Chin', 'Low Jia Ying', 'Low Jia Ying', 'Teoh Jun Ling', 'Lee Sook Chin',
    'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin', 'Low Jia Ying', 'Hon Yi Ni',
    'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling', 'Low Jia Ying', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Low Jia Ying', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Low Jia Ying', 'Teoh Jun Ling', 'Low Jia Ying', 'Low Jia Ying', 'Lee Sook Chin',
    'Hon Yi Ni', 'Lee Sook Chin', 'Lee Sook Chin', 'Low Jia Ying', 'Low Jia Ying',
    'Lee Sook Chin', 'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni', 'Low Jia Ying',
    'Lee Sook Chin', 'Low Jia Ying', 'Lee Sook Chin', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin',
    'Lee Sook Chin', 'Hon Yi Ni', 'Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni',
    'Low Jia Ying', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Low Jia Ying',
    'Low Jia Ying', 'Low Jia Ying', 'Lee Sook Chin', 'Hon Yi Ni', 'Lee Sook Chin',
    'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Low Jia Ying', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Low Jia Ying', 'Teoh Jun Ling', 'Low Jia Ying', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Low Jia Ying',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin',
    'Teoh Jun Ling', 'Low Jia Ying', 'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Low Jia Ying',
    'Teoh Jun Ling', 'Lee Sook Chin', 'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin',
    'Low Jia Ying', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Low Jia Ying',
    'Lee Sook Chin', 'Low Jia Ying', 'Teoh Jun Ling', 'Low Jia Ying', 'Lee Sook Chin',
    'Low Jia Ying', 'Hon Yi Ni', 'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Hon Yi Ni', 'Low Jia Ying', 'Hon Yi Ni', 'Low Jia Ying', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Low Jia Ying', 'Hon Yi Ni', 'Hon Yi Ni', 'Low Jia Ying',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Low Jia Ying', 'Hon Yi Ni', 'Teoh Jun Ling', 'Low Jia Ying', 'Hon Yi Ni',
    'Low Jia Ying', 'Lee Sook Chin', 'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin',
    'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Hon Yi Ni',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Lee Sook Chin', 'Low Jia Ying', 'Low Jia Ying',
    'Low Jia Ying', 'Low Jia Ying', 'Low Jia Ying', 'Teoh Jun Ling', 'Teoh Jun Ling',
    'Teoh Jun Ling', 'Low Jia Ying', 'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Low Jia Ying', 'Low Jia Ying', 'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin',
    'Hon Yi Ni', 'Hon Yi Ni', 'Lee Sook Chin', 'Lee Sook Chin', 'Hon Yi Ni',
    'Hon Yi Ni', 'Low Jia Ying', 'Low Jia Ying', 'Lee Sook Chin', 'Teoh Jun Ling',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin',
    'Lee Sook Chin', 'Teoh Jun Ling', 'Lee Sook Chin', 'Lee Sook Chin', 'Lee Sook Chin',
    'Low Jia Ying', 'Low Jia Ying', 'Teoh Jun Ling', 'Lee Sook Chin'
]

# Count merchants per MGS
from collections import Counter
mgs_counts = Counter(mgs_list)

print("="*80)
print("MGS ASSIGNMENT ANALYSIS")
print("="*80)
print(f"\nTotal merchants in list: {len(mgs_list)}")
print(f"\nMGS Distribution:")
for mgs, count in mgs_counts.most_common():
    print(f"  {mgs}: {count} merchants")

# Save to JSON for query generation
mgs_assignments = {
    'total_merchants': len(mgs_list),
    'mgs_counts': dict(mgs_counts),
    'mgs_list': mgs_list
}

with open('mgs_assignments.json', 'w', encoding='utf-8') as f:
    json.dump(mgs_assignments, f, indent=2, ensure_ascii=False)

print(f"\n[OK] Saved MGS assignments to: mgs_assignments.json")
print("\n[INFO] Note: This list appears to be merchant-to-MGS assignments")
print("       To query impact, we need to match these with merchant IDs from the database")

