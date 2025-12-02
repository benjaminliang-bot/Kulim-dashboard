#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process SQL query results for Kombo Jimat distribution and update forecast
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# SQL Query Results (from the query execution)
sql_results = [
    {'month': '2025-10-01', 'day_of_month': 30, 'kombo_jimat_orders': 1201, 'kombo_jimat_gmv_myr': 2187.4246},
    {'month': '2025-10-01', 'day_of_month': 29, 'kombo_jimat_orders': 2104, 'kombo_jimat_gmv_myr': 3299.1325},
    {'month': '2025-10-01', 'day_of_month': 28, 'kombo_jimat_orders': 22440, 'kombo_jimat_gmv_myr': 26294.1447},
    {'month': '2025-09-01', 'day_of_month': 28, 'kombo_jimat_orders': 199, 'kombo_jimat_gmv_myr': 466.3042},
    {'month': '2025-09-01', 'day_of_month': 27, 'kombo_jimat_orders': 183, 'kombo_jimat_gmv_myr': 428.8963},
    {'month': '2025-08-01', 'day_of_month': 28, 'kombo_jimat_orders': 738, 'kombo_jimat_gmv_myr': 1273.8555},
    {'month': '2025-07-01', 'day_of_month': 31, 'kombo_jimat_orders': 641, 'kombo_jimat_gmv_myr': 982.4864},
    {'month': '2025-07-01', 'day_of_month': 30, 'kombo_jimat_orders': 1738, 'kombo_jimat_gmv_myr': 2559.7152},
    {'month': '2025-07-01', 'day_of_month': 29, 'kombo_jimat_orders': 20500, 'kombo_jimat_gmv_myr': 22941.5694},
    {'month': '2025-07-01', 'day_of_month': 28, 'kombo_jimat_orders': 18141, 'kombo_jimat_gmv_myr': 19917.0958},
    {'month': '2025-05-01', 'day_of_month': 31, 'kombo_jimat_orders': 5, 'kombo_jimat_gmv_myr': 2.352},
    {'month': '2025-05-01', 'day_of_month': 30, 'kombo_jimat_orders': 295, 'kombo_jimat_gmv_myr': 421.3526},
    {'month': '2025-05-01', 'day_of_month': 29, 'kombo_jimat_orders': 983, 'kombo_jimat_gmv_myr': 1317.1762},
    {'month': '2025-05-01', 'day_of_month': 28, 'kombo_jimat_orders': 6064, 'kombo_jimat_gmv_myr': 7207.0965},
    {'month': '2025-04-01', 'day_of_month': 30, 'kombo_jimat_orders': 9754, 'kombo_jimat_gmv_myr': 12058.7835},
    {'month': '2025-04-01', 'day_of_month': 29, 'kombo_jimat_orders': 17795, 'kombo_jimat_gmv_myr': 19185.321},
    {'month': '2025-04-01', 'day_of_month': 28, 'kombo_jimat_orders': 14987, 'kombo_jimat_gmv_myr': 15544.3503},
    {'month': '2025-04-01', 'day_of_month': 27, 'kombo_jimat_orders': 4387, 'kombo_jimat_gmv_myr': 4065.5694},
    {'month': '2025-02-01', 'day_of_month': 28, 'kombo_jimat_orders': 2265, 'kombo_jimat_gmv_myr': 2224.197},
    {'month': '2025-02-01', 'day_of_month': 27, 'kombo_jimat_orders': 2878, 'kombo_jimat_gmv_myr': 2933.835},
    {'month': '2025-02-01', 'day_of_month': 26, 'kombo_jimat_orders': 7748, 'kombo_jimat_gmv_myr': 8326.6735},
    {'month': '2025-02-01', 'day_of_month': 25, 'kombo_jimat_orders': 12633, 'kombo_jimat_gmv_myr': 13220.0315},
    {'month': '2024-11-01', 'day_of_month': 28, 'kombo_jimat_orders': 452, 'kombo_jimat_gmv_myr': 526.5716},
    {'month': '2024-11-01', 'day_of_month': 27, 'kombo_jimat_orders': 992, 'kombo_jimat_gmv_myr': 1163.6935},
    {'month': '2024-10-01', 'day_of_month': 31, 'kombo_jimat_orders': 319, 'kombo_jimat_gmv_myr': 367.5223},
    {'month': '2024-10-01', 'day_of_month': 30, 'kombo_jimat_orders': 847, 'kombo_jimat_gmv_myr': 939.5992},
    {'month': '2024-10-01', 'day_of_month': 29, 'kombo_jimat_orders': 11616, 'kombo_jimat_gmv_myr': 11080.559},
    {'month': '2024-10-01', 'day_of_month': 28, 'kombo_jimat_orders': 7492, 'kombo_jimat_gmv_myr': 7451.6562},
    {'month': '2024-09-01', 'day_of_month': 30, 'kombo_jimat_orders': 22, 'kombo_jimat_gmv_myr': 46.5502},
    {'month': '2024-08-01', 'day_of_month': 30, 'kombo_jimat_orders': 82, 'kombo_jimat_gmv_myr': 221.6943},
    {'month': '2024-08-01', 'day_of_month': 29, 'kombo_jimat_orders': 268, 'kombo_jimat_gmv_myr': 350.9817},
    {'month': '2024-08-01', 'day_of_month': 28, 'kombo_jimat_orders': 655, 'kombo_jimat_gmv_myr': 761.9775},
    {'month': '2024-07-01', 'day_of_month': 31, 'kombo_jimat_orders': 221, 'kombo_jimat_gmv_myr': 302.1405},
    {'month': '2024-07-01', 'day_of_month': 30, 'kombo_jimat_orders': 5527, 'kombo_jimat_gmv_myr': 5748.1338},
    {'month': '2024-07-01', 'day_of_month': 29, 'kombo_jimat_orders': 4301, 'kombo_jimat_gmv_myr': 4445.9265},
    {'month': '2024-07-01', 'day_of_month': 28, 'kombo_jimat_orders': 1796, 'kombo_jimat_gmv_myr': 1663.4132},
    {'month': '2024-06-01', 'day_of_month': 29, 'kombo_jimat_orders': 116, 'kombo_jimat_gmv_myr': 120.7564},
    {'month': '2024-06-01', 'day_of_month': 28, 'kombo_jimat_orders': 395, 'kombo_jimat_gmv_myr': 403.5603},
    {'month': '2024-06-01', 'day_of_month': 27, 'kombo_jimat_orders': 11592, 'kombo_jimat_gmv_myr': 11263.3036},
    {'month': '2024-05-01', 'day_of_month': 30, 'kombo_jimat_orders': 67, 'kombo_jimat_gmv_myr': 70.1233},
    {'month': '2024-05-01', 'day_of_month': 29, 'kombo_jimat_orders': 169, 'kombo_jimat_gmv_myr': 180.9744},
    {'month': '2024-05-01', 'day_of_month': 28, 'kombo_jimat_orders': 7547, 'kombo_jimat_gmv_myr': 7143.955},
    {'month': '2024-04-01', 'day_of_month': 30, 'kombo_jimat_orders': 4809, 'kombo_jimat_gmv_myr': 4769.9352},
    {'month': '2024-04-01', 'day_of_month': 29, 'kombo_jimat_orders': 1363, 'kombo_jimat_gmv_myr': 1109.2273},
    {'month': '2024-04-01', 'day_of_month': 28, 'kombo_jimat_orders': 1796, 'kombo_jimat_gmv_myr': 1556.6475},
    {'month': '2024-04-01', 'day_of_month': 27, 'kombo_jimat_orders': 1761, 'kombo_jimat_gmv_myr': 1532.4969},
    {'month': '2024-03-01', 'day_of_month': 31, 'kombo_jimat_orders': 1889, 'kombo_jimat_gmv_myr': 1664.8835},
    {'month': '2024-03-01', 'day_of_month': 30, 'kombo_jimat_orders': 1903, 'kombo_jimat_gmv_myr': 1671.1734},
    {'month': '2024-03-01', 'day_of_month': 29, 'kombo_jimat_orders': 1843, 'kombo_jimat_gmv_myr': 1631.4198},
    {'month': '2024-03-01', 'day_of_month': 28, 'kombo_jimat_orders': 1986, 'kombo_jimat_gmv_myr': 1714.1097},
]

