"""
Create CSV file from merchant query results
"""

import csv

# Headers
headers = [
    'merchant_id_nk',
    'merchant_name', 
    'area_name',
    'halal_status',
    'primary_cuisine_id',
    'segment',
    'custom_segment',
    'am_name',
    'last_order_date',
    'merchant_status'
]

# Sample data rows (first few from the query results)
# The full data would come from parsing the query output
sample_rows = [
    ['1-CZEJRAMXLU6JAT', 'Auntie Anne\'s - AEON Bukit Mertajam', 'Alma Jaya', 'Halal', '[519,79,81,24,62]', 'Enterprise', 'None', '', '2023-04-12', 'Churned'],
    ['1-C6EKDEMBNELUJA', 'D\'Laksa - Aeon Bukit Mertajam', 'Alma Jaya', 'Halal', '[24,79,104,126,2667]', 'Mid-Market', 'KVAM', 'emily.lee@grabtaxi.com', '2025-12-01', 'Active'],
    # ... more rows would be added here
]

def create_csv():
    """Create CSV file"""
    output_file = 'penang_mainland_merchants.csv'
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        # writer.writerows(sample_rows)  # Uncomment when you have full data
    
    print(f"CSV file structure created: {output_file}")
    print(f"Headers: {', '.join(headers)}")
    print("\nNote: This is a template. The full CSV will be created by parsing the complete query results.")

if __name__ == "__main__":
    create_csv()

