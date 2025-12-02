import pandas as pd
import re
import numpy as np
from io import StringIO
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# ---------------------------------
# 1. YOUR CLEAN DATA
# ---------------------------------

# Here is the clean data you provided:
data_string = """
City	Jan-24	Feb-24	Mar-24	Apr-24	May-24	Jun-24	Jul-24	Aug-24	Sep-24	Oct-24	Nov-24	Dec-24	Jan-25	Feb-25	Mar-25	Apr-25	May-25	Jun-25	Jul-25	Aug-25	Sep-25	Oct-25	Nov-25	Dec-25
Alor Setar	54.1	56.3	59.86	58.4	59.27	56.51	57.45	59.4	59.31	59.79	58.44	60.75	63.65	60.04	66.44	66.03	56.61	56.2	52.37	55.31	59.91	58.43	58.43	58.43
Batu Pahat	39.75	44.81	48.68	38.67	43.31	43.17	41.3	41.69	43.49	41.39	43.41	45.09	49.95	46.72	47.47	48.77	45.27	44.8	43.34	44.57	43.93	43.2	43.2	43.2
Bintulu	43.32	44.44	54.92	50.11	50.2	44.28	46.96	48.63	44.2	48.6	51.69	47.47	51.34	57.91	45.3	46.56	50.43	51.28	43.25	45.49	44.65	47.93	47.93	47.93
Ipoh	62.86	62.59	63.94	60.49	55.14	56.26	67.04	64.46	65.68	65.49	65.54	67.28	69.65	66.11	70.1	67.24	66.43	65.08	64.83	66.71	66.35	62.68	62.68	62.68
Johor Bahru	65.86	65.86	66.31	66.24	67.07	67.89	68.97	70.64	69.76	68.54	69.19	70.16	71.57	69.92	69.84	69.24	69.38	69.78	69.72	70.56	70.47	68.31	68.31	68.31
Kangar	37.29	39	31.95	37.52	34.79	36.61	34.69	37	47.98	42.42	35.76	40.61	37.48	38.45	41.99	40.39	36.62	39.71	41.8	43.88	48.47	37.81	37.81	37.81
Kemaman	36.29	33.64	39.5	38.05	31	33.56	32.36	31.79	36.94	38.27	38.54	38.33	37.09	35.27	46.68	39.52	38.5	37.29	39.92	38.31	37.32	35.15	35.15	35.15
Kluang	33.78	39.46	36.88	32.81	32.92	31.93	35.08	38.39	43.59	44.24	47.54	57.67	50.47	51.33	60.49	60.24	64.03	58.31	48.82	44.59	44.03	36.46	36.46	36.46
Kota Bharu	41.86	41.22	41.85	43.05	40	42.86	49.3	47.76	45.06	44.21	45.07	73.78	46.72	44.17	50.21	46.53	45.24	46.71	43.87	42.29	45.52	44.1	44.1	44.1
Kota Kinabalu	42.83	43.12	41.29	42.15	42.95	42.46	42.72	43.7	44.02	43.99	43.42	45.44	44.23	45.08	42.77	42.89	43.15	43.76	43.15	45.62	44.47	43.24	43.24	43.24
Kuala Terengganu	40.84	41.6	39.7	47.29	36.59	39.45	38.98	41.32	40.65	43.31	43.23	49.5	50.41	48.31	56.3	48.56	47.98	49.57	43.32	41.75	41.06	41.13	41.13	41.13
Kuantan	60.94	60.37	62.07	63.95	62.42	62.23	63.76	63.69	59.7	55.8	53.62	52.87	54.49	55.37	56.8	55.88	55.32	57.25	56.49	65.22	60.3	62.75	62.75	62.75
Kuching	46.01	45.4	45.52	45.45	46.11	45.05	44.54	46.18	45.31	45.39	45.66	47.33	47.21	46.76	45.74	45.26	44.87	45.28	47.03	49.59	45.77	45.97	45.97	45.97
Labuan	56.42	51.34	47.67	48.01	54.19	51.41	51.99	51.92	51	49.42	53.13	49.58	53.25	49.37	55.64	52.12	49.01	51.54	52.32	58.61	51.51	52.07	52.07	52.07
Lahad Datu	31.56	31.92	34.68	28.74	29.91	32.84	34.24	30.1	44.35	34.02	39.14	37.06	43.14	38.34	41.29	43.63	37.15	49.69	42.11	44.79	44.8	33.48	33.48	33.48
Langkawi	43.63	47.28	49.22	46.28	42.16	46.16	45.8	48.95	45.59	46	48.09	49.49	46.33	47.66	52.24	50.51	43.66	46.86	51.57	52.24	46.05	46.59	46.59	46.59
Melaka	54.49	55.87	56.14	54.54	56.19	55.1	57.23	57.28	59.7	60.27	59.57	63.48	63.89	62.09	65.25	62.89	77.71	62.14	63.57	65.4	60.3	56.85	56.85	56.85
Miri	45.8	43.78	46.05	43.37	42.98	44.66	45.34	46.35	47.24	47.47	47.64	51.53	51.07	50.19	51.16	47.45	47.63	47.96	50.3	49.89	47.72	45.52	45.52	45.52
Muar	43.26	47.05	47.01	46.88	47.21	47.68	45.59	45.76	48.54	47.9	44.76	46.02	53.48	52.06	50.07	51.58	46.25	45.61	47.75	45.4	49.03	47.02	47.02	47.02
Negeri Sembilan	62.09	64.75	68.29	67.17	66.84	66.82	67.08	69.86	68.57	67.99	70	69.77	71.03	69.85	72.53	70.95	71.4	69.88	68.84	70.18	69.27	67.51	67.51	67.51
Penang	73.03	72.18	73.63	72.75	74.96	74.21	72.66	77.68	77.33	75.16	76.47	77.26	80.13	78.65	79.78	77.62	77.34	76	75.12	78.39	78.12	75.02	75.02	75.02
Sandakan	38.05	41.52	38.8	37.85	40.65	38.38	36.84	41.33	37.55	42.35	38.58	43.96	42.65	40.98	39.26	38.39	36.66	37.6	38.86	41.43	37.94	39.39	39.39	39.39
Sibu	40.92	40.29	45.72	43.92	46.74	41.22	39.96	38.92	40.98	41.12	43.37	41.24	42.43	43.7	40.81	40.46	42.19	40.78	43.8	57.53	41.39	42.5	42.5	42.5
Sungai Petani	41.46	44.67	47.6	49.63	43.94	47.29	45.43	46	47.05	43.69	49.04	64.77	46.89	48.72	49.8	48.24	46.43	45.37	44.31	54.01	47.53	46.36	46.36	46.36
Tawau	41.3	39.12	39.74	41.5	44.39	45.08	43.94	46.82	46.89	44.9	43.5	47.81	46.44	46.26	49.12	45.74	43.47	45.64	46.32	48.15	47.37	43.63	43.63	43.63
"""

