"""
Script to populate Kulim commercial metrics in the HTML dashboard
Queries data and updates the HTML file with actual values
"""

import json
import re
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def generate_metrics_query():
    """Generate SQL query for Kulim commercial metrics using area_id from d_area"""
    return """
    WITH kulim_areas AS (
        SELECT DISTINCT area_id
        FROM ocd_adw.d_area
        WHERE city_id = 13 
            AND area_name = 'Kulim'  -- Exact match to match dashboard numbers
    ),
    kulim_merchants AS (
        SELECT DISTINCT m.merchant_id_nk
        FROM ocd_adw.d_merchant m
        INNER JOIN ocd_adw.d_area a 
            ON m.city_id = a.city_id 
            AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
        INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
        WHERE m.city_id = 13 
            AND m.status = 'ACTIVE'
            AND m.geohash IS NOT NULL
    ),
    monthly_metrics AS (
        SELECT 
            CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
            COUNT(DISTINCT f.merchant_id) as active_merchants,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_passengers,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_gmv,
            AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value END) as avg_order_value
        FROM ocd_adw.f_food_metrics f
        WHERE f.city_id = 13
            AND f.country_id = 1
            AND f.business_type = 0
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kulim_merchants)
            AND CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) IN (202509, 202510, 202511)
        GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
    )
    SELECT 
        month_id,
        active_merchants,
        unique_passengers,
        completed_orders,
        total_gmv,
        avg_order_value
    FROM monthly_metrics
    ORDER BY month_id
    """

def update_html_with_metrics(html_file, metrics_data):
    """Update HTML file with commercial metrics data"""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create JavaScript data object
    js_data = {
        'september': {
            'gmv': metrics_data.get('202509', {}).get('total_gmv'),
            'orders': metrics_data.get('202509', {}).get('completed_orders'),
            'merchants': metrics_data.get('202509', {}).get('active_merchants'),
            'passengers': metrics_data.get('202509', {}).get('unique_passengers'),
            'aov': metrics_data.get('202509', {}).get('avg_order_value')
        },
        'october': {
            'gmv': metrics_data.get('202510', {}).get('total_gmv'),
            'orders': metrics_data.get('202510', {}).get('completed_orders'),
            'merchants': metrics_data.get('202510', {}).get('active_merchants'),
            'passengers': metrics_data.get('202510', {}).get('unique_passengers'),
            'aov': metrics_data.get('202510', {}).get('avg_order_value')
        },
        'november': {
            'gmv': metrics_data.get('202511', {}).get('total_gmv'),
            'orders': metrics_data.get('202511', {}).get('completed_orders'),
            'merchants': metrics_data.get('202511', {}).get('active_merchants'),
            'passengers': metrics_data.get('202511', {}).get('unique_passengers'),
            'aov': metrics_data.get('202511', {}).get('avg_order_value')
        }
    }
    
    # Find and replace the commercialMetrics initialization
    pattern = r'const commercialMetrics = \{[\s\S]*?\};'
    replacement = f'const commercialMetrics = {json.dumps(js_data, indent=12)};'
    
    html_content = re.sub(pattern, replacement, html_content)
    
    # Also add auto-update call if data exists
    if any(js_data['september'].values()) or any(js_data['october'].values()) or any(js_data['november'].values()):
        # Find the updateCommercialMetrics call and add updateMetricsData call before it
        if 'updateMetricsData(' not in html_content:
            update_call = f"""
        // Auto-populate with query results
        updateMetricsData({json.dumps(js_data, indent=8)});
        """
            html_content = html_content.replace(
                'window.addEventListener(\'DOMContentLoaded\', function() {',
                update_call + '\n        window.addEventListener(\'DOMContentLoaded\', function() {'
            )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML file updated with commercial metrics data!")

def main():
    print("="*80)
    print("KULIM COMMERCIAL METRICS POPULATOR")
    print("="*80)
    print()
    print("This script will:")
    print("1. Generate SQL query for Kulim commercial metrics")
    print("2. Execute query via MCP tools")
    print("3. Update HTML file with actual data")
    print()
    print("="*80)
    print("SQL QUERY:")
    print("="*80)
    print()
    print(generate_metrics_query())
    print()
    print("="*80)
    print("NEXT STEPS:")
    print("="*80)
    print()
    print("1. Execute the SQL query above via Hubble/Presto MCP")
    print("2. Parse the results into metrics_data dictionary")
    print("3. Call update_html_with_metrics('kulim_penang_comprehensive_analysis.html', metrics_data)")
    print()
    print("Example metrics_data format:")
    print(json.dumps({
        '202509': {
            'total_gmv': 50000.00,
            'completed_orders': 1200,
            'active_merchants': 25,
            'unique_passengers': 800,
            'avg_order_value': 41.67
        },
        '202510': {
            'total_gmv': 55000.00,
            'completed_orders': 1300,
            'active_merchants': 26,
            'unique_passengers': 850,
            'avg_order_value': 42.31
        },
        '202511': {
            'total_gmv': 30000.00,
            'completed_orders': 700,
            'active_merchants': 24,
            'unique_passengers': 500,
            'avg_order_value': 42.86
        }
    }, indent=2))

if __name__ == '__main__':
    main()

