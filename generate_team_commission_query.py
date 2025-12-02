import pandas as pd

# Load tracker to get merchant assignments
path = r"C:\Users\benjamin.liang\Downloads\penang main tracker 2.xlsx"
df = pd.read_excel(path, sheet_name='Sheet1', header=1)
df.columns = [str(c) for c in df.columns]

# Get merchant assignments
ek_merchants = df[df['MGS'].notna()]['Mex ID'].dropna().unique().tolist()
xr_merchants = df[df['AMBD'] == 'NMA']['Mex ID'].dropna().unique().tolist()
cy_merchants = df[df['AM'].str.contains('chiayee', case=False, na=False)]['Mex ID'].dropna().unique().tolist()
darren_merchants = df[df['AM'].str.contains('darren', case=False, na=False)]['Mex ID'].dropna().unique().tolist()
suki_merchants = df[df['AM'].str.contains('suki', case=False, na=False)]['Mex ID'].dropna().unique().tolist()

print(f"EK merchants: {len(ek_merchants)}")
print(f"XR merchants: {len(xr_merchants)}")
print(f"CY merchants: {len(cy_merchants)}")
print(f"Darren merchants: {len(darren_merchants)}")
print(f"Suki merchants: {len(suki_merchants)}")

# Generate SQL query with merchant IDs
def generate_values_clause(merchant_ids, owner_name):
    if not merchant_ids:
        return ""
    values = ",\n        ".join([f"('{mid}', '{owner_name}')" for mid in merchant_ids[:1000]])  # Limit to avoid query size issues
    return values

# Create SQL query
sql_query = f"""
WITH team_assignments AS (
    SELECT merchant_id_nk, owner
    FROM (VALUES
        {generate_values_clause(ek_merchants, 'EK')},
        {generate_values_clause(xr_merchants, 'XR')},
        {generate_values_clause(cy_merchants, 'CY')},
        {generate_values_clause(darren_merchants, 'Darren')},
        {generate_values_clause(suki_merchants, 'Suki')}
    ) AS t(merchant_id_nk, owner)
),
monthly_team_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        ta.owner,
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
    INNER JOIN team_assignments ta ON f.merchant_id = ta.merchant_id_nk
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250101
        AND f.date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER), ta.owner
),
monthly_total_penang_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as total_penang_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250101
        AND f.date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    mtg.month_id,
    mtg.owner,
    mtg.team_gmv,
    mtp.total_penang_gmv,
    ROUND(mtg.team_gmv * 100.0 / NULLIF(mtp.total_penang_gmv, 0), 2) as gmv_pct_of_penang,
    ROUND(mtg.team_commission_billing * 100.0 / NULLIF(mtg.team_gmv, 0), 4) as commission_rate_pct
FROM monthly_team_gmv mtg
INNER JOIN monthly_total_penang_gmv mtp ON mtg.month_id = mtp.month_id
WHERE mtg.owner IN ('EK', 'XR', 'CY', 'Darren', 'Suki')
ORDER BY mtg.month_id, mtg.owner
"""

# Save query to file
with open('team_commission_query.sql', 'w', encoding='utf-8') as f:
    f.write(sql_query)

print("\nSQL query generated and saved to team_commission_query.sql")
print(f"Note: Query includes all {len(ek_merchants) + len(xr_merchants) + len(cy_merchants) + len(darren_merchants) + len(suki_merchants)} merchants")