# ---------------------------------
# 2. DATA CLEANING AND PREPARATION
# ---------------------------------

# Read the data. This assumes your data is tab-separated (which is
# standard when copying from Excel).
# It sets the first column ('City') as the index.
try:
    # Use StringIO to read the string as a file
    # Use sep=r'\t' to split by tabs, and index_col=0 to set 'City' as the row index
    df = pd.read_csv(StringIO(data_string.strip()), sep=r'\t+', engine='python', index_col=0)
except Exception as e:
    print(f"Error reading data: {e}")
    print("---")
    print("Could not parse the data. Please make sure you pasted it correctly inside the \"\"\"...\"\"\"")
    exit()

# Convert all data columns to numeric, just in case
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert columns from strings ('Jan-24') to datetime objects
# The format '%b-%y' matches 'Jan-24'
try:
    df.columns = pd.to_datetime(df.columns, format='%b-%y')
except ValueError as e:
    print(f"Error converting date headers: {e}")
    print("Please make sure your headers are in 'Jan-24' format.")
    exit()

# Transpose so rows are time and columns are cities
df_ts = df.T

# ---------------------------------
# 3. FORECASTING (with Imputation)
# ---------------------------------

forecasts = {}
# Create the date range for the 2026 forecast
forecast_dates = pd.date_range(start='2026-01-01', periods=12, freq='MS')

for city in df_ts.columns:
    city_data = df_ts[city]
    
    # --- Handle Missing Data (NaNs) ---
    # 1. Interpolate: Fill gaps *between* data points
    city_data_filled = city_data.interpolate(method='linear')
    # 2. ffill/bfill: Fill any remaining NaNs at the start or end
    city_data_filled = city_data_filled.ffill().bfill()
    
    # Check if series is *still* all-NaN
    if city_data_filled.isnull().all():
        print(f"Warning: Skipping {city} due to all-NaN data. Forecasting 0.")
        pred = pd.Series([0.0] * 12, index=forecast_dates)
    else:
        try:
            # Initialize the ETS (Holt-Winters) model
            model = ExponentialSmoothing(
                city_data_filled,  # Use the *filled* data
                trend='add', 
                seasonal='add', 
                seasonal_periods=12, # 12 months in a year
                damped_trend=True  # Prevents trend from going to infinity
            )
            
            # Fit the model
            fit = model.fit()
            
            # Generate the forecast
            pred = fit.forecast(steps=12)
            
        except Exception as e:
            # Fallback in case the model fails
            print(f"Warning: Model failed for {city}. Using simple mean. Error: {e}")
            pred = pd.Series([city_data_filled.mean()] * 12, index=forecast_dates)

    # AOV shouldn't be negative, so we set a floor of 0
    pred[pred < 0] = 0
    forecasts[city] = pred

# ---------------------------------
# 4. EXPORT RESULTS
# ---------------------------------

# Combine all city forecasts into a single DataFrame
forecast_df = pd.DataFrame(forecasts)

# Transpose back to the original orientation (Cities as rows)
forecast_df_final = forecast_df.T

# Set the column names to the forecasted months
forecast_df_final.columns = forecast_dates.strftime('%b-2026')

# Define the output filename
output_filename = "forecast_AOV_2026.csv"

# Export the DataFrame to a CSV file, formatting to 2 decimal places
forecast_df_final.to_csv(output_filename, float_format='%.2f')

print(f"✅ Successfully exported AOV forecast to: {output_filename}")

# Print the DataFrame to the console
print("\n--- AOV Forecast for 2026 ---")
print(forecast_df_final.round(2))