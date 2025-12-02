#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update forecast generation to use historical Kombo Jimat distribution pattern
This script shows how to incorporate the distribution weights into forecast generation
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_distribution_pattern():
    """Load the Kombo Jimat distribution pattern"""
    with open('kombo_jimat_distribution_pattern.json', 'r') as f:
        return json.load(f)

def apply_distribution_to_forecast(monthly_kombo_orders, distribution_weights):
    """
    Apply historical distribution pattern to monthly Kombo Jimat orders
    
    Args:
        monthly_kombo_orders: Total monthly Kombo Jimat orders
        distribution_weights: [weight_pos1, weight_pos2, weight_pos3, weight_pos4]
                             where weight_pos1 is for 4th last day, weight_pos4 is for last day
    
    Returns:
        dict with daily orders for the 4 campaign days
    """
    return {
        'position_1_4th_last': monthly_kombo_orders * distribution_weights[0],
        'position_2_3rd_last': monthly_kombo_orders * distribution_weights[1],
        'position_3_2nd_last': monthly_kombo_orders * distribution_weights[2],
        'position_4_last': monthly_kombo_orders * distribution_weights[3]
    }

def generate_daily_forecast_with_distribution(forecast_df, distribution_weights):
    """
    Generate daily forecast incorporating Kombo Jimat distribution pattern
    
    Args:
        forecast_df: DataFrame with monthly forecast including 'kombo_jimat_monthly_orders'
        distribution_weights: Distribution weights from historical analysis
    
    Returns:
        DataFrame with daily breakdown including correctly distributed Kombo Jimat orders
    """
    
    print("=" * 100)
    print("UPDATING FORECAST WITH HISTORICAL DISTRIBUTION PATTERN")
    print("=" * 100)
    print("\nDistribution Weights:")
    print(f"  Position 1 (4th last day): {distribution_weights[0]:.3f} ({distribution_weights[0]*100:.1f}%)")
    print(f"  Position 2 (3rd last day): {distribution_weights[1]:.3f} ({distribution_weights[1]*100:.1f}%)")
    print(f"  Position 3 (2nd last day): {distribution_weights[2]:.3f} ({distribution_weights[2]*100:.1f}%)")
    print(f"  Position 4 (LAST day):     {distribution_weights[3]:.3f} ({distribution_weights[3]*100:.1f}%)")
    
    daily_forecast = []
    
    for month, row in forecast_df.iterrows():
        month_date = pd.to_datetime(month)
        days_in_month = month_date.days_in_month
        monthly_kombo_orders = row.get('kombo_jimat_monthly_orders', 0)
        
        if monthly_kombo_orders > 0:
            # Calculate orders for each of the last 4 days
            day_positions = [4, 3, 2, 1]  # Last day, 2nd last, 3rd last, 4th last
            day_orders = []
            
            for i, pos in enumerate(day_positions):
                day_num = days_in_month - pos + 1
                orders = monthly_kombo_orders * distribution_weights[3-i]  # Reverse order
                day_orders.append({
                    'date': month_date.replace(day=day_num),
                    'day_position': pos,
                    'kombo_jimat_orders': orders
                })
            
            daily_forecast.extend(day_orders)
    
    return pd.DataFrame(daily_forecast)

if __name__ == "__main__":
    # Load distribution pattern
    pattern = load_distribution_pattern()
    weights = pattern['distribution_weights']
    
    print("=" * 100)
    print("KOMBO JIMAT DISTRIBUTION PATTERN LOADED")
    print("=" * 100)
    print(f"\nHighest day: Position {pattern['highest_day_position']} (LAST day)")
    print(f"\nUse these weights when distributing monthly Kombo Jimat orders:")
    print(f"  Position 1 (4th last): {weights[0]:.3f} = {weights[0]*100:.1f}%")
    print(f"  Position 2 (3rd last): {weights[1]:.3f} = {weights[1]*100:.1f}%")
    print(f"  Position 3 (2nd last): {weights[2]:.3f} = {weights[2]*100:.1f}%")
    print(f"  Position 4 (LAST):     {weights[3]:.3f} = {weights[3]*100:.1f}%")
    
    print("\n" + "=" * 100)
    print("INTEGRATION INSTRUCTIONS")
    print("=" * 100)
    print("""
To update your forecast generation script:

1. Load the distribution pattern:
   import json
   with open('kombo_jimat_distribution_pattern.json', 'r') as f:
       pattern = json.load(f)
   weights = pattern['distribution_weights']

2. When calculating daily Kombo Jimat orders for the last 4 days of each month:
   
   monthly_kombo_orders = ...  # Your monthly forecast
   
   # Instead of equal distribution (25% each):
   # daily_orders = monthly_kombo_orders / 4  # ❌ WRONG
   
   # Use historical distribution:
   orders_day_4th_last = monthly_kombo_orders * weights[0]  # 7.8%
   orders_day_3rd_last = monthly_kombo_orders * weights[1]  # 11.6%
   orders_day_2nd_last = monthly_kombo_orders * weights[2]  # 27.5%
   orders_day_last = monthly_kombo_orders * weights[3]      # 53.1%
   
3. Apply this to all months in your 2026 forecast
""")
    
    # Example calculation
    print("\n" + "=" * 100)
    print("EXAMPLE CALCULATION")
    print("=" * 100)
    example_monthly = 10000
    print(f"\nFor monthly Kombo Jimat orders = {example_monthly:,}:")
    for i, (pos, weight, label) in enumerate(zip([1, 2, 3, 4], weights, 
                                                  ['4th last', '3rd last', '2nd last', 'LAST']), 1):
        orders = example_monthly * weight
        print(f"  Position {pos} ({label} day): {orders:,.0f} orders ({weight*100:.1f}%)")

