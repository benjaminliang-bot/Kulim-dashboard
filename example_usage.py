#!/usr/bin/env python3
"""
Example Usage: How to split organic and inorganic growth from your GMV data
"""

import pandas as pd
import numpy as np
from simple_growth_splitter import split_organic_inorganic_growth, plot_growth_split, print_summary

def load_your_data():
    """
    Load your actual GMV data
    Replace this with your actual data loading code
    """
    # Example: Load from CSV
    # df = pd.read_csv('your_gmv_data.csv')
    
    # Example: Load from Excel
    # df = pd.read_excel('your_gmv_data.xlsx')
    
    # Example: Load from database
    # import sqlite3
    # conn = sqlite3.connect('your_database.db')
    # df = pd.read_sql_query("SELECT * FROM gmv_table", conn)
    
    # For demonstration, create sample data
    print("Creating sample data (replace with your actual data loading)...")
    
    np.random.seed(42)
    start_date = pd.to_datetime('2023-01-01')
    end_date = pd.to_datetime('2024-12-31')
    dates = pd.date_range(start_date, end_date, freq='D')
    
    data = []
    for date in dates:
        # Simulate organic growth (trend + seasonal + noise)
        trend = 1000 + (date - start_date).days * 2
        seasonal = 200 * np.sin(2 * np.pi * (date - start_date).days / 365)
        organic_gmv = trend + seasonal + np.random.normal(0, 50)
        
        # Simulate inorganic growth (random spikes)
        inorganic_gmv = np.random.exponential(100) if np.random.random() < 0.1 else 0
        
        # Simulate source attribution
        sources = ['organic_search', 'direct', 'paid_search', 'social_ads', 'email', 'referral']
        source = np.random.choice(sources, p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.1])
        
        data.append({
            'date': date,
            'gmv': organic_gmv + inorganic_gmv,
            'source': source
        })
    
    return pd.DataFrame(data)

