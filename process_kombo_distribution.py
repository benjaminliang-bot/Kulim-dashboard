#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process SQL query results and update forecast with correct distribution pattern
"""

import pandas as pd
import numpy as np
import sys

def process_sql_results_and_get_pattern(sql_results_file):
    """
    Process SQL results file and return distribution pattern
    
    Args:
        sql_results_file: Path to CSV file with SQL query results
                          Expected columns: month, day_of_month, kombo_jimat_orders, kombo_jimat_gmv
    
    Returns:
        dict with distribution pattern and weights
    """
    
    print("=" * 100)
    print("PROCESSING SQL RESULTS FOR KOMBO JIMAT DISTRIBUTION")
    print("=" * 100)
    
    # Load SQL results
    try:
        df = pd.read_csv(sql_results_file)
        print(f"\nLoaded SQL results: {len(df)} rows")
        print(f"Columns: {', '.join(df.columns)}")
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    
    # Ensure required columns exist
    required_cols = ['month', 'day_of_month', 'kombo_jimat_orders']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"\nERROR: Missing required columns: {', '.join(missing_cols)}")
        print(f"Available columns: {', '.join(df.columns)}")
        return None
    
    # Convert month to datetime
    df['month'] = pd.to_datetime(df['month'])
    df['year_month'] = df['month'].dt.to_period('M')
    
    # Calculate day position (how many days from end of month)
    # Position 1 = 4th last day, Position 4 = last day
    df['days_in_month'] = df['month'].dt.days_in_month
    df['day_position'] = df['days_in_month'] - df['day_of_month'] + 1
    
    # Filter to only last 4 days (positions 1-4)
    df = df[df['day_position'].isin([1, 2, 3, 4])].copy()
    
    print(f"\nFiltered to last 4 days: {len(df)} rows")
    print(f"Months analyzed: {df['year_month'].nunique()}")
    
    # Analyze distribution by day position
    print("\n" + "=" * 100)
    print("DISTRIBUTION ANALYSIS BY DAY POSITION")
    print("=" * 100)
    
    # Calculate distribution for each month
    monthly_patterns = []
    
    for year_month in sorted(df['year_month'].unique()):
        month_data = df[df['year_month'] == year_month].sort_values('day_position')
        
        if len(month_data) == 4:  # All 4 days present
            total_orders = month_data['kombo_jimat_orders'].sum()
            if total_orders > 0:
                percentages = (month_data['kombo_jimat_orders'] / total_orders * 100).tolist()
                monthly_patterns.append({
                    'month': str(year_month),
                    'positions': month_data['day_position'].tolist(),
                    'orders': month_data['kombo_jimat_orders'].tolist(),
                    'percentages': percentages
                })
    
    if not monthly_patterns:
        print("\nERROR: No complete months found with all 4 campaign days")
        return None
    
    # Calculate average distribution
    avg_percentages = np.mean([p['percentages'] for p in monthly_patterns], axis=0)
    avg_orders = np.mean([p['orders'] for p in monthly_patterns], axis=0)
    
    print("\nAverage Distribution Pattern:")
    day_labels = ['4th last day', '3rd last day', '2nd last day', 'LAST day']
    for i, (pos, pct, orders) in enumerate(zip([1, 2, 3, 4], avg_percentages, avg_orders)):
        print(f"  Position {pos} ({day_labels[i]}): {pct:.1f}% | Avg {orders:,.0f} orders")
    
    # Calculate normalized weights (sum to 1.0)
    weights = avg_percentages / 100.0
    
    # Identify highest day
    max_idx = np.argmax(avg_percentages)
    max_pos = max_idx + 1
    
    print(f"\n[PATTERN] Highest day: Position {max_pos} ({day_labels[max_idx]}) with {avg_percentages[max_idx]:.1f}%")
    print(f"Distribution weights: {weights.round(3).tolist()}")
    
    # Check consistency
    std_devs = np.std([p['percentages'] for p in monthly_patterns], axis=0)
    print(f"\nConsistency (Standard Deviation across months):")
    for i, (pos, std) in enumerate(zip([1, 2, 3, 4], std_devs)):
        print(f"  Position {pos}: {std:.1f}% std dev {'[CONSISTENT]' if std < 5 else '[VARIABLE]'}")
    
    return {
        'avg_distribution_pct': avg_percentages.tolist(),
        'distribution_weights': weights.tolist(),
        'highest_day_position': int(max_pos),
        'avg_orders_by_position': avg_orders.tolist(),
        'monthly_patterns': monthly_patterns
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_kombo_distribution.py <sql_results_csv_file>")
        print("\nExample:")
        print("  python process_kombo_distribution.py kombo_jimat_sql_results.csv")
        sys.exit(1)
    
    sql_results_file = sys.argv[1]
    pattern = process_sql_results_and_get_pattern(sql_results_file)
    
    if pattern:
        print("\n" + "=" * 100)
        print("DISTRIBUTION PATTERN SUMMARY")
        print("=" * 100)
        print(f"\nUse these weights in forecast generation:")
        print(f"  Day Position 1 (4th last): {pattern['distribution_weights'][0]:.3f}")
        print(f"  Day Position 2 (3rd last): {pattern['distribution_weights'][1]:.3f}")
        print(f"  Day Position 3 (2nd last): {pattern['distribution_weights'][2]:.3f}")
        print(f"  Day Position 4 (LAST):     {pattern['distribution_weights'][3]:.3f}")
        print(f"\nHighest day: Position {pattern['highest_day_position']}")


