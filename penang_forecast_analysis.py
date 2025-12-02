#!/usr/bin/env python3
"""
Penang GMV Forecast Analysis
Forecast team performance for Jan-Jun 2026 based on historical GMV shape patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def load_gmv_shape_data():
    """Load the GMV shape data"""
    path = r"C:\Users\benjamin.liang\Downloads\penang gmv shape .xlsx"
    df = pd.read_excel(path, sheet_name='Sheet1')
    
    # Convert to monthly shape data
    months = df.columns.tolist()
    shape_values = df.iloc[0].values
    
    # Create a DataFrame with month and shape values
    shape_data = pd.DataFrame({
        'month': months,
        'shape_factor': shape_values
    })
    
    # Add month names and year
    shape_data['month_name'] = shape_data['month'].dt.strftime('%B')
    shape_data['year'] = shape_data['month'].dt.year
    shape_data['month_num'] = shape_data['month'].dt.month
    
    return shape_data

def get_team_targets():
    """Get the rebalanced team targets from previous analysis"""
    return {
        'darren': {'daily': 162707.56, 'monthly': 4881226.8},
        'suki': {'daily': 129958.63, 'monthly': 3898758.8},
        'cy': {'daily': 207308.08, 'monthly': 6219242.4},
        'ek': {'daily': 412417.80, 'monthly': 12372530.0},
        'xr': {'daily': 357067.18, 'monthly': 10712015.0}
    }

def get_team_run_rates():
    """Get current run rates from tracker analysis"""
    return {
        'darren': 135589.63,
        'suki': 108298.86,
        'cy': 172756.73,
        'ek': 255530.26,
        'xr': 221235.52
    }

def calculate_forecast(shape_data, team_targets, team_run_rates):
    """Calculate forecast based on GMV shape patterns"""
    
    # Get Jan-Jun 2026 shape factors
    jan_jun_2026 = shape_data[
        (shape_data['year'] == 2025) & 
        (shape_data['month_num'].isin([1, 2, 3, 4, 5, 6]))
    ].copy()
    
    # Calculate average shape factor for Jan-Jun
    avg_shape_factor = jan_jun_2026['shape_factor'].mean()
    
    print("GMV SHAPE ANALYSIS")
    print("="*50)
    print("Jan-Jun 2026 shape factors:")
    for _, row in jan_jun_2026.iterrows():
        print(f"{row['month_name']}: {row['shape_factor']:.3f}")
    print(f"Average Jan-Jun shape factor: {avg_shape_factor:.3f}")
    print()
    
    # Calculate forecasts for each team member
    forecasts = {}
    
    for owner in team_targets.keys():
        current_run_rate = team_run_rates[owner]
        target_daily = team_targets[owner]['daily']
        target_monthly = team_targets[owner]['monthly']
        
        # Apply shape factor to current run rate
        forecast_daily = current_run_rate * avg_shape_factor
        forecast_monthly = forecast_daily * 30
        
        # Calculate gap vs target
        daily_gap = target_daily - forecast_daily
        monthly_gap = target_monthly - forecast_monthly
        gap_percentage = (daily_gap / target_daily) * 100
        
        forecasts[owner] = {
            'current_run_rate': current_run_rate,
            'target_daily': target_daily,
            'target_monthly': target_monthly,
            'forecast_daily': forecast_daily,
            'forecast_monthly': forecast_monthly,
            'daily_gap': daily_gap,
            'monthly_gap': monthly_gap,
            'gap_percentage': gap_percentage,
            'achievement_rate': (forecast_daily / target_daily) * 100
        }
    
    return forecasts, jan_jun_2026

def generate_forecast_report(forecasts, jan_jun_2026):
    """Generate comprehensive forecast report"""
    
    print("TEAM FORECAST ANALYSIS - JAN-JUN 2026")
    print("="*60)
    print("Based on historical GMV shape patterns")
    print("="*60)
    
    # Summary table
    summary_data = []
    for owner, data in forecasts.items():
        summary_data.append({
            'Owner': owner.upper(),
            'Current Run Rate': f"${data['current_run_rate']:,.0f}",
            'Target Daily': f"${data['target_daily']:,.0f}",
            'Forecast Daily': f"${data['forecast_daily']:,.0f}",
            'Daily Gap': f"${data['daily_gap']:,.0f}",
            'Gap %': f"{data['gap_percentage']:.1f}%",
            'Achievement Rate': f"{data['achievement_rate']:.1f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    print("\nSUMMARY TABLE:")
    print(summary_df.to_string(index=False))
    
    # Detailed analysis
    print("\n" + "="*60)
    print("DETAILED ANALYSIS BY OWNER")
    print("="*60)
    
    for owner, data in forecasts.items():
        print(f"\n{owner.upper()}:")
        print(f"  Current run rate: ${data['current_run_rate']:,.0f}/day")
        print(f"  2026 target: ${data['target_daily']:,.0f}/day")
        print(f"  Forecast: ${data['forecast_daily']:,.0f}/day")
        print(f"  Gap: ${data['daily_gap']:,.0f}/day ({data['gap_percentage']:.1f}%)")
        print(f"  Achievement rate: {data['achievement_rate']:.1f}%")
        
        if data['achievement_rate'] >= 100:
            print(f"  Status: ✅ ON TRACK")
        elif data['achievement_rate'] >= 80:
            print(f"  Status: ⚠️  CLOSE - needs {data['gap_percentage']:.1f}% improvement")
        else:
            print(f"  Status: ❌ BEHIND - needs {data['gap_percentage']:.1f}% improvement")
    
    # Overall assessment
    print("\n" + "="*60)
    print("OVERALL ASSESSMENT")
    print("="*60)
    
    total_target = sum(data['target_daily'] for data in forecasts.values())
    total_forecast = sum(data['forecast_daily'] for data in forecasts.values())
    total_gap = total_target - total_forecast
    total_gap_pct = (total_gap / total_target) * 100
    
    print(f"Total team target: ${total_target:,.0f}/day")
    print(f"Total team forecast: ${total_forecast:,.0f}/day")
    print(f"Total gap: ${total_gap:,.0f}/day ({total_gap_pct:.1f}%)")
    
    if total_gap_pct <= 0:
        print("Status: ✅ TEAM ON TRACK")
    elif total_gap_pct <= 10:
        print("Status: ⚠️  TEAM CLOSE - minor adjustments needed")
    else:
        print("Status: ❌ TEAM BEHIND - significant improvements needed")
    
    return summary_df

def create_forecast_excel(forecasts, jan_jun_2026, summary_df):
    """Create Excel file with forecast analysis"""
    
    out_path = r"C:\Users\benjamin.liang\Downloads\penang_forecast_analysis.xlsx"
    
    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        # Summary table
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Detailed forecasts
        detailed_data = []
        for owner, data in forecasts.items():
            detailed_data.append({
                'Owner': owner.upper(),
                'Current_Run_Rate_Daily': data['current_run_rate'],
                'Target_Daily': data['target_daily'],
                'Target_Monthly': data['target_monthly'],
                'Forecast_Daily': data['forecast_daily'],
                'Forecast_Monthly': data['forecast_monthly'],
                'Daily_Gap': data['daily_gap'],
                'Monthly_Gap': data['monthly_gap'],
                'Gap_Percentage': data['gap_percentage'],
                'Achievement_Rate': data['achievement_rate'],
                'Status': 'ON TRACK' if data['achievement_rate'] >= 100 else 
                         'CLOSE' if data['achievement_rate'] >= 80 else 'BEHIND'
            })
        
        detailed_df = pd.DataFrame(detailed_data)
        detailed_df.to_excel(writer, sheet_name='Detailed_Forecast', index=False)
        
        # GMV shape data
        jan_jun_2026.to_excel(writer, sheet_name='GMV_Shape_Data', index=False)
        
        # Recommendations
        recommendations = [
            "1. Focus on owners with <80% achievement rate",
            "2. Implement targeted campaigns for underperforming segments",
            "3. Consider redistributing load from overperforming to underperforming owners",
            "4. Monitor monthly performance against forecast",
            "5. Adjust targets based on actual vs forecast performance"
        ]
        
        rec_df = pd.DataFrame({'Recommendations': recommendations})
        rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
    
    print(f"\nForecast analysis saved to: {out_path}")
    return out_path

def main():
    """Main analysis function"""
    
    print("PENANG GMV FORECAST ANALYSIS")
    print("="*60)
    print("Forecasting team performance for Jan-Jun 2026")
    print("Based on historical GMV shape patterns")
    print("="*60)
    
    # Load data
    shape_data = load_gmv_shape_data()
    team_targets = get_team_targets()
    team_run_rates = get_team_run_rates()
    
    # Calculate forecasts
    forecasts, jan_jun_2026 = calculate_forecast(shape_data, team_targets, team_run_rates)
    
    # Generate report
    summary_df = generate_forecast_report(forecasts, jan_jun_2026)
    
    # Create Excel file
    excel_path = create_forecast_excel(forecasts, jan_jun_2026, summary_df)
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. Review individual owner performance gaps")
    print("2. Develop action plans for underperforming owners")
    print("3. Monitor monthly progress against forecasts")
    print("4. Adjust strategies based on actual performance")
    print("5. Consider target adjustments if forecasts are consistently off")

if __name__ == "__main__":
    main()
