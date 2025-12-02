"""
Read segmentation from Main Tracker V2 tab, column J
and check if it covers all Penang MEX merchants
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle
import sys
import io
import json
import csv

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SPREADSHEET_ID = '1VV1vACl4NaIu76HMvP4kgi9szvLNJn8ByA8_vHgukPs'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate():
    """Authenticate and return service object"""
    creds = None
    token_file = 'token_sheets.pickle'
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found!")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    else:
        if not creds.has_scopes(SCOPES):
            print("Token doesn't have Sheets API scope. Re-authenticating...")
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found!")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
    
    return build('sheets', 'v4', credentials=creds)

def get_main_tracker_data(service, spreadsheet_id, sheet_name='Main Tracker V2'):
    """Get merchant data from Main Tracker V2 tab"""
    try:
        # Read key columns: merchant_id (likely column A), merchant name, and column J (segmentation)
        # Let's read a wider range to identify columns
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:Z"  # Read first 26 columns
        ).execute()
        
        values = result.get('values', [])
        return values
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def analyze_segmentation_column_j(data):
    """Analyze column J segmentation values"""
    if not data or len(data) < 2:
        return {}
    
    # Column J is index 9 (0-based, so column 10)
    # First row is likely header
    header_row = data[0] if data else []
    print(f"Header row: {header_row[:15]}")
    
    # Find which column is merchant_id and which is column J
    merchant_id_col = None
    merchant_name_col = None
    segmentation_col = 9  # Column J (0-based index 9)
    
    for i, header in enumerate(header_row[:15]):
        header_lower = str(header).lower()
        if 'merchant' in header_lower and 'id' in header_lower:
            merchant_id_col = i
        if 'merchant' in header_lower and 'name' in header_lower:
            merchant_name_col = i
    
    print(f"Merchant ID column: {merchant_id_col}")
    print(f"Merchant Name column: {merchant_name_col}")
    print(f"Segmentation column (J): {segmentation_col}")
    print()
    
    # Extract segmentation data
    segmentation_data = []
    t3_count = 0
    t20_count = 0
    segmentation_dist = {}
    
    for i, row in enumerate(data[1:], start=2):  # Skip header
        if len(row) <= segmentation_col:
            continue
        
        merchant_id = row[merchant_id_col] if merchant_id_col and merchant_id_col < len(row) else ''
        merchant_name = row[merchant_name_col] if merchant_name_col and merchant_name_col < len(row) else ''
        segmentation = row[segmentation_col] if segmentation_col < len(row) else ''
        
        if segmentation and segmentation.strip():
            seg_value = segmentation.strip()
            segmentation_data.append({
                'row': i,
                'merchant_id': merchant_id,
                'merchant_name': merchant_name,
                'segmentation': seg_value
            })
            
            # Count T3 and T20
            if 'T3' in seg_value:
                t3_count += 1
            if 'T20' in seg_value:
                t20_count += 1
            
            # Distribution
            segmentation_dist[seg_value] = segmentation_dist.get(seg_value, 0) + 1
    
    return {
        'data': segmentation_data,
        't3_count': t3_count,
        't20_count': t20_count,
        'distribution': segmentation_dist,
        'total': len(segmentation_data)
    }

def main():
    print("="*80)
    print("READING MAIN TRACKER V2 SEGMENTATION (COLUMN J)")
    print("="*80)
    print()
    
    service = authenticate()
    if not service:
        return
    
    # Get data from Main Tracker V2
    print("Reading data from 'Main Tracker V2' tab...")
    data = get_main_tracker_data(service, SPREADSHEET_ID)
    
    if not data:
        print("Failed to read data")
        return
    
    print(f"Read {len(data)} rows")
    print()
    
    # Analyze segmentation
    analysis = analyze_segmentation_column_j(data)
    
    print("="*80)
    print("SEGMENTATION ANALYSIS (COLUMN J)")
    print("="*80)
    print(f"Total merchants with segmentation: {analysis['total']}")
    print(f"T3 merchants: {analysis['t3_count']}")
    print(f"T20 merchants: {analysis['t20_count']}")
    print()
    print("Segmentation Distribution:")
    for seg, count in sorted(analysis['distribution'].items(), key=lambda x: -x[1]):
        print(f"  {seg}: {count}")
    print()
    
    # Save to file
    with open('main_tracker_segmentation.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print("Segmentation data saved to: main_tracker_segmentation.json")
    
    # Save CSV
    if analysis['data']:
        with open('main_tracker_segmentation.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['row', 'merchant_id', 'merchant_name', 'segmentation'])
            writer.writeheader()
            writer.writerows(analysis['data'])
        print("Segmentation CSV saved to: main_tracker_segmentation.csv")

if __name__ == '__main__':
    main()


