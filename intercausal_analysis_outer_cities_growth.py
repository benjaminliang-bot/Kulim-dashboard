#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inter-Causal Analysis: What Drives the Growth in Outer Cities (OC)
Analysis of factors driving the increment from August/September to October 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime

def perform_intercausal_analysis():
    """
    Comprehensive inter-causal analysis to identify drivers of OC cities growth
    """
    
    print("=" * 100)
    print("INTER-CAUSAL ANALYSIS: WHAT DRIVES OUTER CITIES GROWTH?")
    print("=" * 100)
    print("\nAnalyzing factors driving the increment from Aug/Sep 2025 to October 2025")
    
    # Period comparison data
    periods = {
        'August 2025': {
            'orders': 7633154,
            'completed_orders': 7001345,
            'gmv': 264764184.81,
            'completion_rate': 91.7,
            'allocation_rate': 91.3,
            'merchants': 47868,
            'eaters': 1730809,
            'avg_basket': 33.48,
            'promo_penetration': 47.5,
            'promo_expense': 27367597.23,
            'avg_promo': 8.37,
            'orders_per_eater': 4.0,
            'orders_per_merchant': 146,
            'avg_time_to_allocate': 597.7
        },
        'September 2025': {
            'orders': 7361673,
            'completed_orders': 6728905,
            'gmv': 257397369.20,
            'completion_rate': 91.4,
            'allocation_rate': 91.1,
            'merchants': 48269,
            'eaters': 1724667,
            'avg_basket': 33.91,
            'promo_penetration': 49.1,
            'promo_expense': 28546925.95,
            'avg_promo': 8.76,
            'orders_per_eater': 3.9,
            'orders_per_merchant': 139,
            'avg_time_to_allocate': 600.1
        },
        'October 2025': {
            'orders': 7906094,
            'completed_orders': 7259345,
            'gmv': 274581392.68,
            'completion_rate': 91.8,
            'allocation_rate': 91.6,
            'merchants': 49240,
            'eaters': 1795529,
            'avg_basket': 33.51,
            'promo_penetration': 48.8,
            'promo_expense': 31758798.85,
            'avg_promo': 9.08,
            'orders_per_eater': 4.0,
            'orders_per_merchant': 147,
            'avg_time_to_allocate': 605.7
        }
    }
    
    # Calculate deltas
    oct_vs_sep = {}
    oct_vs_aug = {}
    
    for metric in ['orders', 'completed_orders', 'gmv', 'merchants', 'eaters', 
                   'completion_rate', 'allocation_rate', 'avg_basket', 
                   'promo_penetration', 'promo_expense', 'avg_promo',
                   'orders_per_eater', 'orders_per_merchant', 'avg_time_to_allocate']:
        oct_vs_sep[metric] = periods['October 2025'][metric] - periods['September 2025'][metric]
        oct_vs_aug[metric] = periods['October 2025'][metric] - periods['August 2025'][metric]
        
        # Calculate percentage change
        if periods['September 2025'][metric] != 0:
            oct_vs_sep[f'{metric}_pct'] = (oct_vs_sep[metric] / periods['September 2025'][metric]) * 100
        if periods['August 2025'][metric] != 0:
            oct_vs_aug[f'{metric}_pct'] = (oct_vs_aug[metric] / periods['August 2025'][metric]) * 100
    
    print("\n" + "=" * 100)
    print("1. PRIMARY GROWTH DRIVERS")
    print("=" * 100)
    
    print("\n[A] Volume Growth Factors")
    print("-" * 100)
    
    print(f"\n1.1 Total Orders Growth:")
    print(f"   October vs September: {oct_vs_sep['orders']:+,} orders ({oct_vs_sep['orders_pct']:+.2f}%)")
    print(f"   October vs August:    {oct_vs_aug['orders']:+,} orders ({oct_vs_aug['orders_pct']:+.2f}%)")
    print(f"   → PRIMARY DRIVER: +7.4% order volume growth from September")
    
    print(f"\n1.2 Eater Base Expansion:")
    print(f"   October vs September: {oct_vs_sep['eaters']:+,} eaters ({oct_vs_sep['eaters_pct']:+.2f}%)")
    print(f"   October vs August:    {oct_vs_aug['eaters']:+,} eaters ({oct_vs_aug['eaters_pct']:+.2f}%)")
    print(f"   → CAUSAL FACTOR: +4.1% growth in unique eater base from September")
    print(f"   → Impact: {oct_vs_sep['eaters']:,} new eaters contributing to order growth")
    
    print(f"\n1.3 Orders per Eater:")
    print(f"   October: {periods['October 2025']['orders_per_eater']:.1f} orders/eater")
    print(f"   September: {periods['September 2025']['orders_per_eater']:.1f} orders/eater")
    print(f"   Change: {oct_vs_sep['orders_per_eater']:+.2f} orders/eater")
    print(f"   → CAUSAL FACTOR: Slight increase in frequency per eater")
    
    print(f"\n1.4 Merchant Base Growth:")
    print(f"   October vs September: {oct_vs_sep['merchants']:+,} merchants ({oct_vs_sep['merchants_pct']:+.2f}%)")
    print(f"   October vs August:    {oct_vs_aug['merchants']:+,} merchants ({oct_vs_aug['merchants_pct']:+.2f}%)")
    print(f"   → CAUSAL FACTOR: +2.0% merchant expansion increases supply capacity")
    
    print(f"\n1.5 Orders per Merchant:")
    print(f"   October: {periods['October 2025']['orders_per_merchant']:.1f} orders/merchant")
    print(f"   September: {periods['September 2025']['orders_per_merchant']:.1f} orders/merchant")
    print(f"   Change: {oct_vs_sep['orders_per_merchant']:+.1f} orders/merchant ({oct_vs_sep['orders_per_merchant_pct']:+.1f}%)")
    print(f"   → CAUSAL FACTOR: Higher merchant utilization drives growth")
    
    print("\n[B] Quality & Efficiency Factors")
    print("-" * 100)
    
    print(f"\n2.1 Completion Rate Improvement:")
    print(f"   October vs September: {oct_vs_sep['completion_rate']:+.1f}pp ({oct_vs_sep['completion_rate_pct']:+.2f}% relative)")
    print(f"   October: {periods['October 2025']['completion_rate']:.1f}%")
    print(f"   September: {periods['September 2025']['completion_rate']:.1f}%")
    print(f"   → CAUSAL FACTOR: +0.4pp improvement in completion rate = +{int(oct_vs_sep['completed_orders']):,} more completed orders")
    
    print(f"\n2.2 Allocation Rate Improvement:")
    print(f"   October vs September: {oct_vs_sep['allocation_rate']:+.1f}pp")
    print(f"   October: {periods['October 2025']['allocation_rate']:.1f}%")
    print(f"   September: {periods['September 2025']['allocation_rate']:.1f}%")
    print(f"   → CAUSAL FACTOR: Better order allocation efficiency")
    
    print("\n[C] Revenue & Value Factors")
    print("-" * 100)
    
    print(f"\n3.1 GMV Growth:")
    print(f"   October vs September: MYR {oct_vs_sep['gmv']:+,.2f} ({oct_vs_sep['gmv_pct']:+.2f}%)")
    print(f"   October vs August:    MYR {oct_vs_aug['gmv']:+,.2f} ({oct_vs_aug['gmv_pct']:+.2f}%)")
    print(f"   → PRIMARY DRIVER: +6.7% GMV growth from September")
    
    print(f"\n3.2 Average Basket Size:")
    print(f"   October vs September: MYR {oct_vs_sep['avg_basket']:.2f}")
    print(f"   October: MYR {periods['October 2025']['avg_basket']:.2f}")
    print(f"   September: MYR {periods['September 2025']['avg_basket']:.2f}")
    print(f"   → FACTOR: Slight decline in basket size (-MYR 0.40) but offset by volume")
    
    print("\n[D] Promotion & Marketing Factors")
    print("-" * 100)
    
    print(f"\n4.1 Promotion Penetration:")
    print(f"   October: {periods['October 2025']['promo_penetration']:.1f}%")
    print(f"   September: {periods['September 2025']['promo_penetration']:.1f}%")
    print(f"   Change: {oct_vs_sep['promo_penetration']:.1f}pp")
    print(f"   → FACTOR: Slight decrease in promo penetration but higher absolute spend")
    
    print(f"\n4.2 Total Promotion Expense:")
    print(f"   October vs September: MYR {oct_vs_sep['promo_expense']:+,.2f} ({oct_vs_sep['promo_expense_pct']:+.2f}%)")
    print(f"   October: MYR {periods['October 2025']['promo_expense']:,.2f}")
    print(f"   September: MYR {periods['September 2025']['promo_expense']:,.2f}")
    print(f"   → CAUSAL FACTOR: +11.2% increase in promo investment drives order growth")
    
    print(f"\n4.3 Average Promotion Value per Order:")
    print(f"   October vs September: MYR {oct_vs_sep['avg_promo']:+.2f}")
    print(f"   October: MYR {periods['October 2025']['avg_promo']:.2f}")
    print(f"   September: MYR {periods['September 2025']['avg_promo']:.2f}")
    print(f"   → CAUSAL FACTOR: Higher promo value per order (MYR +0.32) increases attractiveness")
    
    print("\n[E] Operational Efficiency Factors")
    print("-" * 100)
    
    print(f"\n5.1 Average Time to Allocate:")
    print(f"   October: {periods['October 2025']['avg_time_to_allocate']:.1f} seconds")
    print(f"   September: {periods['September 2025']['avg_time_to_allocate']:.1f} seconds")
    print(f"   Change: {oct_vs_sep['avg_time_to_allocate']:+.1f} seconds")
    print(f"   → FACTOR: Slight increase in allocation time (may need monitoring)")
    
    print("\n" + "=" * 100)
    print("2. INTER-CAUSAL RELATIONSHIP ANALYSIS")
    print("=" * 100)
    
    print("\n[A] Primary Causal Chain:")
    print("""
    EATER BASE EXPANSION (+4.1%)
         ↓
    More Unique Eaters → More Order Opportunities
         ↓
    ORDER VOLUME GROWTH (+7.4%)
         ↓
    Higher Completion Rate (+0.4pp) → Better Fulfillment
         ↓
    GMV GROWTH (+6.7%)
    """)
    
    print("\n[B] Secondary Causal Factors:")
    print("""
    1. MERCHANT EXPANSION (+2.0%)
       → Increases supply capacity
       → Better order fulfillment options
       → Higher orders per merchant (+5.8%)
    
    2. PROMOTION INVESTMENT (+11.2% spend)
       → Higher promo value per order (+3.7%)
       → Maintains order attractiveness despite lower penetration
       → Drives order frequency
    
    3. OPERATIONAL EFFICIENCY
       → Improved allocation rate (+0.5pp)
       → Better completion rate (+0.4pp)
       → Reduces order loss
    """)
    
    print("\n[C] Compensating Factors:")
    print("""
    1. BASKET SIZE DECLINE (-MYR 0.40)
       → Partially offset by higher order volume
       → Net positive GMV impact due to volume
    
    2. PROMO PENETRATION DECLINE (-0.3pp)
       → Compensated by higher promo value per order
       → Total promo investment still increases
    """)
    
    print("\n" + "=" * 100)
    print("3. DRIVER IMPORTANCE RANKING")
    print("=" * 100)
    
    drivers = [
        {'factor': 'Eater Base Expansion', 'impact': 'HIGH', 'contribution': '+4.1%', 'description': 'Primary driver - 70,862 new eaters'},
        {'factor': 'Order Volume Growth', 'impact': 'HIGH', 'contribution': '+7.4%', 'description': 'Direct result - 544,421 more orders'},
        {'factor': 'Promotion Investment', 'impact': 'HIGH', 'contribution': '+11.2%', 'description': 'MYR 3.2M more promo spend'},
        {'factor': 'Merchant Base Growth', 'impact': 'MEDIUM', 'contribution': '+2.0%', 'description': '+971 new merchants increase supply'},
        {'factor': 'Completion Rate Improvement', 'impact': 'MEDIUM', 'contribution': '+0.4pp', 'description': 'Better fulfillment = +30K more completed orders'},
        {'factor': 'Orders per Merchant', 'impact': 'MEDIUM', 'contribution': '+5.8%', 'description': 'Higher merchant utilization'},
        {'factor': 'Average Promo Value', 'impact': 'MEDIUM', 'contribution': '+3.7%', 'description': 'More attractive promotions'},
        {'factor': 'Allocation Rate Improvement', 'impact': 'LOW', 'contribution': '+0.5pp', 'description': 'Better order allocation'},
        {'factor': 'Basket Size Change', 'impact': 'LOW', 'contribution': '-0.4 MYR', 'description': 'Slight decline, offset by volume'}
    ]
    
    drivers_df = pd.DataFrame(drivers)
    print("\n" + drivers_df.to_string(index=False))
    
    print("\n" + "=" * 100)
    print("4. CITY-LEVEL GROWTH DRIVERS (Top Contributors)")
    print("=" * 100)
    
    city_growth = [
        {'city': 'Johor Bahru', 'oct_orders': 1964877, 'sep_orders': 1815776, 'growth_pct': 8.2, 'order_delta': 149101},
        {'city': 'Kota Kinabalu', 'oct_orders': 635839, 'sep_orders': 576041, 'growth_pct': 10.4, 'order_delta': 59798},
        {'city': 'Kuching', 'oct_orders': 573326, 'sep_orders': 521980, 'growth_pct': 9.8, 'order_delta': 51346},
        {'city': 'Melaka', 'oct_orders': 521968, 'sep_orders': 477378, 'growth_pct': 9.3, 'order_delta': 44590},
        {'city': 'Penang', 'oct_orders': 1285577, 'sep_orders': 1219460, 'growth_pct': 5.4, 'order_delta': 66117},
        {'city': 'Ipoh', 'oct_orders': 729902, 'sep_orders': 705665, 'growth_pct': 3.4, 'order_delta': 24237}
    ]
    
    city_df = pd.DataFrame(city_growth)
    city_df['share_of_total_growth'] = (city_df['order_delta'] / city_df['order_delta'].sum() * 100).round(1)
    print("\n" + city_df.to_string(index=False))
    
    print(f"\n→ Top 3 cities (Johor Bahru, Kota Kinabalu, Kuching) contribute {city_df['share_of_total_growth'].head(3).sum():.1f}% of total growth")
    
    print("\n" + "=" * 100)
    print("5. KEY INSIGHTS & RECOMMENDATIONS")
    print("=" * 100)
    
    print("\n[A] Primary Growth Drivers Identified:")
    print("""
    1. EATER BASE EXPANSION is the #1 driver
       - +70,862 new eaters from September to October
       - Represents 4.1% growth in base
       - Drives volume through new customer acquisition
    
    2. PROMOTION INVESTMENT drives order growth
       - +11.2% increase in total promo spend
       - Higher average promo value per order
       - Maintains attractiveness despite lower penetration
    
    3. MERCHANT EXPANSION increases supply
       - +971 new merchants (+2.0%)
       - Higher orders per merchant (+5.8%)
       - Better fulfillment options
    """)
    
    print("\n[B] Operational Efficiency Improvements:")
    print("""
    1. COMPLETION RATE improvement (+0.4pp)
       - Reduces order loss
       - Better fulfillment quality
    
    2. ALLOCATION RATE improvement (+0.5pp)
       - More orders successfully allocated
       - Better driver-merchant matching
    """)
    
    print("\n[C] Strategic Recommendations:")
    print("""
    1. CONTINUE EATER ACQUISITION
       - Focus on high-growth cities (Johor Bahru, Kota Kinabalu, Kuching)
       - Maintain investment in new eater acquisition channels
    
    2. OPTIMIZE PROMOTION STRATEGY
       - Current high promo investment is driving growth
       - Consider balancing penetration vs value
       - Monitor ROI on promo spend
    
    3. SUSTAIN MERCHANT EXPANSION
       - Continue merchant onboarding, especially in top cities
       - Focus on merchant quality to maintain high utilization
    
    4. MONITOR OPERATIONAL METRICS
       - Maintain high completion rates (currently 91.8%)
       - Monitor allocation time (slight increase noted)
       - Focus on reducing order loss
    
    5. CITY-LEVEL FOCUS
       - Prioritize support for top growth cities
       - Johor Bahru alone contributes 27% of total growth
       - Kota Kinabalu shows highest growth rate (10.4%)
    """)
    
    # Save analysis to CSV
    analysis_summary = pd.DataFrame({
        'Factor': ['Eater Base Expansion', 'Order Volume Growth', 'Promotion Investment', 
                  'Merchant Base Growth', 'Completion Rate Improvement', 'Orders per Merchant',
                  'Average Promo Value', 'Allocation Rate Improvement', 'Basket Size Change'],
        'Impact_Level': ['HIGH', 'HIGH', 'HIGH', 'MEDIUM', 'MEDIUM', 'MEDIUM', 'MEDIUM', 'LOW', 'LOW'],
        'Oct_vs_Sep_Change': [f"+{oct_vs_sep['eaters']:,}", f"+{oct_vs_sep['orders']:,}", 
                              f"MYR {oct_vs_sep['promo_expense']:+,.2f}",
                              f"+{oct_vs_sep['merchants']:,}", f"+{oct_vs_sep['completion_rate']:.1f}pp",
                              f"+{oct_vs_sep['orders_per_merchant']:.1f}", 
                              f"MYR {oct_vs_sep['avg_promo']:+.2f}", 
                              f"+{oct_vs_sep['allocation_rate']:.1f}pp",
                              f"MYR {oct_vs_sep['avg_basket']:.2f}"],
        'Percentage_Change': [f"{oct_vs_sep['eaters_pct']:+.2f}%", f"{oct_vs_sep['orders_pct']:+.2f}%",
                             f"{oct_vs_sep['promo_expense_pct']:+.2f}%", f"{oct_vs_sep['merchants_pct']:+.2f}%",
                             f"{oct_vs_sep['completion_rate_pct']:+.2f}%", f"{oct_vs_sep['orders_per_merchant_pct']:+.1f}%",
                             f"{oct_vs_sep.get('avg_promo_pct', 0):+.2f}%", 
                             f"{oct_vs_sep.get('allocation_rate_pct', 0):+.2f}%",
                             f"{oct_vs_sep['avg_basket_pct']:+.2f}%"]
    })
    
    analysis_summary.to_csv('intercausal_analysis_drivers.csv', index=False, encoding='utf-8')
    print("\n[OK] Saved analysis to: intercausal_analysis_drivers.csv")
    
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    perform_intercausal_analysis()

