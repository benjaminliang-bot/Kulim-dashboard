"""
Update Kulim Dashboard Script
Automates the process of:
1. Querying latest Kulim commercial metrics
2. Updating the HTML dashboard
3. Committing and pushing to GitHub
"""

import json
import os
import re
import sys
import io
import subprocess
from datetime import datetime

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
    print(f"Reading HTML file: {html_file}")
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
    
    # Format the replacement with proper indentation
    replacement = 'const commercialMetrics = ' + json.dumps(js_data, indent=12)
    replacement = replacement.replace('"', '')  # Remove quotes from keys
    replacement = replacement.replace("'", '"')  # Replace single quotes with double
    replacement = replacement.replace('True', 'true').replace('False', 'false').replace('None', 'null')
    replacement += ';'
    
    html_content = re.sub(pattern, replacement, html_content)
    
    # Update all date fields with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_date_formatted = datetime.now().strftime('%B %d, %Y')
    
    # Update Query Date in data source section
    date_pattern = r'<strong>Query Date:</strong> \d{4}-\d{2}-\d{2}'
    html_content = re.sub(date_pattern, f'<strong>Query Date:</strong> {current_date}', html_content)
    
    # Update Report Date
    report_date_pattern = r'<strong>Report Date:</strong> [A-Za-z]+ \d{1,2}, \d{4}'
    html_content = re.sub(report_date_pattern, f'<strong>Report Date:</strong> {current_date_formatted}', html_content)
    
    # Update JavaScript comment date
    js_comment_pattern = r'// Query executed: \d{4}-\d{2}-\d{2}'
    html_content = re.sub(js_comment_pattern, f'// Query executed: {current_date}', html_content)
    
    # Update Report Period end date (if it exists)
    report_period_pattern = r'<strong>Report Period:</strong> [^<]+ - ([A-Za-z]+ \d{1,2}, \d{4})'
    match = re.search(report_period_pattern, html_content)
    if match:
        # Update the end date in Report Period
        html_content = re.sub(
            r'(<strong>Report Period:</strong> [^<]+ - )([A-Za-z]+ \d{1,2}, \d{4})',
            f'\\1{current_date_formatted}',
            html_content
        )
    
    print(f"Writing updated HTML file: {html_file}")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ HTML file updated with commercial metrics data!")
    return js_data

def git_commit_and_push(commit_message):
    """Commit and push changes to GitHub"""
    try:
        print("\n" + "="*80)
        print("COMMITTING AND PUSHING TO GITHUB")
        print("="*80)
        
        # Add files
        print("\n1. Adding files to git...")
        subprocess.run(['git', 'add', 'kulim_penang_comprehensive_analysis.html', 'index.html'], 
                      check=True, capture_output=True, text=True)
        
        # Copy to index.html
        print("2. Copying to index.html for GitHub Pages...")
        if sys.platform == 'win32':
            subprocess.run(['copy', 'kulim_penang_comprehensive_analysis.html', 'index.html'], 
                          shell=True, check=True)
        else:
            subprocess.run(['cp', 'kulim_penang_comprehensive_analysis.html', 'index.html'], 
                          check=True)
        
        subprocess.run(['git', 'add', 'index.html'], check=True, capture_output=True, text=True)
        
        # Commit
        print(f"3. Committing changes: {commit_message}")
        subprocess.run(['git', 'commit', '-m', commit_message], 
                      check=True, capture_output=True, text=True)
        
        # Push
        print("4. Pushing to GitHub...")
        subprocess.run(['git', 'push'], check=True, capture_output=True, text=True)
        
        print("\n✓ Successfully pushed to GitHub!")
        print("   Repository: https://github.com/benjaminliang-bot/Kulim-dashboard")
        print("   GitHub Pages: https://benjaminliang-bot.github.io/Kulim-dashboard/")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error during git operations: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False
    
    return True

def main():
    print("="*80)
    print("KULIM DASHBOARD UPDATE SCRIPT")
    print("="*80)
    print()
    print("This script will:")
    print("1. Generate SQL query for latest Kulim commercial metrics")
    print("2. Display the query (execute manually via MCP tools)")
    print("3. Update HTML file with the results")
    print("4. Commit and push to GitHub")
    print()
    print("="*80)
    print("SQL QUERY TO EXECUTE:")
    print("="*80)
    print()
    
    query = generate_metrics_query()
    print(query)
    print()
    print("="*80)
    print("INSTRUCTIONS:")
    print("="*80)
    print()
    print("1. Copy the SQL query above")
    print("2. Execute it via Hubble/Presto MCP tools")
    print("3. Parse the results into the format below")
    print("4. Run this script again with the data, or update manually")
    print()
    print("="*80)
    print("EXPECTED DATA FORMAT:")
    print("="*80)
    print()
    
    example_data = {
        '202509': {
            'total_gmv': 499340.10,
            'completed_orders': 15915,
            'active_merchants': 139,
            'unique_passengers': 8207,
            'avg_order_value': 31.38
        },
        '202510': {
            'total_gmv': 568189.00,
            'completed_orders': 17968,
            'active_merchants': 143,
            'unique_passengers': 8983,
            'avg_order_value': 31.62
        },
        '202511': {
            'total_gmv': 168853.68,
            'completed_orders': 5423,
            'active_merchants': 132,
            'unique_passengers': 3873,
            'avg_order_value': 31.14
        }
    }
    
    print(json.dumps(example_data, indent=2))
    print()
    print("="*80)
    print("AUTOMATIC UPDATE (if data provided):")
    print("="*80)
    print()
    
    # Check if data is provided as command line argument or file
    if len(sys.argv) > 1:
        try:
            # Check if argument is a file path
            if sys.argv[1].endswith('.json') or os.path.exists(sys.argv[1]):
                # Read from file
                with open(sys.argv[1], 'r', encoding='utf-8') as f:
                    metrics_data = json.load(f)
            else:
                # Try to parse JSON data from command line
                data_json = sys.argv[1]
                metrics_data = json.loads(data_json)
            
            print("Updating HTML with provided data...")
            js_data = update_html_with_metrics('kulim_penang_comprehensive_analysis.html', metrics_data)
            
            # Ask if user wants to commit and push
            print("\n" + "="*80)
            response = input("Commit and push to GitHub? (y/n): ").strip().lower()
            
            if response == 'y' or response == 'yes':
                commit_message = f"Update Kulim dashboard metrics - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                git_commit_and_push(commit_message)
            else:
                print("\n✓ HTML updated. Changes not committed.")
                print("   Run 'git add' and 'git commit' manually when ready.")
        except json.JSONDecodeError:
            print("✗ Invalid JSON data provided")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print("No data provided. Run with JSON data as argument:")
        print("  python update_kulim.py '{\"202510\": {\"total_gmv\": 568189.00, ...}}'")
        print()
        print("Or update the HTML file manually using the query results above.")

if __name__ == '__main__':
    main()


