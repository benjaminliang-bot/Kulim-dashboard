#!/usr/bin/env python3
"""
Analyze your 2025 daily GMV data for organic vs inorganic growth
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data(file_path):
    """Load and clean the Excel data"""
    print("Loading data from Excel file...")
    
    # Load the data
    df = pd.read_excel(file_path)
    
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Clean the data
    # Replace [NULL] with NaN
    df = df.replace('[NULL]', np.nan)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Convert GMV to numeric, handling any non-numeric values
    df['gmv'] = pd.to_numeric(df['gmv'], errors='coerce')
    
    # Remove rows with missing GMV
    df_clean = df.dropna(subset=['gmv'])
    
    print(f"After cleaning: {df_clean.shape}")
    print(f"Date range: {df_clean['date'].min()} to {df_clean['date'].max()}")
    print(f"Total GMV: ${df_clean['gmv'].sum():,.2f}")
    
    return df_clean

def split_organic_inorganic_growth(df, gmv_column='gmv', date_column='date', method='baseline', window=30):
    """Split GMV growth into organic and inorganic components"""
    
    # Aggregate by date (in case there are multiple records per date)
    daily_gmv = df.groupby(date_column)[gmv_column].sum()
    
    if method == 'baseline':
        # Calculate moving average baseline
        baseline = daily_gmv.rolling(window=window).mean()
        
        # Calculate growth rates
        actual_growth = daily_gmv.pct_change()
        baseline_growth = baseline.pct_change()
        
        # Identify inorganic growth as deviations from baseline
        inorganic_growth = actual_growth - baseline_growth
        
        # Calculate GMV components
        organic_gmv = daily_gmv * (1 + baseline_growth.fillna(0))
        inorganic_gmv = daily_gmv - organic_gmv
        
        return {
            'organic_gmv': organic_gmv,
            'inorganic_gmv': inorganic_gmv,
            'organic_growth_rate': baseline_growth,
            'inorganic_growth_rate': inorganic_growth,
            'baseline': baseline,
            'method': 'baseline'
        }
    
    elif method == 'decomposition':
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        # Decompose time series
        decomposition = seasonal_decompose(daily_gmv, model='additive', period=30)
        
        # Extract components
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        
        # Organic = trend + seasonal (predictable patterns)
        # Inorganic = residual (unexplained variations)
        organic_gmv = trend + seasonal
        inorganic_gmv = residual
        
        # Calculate growth rates
        organic_growth = organic_gmv.pct_change().fillna(0)
        inorganic_growth = inorganic_gmv.pct_change().fillna(0)
        
        return {
            'organic_gmv': organic_gmv,
            'inorganic_gmv': inorganic_gmv,
            'organic_growth_rate': organic_growth,
            'inorganic_growth_rate': inorganic_growth,
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'method': 'decomposition'
        }

def analyze_by_dimensions(df):
    """Analyze growth by different dimensions (city, category, region)"""
    
    print("\n" + "="*60)
    print("ANALYSIS BY DIMENSIONS")
    print("="*60)
    
    # By City
    if 'city' in df.columns:
        print("\nTop 10 Cities by GMV:")
        city_gmv = df.groupby('city')['gmv'].sum().sort_values(ascending=False).head(10)
        for city, gmv in city_gmv.items():
            print(f"{city}: ${gmv:,.2f}")
    
    # By Category
    if 'category_win' in df.columns:
        print("\nGMV by Category:")
        category_gmv = df.groupby('category_win')['gmv'].sum().sort_values(ascending=False)
        for category, gmv in category_gmv.items():
            print(f"{category}: ${gmv:,.2f}")
    
    # By Region
    if 'region' in df.columns:
        print("\nGMV by Region:")
        region_gmv = df.groupby('region')['gmv'].sum().sort_values(ascending=False)
        for region, gmv in region_gmv.items():
            print(f"{region}: ${gmv:,.2f}")

def plot_growth_analysis(results, title="Growth Attribution Analysis"):
    """Plot the growth analysis results"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: GMV Components
    axes[0, 0].plot(results['organic_gmv'].index, results['organic_gmv'].values, 
                    label='Organic GMV', color='green', linewidth=2)
    axes[0, 0].plot(results['inorganic_gmv'].index, results['inorganic_gmv'].values, 
                    label='Inorganic GMV', color='red', linewidth=2)
    axes[0, 0].set_title('GMV Components Over Time')
    axes[0, 0].set_ylabel('GMV')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Growth Rates
    axes[0, 1].plot(results['organic_growth_rate'].index, results['organic_growth_rate'].values, 
                    label='Organic Growth', color='green', alpha=0.7)
    axes[0, 1].plot(results['inorganic_growth_rate'].index, results['inorganic_growth_rate'].values, 
                    label='Inorganic Growth', color='red', alpha=0.7)
    axes[0, 1].set_title('Growth Rates Over Time')
    axes[0, 1].set_ylabel('Growth Rate')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Cumulative Growth
    cumulative_organic = (1 + results['organic_growth_rate']).cumprod()
    cumulative_inorganic = (1 + results['inorganic_growth_rate']).cumprod()
    
    axes[1, 0].plot(cumulative_organic.index, cumulative_organic.values, 
                    label='Cumulative Organic', color='green', linewidth=2)
    axes[1, 0].plot(cumulative_inorganic.index, cumulative_inorganic.values, 
                    label='Cumulative Inorganic', color='red', linewidth=2)
    axes[1, 0].set_title('Cumulative Growth')
    axes[1, 0].set_ylabel('Cumulative Growth Factor')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Distribution of Growth Rates
    axes[1, 1].hist(results['organic_growth_rate'].dropna(), bins=30, alpha=0.7, 
                    label='Organic Growth', color='green', density=True)
    axes[1, 1].hist(results['inorganic_growth_rate'].dropna(), bins=30, alpha=0.7, 
                    label='Inorganic Growth', color='red', density=True)
    axes[1, 1].set_title('Distribution of Growth Rates')
    axes[1, 1].set_xlabel('Growth Rate')
    axes[1, 1].set_ylabel('Density')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.show()

