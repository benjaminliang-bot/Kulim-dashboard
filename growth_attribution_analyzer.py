#!/usr/bin/env python3
"""
Growth Attribution Analyzer
A comprehensive tool for splitting organic and inorganic growth from GMV data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

class GrowthAttributionAnalyzer:
    def __init__(self):
        self.data = None
        self.organic_gmv = None
        self.inorganic_gmv = None
        self.models = {}
        
    def load_data(self, df: pd.DataFrame, gmv_column: str, date_column: str, 
                  source_column: Optional[str] = None):
        """Load and prepare data for analysis"""
        self.data = df.copy()
        self.gmv_column = gmv_column
        self.date_column = date_column
        self.source_column = source_column
        
        # Ensure date column is datetime
        self.data[date_column] = pd.to_datetime(self.data[date_column])
        self.data = self.data.sort_values(date_column)
        
        print(f"Data loaded: {len(self.data)} records from {self.data[date_column].min()} to {self.data[date_column].max()}")
        
    def method1_time_series_decomposition(self):
        """Method 1: Time Series Decomposition"""
        print("\n=== Method 1: Time Series Decomposition ===")
        
        # Aggregate data by date
        daily_gmv = self.data.groupby(self.date_column)[self.gmv_column].sum()
        
        # Decompose time series
        decomposition = seasonal_decompose(daily_gmv, model='additive', period=30)
        
        # Extract components
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        
        # Identify organic vs inorganic growth
        # Organic = trend + seasonal (predictable patterns)
        # Inorganic = residual (unexplained variations)
        organic_gmv = trend + seasonal
        inorganic_gmv = residual
        
        # Store results
        self.organic_gmv = organic_gmv
        self.inorganic_gmv = inorganic_gmv
        
        # Calculate growth rates
        organic_growth = organic_gmv.pct_change().fillna(0)
        inorganic_growth = inorganic_gmv.pct_change().fillna(0)
        
        print(f"Organic Growth Rate: {organic_growth.mean():.4f} ({organic_growth.mean()*100:.2f}%)")
        print(f"Inorganic Growth Rate: {inorganic_growth.mean():.4f} ({inorganic_growth.mean()*100:.2f}%)")
        
        return {
            'organic_gmv': organic_gmv,
            'inorganic_gmv': inorganic_gmv,
            'organic_growth_rate': organic_growth,
            'inorganic_growth_rate': inorganic_growth,
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual
        }
    
    def method2_baseline_growth(self, window: int = 30):
        """Method 2: Baseline Growth Model"""
        print(f"\n=== Method 2: Baseline Growth Model (window={window}) ===")
        
        # Aggregate data by date
        daily_gmv = self.data.groupby(self.date_column)[self.gmv_column].sum()
        
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
        
        # Store results
        self.organic_gmv = organic_gmv
        self.inorganic_gmv = inorganic_gmv
        
        print(f"Baseline Growth Rate: {baseline_growth.mean():.4f} ({baseline_growth.mean()*100:.2f}%)")
        print(f"Inorganic Growth Rate: {inorganic_growth.mean():.4f} ({inorganic_growth.mean()*100:.2f}%)")
        
        return {
            'organic_gmv': organic_gmv,
            'inorganic_gmv': inorganic_gmv,
            'baseline_growth_rate': baseline_growth,
            'inorganic_growth_rate': inorganic_growth,
            'baseline': baseline
        }
    
    def method3_source_attribution(self, organic_sources: List[str] = None, 
                                 inorganic_sources: List[str] = None):
        """Method 3: Source-Based Attribution"""
        if not self.source_column:
            print("Source column not provided. Skipping source attribution method.")
            return None
            
        print("\n=== Method 3: Source-Based Attribution ===")
        
        # Default source classifications
        if organic_sources is None:
            organic_sources = ['organic_search', 'direct', 'referral', 'email', 'organic_social']
        if inorganic_sources is None:
            inorganic_sources = ['paid_search', 'social_ads', 'display_ads', 'affiliate', 'paid_social']
        
        # Calculate GMV by source and date
        source_gmv = self.data.groupby([self.date_column, self.source_column])[self.gmv_column].sum().unstack(fill_value=0)
        
        # Calculate organic vs inorganic GMV
        organic_gmv = source_gmv[source_gmv.columns.intersection(organic_sources)].sum(axis=1)
        inorganic_gmv = source_gmv[source_gmv.columns.intersection(inorganic_sources)].sum(axis=1)
        
        # Fill missing values with 0
        organic_gmv = organic_gmv.fillna(0)
        inorganic_gmv = inorganic_gmv.fillna(0)
        
        # Store results
        self.organic_gmv = organic_gmv
        self.inorganic_gmv = inorganic_gmv
        
        # Calculate growth rates
        organic_growth = organic_gmv.pct_change().fillna(0)
        inorganic_growth = inorganic_gmv.pct_change().fillna(0)
        
        print(f"Organic Growth Rate: {organic_growth.mean():.4f} ({organic_growth.mean()*100:.2f}%)")
        print(f"Inorganic Growth Rate: {inorganic_growth.mean():.4f} ({inorganic_growth.mean()*100:.2f}%)")
        
        return {
            'organic_gmv': organic_gmv,
            'inorganic_gmv': inorganic_gmv,
            'organic_growth_rate': organic_growth,
            'inorganic_growth_rate': inorganic_growth,
            'source_breakdown': source_gmv
        }
    
    def method4_machine_learning(self, features: List[str] = None):
        """Method 4: Machine Learning Approach"""
        print("\n=== Method 4: Machine Learning Approach ===")
        
        # Prepare features
        if features is None:
            features = self._create_default_features()
        
        # Create feature matrix
        X = self._create_feature_matrix(features)
        y = self.data[self.gmv_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        results = {}
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            
            r2 = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            
            results[name] = {
                'model': model,
                'r2_score': r2,
                'mse': mse,
                'predictions': y_pred
            }
            
            print(f"{name} - R²: {r2:.4f}, MSE: {mse:.4f}")
        
        # Use best model for attribution
        best_model_name = max(results.keys(), key=lambda x: results[x]['r2_score'])
        best_model = results[best_model_name]['model']
        
        # Predict on full dataset
        X_full_scaled = scaler.transform(X)
        predictions = best_model.predict(X_full_scaled)
        
        # Calculate residuals (inorganic growth)
        residuals = y - predictions
        
        # Store results
        self.models['ml_model'] = best_model
        self.models['scaler'] = scaler
        self.models['features'] = features
        
        print(f"Best model: {best_model_name}")
        
        return {
            'model': best_model,
            'predictions': predictions,
            'residuals': residuals,
            'r2_score': results[best_model_name]['r2_score'],
            'feature_importance': self._get_feature_importance(best_model, features)
        }
    
    def _create_default_features(self) -> List[str]:
        """Create default features for ML model"""
        features = []
        
        # Date-based features
        self.data['year'] = self.data[self.date_column].dt.year
        self.data['month'] = self.data[self.date_column].dt.month
        self.data['day_of_week'] = self.data[self.date_column].dt.dayofweek
        self.data['day_of_month'] = self.data[self.date_column].dt.day
        
        features.extend(['year', 'month', 'day_of_week', 'day_of_month'])
        
        # Lag features
        for lag in [1, 7, 30]:
            self.data[f'gmv_lag_{lag}'] = self.data[self.gmv_column].shift(lag)
            features.append(f'gmv_lag_{lag}')
        
        # Rolling statistics
        for window in [7, 30]:
            self.data[f'gmv_ma_{window}'] = self.data[self.gmv_column].rolling(window=window).mean()
            self.data[f'gmv_std_{window}'] = self.data[self.gmv_column].rolling(window=window).std()
            features.extend([f'gmv_ma_{window}', f'gmv_std_{window}'])
        
        return features
    
    def _create_feature_matrix(self, features: List[str]) -> pd.DataFrame:
        """Create feature matrix for ML model"""
        # Remove rows with NaN values
        feature_data = self.data[features].fillna(0)
        return feature_data
    
    def _get_feature_importance(self, model, features: List[str]) -> pd.DataFrame:
        """Get feature importance from model"""
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_)
        else:
            return pd.DataFrame()
        
        return pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=False)
    
    def plot_growth_attribution(self, method: str = 'decomposition'):
        """Plot growth attribution results"""
        if self.organic_gmv is None or self.inorganic_gmv is None:
            print("No attribution results available. Run an attribution method first.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: GMV Components
        axes[0, 0].plot(self.organic_gmv.index, self.organic_gmv.values, label='Organic GMV', color='green')
        axes[0, 0].plot(self.inorganic_gmv.index, self.inorganic_gmv.values, label='Inorganic GMV', color='red')
        axes[0, 0].set_title('GMV Components Over Time')
        axes[0, 0].set_ylabel('GMV')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Plot 2: Growth Rates
        organic_growth = self.organic_gmv.pct_change().fillna(0)
        inorganic_growth = self.inorganic_gmv.pct_change().fillna(0)
        
        axes[0, 1].plot(organic_growth.index, organic_growth.values, label='Organic Growth', color='green')
        axes[0, 1].plot(inorganic_growth.index, inorganic_growth.values, label='Inorganic Growth', color='red')
        axes[0, 1].set_title('Growth Rates Over Time')
        axes[0, 1].set_ylabel('Growth Rate')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Plot 3: Cumulative Growth
        cumulative_organic = (1 + organic_growth).cumprod()
        cumulative_inorganic = (1 + inorganic_growth).cumprod()
        
        axes[1, 0].plot(cumulative_organic.index, cumulative_organic.values, label='Cumulative Organic', color='green')
        axes[1, 0].plot(cumulative_inorganic.index, cumulative_inorganic.values, label='Cumulative Inorganic', color='red')
        axes[1, 0].set_title('Cumulative Growth')
        axes[1, 0].set_ylabel('Cumulative Growth Factor')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Plot 4: Distribution of Growth Rates
        axes[1, 1].hist(organic_growth.dropna(), bins=30, alpha=0.7, label='Organic Growth', color='green')
        axes[1, 1].hist(inorganic_growth.dropna(), bins=30, alpha=0.7, label='Inorganic Growth', color='red')
        axes[1, 1].set_title('Distribution of Growth Rates')
        axes[1, 1].set_xlabel('Growth Rate')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def export_results(self, filename: str):
        """Export results to Excel"""
        if self.organic_gmv is None or self.inorganic_gmv is None:
            print("No attribution results available. Run an attribution method first.")
            return
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Summary results
            summary_data = pd.DataFrame({
                'Date': self.organic_gmv.index,
                'Organic_GMV': self.organic_gmv.values,
                'Inorganic_GMV': self.inorganic_gmv.values,
                'Total_GMV': self.organic_gmv.values + self.inorganic_gmv.values,
                'Organic_Growth_Rate': self.organic_gmv.pct_change().fillna(0),
                'Inorganic_Growth_Rate': self.inorganic_gmv.pct_change().fillna(0)
            })
            
            summary_data.to_excel(writer, sheet_name='Growth_Attribution', index=False)
            
            # Feature importance (if available)
            if 'ml_model' in self.models and 'feature_importance' in self.models:
                self.models['feature_importance'].to_excel(writer, sheet_name='Feature_Importance', index=False)
        
        print(f"Results exported to {filename}")

def create_sample_data():
    """Create sample data for demonstration"""
    np.random.seed(42)
    
    # Create date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Create sample data
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
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Create sample data
    print("Creating sample data...")
    sample_data = create_sample_data()
    
    # Initialize analyzer
    analyzer = GrowthAttributionAnalyzer()
    analyzer.load_data(sample_data, 'gmv', 'date', 'source')
    
    # Run different attribution methods
    print("\n" + "="*60)
    print("GROWTH ATTRIBUTION ANALYSIS")
    print("="*60)
    
    # Method 1: Time Series Decomposition
    results1 = analyzer.method1_time_series_decomposition()
    
    # Method 2: Baseline Growth
    results2 = analyzer.method2_baseline_growth()
    
    # Method 3: Source Attribution
    results3 = analyzer.method3_source_attribution()
    
    # Method 4: Machine Learning
    results4 = analyzer.method4_machine_learning()
    
    # Plot results
    print("\nGenerating visualizations...")
    analyzer.plot_growth_attribution()
    
    # Export results
    analyzer.export_results("growth_attribution_results.xlsx")
    print("\nAnalysis complete!")
