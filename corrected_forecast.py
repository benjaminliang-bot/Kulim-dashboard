import pandas as pd
import numpy as np

# Load updated GMV shape data with actual daily GMV values
path = r"C:\Users\benjamin.liang\Downloads\penang gmv shape .xlsx"
df = pd.read_excel(path, sheet_name='Sheet1')
months = df.columns.tolist()
daily_gmv_values = df.iloc[0].values

# Create shape data DataFrame
shape_data = pd.DataFrame({'month': months, 'daily_gmv': daily_gmv_values})
shape_data['month_name'] = shape_data['month'].dt.strftime('%B')
shape_data['year'] = shape_data['month'].dt.year
shape_data['month_num'] = shape_data['month'].dt.month

# Get Jan-Jun 2026 daily GMV values
jan_jun_2026 = shape_data[(shape_data['year'] == 2025) & (shape_data['month_num'].isin([1,2,3,4,5,6]))].copy()
avg_daily_gmv = jan_jun_2026['daily_gmv'].mean()

print('UPDATED GMV SHAPE ANALYSIS - JAN-JUN 2026')
print('='*60)
print('Actual daily GMV values for Jan-Jun 2026:')
for _, row in jan_jun_2026.iterrows():
    print(f"{row['month_name']}: ${row['daily_gmv']:,.0f}")
print(f"Average daily GMV: ${avg_daily_gmv:,.0f}")

# Correct targets from the photo
team_targets = {
    'EK': {'daily': 339118.83, 'monthly': 10173564.87, '6m_total': 61041389.20},
    'XR': {'daily': 123315.94, 'monthly': 3699478.13, '6m_total': 22196868.80},
    'CY': {'daily': 184973.91, 'monthly': 5549217.20, '6m_total': 33295303.20},
    'Darren': {'daily': 246631.88, 'monthly': 7398956.27, '6m_total': 44393737.60},
    'Suki': {'daily': 184973.91, 'monthly': 5549217.20, '6m_total': 33295303.20},
    'Jamie': {'daily': 215802.89, 'monthly': 6474086.73, '6m_total': 38844520.40}
}

# Current run rates from the photo
current_run_rates = {
    'EK': 504002.00,
    'XR': 357067.00,
    'CY': 207308.00,
    'Darren': 162708.00,
    'Suki': 129959.00,
    'Jamie': 0  # No current RR provided
}

print('\nTEAM FORECAST ANALYSIS - JAN-JUN 2026')
print('='*60)
print('Based on actual daily GMV values and current run rates')
print('='*60)

# Calculate forecasts
forecasts = {}
for owner in team_targets.keys():
    current_rr = current_run_rates[owner]
    target_daily = team_targets[owner]['daily']
    
    # If current RR is 0, use a conservative estimate
    if current_rr == 0:
        # Use average of other team members as baseline
        avg_rr = np.mean([rr for rr in current_run_rates.values() if rr > 0])
        current_rr = avg_rr * 0.8  # 80% of average as conservative estimate
    
    # Forecast based on current run rate vs actual daily GMV pattern
    # Scale current run rate by the ratio of actual GMV to average
    avg_historical_gmv = shape_data[shape_data['year'] == 2024]['daily_gmv'].mean()
    gmv_ratio = avg_daily_gmv / avg_historical_gmv if avg_historical_gmv > 0 else 1
    
    forecast_daily = current_rr * gmv_ratio
    daily_gap = target_daily - forecast_daily
    gap_percentage = (daily_gap / target_daily) * 100 if target_daily > 0 else 0
    achievement_rate = (forecast_daily / target_daily) * 100 if target_daily > 0 else 0
    
    forecasts[owner] = {
        'current_rr': current_rr,
        'target_daily': target_daily,
        'forecast_daily': forecast_daily,
        'daily_gap': daily_gap,
        'gap_percentage': gap_percentage,
        'achievement_rate': achievement_rate,
        'monthly_forecast': forecast_daily * 30,
        '6m_forecast': forecast_daily * 180
    }

