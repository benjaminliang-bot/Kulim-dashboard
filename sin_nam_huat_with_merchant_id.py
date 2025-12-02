import pandas as pd

# Commission data with merchant_id_nk
commission_data = {
    'merchant_id_nk': [
        '1-C2CZTRKGAKLCLT', '1-C2C2MBA2PE3JRE', '1-C2K3TYW3GNDJAN', 
        '1-C2CKA6JYAKKCJX', '1-C2EWE7WYRCKCGJ', '1-C2C2PFEJE76YVN',
        '1-C2L1WFWBGX6FT6', '1-C25VVJLGJU2UCA', '1-C7AUMF2ULXAJRJ',
        '1-C3VZLGBZLZJVNX', '1-C4KVVLDZNJMBWA'
    ],
    'merchant_name': [
        'Sin Nam Huat Roasted Chicken & Duck Rice - Island Glades [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Burma [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Persiaran Mahsuri [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Macalister [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Ayer Itam [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Fettes [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Solok Sungai Pinang [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Bagan Ajam [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Lintang Batu Maung 4 [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Kedai Kopi Golden Lake [Non-Halal]',
        '[INACTV: COCO] Sin Nam Huat Roasted Chicken & Duck Rice - Lintang Batu Maung 4 [Non-Halal]'
    ],
    'completed_orders': [20805, 8296, 9033, 7466, 7646, 7967, 7207, 5823, 3571, 2540, 530],
    'total_gmv': [793393.77, 305062.28, 300948.39, 281071.84, 279393.70, 263487.17, 262557.44, 199692.97, 140826.65, 82534.52, 18393.18],
    'total_commission_billing': [148724.10, 60058.40, 58936.90, 55573.68, 53650.27, 52086.00, 51172.86, 38457.82, 25825.73, 15913.54, 3447.92],
    'commission_rate_pct': [18.7453, 19.6873, 19.5837, 19.7721, 19.2024, 19.7679, 19.4902, 19.2585, 18.3387, 19.2811, 18.7456]
}

df = pd.DataFrame(commission_data)

# We'll get merchant_id from the query result
# For now, let me create the structure and we'll populate merchant_id

print("SIN NAM HUAT COMMISSION ANALYSIS WITH MERCHANT_ID")
print("="*80)
print("Waiting for merchant_id data from query...")

