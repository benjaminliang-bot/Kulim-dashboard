#!/usr/bin/env python3
"""
Simple Growth Splitter
A straightforward tool to split organic and inorganic growth from GMV data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, List, Optional

def split_organic_inorganic_growth(df: pd.DataFrame, 
                                 gmv_column: str, 
                                 date_column: str,
                                 method: str = 'baseline',
                                 window: int = 30,
                                 source_column: Optional[str] = None,
                                 organic_sources: Optional[List[str]] = None) -> Dict:
    """
    Split GMV growth into organic and inorganic components
    
    Parameters:
    - df: DataFrame with GMV data
    - gmv_column: Name of GMV column
    - date_column: Name of date column
    - method: 'baseline', 'decomposition', or 'source'
    - window: Window size for baseline method
    - source_column: Name of source column (for source method)
    - organic_sources: List of organic source names
    
    Returns:
    - Dictionary with organic_gmv, inorganic_gmv, and growth rates
    """
    
    # Ensure date column is datetime
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(date_column)
    
    # Aggregate by date
    daily_gmv = df.groupby(date_column)[gmv_column].sum()
    
    if method == 'baseline':
        return _baseline_method(daily_gmv, window)
    elif method == 'decomposition':
        return _decomposition_method(daily_gmv)
    elif method == 'source' and source_column:
        return _source_method(df, gmv_column, date_column, source_column, organic_sources)
    else:
        raise ValueError("Invalid method or missing source_column for source method")

def _baseline_method(daily_gmv: pd.Series, window: int) -> Dict:
    """Baseline method: Use moving average as organic growth baseline"""
    
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
        'baseline': baseline
    }

def _decomposition_method(daily_gmv: pd.Series) -> Dict:
    """Decomposition method: Use time series decomposition"""
    
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
        'residual': residual
    }

def _source_method(df: pd.DataFrame, gmv_column: str, date_column: str, 
                  source_column: str, organic_sources: Optional[List[str]]) -> Dict:
    """Source method: Attribute based on source characteristics"""
    
    # Default organic sources
    if organic_sources is None:
        organic_sources = ['organic_search', 'direct', 'referral', 'email', 'organic_social']
    
    # Calculate GMV by source and date
    source_gmv = df.groupby([date_column, source_column])[gmv_column].sum().unstack(fill_value=0)
    
    # Calculate organic vs inorganic GMV
    organic_gmv = source_gmv[source_gmv.columns.intersection(organic_sources)].sum(axis=1)
    inorganic_gmv = source_gmv[source_gmv.columns.intersection(
        [col for col in source_gmv.columns if col not in organic_sources]
    )].sum(axis=1)
    
    # Fill missing values with 0
    organic_gmv = organic_gmv.fillna(0)
    inorganic_gmv = inorganic_gmv.fillna(0)
    
    # Calculate growth rates
    organic_growth = organic_gmv.pct_change().fillna(0)
    inorganic_growth = inorganic_gmv.pct_change().fillna(0)
    
    return {
        'organic_gmv': organic_gmv,
        'inorganic_gmv': inorganic_gmv,
        'organic_growth_rate': organic_growth,
        'inorganic_growth_rate': inorganic_growth,
        'source_breakdown': source_gmv
    }

def plot_growth_split(results: Dict, title: str = "Growth Attribution"):
    """Plot the growth split results"""
    
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

def print_summary(results: Dict):
    """Print summary statistics"""
    
    print("\n" + "="*50)
    print("GROWTH ATTRIBUTION SUMMARY")
    print("="*50)
    
    # Calculate summary statistics
    organic_growth_mean = results['organic_growth_rate'].mean()
    inorganic_growth_mean = results['inorganic_growth_rate'].mean()
    
    organic_gmv_total = results['organic_gmv'].sum()
    inorganic_gmv_total = results['inorganic_gmv'].sum()
    total_gmv = organic_gmv_total + inorganic_gmv_total
    
    organic_share = organic_gmv_total / total_gmv * 100
    inorganic_share = inorganic_gmv_total / total_gmv * 100
    
    print(f"Total GMV: ${total_gmv:,.2f}")
    print(f"Organic GMV: ${organic_gmv_total:,.2f} ({organic_share:.1f}%)")
    print(f"Inorganic GMV: ${inorganic_gmv_total:,.2f} ({inorganic_share:.1f}%)")
    print()
    print(f"Average Organic Growth Rate: {organic_growth_mean:.4f} ({organic_growth_mean*100:.2f}%)")
    print(f"Average Inorganic Growth Rate: {inorganic_growth_mean:.4f} ({inorganic_growth_mean*100:.2f}%)")
    print()
    print(f"Organic Growth Volatility: {results['organic_growth_rate'].std():.4f}")
    print(f"Inorganic Growth Volatility: {results['inorganic_growth_rate'].std():.4f}")

# Example usage
if __name__ == "__main__":
    # Create sample data
    print("Creating sample data...")
    
    # Generate sample data
    np.random.seed(42)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    data = []
    for date in dates:
        # Organic growth (trend + seasonal)
        trend = 1000 + (date - start_date).days * 2
        seasonal = 200 * np.sin(2 * np.pi * (date - start_date).days / 365)
        organic_gmv = trend + seasonal + np.random.normal(0, 50)
        
        # Inorganic growth (random spikes)
        inorganic_gmv = np.random.exponential(100) if np.random.random() < 0.1 else 0
        
        # Source attribution
        sources = ['organic_search', 'direct', 'paid_search', 'social_ads', 'email']
        source = np.random.choice(sources, p=[0.3, 0.2, 0.2, 0.2, 0.1])
        
        data.append({
            'date': date,
            'gmv': organic_gmv + inorganic_gmv,
            'source': source
        })
    
    sample_df = pd.DataFrame(data)
    
    # Test different methods
    print("\nTesting different methods...")
    
    # Method 1: Baseline
    print("\n1. Baseline Method:")
    results1 = split_organic_inorganic_growth(sample_df, 'gmv', 'date', method='baseline')
    print_summary(results1)
    
    # Method 2: Decomposition
    print("\n2. Decomposition Method:")
    results2 = split_organic_inorganic_growth(sample_df, 'gmv', 'date', method='decomposition')
    print_summary(results2)
    
    # Method 3: Source Attribution
    print("\n3. Source Attribution Method:")
    results3 = split_organic_inorganic_growth(sample_df, 'gmv', 'date', method='source', 
                                            source_column='source')
    print_summary(results3)
    
    # Plot results
    print("\nGenerating visualizations...")
    plot_growth_split(results1, "Baseline Method")
    plot_growth_split(results2, "Decomposition Method")
    plot_growth_split(results3, "Source Attribution Method")
