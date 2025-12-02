"""
Read MGS assignments from Main Tracker V2 Google Sheet
Match merchant IDs with MGS names to query impact
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
        # Read columns: merchant_id, merchant_name, and MGS column
        # Need to identify which column has MGS assignments
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:Z"  # Read first 26 columns
        ).execute()
        
        values = result.get('values', [])
        return values
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def find_mgs_column(data):
    """Find which column contains MGS assignments"""
    if not data or len(data) < 2:
        return None
    
    header_row = data[0]
    print("Header row:", header_row[:15])
    
    # Look for MGS column
    mgs_col = None
    merchant_id_col = None
    
    for i, header in enumerate(header_row[:20]):
        header_str = str(header).lower()
        if 'mgs' in header_str or 'merchant growth' in header_str:
            mgs_col = i
        if 'merchant' in header_str and 'id' in header_str:
            merchant_id_col = i
    
    return merchant_id_col, mgs_col

def extract_mgs_assignments(data, merchant_id_col, mgs_col):
    """Extract merchant ID to MGS mapping"""
    mgs_assignments = {}
    mgs_names = ['Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin']
    
    for row in data[1:]:  # Skip header
        if len(row) <= max(merchant_id_col or 0, mgs_col or 0):
            continue
        
        merchant_id = row[merchant_id_col] if merchant_id_col and merchant_id_col < len(row) else ''
        mgs_name = row[mgs_col] if mgs_col and mgs_col < len(row) else ''
        
        if merchant_id and mgs_name and mgs_name.strip() in mgs_names:
            if mgs_name.strip() not in mgs_assignments:
                mgs_assignments[mgs_name.strip()] = []
            mgs_assignments[mgs_name.strip()].append(merchant_id.strip())
    
    return mgs_assignments

def main():
    print("="*80)
    print("READING MGS ASSIGNMENTS FROM MAIN TRACKER V2")
    print("="*80)
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
    
    # Find MGS column
    merchant_id_col, mgs_col = find_mgs_column(data)
    print(f"Merchant ID column: {merchant_id_col}")
    print(f"MGS column: {mgs_col}")
    print()
    
    if mgs_col is None:
        print("ERROR: Could not find MGS column in sheet")
        print("Please check the sheet structure")
        return
    
    # Extract assignments
    mgs_assignments = extract_mgs_assignments(data, merchant_id_col, mgs_col)
    
    print("="*80)
    print("MGS ASSIGNMENTS FOUND")
    print("="*80)
    for mgs, merchants in mgs_assignments.items():
        print(f"{mgs}: {len(merchants)} merchants")
    
    # Save to JSON
    with open('mgs_merchant_assignments.json', 'w', encoding='utf-8') as f:
        json.dump(mgs_assignments, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Saved MGS assignments to: mgs_merchant_assignments.json")
    print("\n[INFO] Ready to query impact metrics for each MGS")

if __name__ == '__main__':
    main()


