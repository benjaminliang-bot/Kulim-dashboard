#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze historical Kombo Jimat order distribution across the last 4 days
This will help identify the actual distribution pattern to apply to forecasts
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_kombo_distribution_from_sql_results(sql_results_df):
    """
    Analyze Kombo Jimat order distribution from SQL query results
    
    Expected SQL results columns:
    - month: Month (YYYY-MM-01 format)
    - day_of_month: Day of month (1-31)
    - kombo_jimat_orders: Number of Kombo Jimat orders
    - kombo_jimat_gmv: GMV from Kombo Jimat orders
    """
    
    print("=" * 100)
    print("HISTORICAL KOMBO JIMAT DISTRIBUTION ANALYSIS")
    print("=" * 100)
    
    df = sql_results_df.copy()
    df['month'] = pd.to_datetime(df['month'])
    
    # Calculate day position (1 = 4th last day, 4 = last day)
    df['day_position'] = None
    for idx, row in df.iterrows():
        month_start = df['month'].dt.to_period('M').dt.start_time
        days_in_month = month_start.dt.days_in_month
        day_of_month = row['day_of_month']
        day_position = days_in_month - day_of_month + 1
        
        if 1 <= day_position <= 4:
            df.loc[idx, 'day_position'] = int(day_position)
    
    # Filter to only last 4 days
    df = df[df['day_position'].isin([1, 2, 3, 4])].copy()
    
    print(f"\nTotal campaign days analyzed: {len(df)}")
    print(f"Total months: {df['month'].nunique()}")
    
    # Analyze distribution by day position
    print("\n" + "=" * 100)
    print("DISTRIBUTION BY DAY POSITION (Across All Months)")
    print("=" * 100)
    
    distribution = df.groupby('day_position').agg({
        'kombo_jimat_orders': ['mean', 'sum', 'std'],
        'kombo_jimat_gmv': ['mean', 'sum']
    }).round(0)
    
    print("\nAverage Orders per Day Position:")
    for position in [1, 2, 3, 4]:
        pos_data = df[df['day_position'] == position]['kombo_jimat_orders']
        if len(pos_data) > 0:
            avg = pos_data.mean()
            total = pos_data.sum()
            pct_of_total = (total / df['kombo_jimat_orders'].sum()) * 100
            print(f"  Position {position} ({'4th last' if position==1 else f'{5-position}th to last' if position<4 else 'LAST'} day): "
                  f"Avg {avg:,.0f} orders, Total {total:,.0f} orders ({pct_of_total:.1f}% of total)")
    
    # Calculate distribution percentages
    monthly_distributions = []
    for month in df['month'].unique():
        month_data = df[df['month'] == month].sort_values('day_position')
        if len(month_data) == 4:
            total_month_orders = month_data['kombo_jimat_orders'].sum()
            percentages = (month_data['kombo_jimat_orders'] / total_month_orders * 100).tolist()
            monthly_distributions.append(percentages)
    
    if monthly_distributions:
        avg_distribution = np.mean(monthly_distributions, axis=0)
        print("\nAverage Distribution Pattern (% of monthly Kombo Jimat orders):")
        for i, (pos, pct) in enumerate(zip([1, 2, 3, 4], avg_distribution), 1):
            day_label = '4th last' if pos == 1 else f'{5-pos}th to last' if pos < 4 else 'LAST'
            print(f"  Position {pos} ({day_label} day): {pct:.1f}%")
        
        # Identify the highest day
        max_pos = np.argmax(avg_distribution) + 1
        print(f"\n[PATTERN IDENTIFIED] Highest day is Position {max_pos} "
              f"({'4th last' if max_pos==1 else f'{5-max_pos}th to last' if max_pos<4 else 'LAST'} day) with {avg_distribution[max_pos-1]:.1f}%")
        
        # Check if distribution is relatively equal
        if max(avg_distribution) - min(avg_distribution) < 5:
            print("[NOTE] Distribution is relatively equal across days")
        else:
            print(f"[NOTE] Distribution varies by up to {max(avg_distribution) - min(avg_distribution):.1f} percentage points")
        
        return {
            'avg_distribution_pct': avg_distribution.tolist(),
            'highest_day_position': int(max_pos),
            'distribution_weights': avg_distribution / avg_distribution.sum()  # Normalized weights
        }
    
    return None

def load_sql_results_from_csv(csv_file):
    """Load SQL results from CSV file"""
    df = pd.read_csv(csv_file)
    return df

def load_sql_results_from_dataframe(df):
    """Load SQL results from DataFrame"""
    return df

# Example usage
if __name__ == "__main__":
    print("=" * 100)
    print("KOMBO JIMAT DISTRIBUTION ANALYZER")
    print("=" * 100)
    print("\nThis script analyzes historical Kombo Jimat order distribution")
    print("across the last 4 days of each month.\n")
    print("USAGE:")
    print("1. Run the SQL query (provided in analyze_kombo_distribution.sql)")
    print("2. Export results to CSV or DataFrame")
    print("3. Load and analyze:")
    print("\n   from analyze_historical_kombo_distribution import analyze_kombo_distribution_from_sql_results")
    print("   import pandas as pd")
    print("   df = pd.read_csv('kombo_jimat_sql_results.csv')")
    print("   pattern = analyze_kombo_distribution_from_sql_results(df)")
    print("\n4. Use the pattern weights to update forecast distribution")


