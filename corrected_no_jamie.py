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

# Get Jul-Sep 2025 vs Jan-Jun 2026
jul_sep_2025 = shape_data[(shape_data['year'] == 2025) & (shape_data['month_num'].isin([7,8,9]))].copy()
jan_jun_2026 = shape_data[(shape_data['year'] == 2025) & (shape_data['month_num'].isin([1,2,3,4,5,6]))].copy()

avg_jul_sep = jul_sep_2025['daily_gmv'].mean()
avg_jan_jun = jan_jun_2026['daily_gmv'].mean()
seasonal_factor = avg_jan_jun / avg_jul_sep

print('CORRECTED FORECAST (EXCLUDING JAMIE - NO DATA)')
print('='*60)

# Current run rates (EXCLUDING Jamie - no data provided)
current_run_rates = {
    'EK': 504002.00,
    'XR': 357067.00, 
    'CY': 207308.00,
    'Darren': 162708.00,
    'Suki': 129959.00
}

# Team targets
team_targets = {
    'EK': 339118.83,
    'XR': 123315.94,
    'CY': 184973.91,
    'Darren': 246631.88,
    'Suki': 184973.91,
    'Jamie': 215802.89  # Target exists but no current RR data
}

print(f'Seasonal adjustment factor: {seasonal_factor:.3f}')
print(f'Jan-Jun is {seasonal_factor:.1%} of Jul-Sep levels')
print()

print('FORECAST ANALYSIS (EXCLUDING JAMIE):')
print('Owner   | Target Daily | Seasonally Adjusted RR | Gap        | Gap % | Achievement Rate')
print('-'*90)

total_target_without_jamie = 0
total_forecast_without_jamie = 0

for owner in current_run_rates.keys():
    current_rr = current_run_rates[owner]
    target_daily = team_targets[owner]
    seasonally_adjusted_rr = current_rr * seasonal_factor
    
    daily_gap = target_daily - seasonally_adjusted_rr
    gap_percentage = (daily_gap / target_daily) * 100 if target_daily > 0 else 0
    achievement_rate = (seasonally_adjusted_rr / target_daily) * 100 if target_daily > 0 else 0
    
    total_target_without_jamie += target_daily
    total_forecast_without_jamie += seasonally_adjusted_rr
    
    print(f'{owner:8} | ${target_daily:>10,.0f} | ${seasonally_adjusted_rr:>20,.0f} | ${daily_gap:>9,.0f} | {gap_percentage:>4.1f}% | {achievement_rate:>13.1f}%')

print()
print('JAMIE: NO CURRENT RR DATA PROVIDED')
print(f'Jamie target: ${team_targets["Jamie"]:,.0f}/day')
print('Cannot calculate forecast without current run rate data')

print()
print('OVERALL ASSESSMENT (EXCLUDING JAMIE):')
total_gap = total_target_without_jamie - total_forecast_without_jamie
total_gap_pct = (total_gap / total_target_without_jamie) * 100
print(f'Total team target (excluding Jamie): ${total_target_without_jamie:,.0f}/day')
print(f'Total forecast (excluding Jamie): ${total_forecast_without_jamie:,.0f}/day')
print(f'Total gap: ${total_gap:,.0f}/day ({total_gap_pct:.1f}%)')

if total_gap_pct <= 0:
    print('Status: TEAM ON TRACK (excluding Jamie)')
elif total_gap_pct <= 10:
    print('Status: TEAM CLOSE (excluding Jamie)')
else:
    print('Status: TEAM BEHIND (excluding Jamie)')

print()
print('NOTE: Jamie needs current run rate data to be included in forecast analysis')
print('Jamie target: $215,803/day - but no current performance data available')
