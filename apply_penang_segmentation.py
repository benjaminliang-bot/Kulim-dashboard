"""
Apply Penang MEX segmentation based on structure from Google Sheets
This script:
1. Reads the segmentation structure from penang_segmentation.json
2. Queries merchant data for Penang (city_id = 13)
3. Matches merchants and applies segmentation
4. Generates updated segmentation output
"""

import json
import csv
from typing import List, Dict, Any
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def load_segmentation_structure(json_file: str = 'penang_segmentation.json') -> List[Dict[str, Any]]:
    """Load segmentation structure from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data or len(data) < 2:
        return []
    
    # First row is header
    headers = [h.lower().strip() for h in data[0]]
    merchants = []
    
    for row in data[1:]:
        if not row or len(row) == 0:
            continue
        
        merchant = {}
        for i, header in enumerate(headers):
            if i < len(row):
                merchant[header] = row[i].strip() if row[i] else ''
            else:
                merchant[header] = ''
        merchants.append(merchant)
    
    return merchants

def analyze_segmentation_structure(merchants: List[Dict]) -> Dict[str, Any]:
    """Analyze the segmentation structure to understand the logic"""
    analysis = {
        'total_merchants': len(merchants),
        'island_mainland_distribution': {},
        'area_distribution': {},
        'ambd_distribution': {},
        'best_window_distribution': {},
        'mgs_distribution': {},
        'am_distribution': {}
    }
    
    for m in merchants:
        # Island/Mainland
        island_mainland = m.get('island/mainland', '').strip()
        if island_mainland:
            analysis['island_mainland_distribution'][island_mainland] = \
                analysis['island_mainland_distribution'].get(island_mainland, 0) + 1
        
        # Area Name
        area = m.get('area name', '').strip()
        if area:
            analysis['area_distribution'][area] = \
                analysis['area_distribution'].get(area, 0) + 1
        
        # AMBD (segmentation code)
        ambd = m.get('ambd', '').strip()
        if ambd:
            analysis['ambd_distribution'][ambd] = \
                analysis['ambd_distribution'].get(ambd, 0) + 1
        
        # Best Window
        window = m.get('best_window', '').strip()
        if window:
            analysis['best_window_distribution'][window] = \
                analysis['best_window_distribution'].get(window, 0) + 1
        
        # MGS
        mgs = m.get('mgs', '').strip()
        if mgs:
            analysis['mgs_distribution'][mgs] = \
                analysis['mgs_distribution'].get(mgs, 0) + 1
        
        # AM
        am = m.get('am', '').strip()
        if am:
            analysis['am_distribution'][am] = \
                analysis['am_distribution'].get(am, 0) + 1
    
    return analysis

def generate_segmentation_mapping(merchants: List[Dict]) -> Dict[str, Dict[str, Any]]:
    """
    Generate a mapping of merchant_id to segmentation attributes
    This will be used to update merchant segmentation
    """
    mapping = {}
    
    for m in merchants:
        merchant_id = m.get('merchant_id', '').strip()
        if not merchant_id:
            continue
        
        mapping[merchant_id] = {
            'merchant_id': merchant_id,
            'merchant_name': m.get('mex name', '').strip(),
            'best_window': m.get('best_window', '').strip(),
            'why': m.get('why', '').strip(),
            'island_mainland': m.get('island/mainland', '').strip(),
            'area_name': m.get('area name', '').strip(),
            'ambd': m.get('ambd', '').strip(),  # This appears to be the segmentation code
            'signature': m.get('signature', '').strip(),
            'mgs': m.get('mgs', '').strip(),
            'am': m.get('am', '').strip(),
            'top_20_percent': m.get('top 20%', '').strip(),
            'gmv_aug': m.get('gmv aug', '').strip(),
            'mom_growth': m.get('mom growth', '').strip()
        }
    
    return mapping

def generate_sql_query_for_penang_merchants(merchant_ids: List[str]) -> str:
    """
    Generate SQL query to get merchant data for Penang
    This will be executed via Hubble MCP
    """
    # Convert merchant IDs to SQL IN clause
    merchant_id_list = "', '".join(merchant_ids)
    
    query = f"""
    SELECT 
        merchant_id,
        merchant_id_nk,
        merchant_name,
        city_id,
        district,
        am_name,
        segment,
        custom_segment,
        address,
        latitude,
        longitude
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND merchant_id_nk IN ('{merchant_id_list}')
    ORDER BY merchant_name
    LIMIT 1000
    """
    
    return query

def generate_segmentation_summary(mapping: Dict[str, Dict], analysis: Dict) -> str:
    """Generate a summary of the segmentation structure"""
    summary = []
    summary.append("="*80)
    summary.append("PENANG MEX SEGMENTATION SUMMARY")
    summary.append("="*80)
    summary.append("")
    summary.append(f"Total Merchants in Segmentation: {analysis['total_merchants']}")
    summary.append("")
    
    summary.append("ISLAND/MAINLAND DISTRIBUTION:")
    for key, count in sorted(analysis['island_mainland_distribution'].items()):
        summary.append(f"  {key}: {count}")
    summary.append("")
    
    summary.append("AREA DISTRIBUTION:")
    for key, count in sorted(analysis['area_distribution'].items()):
        summary.append(f"  {key}: {count}")
    summary.append("")
    
    summary.append("AMBD (Segmentation Code) DISTRIBUTION:")
    for key, count in sorted(analysis['ambd_distribution'].items()):
        summary.append(f"  {key}: {count}")
    summary.append("")
    
    summary.append("BEST WINDOW DISTRIBUTION:")
    for key, count in sorted(analysis['best_window_distribution'].items()):
        summary.append(f"  {key}: {count}")
    summary.append("")
    
    summary.append("MGS DISTRIBUTION:")
    for key, count in sorted(analysis['mgs_distribution'].items()):
        summary.append(f"  {key}: {count}")
    summary.append("")
    
    summary.append("="*80)
    summary.append("SEGMENTATION LOGIC:")
    summary.append("="*80)
    summary.append("Based on the structure, segmentation appears to use:")
    summary.append("1. AMBD codes: MGS (Merchant Growth Specialist), NMA (New Merchant Acquisition?), MA (Merchant Acquisition?)")
    summary.append("2. Geographic: Island vs Mainland")
    summary.append("3. Area: Specific areas within Penang (Georgetown, Tanjung Bungah, etc.)")
    summary.append("4. Best Window: LUNCH vs DINNER")
    summary.append("5. Why criteria: NTU uplift, NTU/RM metrics, promo saturation, ops risks")
    summary.append("")
    
    return "\n".join(summary)

def save_segmentation_mapping(mapping: Dict[str, Dict], filename: str = 'penang_segmentation_mapping.json'):
    """Save the segmentation mapping to JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    print(f"Segmentation mapping saved to: {filename}")

