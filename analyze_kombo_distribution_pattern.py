#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze Kombo Jimat order distribution across the last 4 days of each month
This script helps identify patterns in how orders are distributed across campaign days
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 100)
print("KOMBO JIMAT DISTRIBUTION PATTERN ANALYSIS")
print("=" * 100)
print("\nPURPOSE:")
print("To understand how Kombo Jimat orders are typically distributed across the")
print("last 4 days of each month historically, so we can apply the correct pattern")
print("to the forecast instead of assuming equal distribution.\n")

print("=" * 100)
print("CURRENT FORECAST DISTRIBUTION (Checking what we have now)")
print("=" * 100)

# Check current forecast
try:
    df = pd.read_csv('kombo_jimat_daily_forecast_2026.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_month'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['days_in_month'] = df['date'].dt.days_in_month
    
    # Get last 4 days for each month
    df['is_last_4_days'] = df['day_of_month'] > (df['days_in_month'] - 4)
    kombo_days = df[df['kombo_jimat_daily_orders'] > 0].copy()
    
    if len(kombo_days) > 0:
        kombo_days['day_position'] = kombo_days['days_in_month'] - kombo_days['day_of_month'] + 1
        
        print("\nCurrent Forecast Distribution (Sample - January 2026):")
        jan_kombo = kombo_days[kombo_days['month'] == 1].sort_values('day_of_month')
        for idx, row in jan_kombo.iterrows():
            print(f"  Day {int(row['day_of_month'])} (Position {int(row['day_position'])} of 4): "
                  f"{row['kombo_jimat_daily_orders']:,.0f} orders")
        
        # Analyze distribution pattern
        print("\nDistribution Pattern Analysis (All months):")
        for month in range(1, 13):
            month_kombo = kombo_days[kombo_days['month'] == month].sort_values('day_of_month')
            if len(month_kombo) == 4:
                orders_list = month_kombo['kombo_jimat_daily_orders'].tolist()
                total = sum(orders_list)
                percentages = [o/total*100 for o in orders_list]
                
                print(f"\nMonth {month}:")
                for i, (day, orders, pct) in enumerate(zip(
                    month_kombo['day_of_month'].tolist(),
                    orders_list,
                    percentages
                ), 1):
                    print(f"  Day {int(day)} ({'Last' if i==1 else f'{5-i}th to last'}): "
                          f"{orders:,.0f} orders ({pct:.1f}%)")
                
                # Check if distribution is equal
                if max(percentages) - min(percentages) < 1:
                    print(f"  [ISSUE] Distribution is almost equal across all 4 days")
                else:
                    max_day = orders_list.index(max(orders_list)) + 1
                    print(f"  [NOTE] Highest day is day {int(month_kombo.iloc[max_day-1]['day_of_month'])}")
    else:
        print("No Kombo Jimat days found in forecast")

except FileNotFoundError:
    print("CSV file not found. Please run the forecast generation first.")

print("\n" + "=" * 100)
print("SQL QUERY NEEDED FOR HISTORICAL ANALYSIS")
print("=" * 100)
print("\nTo analyze historical distribution, please provide:")
print("1. The SQL query you mentioned earlier")
print("2. Or run this SQL query template (modify table/column names as needed):\n")
print("""
SELECT 
    DATE_TRUNC('month', order_date) as month,
    EXTRACT(DAY FROM order_date) as day_of_month,
    COUNT(*) as kombo_jimat_orders,
    SUM(order_value) as kombo_jimat_gmv,
    -- Day position: 1 = 4th last day, 4 = last day
    CASE 
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM 
            (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '1 day')) THEN 4
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM 
            (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '2 day')) THEN 3
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM 
            (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '3 day')) THEN 2
        WHEN EXTRACT(DAY FROM order_date) = EXTRACT(DAY FROM 
            (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '4 day')) THEN 1
    END as day_position
FROM orders_table
WHERE 
    promo_type LIKE '%Kombo Jimat%'
    AND city_id = 13  -- Penang
    AND booking_simple_state = 'COMPLETED'
    AND order_date >= '2024-01-01'
    AND EXTRACT(DAY FROM order_date) > EXTRACT(DAY FROM 
        (DATE_TRUNC('month', order_date) + INTERVAL '1 month' - INTERVAL '5 day'))
GROUP BY month, day_of_month
ORDER BY month, day_of_month DESC
""")

print("\n" + "=" * 100)
print("NEXT STEPS")
print("=" * 100)
print("\n1. Please provide the SQL query results or run the SQL above")
print("2. This script will analyze the distribution pattern:")
print("   - Which day (1st, 2nd, 3rd, or 4th from last) typically has most orders")
print("   - Distribution percentages across the 4 days")
print("   - Whether there's a pattern (e.g., last day highest, first day highest, etc.)")
print("3. Then update the forecast to reflect this historical pattern")


