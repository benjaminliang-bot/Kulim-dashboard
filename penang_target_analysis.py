#!/usr/bin/env python3
"""
Penang 2026 Target Analysis
Calculate inorganic GMV needed to hit 2026 targets based on 2025 performance
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
    penang_monthly = penang_daily.resample('M').sum()
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

def calculate_2026_targets():
    """Calculate 2026 targets and inorganic GMV needed"""
    
    # 2026 Penang targets (from your image)
    targets_2026 = {
        'January': 1591253.27,
        'February': 1714018.20,
        'March': 1807120.47,
        'April': 1727299.41,
        'May': 1390025.32,
        'June': 1638585.25
    }
    
    print('\n' + '='*60)
    print('2026 PENANG TARGETS ANALYSIS')
    print('='*60)
    
    # Analyze 2025 performance
    penang_2025 = analyze_penang_2025()
    
    # Calculate 2025 monthly averages for comparison
    monthly_2025 = penang_2025['monthly_totals']
    avg_monthly_2025 = monthly_2025.mean()
    
    print(f'\n2025 AVERAGE MONTHLY GMV: ${avg_monthly_2025:,.2f}')
    
    # Calculate 2026 targets
    total_target_2026 = sum(targets_2026.values())
    avg_monthly_2026 = total_target_2026 / 6
    
    print(f'\n2026 TARGETS:')
    print(f'Total Jan-June 2026: ${total_target_2026:,.2f}')
    print(f'Average monthly 2026: ${avg_monthly_2026:,.2f}')
    
    # Calculate growth needed
    total_growth_needed = (total_target_2026 - (avg_monthly_2025 * 6)) / (avg_monthly_2025 * 6)
    monthly_growth_needed = (avg_monthly_2026 - avg_monthly_2025) / avg_monthly_2025
    
    print(f'\nGROWTH ANALYSIS:')
    print(f'Total growth needed: {total_growth_needed:.2%}')
    print(f'Monthly growth needed: {monthly_growth_needed:.2%}')
    
    # Project organic growth (assuming same rate as 2025)
    organic_growth_rate = penang_2025['organic_growth_rate']
    inorganic_growth_rate = penang_2025['inorganic_growth_rate']
    
    print(f'\nCURRENT GROWTH RATES (2025):')
    print(f'Organic growth rate: {organic_growth_rate:.4f} ({organic_growth_rate*100:.2f}%)')
    print(f'Inorganic growth rate: {inorganic_growth_rate:.4f} ({inorganic_growth_rate*100:.2f}%)')
    
    # Calculate what we can achieve with current organic growth
    # Assuming 6 months of growth at current organic rate
    months = 6
    organic_contribution = avg_monthly_2025 * ((1 + organic_growth_rate) ** months)
    total_organic_2026 = organic_contribution * months
    
    print(f'\nPROJECTED 2026 PERFORMANCE:')
    print(f'With current organic growth only: ${total_organic_2026:,.2f}')
    print(f'Target: ${total_target_2026:,.2f}')
    print(f'Gap: ${total_target_2026 - total_organic_2026:,.2f}')
    
    # Calculate inorganic GMV needed
    inorganic_gmv_needed = total_target_2026 - total_organic_2026
    inorganic_share_needed = inorganic_gmv_needed / total_target_2026
    
    print(f'\nINORGANIC GMV NEEDED:')
    print(f'Total inorganic GMV needed: ${inorganic_gmv_needed:,.2f}')
    print(f'Inorganic share needed: {inorganic_share_needed:.1%}')
    print(f'Average monthly inorganic GMV: ${inorganic_gmv_needed/6:,.2f}')
    
    # Monthly breakdown
    print(f'\nMONTHLY BREAKDOWN:')
    for month, target in targets_2026.items():
        organic_projection = avg_monthly_2025 * ((1 + organic_growth_rate) ** (list(targets_2026.keys()).index(month) + 1))
        inorganic_needed = target - organic_projection
        inorganic_share = inorganic_needed / target
        
        print(f'{month}:')
        print(f'  Target: ${target:,.2f}')
        print(f'  Organic projection: ${organic_projection:,.2f}')
        print(f'  Inorganic needed: ${inorganic_needed:,.2f} ({inorganic_share:.1%})')
        print()
    
    # Calculate daily inorganic targets
    print(f'DAILY INORGANIC TARGETS:')
    for month, target in targets_2026.items():
        days_in_month = {
            'January': 31, 'February': 28, 'March': 31, 
            'April': 30, 'May': 31, 'June': 30
        }
        
        organic_projection = avg_monthly_2025 * ((1 + organic_growth_rate) ** (list(targets_2026.keys()).index(month) + 1))
        inorganic_needed = target - organic_projection
        daily_inorganic = inorganic_needed / days_in_month[month]
        
        print(f'{month}: ${daily_inorganic:,.2f} per day')
    
    return {
        'total_inorganic_needed': inorganic_gmv_needed,
        'monthly_inorganic_needed': inorganic_gmv_needed / 6,
        'inorganic_share_needed': inorganic_share_needed,
        'monthly_breakdown': {
            month: target - (avg_monthly_2025 * ((1 + organic_growth_rate) ** (list(targets_2026.keys()).index(month) + 1)))
            for month, target in targets_2026.items()
        }
    }

def main():
    """Main analysis function"""
    
    print('PENANG 2026 TARGET ANALYSIS')
    print('='*60)
    print('Based on 2025 performance and 2026 targets')
    print('='*60)
    
    results = calculate_2026_targets()
    
    print('\n' + '='*60)
    print('SUMMARY & RECOMMENDATIONS')
    print('='*60)
    
    print(f'To hit your 2026 Penang targets, you need:')
    print(f'• Total inorganic GMV: ${results["total_inorganic_needed"]:,.2f}')
    print(f'• Average monthly inorganic: ${results["monthly_inorganic_needed"]:,.2f}')
    print(f'• Inorganic share of total: {results["inorganic_share_needed"]:.1%}')
    
    print(f'\nKey insights:')
    print(f'• Your current organic growth is very stable but low')
    print(f'• You need significant inorganic growth to hit targets')
    print(f'• Focus on campaigns, promotions, and new customer acquisition')
    print(f'• Consider geographic expansion within Penang')
    print(f'• Monitor daily performance against inorganic targets')

if __name__ == "__main__":
    main()
