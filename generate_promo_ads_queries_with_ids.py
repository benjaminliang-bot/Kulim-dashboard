"""
Generate Promotion and Ads Participation Queries with Actual T20/T3 Merchant IDs
"""

import json

# Load merchant IDs
with open('t20_merchant_ids.json', 'r') as f:
    t20_merchant_ids = json.load(f)

# Create merchant ID list for SQL IN clause
merchant_ids_sql = ",\n            ".join([f"'{mid}'" for mid in t20_merchant_ids])

# Read the base SQL template
with open('query_promo_ads_redefined_complete.sql', 'r', encoding='utf-8') as f:
    sql_template = f.read()

# Replace the placeholder with actual merchant IDs
sql_final = sql_template.replace(
    """        AND merchant_id_nk IN (
            -- Sample: Replace with full list from t20_merchant_ids.json
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )""",
    f"""        AND merchant_id_nk IN (
            {merchant_ids_sql}
        )"""
).replace(
    """        AND merchant_id_nk IN (
            SELECT merchant_id_nk FROM ocd_adw.d_merchant WHERE city_id = 13 LIMIT 1474
        )""",
    f"""        AND merchant_id_nk IN (
            {merchant_ids_sql}
        )"""
)

# Save the final SQL
with open('query_promo_ads_redefined_final.sql', 'w', encoding='utf-8') as f:
    f.write(sql_final)

print(f"[OK] Generated SQL with {len(t20_merchant_ids)} merchant IDs")
print(f"[INFO] File saved: query_promo_ads_redefined_final.sql")
print(f"[INFO] Ready to execute in Presto/Hubble")