def analyze_growth_attribution():
    """Main analysis function"""
    
    print("="*60)
    print("GROWTH ATTRIBUTION ANALYSIS")
    print("="*60)
    
    # Load your data
    df = load_your_data()
    
    print(f"Data loaded: {len(df)} records")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total GMV: ${df['gmv'].sum():,.2f}")
    print()
    
    # Method 1: Baseline Method (Recommended for most cases)
    print("METHOD 1: BASELINE METHOD")
    print("-" * 30)
    print("Uses moving average as organic growth baseline")
    print("Inorganic growth = deviations from baseline")
    print()
    
    results1 = split_organic_inorganic_growth(
        df, 
        gmv_column='gmv', 
        date_column='date', 
        method='baseline',
        window=30  # 30-day moving average
    )
    
    print_summary(results1)
    plot_growth_split(results1, "Baseline Method - 30 Day Window")
    
    # Method 2: Time Series Decomposition
    print("\n" + "="*60)
    print("METHOD 2: TIME SERIES DECOMPOSITION")
    print("-" * 30)
    print("Separates trend, seasonal, and residual components")
    print("Organic = trend + seasonal, Inorganic = residual")
    print()
    
    results2 = split_organic_inorganic_growth(
        df, 
        gmv_column='gmv', 
        date_column='date', 
        method='decomposition'
    )
    
    print_summary(results2)
    plot_growth_split(results2, "Time Series Decomposition Method")
    
    # Method 3: Source Attribution (if you have source data)
    print("\n" + "="*60)
    print("METHOD 3: SOURCE ATTRIBUTION")
    print("-" * 30)
    print("Attributes growth based on traffic source")
    print("Organic sources vs Inorganic sources")
    print()
    
    # Define organic sources
    organic_sources = ['organic_search', 'direct', 'referral', 'email']
    
    results3 = split_organic_inorganic_growth(
        df, 
        gmv_column='gmv', 
        date_column='date', 
        method='source',
        source_column='source',
        organic_sources=organic_sources
    )
    
    print_summary(results3)
    plot_growth_split(results3, "Source Attribution Method")
    
    # Compare methods
    print("\n" + "="*60)
    print("METHOD COMPARISON")
    print("="*60)
    
    methods = {
        'Baseline': results1,
        'Decomposition': results2,
        'Source Attribution': results3
    }
    
    comparison_data = []
    for method_name, results in methods.items():
        organic_share = results['organic_gmv'].sum() / (results['organic_gmv'].sum() + results['inorganic_gmv'].sum()) * 100
        inorganic_share = results['inorganic_gmv'].sum() / (results['organic_gmv'].sum() + results['inorganic_gmv'].sum()) * 100
        
        comparison_data.append({
            'Method': method_name,
            'Organic Share (%)': f"{organic_share:.1f}%",
            'Inorganic Share (%)': f"{inorganic_share:.1f}%",
            'Avg Organic Growth (%)': f"{results['organic_growth_rate'].mean()*100:.2f}%",
            'Avg Inorganic Growth (%)': f"{results['inorganic_growth_rate'].mean()*100:.2f}%"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    print(comparison_df.to_string(index=False))
    
    # Export results
    print("\n" + "="*60)
    print("EXPORTING RESULTS")
    print("="*60)
    
    # Export detailed results
    with pd.ExcelWriter('growth_attribution_results.xlsx', engine='openpyxl') as writer:
        # Method 1 results
        method1_df = pd.DataFrame({
            'Date': results1['organic_gmv'].index,
            'Organic_GMV': results1['organic_gmv'].values,
            'Inorganic_GMV': results1['inorganic_gmv'].values,
            'Total_GMV': results1['organic_gmv'].values + results1['inorganic_gmv'].values,
            'Organic_Growth_Rate': results1['organic_growth_rate'].values,
            'Inorganic_Growth_Rate': results1['inorganic_growth_rate'].values
        })
        method1_df.to_excel(writer, sheet_name='Baseline_Method', index=False)
        
        # Method 2 results
        method2_df = pd.DataFrame({
            'Date': results2['organic_gmv'].index,
            'Organic_GMV': results2['organic_gmv'].values,
            'Inorganic_GMV': results2['inorganic_gmv'].values,
            'Total_GMV': results2['organic_gmv'].values + results2['inorganic_gmv'].values,
            'Organic_Growth_Rate': results2['organic_growth_rate'].values,
            'Inorganic_Growth_Rate': results2['inorganic_growth_rate'].values
        })
        method2_df.to_excel(writer, sheet_name='Decomposition_Method', index=False)
        
        # Method 3 results
        method3_df = pd.DataFrame({
            'Date': results3['organic_gmv'].index,
            'Organic_GMV': results3['organic_gmv'].values,
            'Inorganic_GMV': results3['inorganic_gmv'].values,
            'Total_GMV': results3['organic_gmv'].values + results3['inorganic_gmv'].values,
            'Organic_Growth_Rate': results3['organic_growth_rate'].values,
            'Inorganic_Growth_Rate': results3['inorganic_growth_rate'].values
        })
        method3_df.to_excel(writer, sheet_name='Source_Attribution_Method', index=False)
        
        # Comparison
        comparison_df.to_excel(writer, sheet_name='Method_Comparison', index=False)
    
    print("Results exported to 'growth_attribution_results.xlsx'")
    
    # Recommendations
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    print("1. BASELINE METHOD: Best for most business cases")
    print("   - Simple and interpretable")
    print("   - Works well with consistent data")
    print("   - Adjust window size based on your business cycle")
    print()
    print("2. DECOMPOSITION METHOD: Best for seasonal businesses")
    print("   - Captures seasonal patterns well")
    print("   - Good for retail, e-commerce with clear seasonality")
    print("   - May over-attribute to organic growth")
    print()
    print("3. SOURCE ATTRIBUTION: Best when you have reliable source data")
    print("   - Most accurate if source data is clean")
    print("   - Requires proper source classification")
    print("   - May miss cross-channel effects")
    print()
    print("RECOMMENDED APPROACH:")
    print("- Use Baseline method as primary")
    print("- Validate with Source attribution if available")
    print("- Use Decomposition for seasonal validation")
    print("- Combine insights from all methods for final decision")

if __name__ == "__main__":
    analyze_growth_attribution()
