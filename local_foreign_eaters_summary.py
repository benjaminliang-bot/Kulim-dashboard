#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local vs Foreign Eaters Analysis Summary
Determining if OC cities eater growth is driven by locals or foreigners
"""

import pandas as pd

def analyze_local_vs_foreign():
    """
    Analyze local vs foreign eater contribution to OC cities growth
    """
    
    print("=" * 100)
    print("LOCAL vs FOREIGN EATERS ANALYSIS: OC CITIES GROWTH DRIVERS")
    print("=" * 100)
    
    # Overall data
    overall_data = {
        'Local': {
            'sep': 1603521,
            'oct': 1668095,
            'delta': 64574,
            'growth_pct': 4.0,
            'share_of_growth': 91.1
        },
        'Foreign': {
            'sep': 121146,
            'oct': 127434,
            'delta': 6288,
            'growth_pct': 5.2,
            'share_of_growth': 8.9
        }
    }
    
    # Top foreign countries
    foreign_countries = [
        {'country': 'China', 'sep': 11284, 'oct': 13513, 'delta': 2229, 'growth_pct': 19.8},
        {'country': 'Singapore', 'sep': 70962, 'oct': 72932, 'delta': 1970, 'growth_pct': 2.8},
        {'country': 'Thailand', 'sep': 5300, 'oct': 5985, 'delta': 685, 'growth_pct': 12.9},
        {'country': 'Indonesia', 'sep': 13719, 'oct': 14365, 'delta': 646, 'growth_pct': 4.7},
        {'country': 'Cocos (Keeling) Islands', 'sep': 1574, 'oct': 1783, 'delta': 209, 'growth_pct': 13.3},
        {'country': 'India', 'sep': 1382, 'oct': 1581, 'delta': 199, 'growth_pct': 14.4},
        {'country': 'United States', 'sep': 1109, 'oct': 1297, 'delta': 188, 'growth_pct': 17.0},
        {'country': 'Taiwan', 'sep': 769, 'oct': 930, 'delta': 161, 'growth_pct': 20.9},
        {'country': 'Vietnam', 'sep': 1972, 'oct': 2097, 'delta': 125, 'growth_pct': 6.3},
        {'country': 'Hong Kong', 'sep': 681, 'oct': 760, 'delta': 79, 'growth_pct': 11.6}
    ]
    
    # City-level data
    city_data = [
        {'city': 'Johor Bahru', 'local_delta': 14426, 'foreign_delta': 2978, 'local_growth': 4.1, 'foreign_growth': 4.5},
        {'city': 'Penang', 'local_delta': 6198, 'foreign_delta': 1840, 'local_growth': 2.3, 'foreign_growth': 9.3},
        {'city': 'Kota Kinabalu', 'local_delta': 7463, 'foreign_delta': 377, 'local_growth': 6.2, 'foreign_growth': 4.4},
        {'city': 'Kuching', 'local_delta': 7451, 'foreign_delta': 9, 'local_growth': 6.7, 'foreign_growth': 0.3},
        {'city': 'Melaka', 'local_delta': 7965, 'foreign_delta': -22, 'local_growth': 6.9, 'foreign_growth': -0.4},
        {'city': 'Ipoh', 'local_delta': 1949, 'foreign_delta': 288, 'local_growth': 1.1, 'foreign_growth': 5.4}
    ]
    
    print("\n" + "=" * 100)
    print("1. OVERALL ANSWER")
    print("=" * 100)
    
    print(f"""
    QUESTION: Is the increase in eaters for OC cities due to foreigners or local?
    
    ANSWER: PRIMARILY LOCAL (91.1%)
    
    Breakdown:
    - Local Malaysians:     +{overall_data['Local']['delta']:,} eaters ({overall_data['Local']['growth_pct']:.1f}% growth) = {overall_data['Local']['share_of_growth']:.1f}% of total growth
    - Foreign Eaters:        +{overall_data['Foreign']['delta']:,} eaters ({overall_data['Foreign']['growth_pct']:.1f}% growth) = {overall_data['Foreign']['share_of_growth']:.1f}% of total growth
    - Total Growth:          +70,862 eaters
    
    → The increase is PRIMARILY DRIVEN BY LOCAL MALAYSIANS (91.1%)
    → Foreign eaters contribute but are not the main driver (8.9%)
    """)
    
    print("\n" + "=" * 100)
    print("2. DETAILED BREAKDOWN")
    print("=" * 100)
    
    print("\n[A] Local vs Foreign Comparison:")
    print("-" * 100)
    
    comparison_df = pd.DataFrame({
        'Category': ['Local (Malaysia Phone)', 'Foreign (Non-Malaysia Phone)'],
        'September 2025': [overall_data['Local']['sep'], overall_data['Foreign']['sep']],
        'October 2025': [overall_data['Local']['oct'], overall_data['Foreign']['oct']],
        'Growth': [overall_data['Local']['delta'], overall_data['Foreign']['delta']],
        'Growth %': [f"+{overall_data['Local']['growth_pct']:.1f}%", f"+{overall_data['Foreign']['growth_pct']:.1f}%"],
        'Share of Total Growth': [f"{overall_data['Local']['share_of_growth']:.1f}%", f"{overall_data['Foreign']['share_of_growth']:.1f}%"]
    })
    
    print("\n" + comparison_df.to_string(index=False))
    
    print(f"\nKey Insights:")
    print(f"  1. Local eaters drive 91.1% of growth (absolute numbers)")
    print(f"  2. Foreign eaters show higher growth rate (5.2% vs 4.0%) but from smaller base")
    print(f"  3. Local base is {overall_data['Local']['sep']/overall_data['Foreign']['sep']:.1f}x larger than foreign base")
    
    print("\n[B] Top Foreign Countries Contributing to Growth:")
    print("-" * 100)
    
    foreign_df = pd.DataFrame(foreign_countries)
    foreign_df['contribution_pct'] = (foreign_df['delta'] / foreign_df['delta'].sum() * 100).round(1)
    foreign_df = foreign_df.sort_values('delta', ascending=False)
    
    print("\n" + foreign_df.to_string(index=False))
    
    print(f"\nTop 3 Foreign Countries = {foreign_df.head(3)['delta'].sum():,} eaters ({foreign_df.head(3)['contribution_pct'].sum():.1f}% of foreign growth)")
    print(f"  - China: {foreign_df.iloc[0]['delta']:,} eaters ({foreign_df.iloc[0]['contribution_pct']:.1f}%)")
    print(f"  - Singapore: {foreign_df.iloc[1]['delta']:,} eaters ({foreign_df.iloc[1]['contribution_pct']:.1f}%)")
    print(f"  - Thailand: {foreign_df.iloc[2]['delta']:,} eaters ({foreign_df.iloc[2]['contribution_pct']:.1f}%)")
    
    print("\n[C] City-Level Local vs Foreign Breakdown:")
    print("-" * 100)
    
    city_df = pd.DataFrame(city_data)
    city_df['total_delta'] = city_df['local_delta'] + city_df['foreign_delta']
    city_df['local_share'] = (city_df['local_delta'] / city_df['total_delta'] * 100).round(1)
    city_df['foreign_share'] = (city_df['foreign_delta'] / city_df['total_delta'] * 100).round(1)
    
    print("\n" + city_df.to_string(index=False))
    
    print("\n" + "=" * 100)
    print("3. KEY INSIGHTS BY CITY")
    print("=" * 100)
    
    print("\n[A] Cities with Highest Local Growth:")
    print(f"  1. Melaka: +{city_df.loc[city_df['city'] == 'Melaka', 'local_delta'].values[0]:,} local eaters ({city_df.loc[city_df['city'] == 'Melaka', 'local_growth'].values[0]:.1f}% growth)")
    print(f"  2. Kuching: +{city_df.loc[city_df['city'] == 'Kuching', 'local_delta'].values[0]:,} local eaters ({city_df.loc[city_df['city'] == 'Kuching', 'local_growth'].values[0]:.1f}% growth)")
    print(f"  3. Kota Kinabalu: +{city_df.loc[city_df['city'] == 'Kota Kinabalu', 'local_delta'].values[0]:,} local eaters ({city_df.loc[city_df['city'] == 'Kota Kinabalu', 'local_growth'].values[0]:.1f}% growth)")
    
    print("\n[B] Cities with Highest Foreign Growth:")
    print(f"  1. Penang: +{city_df.loc[city_df['city'] == 'Penang', 'foreign_delta'].values[0]:,} foreign eaters ({city_df.loc[city_df['city'] == 'Penang', 'foreign_growth'].values[0]:.1f}% growth)")
    print(f"  2. Johor Bahru: +{city_df.loc[city_df['city'] == 'Johor Bahru', 'foreign_delta'].values[0]:,} foreign eaters ({city_df.loc[city_df['city'] == 'Johor Bahru', 'foreign_growth'].values[0]:.1f}% growth)")
    print(f"  3. Kota Kinabalu: +{city_df.loc[city_df['city'] == 'Kota Kinabalu', 'foreign_delta'].values[0]:,} foreign eaters ({city_df.loc[city_df['city'] == 'Kota Kinabalu', 'foreign_growth'].values[0]:.1f}% growth)")
    
    print("\n[C] Notable Patterns:")
    print(f"  - Penang: High foreign growth rate (9.3%) - likely tourism hub")
    print(f"  - Johor Bahru: High absolute foreign growth (+2,978) - proximity to Singapore")
    print(f"  - Melaka: Foreign eater decline (-22) but strong local growth")
    print(f"  - Kuching: Minimal foreign growth (+9) - primarily local-driven")
    
    print("\n" + "=" * 100)
    print("4. STRATEGIC IMPLICATIONS")
    print("=" * 100)
    
    print("\n[A] Primary Strategy (91.1% of growth):")
    print("""
    FOCUS ON LOCAL MALAYSIAN EATER ACQUISITION
    
    Rationale:
    - 91.1% of eater growth comes from local Malaysians
    - This validates current local acquisition strategies
    - Continue and intensify local marketing efforts
    
    Actions:
    1. Maintain local acquisition campaigns
    2. Target local eaters in outer cities
    3. Expand local user base through promotions
    4. Focus on cities with high local growth (Melaka, Kuching, Kota Kinabalu)
    """)
    
    print("\n[B] Secondary Strategy (8.9% of growth):")
    print("""
    LEVERAGE FOREIGN EATER OPPORTUNITY
    
    Rationale:
    - Foreign eaters show higher growth rate (5.2% vs 4.0%)
    - Tourism/visitor segment is growing
    - East Asian markets (especially China) show strong growth
    
    Actions:
    1. Target tourism segment, especially East Asian visitors
    2. Focus on tourist-friendly cities (Penang, Johor Bahru)
    3. Consider China market (19.8% growth rate)
    4. Maintain Singapore connection (largest foreign base)
    """)
    
    print("\n[C] City-Specific Recommendations:")
    print(f"""
    PENANG:
    - High foreign growth (9.3%) - leverage tourism position
    - Continue local acquisition (2.3% growth)
    - Tourism partnerships and promotions
    
    JOHOR BAHRU:
    - Proximity to Singapore drives foreign growth (4.5%)
    - Strong local growth (4.1%) - continue both strategies
    - Cross-border marketing opportunities
    
    MELAKA, KUCHING, KOTA KINABALU:
    - Primarily local-driven growth
    - Focus on local acquisition strategies
    - Less emphasis on foreign segment
    """)
    
    # Save summary
    summary_df = pd.DataFrame({
        'Category': ['Local (Malaysia Phone)', 'Foreign (Non-Malaysia Phone)'],
        'Sep_Eaters': [overall_data['Local']['sep'], overall_data['Foreign']['sep']],
        'Oct_Eaters': [overall_data['Local']['oct'], overall_data['Foreign']['oct']],
        'Growth': [overall_data['Local']['delta'], overall_data['Foreign']['delta']],
        'Growth_Pct': [f"+{overall_data['Local']['growth_pct']:.1f}%", f"+{overall_data['Foreign']['growth_pct']:.1f}%"],
        'Share_of_Total_Growth': [f"{overall_data['Local']['share_of_growth']:.1f}%", f"{overall_data['Foreign']['share_of_growth']:.1f}%"]
    })
    
    summary_df.to_csv('local_vs_foreign_eaters_summary.csv', index=False, encoding='utf-8')
    print("\n[OK] Saved summary to: local_vs_foreign_eaters_summary.csv")
    
    foreign_summary_df = pd.DataFrame(foreign_countries)
    foreign_summary_df.to_csv('top_foreign_countries_oc_growth.csv', index=False, encoding='utf-8')
    print("[OK] Saved foreign countries breakdown to: top_foreign_countries_oc_growth.csv")
    
    city_summary_df = pd.DataFrame(city_data)
    city_summary_df.to_csv('city_local_foreign_breakdown.csv', index=False, encoding='utf-8')
    print("[OK] Saved city breakdown to: city_local_foreign_breakdown.csv")
    
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)
    
    print("\n" + "=" * 100)
    print("CONCLUSION")
    print("=" * 100)
    print(f"""
    The increase in eaters for OC cities is PRIMARILY DRIVEN BY LOCAL MALAYSIANS (91.1%).
    
    While foreign eaters show a higher growth rate (5.2% vs 4.0%), the absolute growth
    comes from local eaters due to their much larger base (13.2x larger).
    
    Strategic Focus:
    → Primary: Continue local Malaysian eater acquisition (91.1% of growth)
    → Secondary: Leverage foreign eater opportunity (8.9% of growth, especially East Asia)
    """)

if __name__ == "__main__":
    analyze_local_vs_foreign()


