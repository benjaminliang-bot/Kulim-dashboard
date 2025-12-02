#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ipoh & Penang: Inter-Causal Analysis Comparison
Detailed driver analysis for these two key OC cities
"""

import pandas as pd

def compare_ipoh_penang():
    """
    Compare growth drivers between Ipoh and Penang
    """
    
    print("=" * 100)
    print("IPOH vs PENANG: INTER-CAUSAL ANALYSIS COMPARISON")
    print("=" * 100)
    
    # Data from queries
    penang_data = {
        'city': 'Penang',
        'sep_orders': 1219460,
        'oct_orders': 1285577,
        'order_growth_pct': 5.4,
        'sep_eaters': 288514,
        'oct_eaters': 296554,
        'eater_growth_pct': 2.8,
        'eater_delta': 8040,
        'sep_merchants': 6411,
        'oct_merchants': 6490,
        'merchant_growth_pct': 1.2,
        'merchant_delta': 79,
        'sep_gmv': 45276009.59,
        'oct_gmv': 47130877.33,
        'gmv_growth_pct': 4.1,
        'sep_basket': 35.78,
        'oct_basket': 35.48,
        'basket_delta': -0.31,
        'sep_promo_pen': 56.1,
        'oct_promo_pen': 56.4,
        'sep_promo_exp': 6767273.07,
        'oct_promo_exp': 7097121.89,
        'promo_growth_pct': 4.9,
        'oct_orders_per_merchant': 198,
        'sep_orders_per_merchant': 190,
        'utilization_growth': 4.2
    }
    
    ipoh_data = {
        'city': 'Ipoh',
        'sep_orders': 705665,
        'oct_orders': 729902,
        'order_growth_pct': 3.4,
        'sep_eaters': 175606,
        'oct_eaters': 177844,
        'eater_growth_pct': 1.3,
        'eater_delta': 2238,
        'sep_merchants': 5017,
        'oct_merchants': 5131,
        'merchant_growth_pct': 2.3,
        'merchant_delta': 114,
        'sep_gmv': 23105450.18,
        'oct_gmv': 23565726.20,
        'gmv_growth_pct': 2.0,
        'sep_basket': 31.42,
        'oct_basket': 31.05,
        'basket_delta': -0.36,
        'sep_promo_pen': 47.3,
        'oct_promo_pen': 46.2,
        'sep_promo_exp': 2718201.46,
        'oct_promo_exp': 2843747.63,
        'promo_growth_pct': 4.6,
        'oct_orders_per_merchant': 142,
        'sep_orders_per_merchant': 141,
        'utilization_growth': 0.7
    }
    
    print("\n" + "=" * 100)
    print("1. PERFORMANCE COMPARISON")
    print("=" * 100)
    
    comparison = pd.DataFrame({
        'Metric': ['Order Growth', 'GMV Growth', 'Eater Growth', 'Merchant Growth', 
                  'Basket Size', 'Promo Penetration', 'Promo Expense Growth',
                  'Orders per Merchant', 'Completion Rate'],
        'Penang': [f"+{penang_data['order_growth_pct']:.1f}%",
                  f"+{penang_data['gmv_growth_pct']:.1f}%",
                  f"+{penang_data['eater_growth_pct']:.1f}% ({penang_data['eater_delta']:,})",
                  f"+{penang_data['merchant_growth_pct']:.1f}% ({penang_data['merchant_delta']})",
                  f"MYR {penang_data['oct_basket']:.2f}",
                  f"{penang_data['oct_promo_pen']:.1f}%",
                  f"+{penang_data['promo_growth_pct']:.1f}%",
                  f"{penang_data['oct_orders_per_merchant']:.0f}",
                  "91.9%"],
        'Ipoh': [f"+{ipoh_data['order_growth_pct']:.1f}%",
                f"+{ipoh_data['gmv_growth_pct']:.1f}%",
                f"+{ipoh_data['eater_growth_pct']:.1f}% ({ipoh_data['eater_delta']:,})",
                f"+{ipoh_data['merchant_growth_pct']:.1f}% ({ipoh_data['merchant_delta']})",
                f"MYR {ipoh_data['oct_basket']:.2f}",
                f"{ipoh_data['oct_promo_pen']:.1f}%",
                f"+{ipoh_data['promo_growth_pct']:.1f}%",
                f"{ipoh_data['oct_orders_per_merchant']:.0f}",
                "91.7%"],
        'Difference': [
            f"+{penang_data['order_growth_pct'] - ipoh_data['order_growth_pct']:.1f}pp",
            f"+{penang_data['gmv_growth_pct'] - ipoh_data['gmv_growth_pct']:.1f}pp",
            f"+{penang_data['eater_growth_pct'] - ipoh_data['eater_growth_pct']:.1f}pp ({penang_data['eater_delta'] - ipoh_data['eater_delta']:,} more)",
            f"-{ipoh_data['merchant_growth_pct'] - penang_data['merchant_growth_pct']:.1f}pp ({ipoh_data['merchant_delta'] - penang_data['merchant_delta']} more)",
            f"+MYR {penang_data['oct_basket'] - ipoh_data['oct_basket']:.2f}",
            f"+{penang_data['oct_promo_pen'] - ipoh_data['oct_promo_pen']:.1f}pp",
            f"+{penang_data['promo_growth_pct'] - ipoh_data['promo_growth_pct']:.3f}pp",
            f"+{penang_data['oct_orders_per_merchant'] - ipoh_data['oct_orders_per_merchant']:.0f}",
            "+0.2pp"
        ]
    })
    
    print("\n" + comparison.to_string(index=False))
    
    print("\n" + "=" * 100)
    print("2. GROWTH DRIVER ANALYSIS")
    print("=" * 100)
    
    print("\n[A] PENANG - DEMAND-PULL MODEL")
    print("-" * 100)
    print(f"""
    Primary Driver: EATER EXPANSION
    - Eater Growth: +{penang_data['eater_delta']:,} eaters (+{penang_data['eater_growth_pct']:.1f}%)
    - Impact: Drives ~51% of order growth
    - Strategy: Demand-focused, acquisition-heavy
    
    Secondary Drivers:
    1. PROMOTION STRATEGY
       - Penetration: {penang_data['oct_promo_pen']:.1f}% (highest among OC cities)
       - Investment Growth: +{penang_data['promo_growth_pct']:.1f}%
       - Role: Key enabler of order growth
    
    2. MERCHANT UTILIZATION
       - Orders per Merchant: {penang_data['oct_orders_per_merchant']:.0f} (+{penang_data['utilization_growth']:.1f}%)
       - Role: High utilization supports growth
    
    Causal Chain:
    EATER EXPANSION → HIGH PROMO PENETRATION → ORDER GROWTH (+{penang_data['order_growth_pct']:.1f}%) → GMV GROWTH (+{penang_data['gmv_growth_pct']:.1f}%)
    """)
    
    print("\n[B] IPOH - SUPPLY-PUSH MODEL")
    print("-" * 100)
    print(f"""
    Primary Driver: MERCHANT EXPANSION
    - Merchant Growth: +{ipoh_data['merchant_delta']} merchants (+{ipoh_data['merchant_growth_pct']:.1f}%)
    - Impact: Highest merchant growth rate among top cities
    - Strategy: Supply-focused, capacity expansion
    
    Secondary Drivers:
    1. EATER EXPANSION
       - Eater Growth: +{ipoh_data['eater_delta']:,} eaters (+{ipoh_data['eater_growth_pct']:.1f}%)
       - Comparison: {ipoh_data['eater_delta']/penang_data['eater_delta']:.1f}x lower than Penang
       - Role: Supporting factor, not primary
    
    2. PROMOTION INVESTMENT
       - Penetration: {ipoh_data['oct_promo_pen']:.1f}% (moderate)
       - Investment Growth: +{ipoh_data['promo_growth_pct']:.1f}%
       - Avg Promo Value: Increased (+MYR 0.38)
       - Role: Supporting growth
    
    Causal Chain:
    MERCHANT EXPANSION → INCREASED SUPPLY → EATER EXPANSION → ORDER GROWTH (+{ipoh_data['order_growth_pct']:.1f}%) → GMV GROWTH (+{ipoh_data['gmv_growth_pct']:.1f}%)
    """)
    
    print("\n" + "=" * 100)
    print("3. KEY DIFFERENCES & INSIGHTS")
    print("=" * 100)
    
    print("\n[A] Growth Model Difference:")
    print("""
    PENANG: Demand-Pull Model
    - Focus: Eater acquisition drives growth
    - Approach: High promotion to attract eaters
    - Result: Higher growth rate (5.4% vs 3.4%)
    
    IPOH: Supply-Push Model
    - Focus: Merchant expansion drives growth
    - Approach: Expand supply capacity first
    - Result: Steady but lower growth rate (3.4%)
    """)
    
    print("\n[B] Eater Growth Gap:")
    eater_gap = penang_data['eater_delta'] - ipoh_data['eater_delta']
    eater_ratio = penang_data['eater_delta'] / ipoh_data['eater_delta']
    print(f"""
    Penang: +{penang_data['eater_delta']:,} eaters
    Ipoh:   +{ipoh_data['eater_delta']:,} eaters
    Gap:    {eater_gap:,} more eaters in Penang
    Ratio:  {eater_ratio:.1f}x more eater growth in Penang
    
    → Ipoh needs to accelerate eater acquisition
    """)
    
    print("\n[C] Promotion Strategy Difference:")
    promo_gap = penang_data['oct_promo_pen'] - ipoh_data['oct_promo_pen']
    print(f"""
    Penang: {penang_data['oct_promo_pen']:.1f}% penetration
    Ipoh:   {ipoh_data['oct_promo_pen']:.1f}% penetration
    Gap:    {promo_gap:.1f}pp difference
    
    → Penang's high penetration drives stronger growth
    → Ipoh can increase promotion to match effectiveness
    """)
    
    print("\n[D] Merchant Strategy Difference:")
    merchant_ratio = ipoh_data['merchant_delta'] / penang_data['merchant_delta']
    print(f"""
    Penang: +{penang_data['merchant_delta']} merchants (+{penang_data['merchant_growth_pct']:.1f}%)
    Ipoh:   +{ipoh_data['merchant_delta']} merchants (+{ipoh_data['merchant_growth_pct']:.1f}%)
    Ratio:  {merchant_ratio:.1f}x more merchant growth in Ipoh
    
    → Ipoh's merchant expansion is a strength
    → Can leverage for faster growth with better eater acquisition
    """)
    
    print("\n" + "=" * 100)
    print("4. RECOMMENDATIONS")
    print("=" * 100)
    
    print("\n[A] For PENANG:")
    print("""
    1. MAINTAIN STRENGTHS:
       ✅ Continue aggressive eater acquisition (+2.8% growth)
       ✅ Maintain high promo penetration (56.4%)
       ✅ Focus on basket size protection (currently MYR 35.48)
    
    2. ADDRESS CHALLENGES:
       ⚠️ Monitor completion rate (declined -0.6pp to 91.9%)
       ⚠️ Address basket size decline (-MYR 0.31)
       ⚠️ Optimize promo ROI (high investment, ensure returns)
    
    3. GROWTH STRATEGY:
       → Leverage current momentum
       → Focus on retention to increase frequency
       → Maintain premium positioning
    """)
    
    print("\n[B] For IPOH:")
    print("""
    1. ACCELERATE EATER ACQUISITION:
       ⚠️ Current +1.3% growth is {ipoh_data['eater_growth_pct']/penang_data['eater_growth_pct']:.1f}x lower than Penang
       → Increase marketing investment
       → Target similar growth rate (+2.5%+)
       → Leverage merchant expansion to attract eaters
    
    2. INCREASE PROMOTION PENETRATION:
       ⚠️ Current 46.2% vs Penang's 56.4% ({promo_gap:.1f}pp gap)
       → Increase promo investment
       → Target 50%+ penetration
       → Learn from Penang's successful strategy
    
    3. LEVERAGE MERCHANT EXPANSION:
       ✅ Strong merchant growth (+2.3% is highest among top cities)
       → Support new merchants with operations
       → Market merchant variety to attract eaters
       → Maintain quality standards
    
    4. BASKET SIZE IMPROVEMENT:
       ⚠️ Current MYR 31.05 vs Penang's MYR 35.48 (MYR {penang_data['oct_basket'] - ipoh_data['oct_basket']:.2f} gap)
       → Upselling strategies
       → Promote higher-value items
       → Target premium segment growth
    """)
    
    print("\n[C] Cross-City Learning:")
    print("""
    PENANG → IPOH:
    → Learn high promo penetration strategy
    → Adopt successful eater acquisition tactics
    → Study basket size optimization
    
    IPOH → PENANG:
    → Learn merchant expansion approach
    → Study operational stability maintenance
    → Balance growth with quality
    """)
    
    # Save summary
    summary_df = pd.DataFrame({
        'City': ['Penang', 'Ipoh'],
        'Order_Growth_Pct': [penang_data['order_growth_pct'], ipoh_data['order_growth_pct']],
        'GMV_Growth_Pct': [penang_data['gmv_growth_pct'], ipoh_data['gmv_growth_pct']],
        'Eater_Growth_Pct': [penang_data['eater_growth_pct'], ipoh_data['eater_growth_pct']],
        'Eater_Delta': [penang_data['eater_delta'], ipoh_data['eater_delta']],
        'Merchant_Growth_Pct': [penang_data['merchant_growth_pct'], ipoh_data['merchant_growth_pct']],
        'Merchant_Delta': [penang_data['merchant_delta'], ipoh_data['merchant_delta']],
        'Promo_Penetration': [penang_data['oct_promo_pen'], ipoh_data['oct_promo_pen']],
        'Basket_Size': [penang_data['oct_basket'], ipoh_data['oct_basket']],
        'Primary_Driver': ['Eater Expansion', 'Merchant Expansion'],
        'Growth_Model': ['Demand-Pull', 'Supply-Push']
    })
    
    summary_df.to_csv('ipoh_penang_driver_comparison.csv', index=False, encoding='utf-8')
    print("\n[OK] Saved comparison to: ipoh_penang_driver_comparison.csv")
    
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    compare_ipoh_penang()


