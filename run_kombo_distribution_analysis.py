#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Kombo Jimat distribution analysis and update forecast
This script processes SQL query results and updates the forecast with historical distribution patterns
"""

import pandas as pd
import numpy as np
import sys
from datetime import datetime, timedelta

def analyze_distribution_from_sql_results(sql_results_df):
    """
    Analyze Kombo Jimat order distribution from SQL query results
    
    Expected columns:
    - month: Month (YYYY-MM-01 format or date)
    - day_of_month: Day of month (1-31)
    - kombo_jimat_orders: Number of orders
    - kombo_jimat_gmv_myr: GMV in MYR (or similar)
    - day_position: Position in last 4 days (1 = 4th last, 4 = last day) [optional]
    """
    
    print("=" * 100)
    print("ANALYZING KOMBO JIMAT DISTRIBUTION FROM SQL RESULTS")
    print("=" * 100)
    
    df = sql_results_df.copy()
    
    # Normalize month column
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'])
    else:
        print("ERROR: 'month' column not found in SQL results")
        return None
    
    # Calculate day position if not provided
    if 'day_position' not in df.columns:
        df['day_of_month'] = pd.to_datetime(df['month']).dt.day
        df['days_in_month'] = pd.to_datetime(df['month']).dt.days_in_month
        df['day_position'] = df['days_in_month'] - df['day_of_month'] + 1
    
    # Filter to only last 4 days (positions 1-4)
    df = df[df['day_position'].isin([1, 2, 3, 4])].copy()
    
    print(f"\nTotal campaign days analyzed: {len(df)}")
    print(f"Total months: {df['month'].nunique()}")
    
    # Calculate distribution by day position
    print("\n" + "=" * 100)
    print("DISTRIBUTION BY DAY POSITION")
    print("=" * 100)
    
    # Analyze each month
    monthly_patterns = []
    for month in sorted(df['month'].unique()):
        month_data = df[df['month'] == month].sort_values('day_position')
        
        if len(month_data) >= 3:  # At least 3 days present
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
                    'orders': month_data['kombo_jimat_orders'].sum()
                })
    
    if not monthly_patterns:
        print("\nERROR: No complete months found")
        return None
    
    # Calculate average distribution
    avg_percentages = np.mean([p['percentages'] for p in monthly_patterns], axis=0)
    
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
    
    # Check consistency
    std_devs = np.std([p['percentages'] for p in monthly_patterns], axis=0)
    print(f"\nConsistency (Standard Deviation across months):")
    for i, (pos, std) in enumerate(zip([1, 2, 3, 4], std_devs), 1):
        print(f"  Position {pos}: {std:.1f}% std dev {'[CONSISTENT]' if std < 5 else '[VARIABLE]'}")
    
    return {
        'avg_distribution_pct': avg_percentages.tolist(),
        'distribution_weights': weights.tolist(),
        'highest_day_position': int(max_pos),
        'monthly_patterns': monthly_patterns
    }

def update_forecast_with_distribution(distribution_pattern):
    """
    Update forecast generation to use historical distribution pattern
    This function shows how to update the forecast logic
    """
    
    print("\n" + "=" * 100)
    print("UPDATED FORECAST LOGIC")
    print("=" * 100)
    
    weights = distribution_pattern['distribution_weights']
    day_labels = ['4th last day', '3rd last day', '2nd last day', 'LAST day']
    
    print("\nWhen generating daily forecast for Kombo Jimat days:")
    print("1. Calculate total monthly Kombo Jimat orders")
    print("2. Distribute across last 4 days using these weights:")
    for i, (pos, weight, label) in enumerate(zip([1, 2, 3, 4], weights, day_labels), 1):
        print(f"   Position {pos} ({label}): {weight:.3f} ({weight*100:.1f}%)")
    
    print("\nExample:")
    print("  If monthly Kombo Jimat orders = 10,000:")
    for i, (pos, weight, label) in enumerate(zip([1, 2, 3, 4], weights, day_labels), 1):
        orders = 10000 * weight
        print(f"    Position {pos} ({label}): {orders:,.0f} orders")
    
    return weights

if __name__ == "__main__":
    print("=" * 100)
    print("KOMBO JIMAT DISTRIBUTION ANALYZER")
    print("=" * 100)
    print("\nThis script analyzes historical Kombo Jimat order distribution")
    print("across the last 4 days of each month and updates the forecast.\n")
    
    if len(sys.argv) < 2:
        print("USAGE:")
        print("  python run_kombo_distribution_analysis.py <sql_results_csv_file>")
        print("\nExample:")
        print("  python run_kombo_distribution_analysis.py kombo_jimat_sql_results.csv")
        print("\nExpected CSV columns:")
        print("  - month: Month (YYYY-MM-01 format)")
        print("  - day_of_month: Day of month (1-31)")
        print("  - kombo_jimat_orders: Number of orders")
        print("  - kombo_jimat_gmv_myr: GMV in MYR (optional)")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    try:
        # Load SQL results
        print(f"\nLoading SQL results from: {csv_file}")
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} rows")
        print(f"Columns: {', '.join(df.columns)}")
        
        # Analyze distribution
        pattern = analyze_distribution_from_sql_results(df)
        
        if pattern:
            # Update forecast logic
            weights = update_forecast_with_distribution(pattern)
            
            # Save distribution pattern
            output_file = 'kombo_jimat_distribution_pattern.json'
            import json
            with open(output_file, 'w') as f:
                json.dump({
                    'avg_distribution_pct': pattern['avg_distribution_pct'],
                    'distribution_weights': pattern['distribution_weights'],
                    'highest_day_position': pattern['highest_day_position']
                }, f, indent=2)
            
            print(f"\n" + "=" * 100)
            print("DISTRIBUTION PATTERN SAVED")
            print("=" * 100)
            print(f"\nSaved to: {output_file}")
            print("\nNext step: Update forecast generation script to use these weights")
            
    except FileNotFoundError:
        print(f"ERROR: File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

