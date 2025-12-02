import pandas as pd
import numpy as np

# Load GMV shape data
path = r"C:\Users\benjamin.liang\Downloads\penang gmv shape .xlsx"
df = pd.read_excel(path, sheet_name='Sheet1')
months = df.columns.tolist()
daily_gmv_values = df.iloc[0].values

# Create shape data DataFrame
shape_data = pd.DataFrame({'month': months, 'daily_gmv': daily_gmv_values})
shape_data['month_name'] = shape_data['month'].dt.strftime('%B')
shape_data['year'] = shape_data['month'].dt.year
shape_data['month_num'] = shape_data['month'].dt.month

# Get Jul-Sep 2025 (current run rate period) vs Jan-Jun 2026 (target period)
jul_sep_2025 = shape_data[(shape_data['year'] == 2025) & (shape_data['month_num'].isin([7,8,9]))].copy()
jan_jun_2026 = shape_data[(shape_data['year'] == 2025) & (shape_data['month_num'].isin([1,2,3,4,5,6]))].copy()

avg_jul_sep = jul_sep_2025['daily_gmv'].mean()
avg_jan_jun = jan_jun_2026['daily_gmv'].mean()
seasonal_factor = avg_jan_jun / avg_jul_sep

print('SEASONALITY ANALYSIS')
print('='*50)
print('Jul-Sep 2025 (current run rate period):')
for _, row in jul_sep_2025.iterrows():
    print(f"{row['month_name']}: ${row['daily_gmv']:,.0f}")
print(f'Average Jul-Sep 2025: ${avg_jul_sep:,.0f}')

print('\nJan-Jun 2026 (target period):')
for _, row in jan_jun_2026.iterrows():
    print(f"{row['month_name']}: ${row['daily_gmv']:,.0f}")
print(f'Average Jan-Jun 2026: ${avg_jan_jun:,.0f}')

print(f'\nSeasonal adjustment factor: {seasonal_factor:.3f}')
print(f'This means Jan-Jun is {seasonal_factor:.1%} of Jul-Sep levels')

# Current run rates (from Jul-Sep 2025)
current_run_rates = {
    'EK': 504002.00,
    'XR': 357067.00, 
    'CY': 207308.00,
    'Darren': 162708.00,
    'Suki': 129959.00,
    'Jamie': 217767.00
}

print('\nSEASONALLY ADJUSTED RUN RATES FOR JAN-JUN 2026:')
print('Owner   | Current RR (Jul-Sep) | Seasonally Adjusted RR (Jan-Jun)')
print('-'*70)
for owner, rr in current_run_rates.items():
    adjusted_rr = rr * seasonal_factor
    print(f'{owner:8} | ${rr:>15,.0f} | ${adjusted_rr:>30,.0f}')

print(f'\nThis shows the team would naturally perform at {seasonal_factor:.1%} of current levels in Jan-Jun due to seasonality.')

# Now recalculate the forecast with seasonality adjustment
team_targets = {
    'EK': {'daily': 339118.83, 'monthly': 10173564.87, '6m_total': 61041389.20},
    'XR': {'daily': 123315.94, 'monthly': 3699478.13, '6m_total': 22196868.80},
    'CY': {'daily': 184973.91, 'monthly': 5549217.20, '6m_total': 33295303.20},
    'Darren': {'daily': 246631.88, 'monthly': 7398956.27, '6m_total': 44393737.60},
    'Suki': {'daily': 184973.91, 'monthly': 5549217.20, '6m_total': 33295303.20},
    'Jamie': {'daily': 215802.89, 'monthly': 6474086.73, '6m_total': 38844520.40}
}

print('\nCORRECTED FORECAST WITH SEASONALITY:')
print('='*60)
print('Owner   | Target Daily | Seasonally Adjusted RR | Gap        | Gap % | Achievement Rate')
print('-'*90)

forecasts = {}
for owner in team_targets.keys():
    current_rr = current_run_rates[owner]
    target_daily = team_targets[owner]['daily']
    seasonally_adjusted_rr = current_rr * seasonal_factor
    
    daily_gap = target_daily - seasonally_adjusted_rr
    gap_percentage = (daily_gap / target_daily) * 100 if target_daily > 0 else 0
    achievement_rate = (seasonally_adjusted_rr / target_daily) * 100 if target_daily > 0 else 0
    
    forecasts[owner] = {
        'target_daily': target_daily,
        'seasonally_adjusted_rr': seasonally_adjusted_rr,
        'daily_gap': daily_gap,
        'gap_percentage': gap_percentage,
        'achievement_rate': achievement_rate
    }
    
    print(f'{owner:8} | ${target_daily:>10,.0f} | ${seasonally_adjusted_rr:>20,.0f} | ${daily_gap:>9,.0f} | {gap_percentage:>4.1f}% | {achievement_rate:>13.1f}%')

# Overall assessment
total_target = sum(data['target_daily'] for data in forecasts.values())
total_forecast = sum(data['seasonally_adjusted_rr'] for data in forecasts.values())
total_gap = total_target - total_forecast
total_gap_pct = (total_gap / total_target) * 100

print('\nOVERALL ASSESSMENT (WITH SEASONALITY):')
print('='*60)
print(f'Total team target: ${total_target:,.0f}/day')
print(f'Total seasonally adjusted forecast: ${total_forecast:,.0f}/day')
print(f'Total gap: ${total_gap:,.0f}/day ({total_gap_pct:.1f}%)')

if total_gap_pct <= 0:
    print('Status: TEAM ON TRACK')
elif total_gap_pct <= 10:
    print('Status: TEAM CLOSE - minor adjustments needed')
else:
    print('Status: TEAM BEHIND - significant improvements needed')

print(f'\nKey insight: The seasonal factor of {seasonal_factor:.3f} means the team naturally performs at {seasonal_factor:.1%} of their Jul-Sep levels during Jan-Jun.')
