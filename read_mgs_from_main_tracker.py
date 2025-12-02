"""
Read MGS assignments from Main Tracker V2
Column C: Merchant ID (MEX ID)
Column F: MEX type category (AM/MGS/BD/KVAM)
Column I: Individual MGS name
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
from collections import defaultdict

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

def get_mgs_assignments(service, spreadsheet_id, sheet_name='Main Tracker V2'):
    """Get merchant IDs and their MGS assignments from Main Tracker V2"""
    try:
        # Read a wider range to get columns C, F, and I
        # Column C = index 2, Column F = index 5, Column I = index 8
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:Z"  # Read columns A-Z to get C, F, I
        ).execute()
        
        values = result.get('values', [])
        return values
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def extract_mgs_mapping(data):
    """Extract merchant ID to MGS mapping"""
    # Column indices (0-based):
    # Column C = index 2 (merchant ID)
    # Column F = index 5 (MEX type)
    # Column I = index 8 (MGS name)
    
    mgs_assignments = defaultdict(list)
    mgs_names = ['Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin']
    
    skipped_header = False
    
    for row in data:
        if not skipped_header:
            skipped_header = True
            continue  # Skip header row
        
        if len(row) < 9:
            continue
        
        merchant_id = row[2].strip() if len(row) > 2 and row[2] else ''
        mex_type = row[5].strip() if len(row) > 5 and row[5] else ''
        mgs_name = row[8].strip() if len(row) > 8 and row[8] else ''
        
        # Filter for MGS type and valid MGS names
        if mex_type.upper() == 'MGS' and merchant_id and mgs_name:
            # Normalize MGS name (handle variations)
            mgs_name_normalized = mgs_name.strip()
            if mgs_name_normalized in mgs_names:
                mgs_assignments[mgs_name_normalized].append(merchant_id)
    
    return mgs_assignments

def main():
    print("="*80)
    print("READING MGS ASSIGNMENTS FROM MAIN TRACKER V2")
    print("="*80)
    print()
    print("Column C: Merchant ID (MEX ID)")
    print("Column F: MEX type category (AM/MGS/BD/KVAM)")
    print("Column I: Individual MGS name")
    print()
    
    service = authenticate()
    if not service:
        return
    
    print("Reading data from 'Main Tracker V2' tab...")
    data = get_mgs_assignments(service, SPREADSHEET_ID)
    
    if not data:
        print("Failed to read data")
        return
    
    print(f"Read {len(data)} rows")
    print()
    
    # Extract MGS assignments
    mgs_assignments = extract_mgs_mapping(data)
    
    print("="*80)
    print("MGS ASSIGNMENTS FOUND")
    print("="*80)
    total_merchants = 0
    for mgs, merchants in sorted(mgs_assignments.items()):
        print(f"{mgs}: {len(merchants)} merchants")
        total_merchants += len(merchants)
    
    print(f"\nTotal MGS merchants: {total_merchants}")
    
    # Save to JSON
    with open('mgs_merchant_assignments.json', 'w', encoding='utf-8') as f:
        json.dump(dict(mgs_assignments), f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Saved MGS assignments to: mgs_merchant_assignments.json")
    print("\n[INFO] Ready to query impact metrics for each MGS")
    
    # Show sample merchant IDs for each MGS
    print("\nSample merchant IDs:")
    for mgs, merchants in sorted(mgs_assignments.items()):
        print(f"\n{mgs}:")
        print(f"  Sample IDs: {merchants[:5]}")

if __name__ == '__main__':
    main()
