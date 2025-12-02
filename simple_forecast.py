import pandas as pd
import numpy as np

# Load GMV shape data
path = r"C:\Users\benjamin.liang\Downloads\penang gmv shape .xlsx"
df = pd.read_excel(path, sheet_name='Sheet1')
months = df.columns.tolist()
shape_values = df.iloc[0].values

# Create shape data DataFrame
shape_data = pd.DataFrame({'month': months, 'shape_factor': shape_values})
shape_data['month_name'] = shape_data['month'].dt.strftime('%B')
shape_data['year'] = shape_data['month'].dt.year
shape_data['month_num'] = shape_data['month'].dt.month

# Get Jan-Jun 2026 shape factors
jan_jun_2026 = shape_data[(shape_data['year'] == 2025) & (shape_data['month_num'].isin([1,2,3,4,5,6]))].copy()
avg_shape_factor = jan_jun_2026['shape_factor'].mean()

print('GMV SHAPE ANALYSIS')
print('='*50)
for _, row in jan_jun_2026.iterrows():
    print(f"{row['month_name']}: {row['shape_factor']:.3f}")
print(f"Average Jan-Jun shape factor: {avg_shape_factor:.3f}")

# Team data
team_targets = {
    'darren': 162707.56,
    'suki': 129958.63, 
    'cy': 207308.08,
    'ek': 412417.80,
    'xr': 357067.18
}

team_run_rates = {
    'darren': 135589.63,
    'suki': 108298.86,
    'cy': 172756.73,
    'ek': 255530.26,
    'xr': 221235.52
}

print('\nTEAM FORECAST ANALYSIS - JAN-JUN 2026')
print('='*60)
print('Based on historical GMV shape patterns')
print('='*60)

# Calculate forecasts
forecasts = {}
for owner in team_targets.keys():
    current_run_rate = team_run_rates[owner]
    target_daily = team_targets[owner]
    forecast_daily = current_run_rate * avg_shape_factor
    daily_gap = target_daily - forecast_daily
    gap_percentage = (daily_gap / target_daily) * 100
    achievement_rate = (forecast_daily / target_daily) * 100
    
    forecasts[owner] = {
        'current_run_rate': current_run_rate,
        'target_daily': target_daily,
        'forecast_daily': forecast_daily,
        'daily_gap': daily_gap,
        'gap_percentage': gap_percentage,
        'achievement_rate': achievement_rate
    }

# Print summary table
print('\nSUMMARY TABLE:')
print('Owner     | Current Run Rate | Target Daily | Forecast Daily | Daily Gap   | Gap % | Achievement Rate')
print('-'*110)
for owner, data in forecasts.items():
    print(f"{owner.upper():8} | ${data['current_run_rate']:>12,.0f} | ${data['target_daily']:>10,.0f} | ${data['forecast_daily']:>13,.0f} | ${data['daily_gap']:>10,.0f} | {data['gap_percentage']:>4.1f}% | {data['achievement_rate']:>13.1f}%")

# Detailed analysis
print('\nDETAILED ANALYSIS:')
for owner, data in forecasts.items():
    print(f'\n{owner.upper()}:')
    print(f'  Current run rate: ${data["current_run_rate"]:,.0f}/day')
    print(f'  2026 target: ${data["target_daily"]:,.0f}/day')
    print(f'  Forecast: ${data["forecast_daily"]:,.0f}/day')
    print(f'  Gap: ${data["daily_gap"]:,.0f}/day ({data["gap_percentage"]:.1f}%)')
    print(f'  Achievement rate: {data["achievement_rate"]:.1f}%')
    
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

if total_gap_pct <= 0:
    print('Status: TEAM ON TRACK')
elif total_gap_pct <= 10:
    print('Status: TEAM CLOSE - minor adjustments needed')
else:
    print('Status: TEAM BEHIND - significant improvements needed')

# Save to Excel
out_path = r"C:\Users\benjamin.liang\Downloads\penang_forecast_analysis.xlsx"
with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
    # Summary data
    summary_data = []
    for owner, data in forecasts.items():
        summary_data.append({
            'Owner': owner.upper(),
            'Current_Run_Rate': data['current_run_rate'],
            'Target_Daily': data['target_daily'],
            'Forecast_Daily': data['forecast_daily'],
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
        'Metric': ['Total Target', 'Total Forecast', 'Total Gap', 'Gap Percentage'],
        'Value': [total_target, total_forecast, total_gap, total_gap_pct]
    })
    overall_data.to_excel(writer, sheet_name='Overall_Assessment', index=False)

print(f'\nForecast analysis saved to: {out_path}')
