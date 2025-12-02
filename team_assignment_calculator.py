#!/usr/bin/env python3
"""
Team Assignment Calculator for 2026 Penang Targets
Calculate how much incremental GMV to assign to each team member
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_incremental_assignments():
    """Calculate incremental GMV assignments for the team"""
    
    # Current performance (2025)
    current_daily_avg = 349899.64
    current_monthly_avg = current_daily_avg * 30
    
    # 2026 targets (daily)
    targets_2026 = {
        'January': 1591253.27,
        'February': 1714018.20,
        'March': 1807120.47,
        'April': 1727299.41,
        'May': 1390025.32,
        'June': 1638585.25
    }
    
    print('TEAM ASSIGNMENT CALCULATOR - 2026 PENANG TARGETS')
    print('='*60)
    
    print(f'CURRENT PERFORMANCE (2025):')
    print(f'Daily average: ${current_daily_avg:,.2f}')
    print(f'Monthly average: ${current_monthly_avg:,.2f}')
    print()
    
    print(f'2026 TARGETS:')
    total_incremental = 0
    monthly_assignments = {}
    
    for month, daily_target in targets_2026.items():
        monthly_target = daily_target * 30
        incremental_monthly = monthly_target - current_monthly_avg
        incremental_daily = daily_target - current_daily_avg
        
        monthly_assignments[month] = {
            'daily_target': daily_target,
            'monthly_target': monthly_target,
            'incremental_daily': incremental_daily,
            'incremental_monthly': incremental_monthly
        }
        
        total_incremental += incremental_monthly
        
        print(f'{month}:')
        print(f'  Daily target: ${daily_target:,.2f}')
        print(f'  Monthly target: ${monthly_target:,.2f}')
        print(f'  Incremental daily: ${incremental_daily:,.2f}')
        print(f'  Incremental monthly: ${incremental_monthly:,.2f}')
        print()
    
    print(f'TOTAL INCREMENTAL GMV (6 months): ${total_incremental:,.2f}')
    print(f'Average incremental monthly: ${total_incremental/6:,.2f}')
    print(f'Average incremental daily: ${total_incremental/6/30:,.2f}')
    
    return monthly_assignments, total_incremental

def calculate_team_assignments(monthly_assignments, total_incremental, team_size=5):
    """Calculate how to distribute incremental GMV among team members"""
    
    print('\n' + '='*60)
    print('TEAM ASSIGNMENT DISTRIBUTION')
    print('='*60)
    
    # Calculate per-person assignments
    avg_incremental_per_person = total_incremental / team_size
    avg_daily_per_person = avg_incremental_per_person / (6 * 30)
    
    print(f'TEAM SIZE: {team_size} people')
    print(f'Average incremental per person (6 months): ${avg_incremental_per_person:,.2f}')
    print(f'Average incremental per person (monthly): ${avg_incremental_per_person/6:,.2f}')
    print(f'Average incremental per person (daily): ${avg_daily_per_person:,.2f}')
    print()
    
    # Monthly breakdown per person
    print('MONTHLY ASSIGNMENTS PER PERSON:')
    for month, data in monthly_assignments.items():
        per_person_monthly = data['incremental_monthly'] / team_size
        per_person_daily = data['incremental_daily'] / team_size
        
        print(f'{month}:')
        print(f'  Per person (monthly): ${per_person_monthly:,.2f}')
        print(f'  Per person (daily): ${per_person_daily:,.2f}')
        print()
    
    # Different team size scenarios
    print('DIFFERENT TEAM SIZE SCENARIOS:')
    print('-' * 40)
    
    for team_size in [3, 4, 5, 6, 8, 10]:
        per_person_total = total_incremental / team_size
        per_person_monthly = per_person_total / 6
        per_person_daily = per_person_monthly / 30
        
        print(f'{team_size} people:')
        print(f'  Per person (6 months): ${per_person_total:,.2f}')
        print(f'  Per person (monthly): ${per_person_monthly:,.2f}')
        print(f'  Per person (daily): ${per_person_daily:,.2f}')
        print()

def calculate_realistic_targets():
    """Calculate more realistic targets based on different growth scenarios"""
    
    print('\n' + '='*60)
    print('REALISTIC TARGET SCENARIOS')
    print('='*60)
    
    current_daily = 349899.64
    current_monthly = current_daily * 30
    
    # Different growth scenarios
    scenarios = {
        'Conservative (50% growth)': 1.5,
        'Moderate (100% growth)': 2.0,
        'Aggressive (200% growth)': 3.0,
        'Very Aggressive (300% growth)': 4.0,
        'Current Target (370% growth)': 4.7
    }
    
    print('GROWTH SCENARIO ANALYSIS:')
    print('-' * 40)
    
    for scenario_name, multiplier in scenarios.items():
        target_daily = current_daily * multiplier
        target_monthly = target_daily * 30
        incremental_daily = target_daily - current_daily
        incremental_monthly = target_monthly - current_monthly
        
        print(f'{scenario_name}:')
        print(f'  Daily target: ${target_daily:,.2f}')
        print(f'  Monthly target: ${target_monthly:,.2f}')
        print(f'  Incremental daily: ${incremental_daily:,.2f}')
        print(f'  Incremental monthly: ${incremental_monthly:,.2f}')
        print(f'  Growth rate: {(multiplier-1)*100:.1f}%')
        print()

def calculate_team_capacity_analysis():
    """Analyze team capacity vs required assignments"""
    
    print('\n' + '='*60)
    print('TEAM CAPACITY ANALYSIS')
    print('='*60)
    
    # Current performance
    current_daily = 349899.64
    current_monthly = current_daily * 30
    
    # Target performance
    target_daily = 1644716.99
    target_monthly = target_daily * 30
    
    # Incremental needed
    incremental_daily = target_daily - current_daily
    incremental_monthly = target_monthly - current_monthly
    
    print(f'CURRENT vs TARGET ANALYSIS:')
    print(f'Current daily: ${current_daily:,.2f}')
    print(f'Target daily: ${target_daily:,.2f}')
    print(f'Incremental daily: ${incremental_daily:,.2f}')
    print(f'Incremental monthly: ${incremental_monthly:,.2f}')
    print()
    
    # Team capacity assumptions
    print('TEAM CAPACITY ASSUMPTIONS:')
    print('-' * 30)
    
    # Assume each person can handle different amounts
    capacity_scenarios = {
        'Low capacity (50K monthly)': 50000,
        'Medium capacity (100K monthly)': 100000,
        'High capacity (200K monthly)': 200000,
        'Very high capacity (300K monthly)': 300000
    }
    
    for capacity_name, monthly_capacity in capacity_scenarios.items():
        people_needed = incremental_monthly / monthly_capacity
        print(f'{capacity_name}:')
        print(f'  People needed: {people_needed:.1f}')
        print(f'  If 5 people: ${monthly_capacity * 5:,.2f} monthly capacity')
        print(f'  Gap: ${incremental_monthly - (monthly_capacity * 5):,.2f}')
        print()

def main():
    """Main analysis function"""
    
    # Calculate incremental assignments
    monthly_assignments, total_incremental = calculate_incremental_assignments()
    
    # Calculate team assignments
    calculate_team_assignments(monthly_assignments, total_incremental, team_size=5)
    
    # Calculate realistic targets
    calculate_realistic_targets()
    
    # Calculate team capacity analysis
    calculate_team_capacity_analysis()
    
    print('\n' + '='*60)
    print('KEY RECOMMENDATIONS')
    print('='*60)
    
    print('1. INCREMENTAL ASSIGNMENTS:')
    print(f'   • Total incremental GMV needed: ${total_incremental:,.2f}')
    print(f'   • Average monthly incremental: ${total_incremental/6:,.2f}')
    print(f'   • Average daily incremental: ${total_incremental/6/30:,.2f}')
    print()
    
    print('2. TEAM ASSIGNMENTS (5 people):')
    print(f'   • Per person (6 months): ${total_incremental/5:,.2f}')
    print(f'   • Per person (monthly): ${total_incremental/5/6:,.2f}')
    print(f'   • Per person (daily): ${total_incremental/5/6/30:,.2f}')
    print()
    
    print('3. REALISTIC CONSIDERATIONS:')
    print('   • Current targets require 370% growth - extremely aggressive')
    print('   • Consider more realistic targets (50-200% growth)')
    print('   • May need to expand team size significantly')
    print('   • Focus on high-impact, high-return activities')
    print()
    
    print('4. ACTION ITEMS:')
    print('   • Assign specific monthly targets to each team member')
    print('   • Set up daily tracking and monitoring')
    print('   • Plan marketing campaigns to support targets')
    print('   • Consider hiring additional team members')
    print('   • Review targets for realism and achievability')

if __name__ == "__main__":
    main()
