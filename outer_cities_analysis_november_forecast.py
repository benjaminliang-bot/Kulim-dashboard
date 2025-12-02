#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis of Outer Cities Performance (October 2025) and November 2025 Forecast
Excluding Klang Valley (city_id = 1)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def generate_november_forecast():
    """
    Generate November 2025 forecast based on October 2025 trends and historical patterns
    """
    
    print("=" * 100)
    print("OUTER CITIES PERFORMANCE ANALYSIS - OCTOBER 2025 & NOVEMBER 2025 FORECAST")
    print("=" * 100)
    
    # October 2025 Actual Data (from queries)
    october_data = {
        'total_orders': 7906094,
        'completed_orders': 7259345,
        'completion_rate_pct': 91.8,
        'total_gmv': 274581392.68,
        'avg_basket_size': 33.51,
        'avg_gmv_per_order': 37.82,
        'unique_merchants': 49240,
        'unique_eaters': 1795529,
        'unique_drivers': 53422,
        'total_commission': 59450761.36
    }
    
    # September 2025 Data for comparison
    september_data = {
        'total_orders': 7361673,
        'completed_orders': 6728905,
        'completion_rate_pct': 91.4,
        'total_gmv': 257397369.20,
        'avg_basket_size': 33.91,
        'avg_gmv_per_order': 38.25,
        'unique_merchants': 48269,
        'unique_eaters': 1724667,
        'unique_drivers': 0,  # Not available
        'total_commission': 55645909.92
    }
    
    # August 2025 Data for comparison
    august_data = {
        'total_orders': 7633154,
        'completed_orders': 7001345,
        'completion_rate_pct': 91.7,
        'total_gmv': 264764184.81,
        'avg_basket_size': 33.48,
        'avg_gmv_per_order': 37.82,
        'unique_merchants': 47868,
        'unique_eaters': 1730809,
        'unique_drivers': 0,  # Not available
        'total_commission': 57512729.61
    }
    
    # Calculate growth rates
    oct_sep_order_growth = (october_data['total_orders'] / september_data['total_orders'] - 1) * 100
    oct_sep_gmv_growth = (october_data['total_gmv'] / september_data['total_gmv'] - 1) * 100
    
    # Average growth rate over last 2 months
    avg_order_growth = ((october_data['total_orders'] / september_data['total_orders'] - 1) + 
                        (september_data['total_orders'] / august_data['total_orders'] - 1)) / 2
    
    # Conservative forecast: 50% of recent growth + slight positive trend
    conservative_growth = avg_order_growth * 0.5 + 0.5  # Add 0.5% base growth
    
    # November 2025 Forecast
    november_forecast = {
        'total_orders': int(october_data['total_orders'] * (1 + conservative_growth / 100)),
        'completion_rate_pct': 91.8,  # Maintain current completion rate
        'avg_basket_size': 33.50,  # Slightly lower as seasonal trend
        'unique_merchants': int(october_data['unique_merchants'] * 1.005),  # Slight growth
        'unique_eaters': int(october_data['unique_eaters'] * 1.01),  # Growth in eater base
    }
    
    november_forecast['completed_orders'] = int(november_forecast['total_orders'] * 
                                                 november_forecast['completion_rate_pct'] / 100)
    november_forecast['avg_gmv_per_order'] = november_forecast['avg_basket_size'] + 4.0  # Delivery fee
    november_forecast['total_gmv'] = november_forecast['completed_orders'] * november_forecast['avg_gmv_per_order']
    november_forecast['total_commission'] = november_forecast['total_gmv'] * 0.216  # ~21.6% commission rate
    
    # Calculate forecast change
    forecast_order_change = november_forecast['total_orders'] - october_data['total_orders']
    forecast_gmv_change = november_forecast['total_gmv'] - october_data['total_gmv']
    
    # Print Analysis
    print("\n" + "=" * 100)
    print("OCTOBER 2025 PERFORMANCE SUMMARY (OUTER CITIES - EXCLUDING KLANG VALLEY)")
    print("=" * 100)
    
    print(f"\nKey Metrics:")
    print(f"  Total Orders:         {october_data['total_orders']:,}")
    print(f"  Completed Orders:     {october_data['completed_orders']:,}")
    print(f"  Completion Rate:      {october_data['completion_rate_pct']:.1f}%")
    print(f"  Total GMV:            MYR {october_data['total_gmv']:,.2f}")
    print(f"  Average Basket Size:  MYR {october_data['avg_basket_size']:.2f}")
    print(f"  Average GMV/Order:    MYR {october_data['avg_gmv_per_order']:.2f}")
    print(f"  Total Commission:     MYR {october_data['total_commission']:,.2f}")
    print(f"  Unique Merchants:     {october_data['unique_merchants']:,}")
    print(f"  Unique Eaters:        {october_data['unique_eaters']:,}")
    print(f"  Unique Drivers:       {october_data['unique_drivers']:,}")
    
    print("\n" + "=" * 100)
    print("PERIOD COMPARISON (AUGUST - OCTOBER 2025)")
    print("=" * 100)
    
    comparison_df = pd.DataFrame({
        'Period': ['August 2025', 'September 2025', 'October 2025'],
        'Total Orders': [august_data['total_orders'], september_data['total_orders'], october_data['total_orders']],
        'Total GMV (MYR)': [august_data['total_gmv'], september_data['total_gmv'], october_data['total_gmv']],
        'Avg Basket Size (MYR)': [august_data['avg_basket_size'], september_data['avg_basket_size'], october_data['avg_basket_size']],
        'Completion Rate (%)': [august_data['completion_rate_pct'], september_data['completion_rate_pct'], october_data['completion_rate_pct']],
        'Unique Merchants': [august_data['unique_merchants'], september_data['unique_merchants'], october_data['unique_merchants']],
        'Unique Eaters': [august_data['unique_eaters'], september_data['unique_eaters'], october_data['unique_eaters']]
    })
    
    print("\n" + comparison_df.to_string(index=False))
    
    print(f"\nGrowth vs September:")
    print(f"  Orders Growth:        {oct_sep_order_growth:+.2f}%")
    print(f"  GMV Growth:           {oct_sep_gmv_growth:+.2f}%")
    
    print("\n" + "=" * 100)
    print("NOVEMBER 2025 FORECAST")
    print("=" * 100)
    
    print(f"\nForecast Methodology:")
    print(f"  - Base: October 2025 actual performance")
    print(f"  - Growth Rate: {conservative_growth:.2f}% (conservative estimate)")
    print(f"  - Assumptions:")
    print(f"    * Completion rate maintained at {november_forecast['completion_rate_pct']:.1f}%")
    print(f"    * Slight decline in basket size (seasonal trend)")
    print(f"    * Continued growth in merchant and eater base")
    
    print(f"\nForecast Metrics:")
    print(f"  Total Orders:         {november_forecast['total_orders']:,} ({forecast_order_change:+,})")
    print(f"  Completed Orders:     {november_forecast['completed_orders']:,}")
    print(f"  Completion Rate:      {november_forecast['completion_rate_pct']:.1f}%")
    print(f"  Total GMV:            MYR {november_forecast['total_gmv']:,.2f} ({forecast_gmv_change:+,.2f})")
    print(f"  Average Basket Size:  MYR {november_forecast['avg_basket_size']:.2f}")
    print(f"  Average GMV/Order:    MYR {november_forecast['avg_gmv_per_order']:.2f}")
    print(f"  Total Commission:     MYR {november_forecast['total_commission']:,.2f}")
    print(f"  Unique Merchants:     {november_forecast['unique_merchants']:,}")
    print(f"  Unique Eaters:        {november_forecast['unique_eaters']:,}")
    
    print(f"\nExpected Change vs October:")
    forecast_order_change_pct = (forecast_order_change / october_data['total_orders']) * 100
    forecast_gmv_change_pct = (forecast_gmv_change / october_data['total_gmv']) * 100
    print(f"  Orders Change:        {forecast_order_change_pct:+.2f}%")
    print(f"  GMV Change:           {forecast_gmv_change_pct:+.2f}%")
    
    # Top Cities Performance Summary
    print("\n" + "=" * 100)
    print("TOP 6 CITIES BY GMV (OCTOBER 2025)")
    print("=" * 100)
    
    top_cities = [
        {'city': 'Johor Bahru', 'gmv': 70583146.36, 'orders': 1964877, 'avg_basket': 34.69},
        {'city': 'Penang', 'gmv': 47130877.33, 'orders': 1285577, 'avg_basket': 35.48},
        {'city': 'Ipoh', 'gmv': 23565726.20, 'orders': 729902, 'avg_basket': 31.05},
        {'city': 'Kota Kinabalu', 'gmv': 23562418.10, 'orders': 635839, 'avg_basket': 35.89},
        {'city': 'Kuching', 'gmv': 20924180.99, 'orders': 573326, 'avg_basket': 34.86},
        {'city': 'Melaka', 'gmv': 18017033.86, 'orders': 521968, 'avg_basket': 32.88}
    ]
    
    cities_df = pd.DataFrame(top_cities)
    print("\n" + cities_df.to_string(index=False))
    
    # Category Performance (GrabFood vs Mix Match)
    print("\n" + "=" * 100)
    print("CATEGORY PERFORMANCE (OCTOBER 2025)")
    print("=" * 100)
    
    categories = [
        {'category': 'GrabFood', 'orders': 7905010, 'gmv': 274544923.69, 'avg_basket': 33.51, 'merchants': 49183},
        {'category': 'GrabFood Mix & Match', 'orders': 1084, 'gmv': 36468.99, 'avg_basket': 31.10, 'merchants': 57}
    ]
    
    categories_df = pd.DataFrame(categories)
    categories_df['gmv_share_pct'] = (categories_df['gmv'] / categories_df['gmv'].sum() * 100).round(2)
    print("\n" + categories_df.to_string(index=False))
    
    # Save forecast to CSV
    forecast_data = {
        'period': ['October 2025 (Actual)', 'November 2025 (Forecast)'],
        'total_orders': [october_data['total_orders'], november_forecast['total_orders']],
        'completed_orders': [october_data['completed_orders'], november_forecast['completed_orders']],
        'completion_rate_pct': [october_data['completion_rate_pct'], november_forecast['completion_rate_pct']],
        'total_gmv_myr': [october_data['total_gmv'], november_forecast['total_gmv']],
        'avg_basket_size_myr': [october_data['avg_basket_size'], november_forecast['avg_basket_size']],
        'avg_gmv_per_order_myr': [october_data['avg_gmv_per_order'], november_forecast['avg_gmv_per_order']],
        'total_commission_myr': [october_data['total_commission'], november_forecast['total_commission']],
        'unique_merchants': [october_data['unique_merchants'], november_forecast['unique_merchants']],
        'unique_eaters': [october_data['unique_eaters'], november_forecast['unique_eaters']]
    }
    
    forecast_df = pd.DataFrame(forecast_data)
    forecast_df.to_csv('outer_cities_november_forecast.csv', index=False, encoding='utf-8')
    print("\n[OK] Saved forecast to: outer_cities_november_forecast.csv")
    
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)
    
    return forecast_df

if __name__ == "__main__":
    forecast_df = generate_november_forecast()

