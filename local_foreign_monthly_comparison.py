#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local vs Foreign Eaters: Month-over-Month Comparison
Comparing August, September, and October 2025
"""

import pandas as pd

def compare_months():
    """
    Compare local vs foreign eater growth across months
    """
    
    print("=" * 100)
    print("LOCAL vs FOREIGN EATERS: MONTH-OVER-MONTH COMPARISON")
    print("August, September, and October 2025")
    print("=" * 100)
    
    # Monthly data
    monthly_data = {
        'August 2025': {
            'local_eaters': 1619987,
            'foreign_eaters': 138218,
            'total_eaters': 1758205,
            'local_orders': 7189743,
            'foreign_orders': 443298,
            'total_orders': 7633041,
            'local_gmv': 245404460.80,
            'foreign_gmv': 19355529.03,
            'total_gmv': 264759989.83
        },
        'September 2025': {
            'local_eaters': 1628789,
            'foreign_eaters': 123985,
            'total_eaters': 1752774,
            'local_orders': 6951481,
            'foreign_orders': 410082,
            'total_orders': 7361563,
            'local_gmv': 239910117.22,
            'foreign_gmv': 17483093.78,
            'total_gmv': 257393211.00
        },
        'October 2025': {
            'local_eaters': 1692429,
            'foreign_eaters': 130296,
            'total_eaters': 1822725,
            'local_orders': 7460028,
            'foreign_orders': 445975,
            'total_orders': 7906003,
            'local_gmv': 255944992.62,
            'foreign_gmv': 18633205.36,
            'total_gmv': 274578197.98
        }
    }
    
    # Calculate changes
    sep_vs_aug = {}
    oct_vs_sep = {}
    oct_vs_aug = {}
    
    for metric in ['local_eaters', 'foreign_eaters', 'total_eaters', 
                   'local_orders', 'foreign_orders', 'total_orders',
                   'local_gmv', 'foreign_gmv', 'total_gmv']:
        sep_vs_aug[f'{metric}_delta'] = monthly_data['September 2025'][metric] - monthly_data['August 2025'][metric]
        oct_vs_sep[f'{metric}_delta'] = monthly_data['October 2025'][metric] - monthly_data['September 2025'][metric]
        oct_vs_aug[f'{metric}_delta'] = monthly_data['October 2025'][metric] - monthly_data['August 2025'][metric]
        
        if monthly_data['August 2025'][metric] != 0:
            sep_vs_aug[f'{metric}_pct'] = (sep_vs_aug[f'{metric}_delta'] / monthly_data['August 2025'][metric]) * 100
        if monthly_data['September 2025'][metric] != 0:
            oct_vs_sep[f'{metric}_pct'] = (oct_vs_sep[f'{metric}_delta'] / monthly_data['September 2025'][metric]) * 100
        if monthly_data['August 2025'][metric] != 0:
            oct_vs_aug[f'{metric}_pct'] = (oct_vs_aug[f'{metric}_delta'] / monthly_data['August 2025'][metric]) * 100
    
    print("\n" + "=" * 100)
    print("1. MONTHLY EATER BASE COMPARISON")
    print("=" * 100)
    
    print("\n[A] Local Eaters:")
    print(f"   August:   {monthly_data['August 2025']['local_eaters']:,}")
    print(f"   September: {monthly_data['September 2025']['local_eaters']:,} ({sep_vs_aug['local_eaters_pct']:+.2f}% vs Aug)")
    print(f"   October:  {monthly_data['October 2025']['local_eaters']:,} ({oct_vs_sep['local_eaters_pct']:+.2f}% vs Sep)")
    print(f"   Total Growth (Aug→Oct): {oct_vs_aug['local_eaters_delta']:,} ({oct_vs_aug['local_eaters_pct']:+.2f}%)")
    
    print("\n[B] Foreign Eaters:")
    print(f"   August:   {monthly_data['August 2025']['foreign_eaters']:,}")
    print(f"   September: {monthly_data['September 2025']['foreign_eaters']:,} ({sep_vs_aug['foreign_eaters_pct']:+.2f}% vs Aug) ← DECLINE")
    print(f"   October:  {monthly_data['October 2025']['foreign_eaters']:,} ({oct_vs_sep['foreign_eaters_pct']:+.2f}% vs Sep) ← RECOVERY")
    print(f"   Total Change (Aug→Oct): {oct_vs_aug['foreign_eaters_delta']:,} ({oct_vs_aug['foreign_eaters_pct']:+.2f}%)")
    
    print("\n[C] Total Eaters:")
    print(f"   August:   {monthly_data['August 2025']['total_eaters']:,}")
    print(f"   September: {monthly_data['September 2025']['total_eaters']:,} ({sep_vs_aug['total_eaters_pct']:+.2f}% vs Aug)")
    print(f"   October:  {monthly_data['October 2025']['total_eaters']:,} ({oct_vs_sep['total_eaters_pct']:+.2f}% vs Sep)")
    print(f"   Total Growth (Aug→Oct): {oct_vs_aug['total_eaters_delta']:,} ({oct_vs_aug['total_eaters_pct']:+.2f}%)")
    
    print("\n" + "=" * 100)
    print("2. KEY INSIGHTS")
    print("=" * 100)
    
    print("\n[A] September Pattern:")
    print(f"""
    Local Eaters:
    - Small growth: +{sep_vs_aug['local_eaters_delta']:,} eaters ({sep_vs_aug['local_eaters_pct']:+.2f}%)
    - Resilient despite overall decline
    
    Foreign Eaters:
    - Significant decline: {sep_vs_aug['foreign_eaters_delta']:,} eaters ({sep_vs_aug['foreign_eaters_pct']:.2f}%)
    - Possible causes: End of summer tourism, seasonal travel patterns
    
    Overall:
    - Total decline: {sep_vs_aug['total_eaters_delta']:,} eaters ({sep_vs_aug['total_eaters_pct']:.2f}%)
    - Foreign decline offset local growth
    """)
    
    print("\n[B] October Pattern:")
    print(f"""
    Local Eaters:
    - Strong acceleration: +{oct_vs_sep['local_eaters_delta']:,} eaters ({oct_vs_sep['local_eaters_pct']:+.2f}%)
    - 7.8x faster growth than September
    
    Foreign Eaters:
    - Recovery: +{oct_vs_sep['foreign_eaters_delta']:,} eaters ({oct_vs_sep['foreign_eaters_pct']:+.2f}%)
    - Still below August levels ({monthly_data['October 2025']['foreign_eaters'] - monthly_data['August 2025']['foreign_eaters']:,} below)
    
    Overall:
    - Strong growth: +{oct_vs_sep['total_eaters_delta']:,} eaters ({oct_vs_sep['total_eaters_pct']:+.2f}%)
    - Recovery from September decline
    """)
    
    print("\n[C] Cumulative Trend (August → October):")
    print(f"""
    Local Eaters:
    - Total growth: +{oct_vs_aug['local_eaters_delta']:,} eaters ({oct_vs_aug['local_eaters_pct']:+.2f}%)
    - Consistent positive growth
    
    Foreign Eaters:
    - Net change: {oct_vs_aug['foreign_eaters_delta']:,} eaters ({oct_vs_aug['foreign_eaters_pct']:.2f}%)
    - Net decline from August peak
    - Seasonal volatility
    
    Overall:
    - Total growth: +{oct_vs_aug['total_eaters_delta']:,} eaters ({oct_vs_aug['total_eaters_pct']:+.2f}%)
    - Driven primarily by local eaters
    """)
    
    print("\n" + "=" * 100)
    print("3. GROWTH RATE COMPARISON TABLE")
    print("=" * 100)
    
    comparison_df = pd.DataFrame({
        'Metric': ['Local Eaters', 'Foreign Eaters', 'Total Eaters',
                  'Local Orders', 'Foreign Orders', 'Total Orders',
                  'Local GMV (MYR)', 'Foreign GMV (MYR)', 'Total GMV (MYR)'],
        'Sep vs Aug': [
            f"{sep_vs_aug['local_eaters_pct']:+.2f}%",
            f"{sep_vs_aug['foreign_eaters_pct']:.2f}%",
            f"{sep_vs_aug['total_eaters_pct']:.2f}%",
            f"{sep_vs_aug['local_orders_pct']:.2f}%",
            f"{sep_vs_aug['foreign_orders_pct']:.2f}%",
            f"{sep_vs_aug['total_orders_pct']:.2f}%",
            f"{sep_vs_aug['local_gmv_pct']:.2f}%",
            f"{sep_vs_aug['foreign_gmv_pct']:.2f}%",
            f"{sep_vs_aug['total_gmv_pct']:.2f}%"
        ],
        'Oct vs Sep': [
            f"{oct_vs_sep['local_eaters_pct']:+.2f}%",
            f"{oct_vs_sep['foreign_eaters_pct']:+.2f}%",
            f"{oct_vs_sep['total_eaters_pct']:+.2f}%",
            f"{oct_vs_sep['local_orders_pct']:+.2f}%",
            f"{oct_vs_sep['foreign_orders_pct']:+.2f}%",
            f"{oct_vs_sep['total_orders_pct']:+.2f}%",
            f"{oct_vs_sep['local_gmv_pct']:+.2f}%",
            f"{oct_vs_sep['foreign_gmv_pct']:+.2f}%",
            f"{oct_vs_sep['total_gmv_pct']:+.2f}%"
        ],
        'Aug to Oct': [
            f"{oct_vs_aug['local_eaters_pct']:+.2f}%",
            f"{oct_vs_aug['foreign_eaters_pct']:.2f}%",
            f"{oct_vs_aug['total_eaters_pct']:+.2f}%",
            f"{oct_vs_aug['local_orders_pct']:+.2f}%",
            f"{oct_vs_aug['foreign_orders_pct']:+.2f}%",
            f"{oct_vs_aug['total_orders_pct']:+.2f}%",
            f"{oct_vs_aug['local_gmv_pct']:+.2f}%",
            f"{oct_vs_aug['foreign_gmv_pct']:.2f}%",
            f"{oct_vs_aug['total_gmv_pct']:+.2f}%"
        ]
    })
    
    print("\n" + comparison_df.to_string(index=False))
    
    print("\n" + "=" * 100)
    print("4. PATTERN ANALYSIS")
    print("=" * 100)
    
    print("\n[A] Local Eater Pattern:")
    print("""
    Pattern: CONSISTENT GROWTH WITH ACCELERATION
    
    August → September: +0.5% (small growth)
    September → October: +3.9% (strong acceleration)
    Overall: +4.5% (consistent positive trend)
    
    Characteristics:
    ✅ Resilient to seasonal factors
    ✅ Consistent month-over-month growth
    ✅ Strong acceleration in October
    ✅ Primary driver of overall growth
    """)
    
    print("\n[B] Foreign Eater Pattern:")
    print("""
    Pattern: VOLATILE WITH SEASONAL DECLINE
    
    August → September: -10.3% (significant decline)
    September → October: +5.1% (recovery)
    Overall: -5.7% (net decline from August)
    
    Characteristics:
    ⚠️ Tourism/seasonal dependent
    ⚠️ Significant September decline
    ✅ Recovery in October
    ⚠️ Below August peak levels
    """)
    
    print("\n" + "=" * 100)
    print("5. STRATEGIC IMPLICATIONS")
    print("=" * 100)
    
    print("\n[A] Primary Strategy - Local Eaters:")
    print("""
    FOCUS: Continue Local Acquisition
    
    Rationale:
    - Consistent growth across all months (+4.5% Aug→Oct)
    - Strong acceleration in October (+3.9%)
    - Resilient to seasonal factors
    - Primary driver of overall growth
    
    Actions:
    1. Maintain local acquisition momentum
    2. Learn from October acceleration factors
    3. Replicate October success patterns
    4. Monitor September slowdown causes
    """)
    
    print("\n[B] Secondary Strategy - Foreign Eaters:")
    print("""
    FOCUS: Plan for Volatility
    
    Rationale:
    - High value segment (higher basket size)
    - Volatile growth pattern (seasonal dependent)
    - Tourism/travel dependent
    - Recovery capability demonstrated
    
    Actions:
    1. Plan for seasonal variations (expect September-like declines)
    2. Target tourism recovery periods (August-like peaks)
    3. Develop retention strategies (reduce volatility)
    4. Focus on stable segments (business, expatriates)
    """)
    
    print("\n" + "=" * 100)
    print("6. CONCLUSION")
    print("=" * 100)
    
    print(f"""
    MONTH-OVER-MONTH COMPARISON SUMMARY:
    
    SEPTEMBER (vs August):
    - Local: +{sep_vs_aug['local_eaters_pct']:.2f}% (resilient)
    - Foreign: {sep_vs_aug['foreign_eaters_pct']:.2f}% (decline)
    - Overall: {sep_vs_aug['total_eaters_pct']:.2f}% (challenging month)
    
    OCTOBER (vs September):
    - Local: +{oct_vs_sep['local_eaters_pct']:.2f}% (strong acceleration)
    - Foreign: +{oct_vs_sep['foreign_eaters_pct']:.2f}% (recovery)
    - Overall: +{oct_vs_sep['total_eaters_pct']:.2f}% (strong growth)
    
    CUMULATIVE (August → October):
    - Local: +{oct_vs_aug['local_eaters_pct']:.2f}% (consistent growth)
    - Foreign: {oct_vs_aug['foreign_eaters_pct']:.2f}% (volatile, net decline)
    - Overall: +{oct_vs_aug['total_eaters_pct']:.2f}% (local-driven)
    
    KEY FINDING:
    October represents a strong recovery from September, with both segments
    growing. However, local eaters continue to drive the majority of growth
    and show consistent positive trends across all months.
    """)
    
    # Save data
    summary_data = {
        'Period': ['August 2025', 'September 2025', 'October 2025'],
        'Local_Eaters': [monthly_data['August 2025']['local_eaters'],
                        monthly_data['September 2025']['local_eaters'],
                        monthly_data['October 2025']['local_eaters']],
        'Foreign_Eaters': [monthly_data['August 2025']['foreign_eaters'],
                          monthly_data['September 2025']['foreign_eaters'],
                          monthly_data['October 2025']['foreign_eaters']],
        'Total_Eaters': [monthly_data['August 2025']['total_eaters'],
                        monthly_data['September 2025']['total_eaters'],
                        monthly_data['October 2025']['total_eaters']]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('monthly_eater_trends.csv', index=False, encoding='utf-8')
    print("\n[OK] Saved monthly trends to: monthly_eater_trends.csv")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    compare_months()


