#!/usr/bin/env python3
"""
Penang 2026 Target Analysis - Corrected
Assuming 2026 targets are DAILY targets, not monthly
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_penang_2025():
    """Analyze Penang 2025 performance"""
    
    # Load the 2025 data
    df = pd.read_excel(r"C:\Users\benjamin.liang\Downloads\2025 daily .xlsx")
    df = df.replace('[NULL]', np.nan)
    df['date'] = pd.to_datetime(df['date'])
    df['gmv'] = pd.to_numeric(df['gmv'], errors='coerce')
    df = df.dropna(subset=['gmv'])
    
    # Filter for Penang data
    penang_data = df[df['city'] == 'Penang'].copy()
    penang_daily = penang_data.groupby('date')['gmv'].sum()
    
    print('PENANG 2025 ANALYSIS')
    print('='*50)
    print(f'Total Penang GMV 2025: ${penang_daily.sum():,.2f}')
    print(f'Average daily GMV: ${penang_daily.mean():,.2f}')
    print(f'Date range: {penang_daily.index.min()} to {penang_daily.index.max()}')
    print(f'Number of days: {len(penang_daily)}')
    
    # Calculate monthly averages
    penang_monthly = penang_daily.resample('ME').sum()
    print(f'\nMonthly GMV 2025:')
    for month, gmv in penang_monthly.items():
        print(f'{month.strftime("%B %Y")}: ${gmv:,.2f}')
    
    # Calculate growth rates
    monthly_growth = penang_monthly.pct_change().dropna()
    print(f'\nMonthly Growth Rates:')
    for month, growth in monthly_growth.items():
        print(f'{month.strftime("%B %Y")}: {growth:.2%}')
    
    # Calculate baseline growth (using 30-day moving average)
    baseline = penang_daily.rolling(window=30).mean()
    baseline_growth = baseline.pct_change()
    
    # Calculate organic vs inorganic growth
    actual_growth = penang_daily.pct_change()
    inorganic_growth = actual_growth - baseline_growth
    
    # Calculate GMV components
    organic_gmv = penang_daily * (1 + baseline_growth.fillna(0))
    inorganic_gmv = penang_daily - organic_gmv
    
    print(f'\nGROWTH ATTRIBUTION (2025):')
    print(f'Organic GMV: ${organic_gmv.sum():,.2f} ({organic_gmv.sum()/penang_daily.sum()*100:.1f}%)')
    print(f'Inorganic GMV: ${inorganic_gmv.sum():,.2f} ({inorganic_gmv.sum()/penang_daily.sum()*100:.1f}%)')
    print(f'Average daily organic growth: {baseline_growth.mean():.4f} ({baseline_growth.mean()*100:.2f}%)')
    print(f'Average daily inorganic growth: {inorganic_growth.mean():.4f} ({inorganic_growth.mean()*100:.2f}%)')
    
    return {
        'daily_avg': penang_daily.mean(),
        'monthly_totals': penang_monthly,
        'monthly_growth': monthly_growth,
        'organic_growth_rate': baseline_growth.mean(),
        'inorganic_growth_rate': inorganic_growth.mean(),
        'organic_share': organic_gmv.sum() / penang_daily.sum(),
        'inorganic_share': inorganic_gmv.sum() / penang_daily.sum()
    }

def calculate_2026_daily_targets():
    """Calculate 2026 daily targets and inorganic GMV needed"""
    
    # 2026 Penang DAILY targets (from your image)
    daily_targets_2026 = {
        'January': 1591253.27,
        'February': 1714018.20,
        'March': 1807120.47,
        'April': 1727299.41,
        'May': 1390025.32,
        'June': 1638585.25
    }
    
    print('\n' + '='*60)
    print('2026 PENANG DAILY TARGETS ANALYSIS')
    print('='*60)
    
    # Analyze 2025 performance
    penang_2025 = analyze_penang_2025()
    
    # Current 2025 daily average
    current_daily_avg = penang_2025['daily_avg']
    
    print(f'\nCURRENT PERFORMANCE (2025):')
    print(f'Average daily GMV: ${current_daily_avg:,.2f}')
    
    # Calculate 2026 targets
    total_daily_2026 = sum(daily_targets_2026.values())
    avg_daily_2026 = total_daily_2026 / 6
    
    print(f'\n2026 DAILY TARGETS:')
    print(f'Average daily target: ${avg_daily_2026:,.2f}')
    print(f'Total Jan-June 2026: ${total_daily_2026 * 30 * 6:,.2f} (assuming 30 days/month)')
    
    # Calculate growth needed
    daily_growth_needed = (avg_daily_2026 - current_daily_avg) / current_daily_avg
    
    print(f'\nGROWTH ANALYSIS:')
    print(f'Daily growth needed: {daily_growth_needed:.2%}')
    print(f'Current daily average: ${current_daily_avg:,.2f}')
    print(f'Target daily average: ${avg_daily_2026:,.2f}')
    print(f'Gap per day: ${avg_daily_2026 - current_daily_avg:,.2f}')
    
    # Project organic growth (assuming same rate as 2025)
    organic_growth_rate = penang_2025['organic_growth_rate']
    inorganic_growth_rate = penang_2025['inorganic_growth_rate']
    
    print(f'\nCURRENT GROWTH RATES (2025):')
    print(f'Organic growth rate: {organic_growth_rate:.4f} ({organic_growth_rate*100:.2f}%)')
    print(f'Inorganic growth rate: {inorganic_growth_rate:.4f} ({inorganic_growth_rate*100:.2f}%)')
    
    # Calculate what we can achieve with current organic growth
    # Assuming 6 months of growth at current organic rate
    months = 6
    organic_contribution_daily = current_daily_avg * ((1 + organic_growth_rate) ** (months * 30))
    total_organic_2026 = organic_contribution_daily * 30 * 6
    
    print(f'\nPROJECTED 2026 PERFORMANCE:')
    print(f'With current organic growth only: ${organic_contribution_daily:,.2f} per day')
    print(f'Target daily: ${avg_daily_2026:,.2f}')
    print(f'Gap per day: ${avg_daily_2026 - organic_contribution_daily:,.2f}')
    
    # Calculate inorganic GMV needed
    inorganic_gmv_needed_daily = avg_daily_2026 - organic_contribution_daily
    inorganic_share_needed = inorganic_gmv_needed_daily / avg_daily_2026
    
    print(f'\nINORGANIC GMV NEEDED:')
    print(f'Daily inorganic GMV needed: ${inorganic_gmv_needed_daily:,.2f}')
    print(f'Monthly inorganic GMV needed: ${inorganic_gmv_needed_daily * 30:,.2f}')
    print(f'Total inorganic GMV (6 months): ${inorganic_gmv_needed_daily * 30 * 6:,.2f}')
    print(f'Inorganic share needed: {inorganic_share_needed:.1%}')
    
    # Monthly breakdown
    print(f'\nMONTHLY BREAKDOWN:')
    for month, target in daily_targets_2026.items():
        organic_projection = current_daily_avg * ((1 + organic_growth_rate) ** (list(daily_targets_2026.keys()).index(month) + 1))
        inorganic_needed = target - organic_projection
        inorganic_share = inorganic_needed / target
        
        print(f'{month}:')
        print(f'  Daily target: ${target:,.2f}')
        print(f'  Organic projection: ${organic_projection:,.2f}')
        print(f'  Inorganic needed: ${inorganic_needed:,.2f} ({inorganic_share:.1%})')
        print(f'  Monthly inorganic: ${inorganic_needed * 30:,.2f}')
        print()
    
    # Calculate what this means in terms of growth
    print(f'GROWTH REQUIREMENTS:')
    print(f'To hit these targets, you need:')
    print(f'• {daily_growth_needed:.1%} daily growth vs current performance')
    print(f'• ${inorganic_gmv_needed_daily:,.2f} additional inorganic GMV per day')
    print(f'• ${inorganic_gmv_needed_daily * 30:,.2f} additional inorganic GMV per month')
    print(f'• This represents {inorganic_share_needed:.1%} of your total daily target')
    
    return {
        'daily_inorganic_needed': inorganic_gmv_needed_daily,
        'monthly_inorganic_needed': inorganic_gmv_needed_daily * 30,
        'total_inorganic_needed': inorganic_gmv_needed_daily * 30 * 6,
        'inorganic_share_needed': inorganic_share_needed,
        'daily_growth_needed': daily_growth_needed,
        'monthly_breakdown': {
            month: (target - (current_daily_avg * ((1 + organic_growth_rate) ** (list(daily_targets_2026.keys()).index(month) + 1)))) * 30
            for month, target in daily_targets_2026.items()
        }
    }

def main():
    """Main analysis function"""
    
    print('PENANG 2026 DAILY TARGET ANALYSIS')
    print('='*60)
    print('Based on 2025 performance and 2026 DAILY targets')
    print('='*60)
    
    results = calculate_2026_daily_targets()
    
    print('\n' + '='*60)
    print('SUMMARY & RECOMMENDATIONS')
    print('='*60)
    
    print(f'To hit your 2026 Penang DAILY targets, you need:')
    print(f'• Daily inorganic GMV: ${results["daily_inorganic_needed"]:,.2f}')
    print(f'• Monthly inorganic GMV: ${results["monthly_inorganic_needed"]:,.2f}')
    print(f'• Total inorganic GMV (6 months): ${results["total_inorganic_needed"]:,.2f}')
    print(f'• Inorganic share of total: {results["inorganic_share_needed"]:.1%}')
    print(f'• Daily growth needed: {results["daily_growth_needed"]:.1%}')
    
    print(f'\nKey insights:')
    print(f'• Your targets are {results["daily_growth_needed"]:.1%} higher than current performance')
    print(f'• You need {results["inorganic_share_needed"]:.1%} inorganic growth to hit targets')
    print(f'• Focus on campaigns, promotions, and new customer acquisition')
    print(f'• Consider geographic expansion within Penang')
    print(f'• Monitor daily performance against inorganic targets')
    
    print(f'\nAction items:')
    print(f'• Set up daily tracking of inorganic GMV')
    print(f'• Plan marketing campaigns to generate ${results["daily_inorganic_needed"]:,.2f} daily')
    print(f'• Monitor progress weekly and adjust strategies')
    print(f'• Consider seasonal adjustments for different months')

if __name__ == "__main__":
    main()