def analyze_distribution():
    """Analyze Kombo Jimat distribution pattern from SQL results"""
    
    print("=" * 100)
    print("KOMBO JIMAT DISTRIBUTION ANALYSIS")
    print("=" * 100)
    
    df = pd.DataFrame(sql_results)
    df['month'] = pd.to_datetime(df['month'])
    df['days_in_month'] = df['month'].dt.days_in_month
    df['day_position'] = df['days_in_month'] - df['day_of_month'] + 1
    
    # Filter to only last 4 days (positions 1-4)
    df = df[df['day_position'].isin([1, 2, 3, 4])].copy()
    
    print(f"\nTotal campaign days analyzed: {len(df)}")
    print(f"Total months: {df['month'].nunique()}")
    
    # Analyze each month
    monthly_patterns = []
    for month in sorted(df['month'].unique()):
        month_data = df[df['month'] == month].sort_values('day_position')
        
        if len(month_data) >= 2:  # At least 2 days present
            total_orders = month_data['kombo_jimat_orders'].sum()
            if total_orders > 0:
                percentages = (month_data['kombo_jimat_orders'] / total_orders * 100).tolist()
                positions = month_data['day_position'].tolist()
                
                # Fill missing positions with 0
                full_percentages = [0.0] * 4
                for pos, pct in zip(positions, percentages):
                    if 1 <= pos <= 4:
                        full_percentages[pos - 1] = pct
                
                monthly_patterns.append({
                    'month': str(month)[:7],  # YYYY-MM
                    'percentages': full_percentages,
                    'orders': total_orders,
                    'day_orders': month_data['kombo_jimat_orders'].tolist(),
                    'positions': positions
                })
    
    if not monthly_patterns:
        print("\nERROR: No complete months found")
        return None
    
    # Calculate average distribution
    avg_percentages = np.mean([p['percentages'] for p in monthly_patterns], axis=0)
    
    print("\n" + "=" * 100)
    print("DISTRIBUTION BY DAY POSITION")
    print("=" * 100)
    print("\nAverage Distribution Pattern (% of monthly Kombo Jimat orders):")
    day_labels = ['4th last day', '3rd last day', '2nd last day', 'LAST day']
    for i, (pos, pct) in enumerate(zip([1, 2, 3, 4], avg_percentages), 1):
        print(f"  Position {pos} ({day_labels[i-1]}): {pct:.1f}%")
    
    # Calculate normalized weights (sum to 1.0)
    weights = avg_percentages / 100.0
    weights = weights / weights.sum()  # Ensure they sum to 1.0
    
    # Identify highest day
    max_idx = np.argmax(avg_percentages)
    max_pos = max_idx + 1
    
    print(f"\n[PATTERN] Highest day: Position {max_pos} ({day_labels[max_idx]}) with {avg_percentages[max_idx]:.1f}%")
    print(f"Normalized weights: {[f'{w:.3f}' for w in weights]}")
    
    # Show monthly breakdowns
    print("\n" + "=" * 100)
    print("MONTHLY BREAKDOWNS")
    print("=" * 100)
    for pattern in monthly_patterns[:10]:  # Show first 10
        print(f"\n{pattern['month']}:")
        for i, (pos, pct) in enumerate(zip(pattern['positions'], [p*100/total if total > 0 else 0 for p, total in zip(pattern['day_orders'], [sum(pattern['day_orders'])]*len(pattern['day_orders']))]), 1):
            if i <= len(pattern['positions']):
                pos_idx = pattern['positions'][i-1] - 1
                pct_val = pattern['percentages'][pos_idx]
                print(f"  Position {pattern['positions'][i-1]}: {pct_val:.1f}% ({pattern['day_orders'][i-1]:,} orders)")
    
    # Check consistency
    std_devs = np.std([p['percentages'] for p in monthly_patterns], axis=0)
    print(f"\n" + "=" * 100)
    print("CONSISTENCY ANALYSIS")
    print("=" * 100)
    print("\nStandard Deviation across months:")
    for i, (pos, std) in enumerate(zip([1, 2, 3, 4], std_devs), 1):
        consistency = 'CONSISTENT' if std < 10 else 'VARIABLE' if std < 20 else 'HIGHLY VARIABLE'
        print(f"  Position {pos}: {std:.1f}% std dev [{consistency}]")
    
    # Save distribution pattern (convert numpy types to native Python types)
    pattern_data = {
        'avg_distribution_pct': [float(x) for x in avg_percentages.tolist()],
        'distribution_weights': [float(x) for x in weights.tolist()],
        'highest_day_position': int(max_pos),
        'monthly_patterns': [
            {
                'month': p['month'],
                'percentages': [float(x) for x in p['percentages']],
                'orders': int(p['orders']),
                'day_orders': [int(x) for x in p['day_orders']],
                'positions': [int(x) for x in p['positions']]
            }
            for p in monthly_patterns
        ]
    }
    
    with open('kombo_jimat_distribution_pattern.json', 'w') as f:
        json.dump(pattern_data, f, indent=2)
    
    print(f"\n" + "=" * 100)
    print("DISTRIBUTION PATTERN SAVED")
    print("=" * 100)
    print(f"\nSaved to: kombo_jimat_distribution_pattern.json")
    print("\nUse these weights in forecast generation:")
    print(f"  Position 1 (4th last): {weights[0]:.3f} ({weights[0]*100:.1f}%)")
    print(f"  Position 2 (3rd last): {weights[1]:.3f} ({weights[1]*100:.1f}%)")
    print(f"  Position 3 (2nd last): {weights[2]:.3f} ({weights[2]*100:.1f}%)")
    print(f"  Position 4 (LAST):     {weights[3]:.3f} ({weights[3]*100:.1f}%)")
    
    return pattern_data

if __name__ == "__main__":
    pattern = analyze_distribution()

