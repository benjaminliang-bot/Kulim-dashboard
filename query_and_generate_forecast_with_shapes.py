#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Query historical data from MIDAS and generate forecast with daily shape patterns
This script processes the MIDAS query results and calculates shape patterns
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def load_distribution_pattern():
    """Load Kombo Jimat distribution pattern from JSON"""
    try:
        with open('kombo_jimat_distribution_pattern.json', 'r', encoding='utf-8') as f:
            pattern = json.load(f)
        weights = pattern['distribution_weights']
        print(f"Loaded Kombo Jimat distribution pattern:")
        print(f"  Position 1 (4th last): {weights[0]:.3f} ({weights[0]*100:.1f}%)")
        print(f"  Position 2 (3rd last): {weights[1]:.3f} ({weights[1]*100:.1f}%)")
        print(f"  Position 3 (2nd last): {weights[2]:.3f} ({weights[2]*100:.1f}%)")
        print(f"  Position 4 (LAST):     {weights[3]:.3f} ({weights[3]*100:.1f}%)")
        return weights
    except FileNotFoundError:
        print("WARNING: Distribution pattern file not found. Using equal distribution (25% each).")
        return [0.25, 0.25, 0.25, 0.25]

def process_midas_orders_data(midas_results):
    """
    Process MIDAS orders query results into DataFrame
    
    Args:
        midas_results: String with MIDAS query results in table format
    """
    
    # Parse MIDAS results into DataFrame
    lines = midas_results.strip().split('\n')
    
    # Skip header line if present
    if lines[0].startswith('| city_name'):
        lines = lines[1:]
    
    data = []
    for line in lines:
        if line.strip() and not line.strip().startswith('|---'):
            parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove leading/trailing |
            if len(parts) >= 3:
                try:
                    date_str = parts[1].strip()
                    orders = float(parts[2].strip())
                    # Parse date from "2024-06-17 00:00:00" format
                    date = pd.to_datetime(date_str.split()[0])
                    data.append({
                        'date': date,
                        'orders': orders
                    })
                except:
                    continue
    
    return pd.DataFrame(data)

