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

# Create SQL query using IN clauses (more efficient)
def format_merchant_list(merchants):
    if not merchants:
        return "('')"  # Empty list
    # Format as ('id1', 'id2', ...)
    merchant_str = "', '".join(merchants)
    return f"('{merchant_str}')"

sql_query = f"""
WITH monthly_team_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        CASE 
            WHEN f.merchant_id IN {format_merchant_list(ek_merchants)} THEN 'EK'
            WHEN f.merchant_id IN {format_merchant_list(xr_merchants)} THEN 'XR'
            WHEN f.merchant_id IN {format_merchant_list(cy_merchants)} THEN 'CY'
            WHEN f.merchant_id IN {format_merchant_list(darren_merchants)} THEN 'Darren'
            WHEN f.merchant_id IN {format_merchant_list(suki_merchants)} THEN 'Suki'
            ELSE NULL
        END as owner,
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
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250101
        AND f.date_id < 20251101
        AND (
            f.merchant_id IN {format_merchant_list(ek_merchants)}
            OR f.merchant_id IN {format_merchant_list(xr_merchants)}
            OR f.merchant_id IN {format_merchant_list(cy_merchants)}
            OR f.merchant_id IN {format_merchant_list(darren_merchants)}
            OR f.merchant_id IN {format_merchant_list(suki_merchants)}
        )
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER), 
        CASE 
            WHEN f.merchant_id IN {format_merchant_list(ek_merchants)} THEN 'EK'
            WHEN f.merchant_id IN {format_merchant_list(xr_merchants)} THEN 'XR'
            WHEN f.merchant_id IN {format_merchant_list(cy_merchants)} THEN 'CY'
            WHEN f.merchant_id IN {format_merchant_list(darren_merchants)} THEN 'Darren'
            WHEN f.merchant_id IN {format_merchant_list(suki_merchants)} THEN 'Suki'
            ELSE NULL
        END
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
WHERE mtg.owner IS NOT NULL
ORDER BY mtg.month_id, mtg.owner
"""

# Save query
with open('team_commission_query_final.sql', 'w', encoding='utf-8') as f:
    f.write(sql_query)

print("\nSQL query generated with all merchants using IN clauses")
print("Saved to team_commission_query_final.sql")

