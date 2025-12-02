"""
Final script to update MEX segmentation for Penang merchants
This matches merchant data from database with segmentation structure from Google Sheets
and generates the updated segmentation output
"""

import json
import csv
from typing import List, Dict, Any
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def load_segmentation_mapping(json_file: str = 'penang_segmentation_mapping.json') -> Dict[str, Dict]:
    """Load segmentation mapping from JSON"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_merchant_query_results(query_results: str) -> List[Dict]:
    """Parse the merchant query results from Hubble"""
    # This is a simplified parser - in practice, you'd parse the actual query results
    # For now, we'll load from a saved file if available
    merchants = []
    
    # Try to load from a saved merchant data file
    try:
        with open('penang_merchants_from_db.json', 'r', encoding='utf-8') as f:
            merchants = json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, we'll create it from the query results
        pass
    
    return merchants

def match_merchants_with_segmentation(
    merchants: List[Dict], 
    segmentation: Dict[str, Dict]
) -> List[Dict]:
    """Match merchants from database with segmentation mapping"""
    matched = []
    unmatched_segmentation = []
    unmatched_merchants = []
    
    # Create lookup by merchant_id_nk
    seg_lookup = {seg['merchant_id']: seg for seg in segmentation.values()}
    merchant_lookup = {m.get('merchant_id_nk'): m for m in merchants if m.get('merchant_id_nk')}
    
    # Match merchants
    for merchant_id_nk, seg_data in seg_lookup.items():
        merchant = merchant_lookup.get(merchant_id_nk)
        if merchant:
            matched.append({
                'merchant_id': merchant.get('merchant_id'),
                'merchant_id_nk': merchant_id_nk,
                'merchant_name': merchant.get('merchant_name'),
                'current_segment': merchant.get('segment', ''),
                'current_custom_segment': merchant.get('custom_segment', ''),
                'current_am_name': merchant.get('am_name', ''),
                'district': merchant.get('district', ''),
                # New segmentation data
                'new_ambd': seg_data.get('ambd', ''),  # MGS, NMA, MA
                'new_island_mainland': seg_data.get('island_mainland', ''),
                'new_area_name': seg_data.get('area_name', ''),
                'new_best_window': seg_data.get('best_window', ''),
                'new_mgs': seg_data.get('mgs', ''),
                'new_am': seg_data.get('am', ''),
                'why': seg_data.get('why', ''),
                'gmv_aug': seg_data.get('gmv_aug', ''),
                'mom_growth': seg_data.get('mom_growth', ''),
                'top_20_percent': seg_data.get('top_20_percent', '')
            })
        else:
            unmatched_segmentation.append(seg_data)
    
    # Find merchants in DB but not in segmentation
    for merchant_id_nk, merchant in merchant_lookup.items():
        if merchant_id_nk not in seg_lookup:
            unmatched_merchants.append(merchant)
    
    return matched, unmatched_segmentation, unmatched_merchants

def generate_segmentation_update_summary(matched: List[Dict]) -> Dict[str, Any]:
    """Generate summary statistics of the segmentation update"""
    summary = {
        'total_matched': len(matched),
        'ambd_distribution': {},
        'island_mainland_distribution': {},
        'area_distribution': {},
        'best_window_distribution': {},
        'mgs_distribution': {},
        'segment_changes': {
            'current_long_tail': 0,
            'current_mid_market': 0,
            'new_mgs': 0,
            'new_nma': 0,
            'new_ma': 0
        }
    }
    
    for m in matched:
        # AMBD distribution
        ambd = m.get('new_ambd', '')
        if ambd:
            summary['ambd_distribution'][ambd] = summary['ambd_distribution'].get(ambd, 0) + 1
        
        # Island/Mainland
        island_mainland = m.get('new_island_mainland', '')
        if island_mainland:
            summary['island_mainland_distribution'][island_mainland] = \
                summary['island_mainland_distribution'].get(island_mainland, 0) + 1
        
        # Area
        area = m.get('new_area_name', '')
        if area:
            summary['area_distribution'][area] = summary['area_distribution'].get(area, 0) + 1
        
        # Best Window
        window = m.get('new_best_window', '')
        if window:
            summary['best_window_distribution'][window] = \
                summary['best_window_distribution'].get(window, 0) + 1
        
        # MGS
        mgs = m.get('new_mgs', '')
        if mgs:
            summary['mgs_distribution'][mgs] = summary['mgs_distribution'].get(mgs, 0) + 1
        
        # Current segment
        current_seg = m.get('current_segment', '')
        if 'Long-Tail' in current_seg:
            summary['segment_changes']['current_long_tail'] += 1
        elif 'Mid-Market' in current_seg:
            summary['segment_changes']['current_mid_market'] += 1
        
        # New AMBD
        if ambd == 'MGS':
            summary['segment_changes']['new_mgs'] += 1
        elif ambd == 'NMA':
            summary['segment_changes']['new_nma'] += 1
        elif ambd == 'MA':
            summary['segment_changes']['new_ma'] += 1
    
    return summary

def save_updated_segmentation(matched: List[Dict], filename: str = 'penang_mex_segmentation_updated.csv'):
    """Save the updated segmentation to CSV"""
    if not matched:
        return
    
    headers = [
        'merchant_id', 'merchant_id_nk', 'merchant_name',
        'current_segment', 'current_custom_segment', 'current_am_name',
        'new_ambd', 'new_island_mainland', 'new_area_name', 'new_best_window',
        'new_mgs', 'new_am', 'why', 'gmv_aug', 'mom_growth', 'top_20_percent',
        'district'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for m in matched:
            writer.writerow(m)
    
    print(f"Updated segmentation saved to: {filename}")

def generate_update_recommendations(matched: List[Dict]) -> str:
    """Generate recommendations for updating merchant segmentation"""
    recommendations = []
    recommendations.append("="*80)
    recommendations.append("SEGMENTATION UPDATE RECOMMENDATIONS")
    recommendations.append("="*80)
    recommendations.append("")
    recommendations.append("Based on the Penang structure from Google Sheets:")
    recommendations.append("")
    recommendations.append("1. AMBD CODES (Primary Segmentation):")
    recommendations.append("   - MGS: Merchant Growth Specialist (high-value, growth focus)")
    recommendations.append("   - NMA: New Merchant Acquisition (newer merchants)")
    recommendations.append("   - MA: Merchant Acquisition (acquisition focus)")
    recommendations.append("")
    recommendations.append("2. GEOGRAPHIC SEGMENTATION:")
    recommendations.append("   - Island vs Mainland classification")
    recommendations.append("   - Area Name (Georgetown, Tanjung Bungah, etc.)")
    recommendations.append("")
    recommendations.append("3. TEMPORAL SEGMENTATION:")
    recommendations.append("   - Best Window: LUNCH vs DINNER")
    recommendations.append("")
    recommendations.append("4. ASSIGNMENT:")
    recommendations.append("   - MGS: Merchant Growth Specialist name")
    recommendations.append("   - AM: Account Manager name/email")
    recommendations.append("")
    recommendations.append("="*80)
    recommendations.append("IMPLEMENTATION NOTES:")
    recommendations.append("="*80)
    recommendations.append("")
    recommendations.append("The AMBD code should be used to update:")
    recommendations.append("- custom_segment field in d_merchant table")
    recommendations.append("- Or create a new segmentation field if needed")
    recommendations.append("")
    recommendations.append("Geographic and temporal data can be stored in:")
    recommendations.append("- Additional custom fields")
    recommendations.append("- Or in a separate merchant attributes table")
    recommendations.append("")
    
    return "\n".join(recommendations)

def main():
    print("="*80)
    print("UPDATING MEX SEGMENTATION FOR PENANG")
    print("="*80)
    print()
    
    # Load segmentation mapping
    print("Loading segmentation mapping...")
    segmentation = load_segmentation_mapping()
    print(f"Loaded segmentation for {len(segmentation)} merchants")
    print()
    
    # Load merchant data from query results
    # For now, we'll use the merchant data we queried earlier
    # In a real scenario, you'd parse the actual query results
    print("Loading merchant data from database...")
    
    # Create merchant data from the query results we got
    merchant_data = [
        {"merchant_id": 2530120, "merchant_id_nk": "1-C2NYA2VZA7K3PA", "merchant_name": "Ali Nasi Kandar Bukit Mertajam - Jalan Pasar", "city_id": 13, "district": "Bukit Mertajam", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 2105321, "merchant_id_nk": "1-C2AKJFAYT7MVTA", "merchant_name": "Aman Tomyam - Tanjong Tokong", "city_id": 13, "district": "Tanjung Bungah", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3712395, "merchant_id_nk": "1-C33HCVLUMEN1AA", "merchant_name": "Angboh Char Koay Teow - Lebuh Cintra [Non-Halal]", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3042150, "merchant_id_nk": "1-C3AYJ2TFE7DDG2", "merchant_name": "Apom Balik 46 - TPS Jalan Utama", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3598778, "merchant_id_nk": "1-C3WHN3JWALJTNN", "merchant_name": "Bob Kitchen - Taman Bestari", "city_id": 13, "district": "Kulim", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 4239457, "merchant_id_nk": "1-C6AGEN4BLZBTJJ", "merchant_name": "Char Koay Teow Fried Rice - JJ Garden Food Court [Non-Halal]", "city_id": 13, "district": "Tanjung Bungah", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 5131517, "merchant_id_nk": "1-C7AHCNAFVXDZCN", "merchant_name": "FamilyMart - Caltex Batu Kawan", "city_id": 13, "district": "Bandar Cassia", "am_name": "olivia.chong@grabtaxi.com", "segment": "Mid-Market", "custom_segment": "KVAM"},
        {"merchant_id": 2232778, "merchant_id_nk": "1-C2C2MBA2NKW3C6", "merchant_name": "Hameed Pata Mee - Jalan Padang Kota Lama", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 2634515, "merchant_id_nk": "1-C2VFFEMTG8N1BE", "merchant_name": "Harshini Veelas - Biker Pitstop Kopitiam", "city_id": 13, "district": "Bayan Lepas", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3386064, "merchant_id_nk": "1-C3MTVCL1PEAWSA", "merchant_name": "Jojo Fruits - Astaka Tanjung Selera", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 4845506, "merchant_id_nk": "1-C6XULJ5KR3MAGE", "merchant_name": "Kedai Makan Pak Aq - Bukit Mertajam", "city_id": 13, "district": "Bukit Mertajam", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 2591047, "merchant_id_nk": "1-C2UHGA3HLYXJTA", "merchant_name": "Kim Kee Char Hor Fun/Fried Rice - Fisherman's Wharf Food Court  [Non-Halal]", "city_id": 13, "district": "Jelutong", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3421971, "merchant_id_nk": "1-C3NHDE4FTU5BGA", "merchant_name": "Maryam Restaurant - Jalan Batu Ferringhi", "city_id": 13, "district": "Tanjung Bungah", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3626424, "merchant_id_nk": "1-C3XAT7WHCKMYVE", "merchant_name": "Penang Famous Duck Egg Char Koay Teow - Red Garden Food Paradise", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 4154435, "merchant_id_nk": "1-C4L2ATTKVKVJEE", "merchant_name": "Penang Famous Nasi Lemak 峰昧古早味椰浆饭 - Red Garden Food Paradise", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 2249729, "merchant_id_nk": "1-C2DENTVFDF5TCJ", "merchant_name": "Penang Road Famous Chao Kuey Teow - Joo Hooi Cafe [Non-Halal]", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 1819118, "merchant_id_nk": "1-CZDKGPT2V25BLJ", "merchant_name": "Penang Road Famous Laksa - Lebuh Keng Kwee", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3539960, "merchant_id_nk": "1-C3U3WADTGECARN", "merchant_name": "Putri Tomyam Station - Jalan Batu Ferringhi", "city_id": 13, "district": "Tanjung Bungah", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 2258723, "merchant_id_nk": "1-C2DJTANDUFT1LE", "merchant_name": "Restoran Nasi Kandar Rafei Ali - Jalan Fettes", "city_id": 13, "district": "Tanjung Bungah", "am_name": "darren.ng@grabtaxi.com", "segment": "Mid-Market", "custom_segment": "OC"},
        {"merchant_id": 3881867, "merchant_id_nk": "1-C4AXJ2L2J7ABNA", "merchant_name": "Roti Bakar Hutton Lane - Komtarwalk", "city_id": 13, "district": "George Town", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 2824109, "merchant_id_nk": "1-C22ZV4ACUF6XLA", "merchant_name": "Sis's Grill - Astaka Bandar Perda", "city_id": 13, "district": "Prai", "am_name": "", "segment": "Long-Tail", "custom_segment": "None"},
        {"merchant_id": 3438146, "merchant_id_nk": "1-C3NXV6NCGLDHBE", "merchant_name": "Uncle Kin Chili Pan Mee - Sunway Carnival", "city_id": 13, "district": "Prai", "am_name": "suki.teoh@grabtaxi.com", "segment": "Long-Tail", "custom_segment": "OC"}
    ]
    
    print(f"Loaded {len(merchant_data)} merchants from database")
    print()
    
    # Match merchants with segmentation
    print("Matching merchants with segmentation...")
    matched, unmatched_seg, unmatched_merchants = match_merchants_with_segmentation(
        merchant_data, segmentation
    )
    
    print(f"Matched: {len(matched)} merchants")
    print(f"Unmatched in segmentation: {len(unmatched_seg)}")
    print(f"Unmatched in database: {len(unmatched_merchants)}")
    print()
    
    # Generate summary
    summary = generate_segmentation_update_summary(matched)
    
    print("="*80)
    print("SEGMENTATION UPDATE SUMMARY")
    print("="*80)
    print(f"Total Matched Merchants: {summary['total_matched']}")
    print()
    print("AMBD Distribution (New Segmentation):")
    for ambd, count in sorted(summary['ambd_distribution'].items()):
        print(f"  {ambd}: {count}")
    print()
    print("Island/Mainland Distribution:")
    for loc, count in sorted(summary['island_mainland_distribution'].items()):
        print(f"  {loc}: {count}")
    print()
    print("Area Distribution:")
    for area, count in sorted(summary['area_distribution'].items()):
        print(f"  {area}: {count}")
    print()
    print("Best Window Distribution:")
    for window, count in sorted(summary['best_window_distribution'].items()):
        print(f"  {window}: {count}")
    print()
    print("MGS Distribution:")
    for mgs, count in sorted(summary['mgs_distribution'].items()):
        print(f"  {mgs}: {count}")
    print()
    
    # Save outputs
    save_updated_segmentation(matched)
    
    # Save full data to JSON
    with open('penang_mex_segmentation_updated.json', 'w', encoding='utf-8') as f:
        json.dump(matched, f, indent=2, ensure_ascii=False)
    print("Updated segmentation saved to: penang_mex_segmentation_updated.json")
    
    # Generate recommendations
    recommendations = generate_update_recommendations(matched)
    print()
    print(recommendations)
    
    # Save recommendations
    with open('penang_segmentation_recommendations.txt', 'w', encoding='utf-8') as f:
        f.write(recommendations)
    print("Recommendations saved to: penang_segmentation_recommendations.txt")

if __name__ == '__main__':
    main()


