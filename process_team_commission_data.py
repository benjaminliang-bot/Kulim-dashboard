import pandas as pd
import numpy as np

# We already have data for CY, Darren, Suki, and "Other" from the previous query
# Now we need to split "Other" into EK and XR using the tracker file

# Load tracker
path = r"C:\Users\benjamin.liang\Downloads\penang main tracker 2.xlsx"
df = pd.read_excel(path, sheet_name='Sheet1', header=1)
df.columns = [str(c) for c in df.columns]

# Get merchant assignments
ek_merchants = set(df[df['MGS'].notna()]['Mex ID'].dropna().unique())
xr_merchants = set(df[df['AMBD'] == 'NMA']['Mex ID'].dropna().unique())
cy_merchants = set(df[df['AM'].str.contains('chiayee', case=False, na=False)]['Mex ID'].dropna().unique())
darren_merchants = set(df[df['AM'].str.contains('darren', case=False, na=False)]['Mex ID'].dropna().unique())
suki_merchants = set(df[df['AM'].str.contains('suki', case=False, na=False)]['Mex ID'].dropna().unique())

print("Merchant counts from tracker:")
print(f"EK (MGS): {len(ek_merchants)}")
print(f"XR (NMA): {len(xr_merchants)}")
print(f"CY: {len(cy_merchants)}")
print(f"Darren: {len(darren_merchants)}")
print(f"Suki: {len(suki_merchants)}")

# The "Other" category from our query includes EK + XR + any unassigned
# We need to query EK and XR separately
# Let me create SQL queries that will work with the merchant lists

# For EK: Query merchants that are in the EK list
ek_query = f"""
WITH ek_merchants AS (
    SELECT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN ({','.join([f"'{m}'" for m in list(ek_merchants)[:1000]])})
),
monthly_ek_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as team_gmv,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.commission_from_merchant, 0) 
            ELSE 0 
        END) as team_commission_billing
    FROM ocd_adw.f_food_metrics f
    INNER JOIN ek_merchants em ON f.merchant_id = em.merchant_id_nk
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250101
        AND f.date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    month_id,
    'EK' as owner,
    team_gmv,
    team_commission_billing,
    ROUND(team_commission_billing * 100.0 / NULLIF(team_gmv, 0), 4) as commission_rate_pct
FROM monthly_ek_gmv
ORDER BY month_id
"""

print("\nNote: Due to large merchant lists, queries need to be batched")
print("Creating batched query approach...")

# Actually, let me try a simpler approach - query all merchants and then
# assign them in Python based on the tracker file
print("\nBetter approach: Query all Penang merchants and assign in Python")

