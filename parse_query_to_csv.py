"""
Parse merchant query results and create CSV file
"""

import csv
import re

# Query result text (from the MCP tool output)
query_result = """| merchant_id_nk | merchant_name | area_name | halal_status | cuisine_names | segment | custom_segment | am_name | last_order_date | merchant_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1-CZEJRAMXLU6JAT | Auntie Anne's - AEON Bukit Mertajam | Alma Jaya | Halal | Beverages, Fast Food, Halal, Healthy, In-Store Prices | Enterprise | None |  | 2023-04-12 | Churned |
| 1-C6EKDEMBNELUJA | D'Laksa - Aeon Bukit Mertajam | Alma Jaya | Halal | Beverages, Halal, Malaysian, Noodles, Selera Popular | Mid-Market | KVAM | emily.lee@grabtaxi.com | 2025-12-01 | Active |
| 1-CYTYGGABLBBGGX | Domino's Pizza - Bukit Mertajam | Alma Jaya | Halal | Fast Food, Halal, Pizza, Selera Popular | Enterprise | BD | wanqing.ng@grabtaxi.com | 2025-12-01 | Active |
| 1-C2AEAXE3VTB3R6 | KFC - AEON Bukit Mertajam | Alma Jaya | Halal | Burgers, Chicken, Fast Food, Fried Chicken, Halal | Enterprise | BD | wenxhing.choo@grabtaxi.com | 2025-12-01 | Active |
| 1-C2AEAXJAACNCC6 | KFC - Alma Bukit Mertajam | Alma Jaya | Halal | Burgers, Chicken, Fast Food, Fried Chicken, Halal | Enterprise | BD | wenxhing.choo@grabtaxi.com | 2025-12-01 | Active |
| 1-C65JJTMFJXXHCA | Kenangan Coffee - AEON Bukit Mertajam | Alma Jaya | Halal | Cafe, Coffee & Tea, Halal, Iced Dessert, Pastries | Enterprise | BD | bernadette.hon@grabtaxi.com | 2025-12-01 | Active |
| 1-CYTDG3NWTXNUT6 | Nando's - AEON Bukit Mertajam | Alma Jaya | Halal | Chicken, Halal, Healthy, Lunch, Western | Enterprise | BD | wanqing.ng@grabtaxi.com | 2025-12-01 | Active |
| 1-C2AALPTYC3JXVN | Pizza Hut - Alma Bkt Mertajam | Alma Jaya | Halal | Chicken, Fast Food, Halal, Pasta, Pizza | Enterprise | BD | bernadette.hon@grabtaxi.com | 2025-12-01 | Active |
| 1-CY4BJ7WWAF5VCJ | Starbucks - AEON Bukit Mertajam | Alma Jaya | Halal | Cakes & Bakeries, Coffee & Tea, Dessert, Halal, Pastries | Enterprise | BD | wanqing.ng@grabtaxi.com | 2025-12-01 | Active |
| 1-CZAHT3KXVVNDC2 | The Chicken Rice Shop - AEON Bukit Mertajam | Alma Jaya | Halal | Chicken, Chicken Rice, Halal, Malaysian, Selera Popular | Enterprise | BD | cheryl.chow@grabtaxi.com | 2025-12-01 | Active |"""

def parse_table_to_csv(query_output_text, output_filename='penang_mainland_merchants.csv'):
    """
    Parse the table-formatted query output and create CSV file
    """
    lines = query_output_text.strip().split('\n')
    
    # Find header row
    header_line_idx = None
    for i, line in enumerate(lines):
        if 'merchant_id_nk' in line and 'merchant_name' in line:
            header_line_idx = i
            break
    
    if header_line_idx is None:
        raise ValueError("Could not find header row in query output")
    
    # Parse headers
    header_line = lines[header_line_idx]
    headers = [h.strip() for h in header_line.split('|')[1:-1]]
    
    # Parse data rows (skip header and separator line)
    data_start = header_line_idx + 2
    data_rows = []
    
    for line in lines[data_start:]:
        if line.strip() and not line.startswith('|---') and '*Execution time' not in line:
            if line.startswith('|'):
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if len(cols) == len(headers):
                    data_rows.append(cols)
    
    # Write to CSV
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data_rows)
    
    print(f"✅ Successfully created {output_filename} with {len(data_rows)} merchants")
    return len(data_rows)

if __name__ == "__main__":
    # Read the full query result from a file or paste it here
    # For now, we'll need to get the full output
    print("This script needs the full query output to parse")
    print("Please provide the complete query result text")