def print_summary(results):
    """Print summary statistics"""
    
    print("\n" + "="*60)
    print("GROWTH ATTRIBUTION SUMMARY")
    print("="*60)
    
    # Calculate summary statistics
    organic_growth_mean = results['organic_growth_rate'].mean()
    inorganic_growth_mean = results['inorganic_growth_rate'].mean()
    
    organic_gmv_total = results['organic_gmv'].sum()
    inorganic_gmv_total = results['inorganic_gmv'].sum()
    total_gmv = organic_gmv_total + inorganic_gmv_total
    
    organic_share = organic_gmv_total / total_gmv * 100
    inorganic_share = inorganic_gmv_total / total_gmv * 100
    
    print(f"Method: {results['method'].upper()}")
    print(f"Total GMV: ${total_gmv:,.2f}")
    print(f"Organic GMV: ${organic_gmv_total:,.2f} ({organic_share:.1f}%)")
    print(f"Inorganic GMV: ${inorganic_gmv_total:,.2f} ({inorganic_share:.1f}%)")
    print()
    print(f"Average Organic Growth Rate: {organic_growth_mean:.4f} ({organic_growth_mean*100:.2f}%)")
    print(f"Average Inorganic Growth Rate: {inorganic_growth_mean:.4f} ({inorganic_growth_mean*100:.2f}%)")
    print()
    print(f"Organic Growth Volatility: {results['organic_growth_rate'].std():.4f}")
    print(f"Inorganic Growth Volatility: {results['inorganic_growth_rate'].std():.4f}")

def main():
    """Main analysis function"""
    
    print("="*60)
    print("2025 DAILY GMV GROWTH ATTRIBUTION ANALYSIS")
    print("="*60)
    
    # Load and clean data
    file_path = r"C:\Users\benjamin.liang\Downloads\2025 daily .xlsx"
    df = load_and_clean_data(file_path)
    
    # Analyze by dimensions
    analyze_by_dimensions(df)
    
    # Method 1: Baseline Method
    print("\n" + "="*60)
    print("METHOD 1: BASELINE METHOD (30-day window)")
    print("="*60)
    
    results1 = split_organic_inorganic_growth(df, method='baseline', window=30)
    print_summary(results1)
    
    # Method 2: Time Series Decomposition
    print("\n" + "="*60)
    print("METHOD 2: TIME SERIES DECOMPOSITION")
    print("="*60)
    
    try:
        results2 = split_organic_inorganic_growth(df, method='decomposition')
        print_summary(results2)
    except Exception as e:
        print(f"Decomposition method failed: {e}")
        results2 = None
    
    # Compare methods
    if results2 is not None:
        print("\n" + "="*60)
        print("METHOD COMPARISON")
        print("="*60)
        
        methods = {
            'Baseline': results1,
            'Decomposition': results2
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
    with pd.ExcelWriter('growth_attribution_2025.xlsx', engine='openpyxl') as writer:
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
        
        # Method 2 results (if available)
        if results2 is not None:
            method2_df = pd.DataFrame({
                'Date': results2['organic_gmv'].index,
                'Organic_GMV': results2['organic_gmv'].values,
                'Inorganic_GMV': results2['inorganic_gmv'].values,
                'Total_GMV': results2['organic_gmv'].values + results2['inorganic_gmv'].values,
                'Organic_Growth_Rate': results2['organic_growth_rate'].values,
                'Inorganic_Growth_Rate': results2['inorganic_growth_rate'].values
            })
            method2_df.to_excel(writer, sheet_name='Decomposition_Method', index=False)
        
        # Comparison
        if results2 is not None:
            comparison_df.to_excel(writer, sheet_name='Method_Comparison', index=False)
        
        # Original data summary
        summary_df = df.groupby('date')['gmv'].sum().reset_index()
        summary_df.to_excel(writer, sheet_name='Daily_GMV_Summary', index=False)
    
    print("Results exported to 'growth_attribution_2025.xlsx'")
    
    # Plot results
    print("\nGenerating visualizations...")
    plot_growth_analysis(results1, "Baseline Method - 2025 GMV Analysis")
    
    if results2 is not None:
        plot_growth_analysis(results2, "Decomposition Method - 2025 GMV Analysis")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