def save_segmentation_csv(mapping: Dict[str, Dict], filename: str = 'penang_segmentation_applied.csv'):
    """Save the segmentation as CSV for easy review"""
    if not mapping:
        return
    
    # Get all keys from first merchant
    first_merchant = next(iter(mapping.values()))
    headers = list(first_merchant.keys())
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for merchant_data in mapping.values():
            writer.writerow(merchant_data)
    print(f"Segmentation CSV saved to: {filename}")

def main():
    print("="*80)
    print("APPLYING PENANG MEX SEGMENTATION")
    print("="*80)
    print()
    
    # Load segmentation structure
    print("Loading segmentation structure from penang_segmentation.json...")
    merchants = load_segmentation_structure()
    
    if not merchants:
        print("ERROR: No segmentation data found!")
        return
    
    print(f"Loaded {len(merchants)} merchants from segmentation structure")
    print()
    
    # Analyze structure
    print("Analyzing segmentation structure...")
    analysis = analyze_segmentation_structure(merchants)
    
    # Generate mapping
    print("Generating segmentation mapping...")
    mapping = generate_segmentation_mapping(merchants)
    
    # Generate summary
    summary = generate_segmentation_summary(mapping, analysis)
    print(summary)
    
    # Save outputs
    save_segmentation_mapping(mapping)
    save_segmentation_csv(mapping)
    
    # Generate SQL query for merchant lookup
    merchant_ids = list(mapping.keys())
    if merchant_ids:
        sql_query = generate_sql_query_for_penang_merchants(merchant_ids[:100])  # Limit to first 100 for query
        print("\n" + "="*80)
        print("SQL QUERY FOR MERCHANT LOOKUP (First 100 merchants):")
        print("="*80)
        print(sql_query)
        print("\nNote: This query can be executed via Hubble MCP to get current merchant data")
        print("and then matched with the segmentation mapping above.")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Review the segmentation mapping in penang_segmentation_mapping.json")
    print("2. Execute the SQL query via Hubble MCP to get current merchant data")
    print("3. Match merchants and update their segmentation based on the mapping")
    print("4. The AMBD field appears to be the key segmentation code (MGS, NMA, MA)")

if __name__ == '__main__':
    main()