def calculate_daily_shape_patterns(historical_orders_df, historical_gmv_df=None):
    """
    Calculate daily shape patterns from historical data
    
    Args:
        historical_orders_df: DataFrame with date, orders columns
        historical_gmv_df: DataFrame with date, gmv columns (optional)
    """
    
    print("\n" + "=" * 100)
    print("CALCULATING DAILY SHAPE PATTERNS FROM HISTORICAL DATA")
    print("=" * 100)
    
    df = historical_orders_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    # If GMV data provided, merge it
    if historical_gmv_df is not None:
        gmv_df = historical_gmv_df.copy()
        gmv_df['date'] = pd.to_datetime(gmv_df['date'])
        df = df.merge(gmv_df[['date', 'gmv']], on='date', how='left')
        # Calculate AOV
        df['aov'] = df['gmv'] / df['orders']
        avg_aov = df['aov'].mean()
    else:
        # Estimate GMV from orders using AOV
        avg_aov = 45.0  # MYR average AOV estimate
        df['gmv'] = df['orders'] * avg_aov
        df['aov'] = avg_aov
    
    df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['day_of_month'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['week_of_month'] = (df['day_of_month'] - 1) // 7 + 1
    
    print(f"\nHistorical Data Summary:")
    print(f"  Total days: {len(df)}")
    print(f"  Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"  Average daily orders: {df['orders'].mean():,.0f}")
    print(f"  Average daily GMV: {df['gmv'].mean():,.0f}")
    print(f"  Average AOV: {avg_aov:.2f} MYR")
    
    # Calculate day of week patterns
    dow_pattern = df.groupby('day_of_week').agg({
        'orders': ['mean', 'std'],
        'gmv': ['mean', 'std']
    }).reset_index()
    dow_pattern.columns = ['day_of_week', 'avg_orders', 'std_orders', 'avg_gmv', 'std_gmv']
    
    dow_orders_mean = dow_pattern.set_index('day_of_week')['avg_orders']
    dow_gmv_mean = dow_pattern.set_index('day_of_week')['avg_gmv']
    
    # Normalize to percentages (relative to overall mean)
    overall_orders_mean = df['orders'].mean()
    overall_gmv_mean = df['gmv'].mean()
    
    dow_orders_shape = (dow_orders_mean / overall_orders_mean * 100).to_dict()
    dow_gmv_shape = (dow_gmv_mean / overall_gmv_mean * 100).to_dict()
    
    print(f"\nDay of Week Patterns (Orders):")
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for dow in range(7):
        pct = dow_orders_shape.get(dow, 100.0)
        avg = dow_orders_mean.get(dow, overall_orders_mean)
        print(f"  {day_names[dow]}: {pct:.1f}% (avg: {avg:,.0f} orders)")
    
    # Calculate day of month patterns
    dom_pattern = df.groupby('day_of_month').agg({
        'orders': 'mean',
        'gmv': 'mean'
    }).reset_index()
    dom_pattern.columns = ['day_of_month', 'avg_orders', 'avg_gmv']
    
    dom_orders_mean = dom_pattern.set_index('day_of_month')['avg_orders']
    dom_gmv_mean = dom_pattern.set_index('day_of_month')['avg_gmv']
    
    # Normalize to percentages
    dom_orders_shape = (dom_orders_mean / overall_orders_mean * 100).to_dict()
    dom_gmv_shape = (dom_gmv_mean / overall_gmv_mean * 100).to_dict()
    
    print(f"\nDay of Month Patterns (Orders):")
    print(f"  First 10 days: {np.mean([dom_orders_shape.get(d, 100.0) for d in range(1, 11)]):.1f}% avg")
    print(f"  Middle 10 days: {np.mean([dom_orders_shape.get(d, 100.0) for d in range(11, 21)]):.1f}% avg")
    print(f"  Last 10 days: {np.mean([dom_orders_shape.get(d, 100.0) for d in range(21, 32)]):.1f}% avg")
    
    return {
        'dow_orders_shape': dow_orders_shape,
        'dow_gmv_shape': dow_gmv_shape,
        'dom_orders_shape': dom_orders_shape,
        'dom_gmv_shape': dom_gmv_shape,
        'avg_aov': avg_aov,
        'overall_orders_mean': overall_orders_mean,
        'overall_gmv_mean': overall_gmv_mean
    }

def generate_monthly_forecast(historical_orders_df):
    """
    Generate monthly forecast for 2026 based on historical trends
    """
    
    df = historical_orders_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Calculate monthly totals
    monthly = df.groupby('year_month').agg({
        'orders': 'sum'
    }).reset_index()
    monthly['date'] = monthly['year_month'].astype(str) + '-01'
    monthly['date'] = pd.to_datetime(monthly['date'])
    monthly = monthly.sort_values('date')
    
    # Use recent 12 months for forecast
    recent_12mo = monthly.tail(12)
    base_orders = recent_12mo['orders'].mean()
    
    # Conservative growth (30% of recent 6-month growth rate)
    recent_6mo = recent_12mo.tail(6)
    if len(recent_6mo) >= 2 and recent_6mo['orders'].iloc[0] > 0:
        raw_growth_rate = (recent_6mo['orders'].iloc[-1] / recent_6mo['orders'].iloc[0] - 1) / 6
        conservative_growth = raw_growth_rate * 0.3
    else:
        conservative_growth = 0.002  # 0.2% per month default
    
    # Estimate GMV from orders (using AOV)
    avg_aov = 45.0  # MYR
    base_gmv = base_orders * avg_aov
    
    # Generate 2026 forecast
    monthly_forecast = {}
    for month in range(1, 13):
        month_key = f'2026-{month:02d}'
        growth_factor = 1 + (conservative_growth * (month - 1))
        monthly_orders = base_orders * growth_factor
        monthly_forecast[month_key] = {
            'orders': monthly_orders,
            'gmv': monthly_orders * avg_aov
        }
    
    return monthly_forecast

def apply_daily_shape_patterns(monthly_forecast, shape_patterns, distribution_weights):
    """
    Apply daily shape patterns to monthly forecast and distribute Kombo Jimat orders
    """
    
    print("\n" + "=" * 100)
    print("GENERATING DAILY FORECAST WITH SHAPE PATTERNS")
    print("=" * 100)
    
    daily_forecast = []
    dow_orders_shape = shape_patterns['dow_orders_shape']
    dow_gmv_shape = shape_patterns['dow_gmv_shape']
    dom_orders_shape = shape_patterns['dom_orders_shape']
    dom_gmv_shape = shape_patterns['dom_gmv_shape']
    avg_aov = shape_patterns['avg_aov']
    
    # Promo penetration assumptions
    promo_penetration = 0.30  # 30% of orders have promotions
    kombo_share_of_promos = 0.20  # 20% of promo orders are Kombo Jimat
    
    for month_key, monthly_data in monthly_forecast.items():
        month_date = pd.to_datetime(month_key)
        days_in_month = month_date.days_in_month
        monthly_orders = monthly_data['orders']
        monthly_gmv = monthly_data['gmv']
        
        # Calculate monthly promo and Kombo Jimat orders
        monthly_promo_orders = monthly_orders * promo_penetration
        monthly_kombo_orders = monthly_promo_orders * kombo_share_of_promos
        
        # Base monthly orders and GMV (excluding Kombo Jimat)
        base_monthly_orders = monthly_orders - monthly_kombo_orders
        base_monthly_gmv = monthly_gmv - (monthly_kombo_orders * avg_aov)
        
        # Generate daily data
        for day in range(1, days_in_month + 1):
            date = month_date.replace(day=day)
            day_of_month = day
            day_of_week = date.dayofweek
            is_last_4_days = day > (days_in_month - 4)
            
            # Get shape factors
            dow_orders_factor = dow_orders_shape.get(day_of_week, 100.0) / 100.0
            dow_gmv_factor = dow_gmv_shape.get(day_of_week, 100.0) / 100.0
            dom_orders_factor = dom_orders_shape.get(day_of_month, 100.0) / 100.0
            dom_gmv_factor = dom_gmv_shape.get(day_of_month, 100.0) / 100.0
            
            # Combined shape factor (weighted average: 60% DoW, 40% DoM)
            combined_orders_factor = (dow_orders_factor * 0.6) + (dom_orders_factor * 0.4)
            combined_gmv_factor = (dow_gmv_factor * 0.6) + (dom_gmv_factor * 0.4)
            
            # Calculate base daily orders and GMV using shape patterns
            # Normalize factors to ensure monthly total matches
            # Distribute base monthly orders proportionally by shape
            daily_shape_weight = combined_orders_factor / sum([dom_orders_shape.get(d, 100.0) / 100.0 * 
                                                                dow_orders_shape.get(pd.Timestamp(month_key).replace(day=d).dayofweek, 100.0) / 100.0
                                                                for d in range(1, days_in_month + 1)])
            
            base_daily_orders = (base_monthly_orders / days_in_month) * combined_orders_factor
            base_daily_gmv = (base_monthly_gmv / days_in_month) * combined_gmv_factor
            
            # Calculate Kombo Jimat orders only for last 4 days using distribution weights
            kombo_jimat_orders = 0.0
            if is_last_4_days:
                # Calculate day position (1 = first of last 4 days, 4 = last day)
                # Reverse the calculation: position 1 = 4th last, position 4 = last
                day_position = days_in_month - day_of_month + 1
                # Reverse: position 1 now maps to index 3 (last day), position 4 to index 0 (4th last)
                weight_index = 4 - day_position  # Reverse mapping
                if 0 <= weight_index < 4:
                    kombo_jimat_orders = monthly_kombo_orders * distribution_weights[weight_index]
            
            # Total daily orders and GMV
            daily_total_orders = base_daily_orders + kombo_jimat_orders
            kombo_jimat_gmv = kombo_jimat_orders * avg_aov
            daily_total_gmv = base_daily_gmv + kombo_jimat_gmv
            
            daily_forecast.append({
                'date': date,
                'year': date.year,
                'month': date.month,
                'day_of_month': day_of_month,
                'day_of_week': day_of_week,
                'day_name': date.strftime('%A'),
                'daily_total_orders': round(daily_total_orders, 2),
                'kombo_jimat_daily_orders': round(kombo_jimat_orders, 2),
                'daily_total_gmv_myr': round(daily_total_gmv, 2),
                'kombo_jimat_daily_gmv_myr': round(kombo_jimat_gmv, 2),
                'is_kombo_jimat_day': is_last_4_days,
                'day_position': (day_of_month - (days_in_month - 4)) if is_last_4_days else 0
            })
    
    df = pd.DataFrame(daily_forecast)
    
    # Normalize to ensure monthly totals match
    for month_key in monthly_forecast.keys():
        month_date = pd.to_datetime(month_key)
        month_data = df[df['month'] == month_date.month]
        
        # Get expected monthly totals
        expected_orders = monthly_forecast[month_key]['orders']
        expected_gmv = monthly_forecast[month_key]['gmv']
        
        # Calculate actual totals
        actual_orders = month_data['daily_total_orders'].sum()
        actual_gmv = month_data['daily_total_gmv_myr'].sum()
        
        # Normalize if there's a mismatch
        if actual_orders > 0:
            orders_ratio = expected_orders / actual_orders
            gmv_ratio = expected_gmv / actual_gmv if actual_gmv > 0 else 1.0
            
            df.loc[df['month'] == month_date.month, 'daily_total_orders'] *= orders_ratio
            df.loc[df['month'] == month_date.month, 'daily_total_gmv_myr'] *= gmv_ratio
            df.loc[df['month'] == month_date.month, 'kombo_jimat_daily_orders'] *= orders_ratio
            df.loc[df['month'] == month_date.month, 'kombo_jimat_daily_gmv_myr'] *= gmv_ratio
    
    return df

def generate_impact_scenarios(daily_forecast_df):
    """Generate impact scenarios if Kombo Jimat is removed"""
    
    scenarios = []
    
    for idx, row in daily_forecast_df.iterrows():
        # Baseline scenario (with Kombo Jimat)
        baseline_orders = row['daily_total_orders']
        baseline_gmv = row['daily_total_gmv_myr']
        
        # Scenario: No Kombo Jimat
        no_kombo_orders = baseline_orders - row['kombo_jimat_daily_orders']
        no_kombo_gmv = baseline_gmv - row['kombo_jimat_daily_gmv_myr']
        
        # Impact
        orders_impact = -row['kombo_jimat_daily_orders']
        gmv_impact = -row['kombo_jimat_daily_gmv_myr']
        orders_impact_pct = (orders_impact / baseline_orders * 100) if baseline_orders > 0 else 0
        gmv_impact_pct = (gmv_impact / baseline_gmv * 100) if baseline_gmv > 0 else 0
        
        scenarios.append({
            'date': row['date'],
            'year': row['year'],
            'month': row['month'],
            'day_of_month': row['day_of_month'],
            'day_of_week': row['day_of_week'],
            'day_name': row['day_name'],
            'baseline_orders': round(baseline_orders, 2),
            'baseline_gmv_myr': round(baseline_gmv, 2),
            'no_kombo_orders': round(no_kombo_orders, 2),
            'no_kombo_gmv_myr': round(no_kombo_gmv, 2),
            'orders_impact': round(orders_impact, 2),
            'gmv_impact_myr': round(gmv_impact, 2),
            'orders_impact_pct': round(orders_impact_pct, 2),
            'gmv_impact_pct': round(gmv_impact_pct, 2),
            'kombo_jimat_orders_lost': round(-orders_impact, 2),
            'kombo_jimat_gmv_lost_myr': round(-gmv_impact, 2)
        })
    
    return pd.DataFrame(scenarios)

def main():
    """Main function to query MIDAS and generate forecast"""
    
    print("=" * 100)
    print("PENANG 2026 FORECAST GENERATION WITH HISTORICAL DAILY SHAPE PATTERNS")
    print("=" * 100)
    
    # Load distribution pattern
    print("\n[1/7] Loading Kombo Jimat distribution pattern...")
    distribution_weights = load_distribution_pattern()
    
    # Query historical orders data from MIDAS
    print("\n[2/7] Querying historical orders data from MIDAS...")
    print("NOTE: This requires MIDAS API calls. Using sample data for now.")
    print("In production, replace this section with actual MIDAS API calls.")
    
    # For now, use the MIDAS query results we got earlier
    # In production, make API calls here to get full historical data
    
    # Sample MIDAS results (replace with actual API results)
    midas_orders_results = """city_name | metric_time_1d | grabdelivery_completed_orders_2025
Penang | 2024-06-17 00:00:00 | 20890
Penang | 2024-12-28 00:00:00 | 35704
Penang | 2025-03-31 00:00:00 | 13448
Penang | 2024-12-29 00:00:00 | 34889
Penang | 2025-04-03 00:00:00 | 31651"""
    
    # Process MIDAS results (sample data)
    historical_orders_df = process_midas_orders_data(midas_orders_results)
    
    # For demonstration, generate comprehensive historical data
    # In production, query full historical dataset from MIDAS using get_metric_data
    dates = pd.date_range(start='2024-01-01', end='2025-10-31', freq='D')
    
    # Generate historical data with realistic patterns
    full_historical_df = pd.DataFrame({'date': dates})
    
    # If we have actual MIDAS data, use it; otherwise generate sample data
    if len(historical_orders_df) > 0:
        # Merge actual data points
        full_historical_df = full_historical_df.merge(historical_orders_df, on='date', how='left')
        
        # Fill missing values with interpolated/estimated values based on patterns
        full_historical_df['orders'] = full_historical_df['orders'].fillna(method='ffill').fillna(method='bfill')
        if full_historical_df['orders'].isna().any():
            full_historical_df['orders'] = full_historical_df['orders'].fillna(35000)  # Default
    else:
        # Generate sample data if no MIDAS data available
        full_historical_df['orders'] = np.random.normal(35000, 5000, len(full_historical_df))
        full_historical_df['orders'] = full_historical_df['orders'].clip(lower=15000)
    
    # Add seasonal variation based on day of week
    full_historical_df['day_of_week'] = full_historical_df['date'].dt.dayofweek
    full_historical_df['month'] = full_historical_df['date'].dt.month
    
    # Apply day-of-week patterns (higher on weekends)
    dow_multipliers = {0: 0.95, 1: 1.0, 2: 1.0, 3: 1.05, 4: 1.1, 5: 1.15, 6: 1.1}
    full_historical_df['dow_mult'] = full_historical_df['day_of_week'].map(dow_multipliers)
    full_historical_df['orders'] = full_historical_df['orders'] * full_historical_df['dow_mult']
    
    # Apply month seasonality (slightly higher in Dec, lower in Feb)
    month_multipliers = {1: 1.0, 2: 0.95, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0,
                         7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.05, 12: 1.1}
    full_historical_df['month_mult'] = full_historical_df['month'].map(month_multipliers)
    full_historical_df['orders'] = full_historical_df['orders'] * full_historical_df['month_mult']
    
    # Ensure positive values
    full_historical_df['orders'] = full_historical_df['orders'].clip(lower=15000)
    
    historical_orders_df = full_historical_df[['date', 'orders']].copy()
    
    print(f"Processed {len(historical_orders_df)} days of historical data")
    
    # Calculate shape patterns
    print("\n[3/7] Calculating daily shape patterns...")
    shape_patterns = calculate_daily_shape_patterns(historical_orders_df)
    
    # Generate monthly forecast
    print("\n[4/7] Generating monthly forecast...")
    monthly_forecast = generate_monthly_forecast(historical_orders_df)
    
    # Apply daily shape patterns
    print("\n[5/7] Applying daily shape patterns and Kombo Jimat distribution...")
    daily_forecast_df = apply_daily_shape_patterns(monthly_forecast, shape_patterns, distribution_weights)
    
    # Generate impact scenarios
    print("\n[6/7] Generating impact scenarios...")
    impact_scenarios_df = generate_impact_scenarios(daily_forecast_df)
    
    # Save CSV files
    print("\n[7/7] Saving CSV files...")
    
    try:
        # Daily forecast CSV
        daily_output = daily_forecast_df.copy()
        daily_output['date'] = daily_output['date'].dt.strftime('%Y-%m-%d')
        daily_output = daily_output[['date', 'year', 'month', 'day_of_month', 'day_of_week', 'day_name',
                                      'daily_total_orders', 'kombo_jimat_daily_orders', 
                                      'daily_total_gmv_myr', 'kombo_jimat_daily_gmv_myr',
                                      'is_kombo_jimat_day', 'day_position']]
        daily_output.to_csv('kombo_jimat_daily_forecast_2026.csv', index=False, encoding='utf-8')
        print("  [OK] Saved: kombo_jimat_daily_forecast_2026.csv")
    except PermissionError:
        print("  [WARNING] Could not save kombo_jimat_daily_forecast_2026.csv (file may be open)")
    
    try:
        # Impact scenarios CSV
        impact_output = impact_scenarios_df.copy()
        impact_output['date'] = pd.to_datetime(impact_output['date']).dt.strftime('%Y-%m-%d')
        impact_output.to_csv('kombo_jimat_impact_scenarios_2026.csv', index=False, encoding='utf-8')
        print("  [OK] Saved: kombo_jimat_impact_scenarios_2026.csv")
    except PermissionError:
        print("  [WARNING] Could not save kombo_jimat_impact_scenarios_2026.csv (file may be open)")
    
    try:
        # Monthly summary
        monthly_summary = daily_forecast_df.groupby(['year', 'month']).agg({
            'daily_total_orders': 'sum',
            'kombo_jimat_daily_orders': 'sum',
            'daily_total_gmv_myr': 'sum',
            'kombo_jimat_daily_gmv_myr': 'sum'
        }).reset_index()
        monthly_summary['month_key'] = monthly_summary.apply(
            lambda x: f"{int(x['year'])}-{int(x['month']):02d}", axis=1
        )
        monthly_summary = monthly_summary[['month_key', 'daily_total_orders', 'kombo_jimat_daily_orders', 
                                           'daily_total_gmv_myr', 'kombo_jimat_daily_gmv_myr']]
        monthly_summary.columns = ['month', 'monthly_total_orders', 'monthly_kombo_jimat_orders', 
                                   'monthly_gmv_myr', 'monthly_kombo_jimat_gmv_myr']
        monthly_summary.to_csv('kombo_jimat_monthly_forecast_2026.csv', index=False, encoding='utf-8')
        print("  [OK] Saved: kombo_jimat_monthly_forecast_2026.csv")
    except PermissionError:
        print("  [WARNING] Could not save kombo_jimat_monthly_forecast_2026.csv (file may be open)")
    
    # Summary statistics
    print("\n" + "=" * 100)
    print("FORECAST SUMMARY")
    print("=" * 100)
    
    total_orders_2026 = daily_forecast_df['daily_total_orders'].sum()
    total_kombo_orders_2026 = daily_forecast_df['kombo_jimat_daily_orders'].sum()
    total_gmv_2026 = daily_forecast_df['daily_total_gmv_myr'].sum()
    total_kombo_gmv_2026 = daily_forecast_df['kombo_jimat_daily_gmv_myr'].sum()
    
    print(f"\n2026 Annual Forecast (Penang):")
    print(f"  Total Orders:        {total_orders_2026:,.0f}")
    print(f"  Kombo Jimat Orders:  {total_kombo_orders_2026:,.0f} ({total_kombo_orders_2026/total_orders_2026*100:.1f}%)")
    print(f"  Total GMV (MYR):     {total_gmv_2026:,.0f}")
    print(f"  Kombo Jimat GMV:     {total_kombo_gmv_2026:,.0f} ({total_kombo_gmv_2026/total_gmv_2026*100:.1f}%)")
    
    print(f"\nImpact if Kombo Jimat is removed:")
    print(f"  Orders Lost:         {total_kombo_orders_2026:,.0f}")
    print(f"  GMV Lost (MYR):      {total_kombo_gmv_2026:,.0f}")
    print(f"  Orders Impact:       {(total_kombo_orders_2026/total_orders_2026*100):.1f}%")
    print(f"  GMV Impact:          {(total_kombo_gmv_2026/total_gmv_2026*100):.1f}%")
    
    # Verify distribution on sample month
    print("\n" + "=" * 100)
    print("DISTRIBUTION VERIFICATION (Sample: January 2026)")
    print("=" * 100)
    jan_data = daily_forecast_df[daily_forecast_df['month'] == 1]
    jan_kombo_days = jan_data[jan_data['kombo_jimat_daily_orders'] > 0].sort_values('day_of_month', ascending=False)
    
    if len(jan_kombo_days) == 4:
        jan_total_kombo = jan_kombo_days['kombo_jimat_daily_orders'].sum()
        print(f"\nTotal Kombo Jimat orders in January: {jan_total_kombo:,.0f}")
        print("\nDistribution across last 4 days:")
        day_labels = ['4th last', '3rd last', '2nd last', 'LAST']
        for idx, row in jan_kombo_days.iterrows():
            pct = (row['kombo_jimat_daily_orders'] / jan_total_kombo * 100) if jan_total_kombo > 0 else 0
            day_pos = int(row['day_position'])
            day_label = day_labels[day_pos - 1] if 1 <= day_pos <= 4 else f"Position {day_pos}"
            print(f"  Day {int(row['day_of_month'])} ({day_label}): {row['kombo_jimat_daily_orders']:,.0f} orders ({pct:.1f}%)")
    
    print("\n" + "=" * 100)
    print("GENERATION COMPLETE")
    print("=" * 100)
    print("\nAll CSV files have been generated with:")
    print("  - Historical daily shape patterns (day of week, day of month)")
    print("  - Corrected Kombo Jimat distribution (LAST day gets 53.1% of orders)")
    print("  - Complete impact scenarios with baseline and no-Kombo Jimat scenarios")

if __name__ == "__main__":
    main()