# Print summary table
print('\nSUMMARY TABLE:')
print('Owner   | Current RR | Target Daily | Forecast Daily | Daily Gap   | Gap % | Achievement Rate')
print('-'*110)
for owner, data in forecasts.items():
    print(f"{owner:8} | ${data['current_rr']:>9,.0f} | ${data['target_daily']:>10,.0f} | ${data['forecast_daily']:>13,.0f} | ${data['daily_gap']:>10,.0f} | {data['gap_percentage']:>4.1f}% | {data['achievement_rate']:>13.1f}%")

# Detailed analysis
print('\nDETAILED ANALYSIS:')
for owner, data in forecasts.items():
    print(f'\n{owner.upper()}:')
    print(f'  Current RR: ${data["current_rr"]:,.0f}/day')
    print(f'  2026 target: ${data["target_daily"]:,.0f}/day')
    print(f'  Forecast: ${data["forecast_daily"]:,.0f}/day')
    print(f'  Gap: ${data["daily_gap"]:,.0f}/day ({data["gap_percentage"]:.1f}%)')
    print(f'  Achievement rate: {data["achievement_rate"]:.1f}%')
    print(f'  6M forecast: ${data["6m_forecast"]:,.0f}')
    
    if data['achievement_rate'] >= 100:
        print(f'  Status: ON TRACK')
    elif data['achievement_rate'] >= 80:
        print(f'  Status: CLOSE - needs {data["gap_percentage"]:.1f}% improvement')
    else:
        print(f'  Status: BEHIND - needs {data["gap_percentage"]:.1f}% improvement')

# Overall assessment
total_target = sum(data['target_daily'] for data in forecasts.values())
total_forecast = sum(data['forecast_daily'] for data in forecasts.values())
total_gap = total_target - total_forecast
total_gap_pct = (total_gap / total_target) * 100

print('\nOVERALL ASSESSMENT')
print('='*60)
print(f'Total team target: ${total_target:,.0f}/day')
print(f'Total team forecast: ${total_forecast:,.0f}/day')
print(f'Total gap: ${total_gap:,.0f}/day ({total_gap_pct:.1f}%)')
print(f'6M total target: ${sum(team_targets[owner]["6m_total"] for owner in team_targets):,.0f}')
print(f'6M total forecast: ${sum(data["6m_forecast"] for data in forecasts.values()):,.0f}')

if total_gap_pct <= 0:
    print('Status: TEAM ON TRACK')
elif total_gap_pct <= 10:
    print('Status: TEAM CLOSE - minor adjustments needed')
else:
    print('Status: TEAM BEHIND - significant improvements needed')

# Save to Excel
out_path = r"C:\Users\benjamin.liang\Downloads\corrected_penang_forecast.xlsx"
with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
    # Summary data
    summary_data = []
    for owner, data in forecasts.items():
        summary_data.append({
            'Owner': owner,
            'Current_RR': data['current_rr'],
            'Target_Daily': data['target_daily'],
            'Target_Monthly': team_targets[owner]['monthly'],
            'Target_6M_Total': team_targets[owner]['6m_total'],
            'Forecast_Daily': data['forecast_daily'],
            'Forecast_Monthly': data['monthly_forecast'],
            'Forecast_6M_Total': data['6m_forecast'],
            'Daily_Gap': data['daily_gap'],
            'Gap_Percentage': data['gap_percentage'],
            'Achievement_Rate': data['achievement_rate'],
            'Status': 'ON TRACK' if data['achievement_rate'] >= 100 else 
                     'CLOSE' if data['achievement_rate'] >= 80 else 'BEHIND'
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Forecast_Summary', index=False)
    
    # GMV shape data
    jan_jun_2026.to_excel(writer, sheet_name='GMV_Shape_Data', index=False)
    
    # Overall assessment
    overall_data = pd.DataFrame({
        'Metric': ['Total Daily Target', 'Total Daily Forecast', 'Total Daily Gap', 'Gap Percentage', 
                  '6M Total Target', '6M Total Forecast', '6M Gap'],
        'Value': [total_target, total_forecast, total_gap, total_gap_pct,
                 sum(team_targets[owner]["6m_total"] for owner in team_targets),
                 sum(data["6m_forecast"] for data in forecasts.values()),
                 sum(team_targets[owner]["6m_total"] for owner in team_targets) - sum(data["6m_forecast"] for data in forecasts.values())]
    })
    overall_data.to_excel(writer, sheet_name='Overall_Assessment', index=False)

print(f'\nCorrected forecast analysis saved to: {out_path}')
