"""
1. Verify if Main Tracker V2 covers all Penang MEX merchants
2. Query T3 performance for last month vs same month last year
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import sys
import io
import json
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SPREADSHEET_ID = '1VV1vACl4NaIu76HMvP4kgi9szvLNJn8ByA8_vHgukPs'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate():
    creds = None
    token_file = 'token_sheets.pickle'
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)

def get_penang_merchants_from_tracker(service):
    """Get all Penang merchants from Main Tracker V2"""
    # Read merchant IDs and segmentation
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Main Tracker V2!C4:J10000'  # Column C (Mex ID) to J (Top 20%)
    ).execute()
    
    values = result.get('values', [])
    
    # Structure: [merchant_id, island/mainland, area, ambd, signature, mgs, am, top_20%]
    merchants = []
    for row in values:
        if len(row) >= 8 and row[0]:  # Has merchant_id
            merchants.append({
                'merchant_id': row[0].strip(),
                'island_mainland': row[1] if len(row) > 1 else '',
                'area': row[2] if len(row) > 2 else '',
                'ambd': row[3] if len(row) > 3 else '',
                'segmentation': row[7] if len(row) > 7 else ''  # Column J
            })
    
    return merchants

def count_t3_merchants(merchants):
    """Count T3 merchants"""
    t3_merchants = [m for m in merchants if m['segmentation'] and 'T3' in m['segmentation']]
    return t3_merchants, len(t3_merchants)

def main():
    print("="*80)
    print("VERIFYING PENANG COVERAGE & T3 ANALYSIS")
    print("="*80)
    print()
    
    service = authenticate()
    
    # Get merchants from Main Tracker V2
    print("Reading merchants from Main Tracker V2...")
    merchants = get_penang_merchants_from_tracker(service)
    print(f"Found {len(merchants)} merchants in Main Tracker V2")
    
    # Count T3
    t3_merchants, t3_count = count_t3_merchants(merchants)
    print(f"T3 merchants: {t3_count}")
    print()
    
    # Get T3 merchant IDs for query
    t3_merchant_ids = [m['merchant_id'] for m in t3_merchants]
    print(f"Sample T3 merchant IDs (first 10): {t3_merchant_ids[:10]}")
    print()
    
    # Save T3 merchant list
    with open('t3_merchant_ids.json', 'w', encoding='utf-8') as f:
        json.dump(t3_merchant_ids, f, indent=2)
    print("T3 merchant IDs saved to: t3_merchant_ids.json")
    
    print("\n" + "="*80)
    print("ANSWER TO YOUR QUESTIONS:")
    print("="*80)
    print("1. Main Tracker V2 has segmentation in Column J for merchants")
    print(f"   - Total merchants with segmentation: {len([m for m in merchants if m['segmentation']])}")
    print(f"   - T3 merchants: {t3_count}")
    print("   - Need to verify if ALL Penang MEX are included (checking against d_merchant...)")
    print()
    print("2. T3 Performance Query:")
    print("   - Last month: October 2025")
    print("   - Same month last year: October 2024")
    print("   - Will query via Midas/Hubble for T3 merchant performance")

if __name__ == '__main__':
    main()


