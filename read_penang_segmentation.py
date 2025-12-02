"""
Script to read Penang MEX segmentation structure from Google Sheets
Uses Google Sheets API to access the segmentation data

Requirements:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

Before running:
    1. Enable Google Sheets API in Google Cloud Console
    2. Use existing credentials.json (or create new OAuth 2.0 credentials)
    3. Place credentials.json in the same directory as this script
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle
import json
import sys
import io

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Google Sheets ID and GID from the URL
SPREADSHEET_ID = '1VV1vACl4NaIu76HMvP4kgi9szvLNJn8ByA8_vHgukPs'
SHEET_GID = '368359462'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate():
    """Authenticate and return service object"""
    creds = None
    token_file = 'token_sheets.pickle'  # Use separate token for Sheets to avoid conflicts
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Check if credentials are valid and have the right scopes
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found!")
                print("Please create OAuth 2.0 credentials in Google Cloud Console")
                print("and save as credentials.json")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    else:
        # Check if scopes are sufficient
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

def get_sheet_data(service, spreadsheet_id, sheet_gid):
    """Get all data from the specified sheet"""
    try:
        # First, get the sheet name from the GID
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_name = None
        for sheet in spreadsheet.get('sheets', []):
            if str(sheet['properties']['sheetId']) == sheet_gid:
                sheet_name = sheet['properties']['title']
                break
        
        if not sheet_name:
            print(f"ERROR: Could not find sheet with GID {sheet_gid}")
            return None
        
        print(f"Reading data from sheet: {sheet_name}")
        
        # Read all data from the sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:Z"  # Read columns A to Z
        ).execute()
        
        values = result.get('values', [])
        return values, sheet_name
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None, None

def display_segmentation_structure(values):
    """Display the segmentation structure in a readable format"""
    if not values:
        print("No data found")
        return
    
    print("\n" + "="*80)
    print("PENANG MEX SEGMENTATION STRUCTURE")
    print("="*80 + "\n")
    
    # Display as table - limit rows to avoid overwhelming output
    max_display_rows = 20
    for i, row in enumerate(values[:max_display_rows]):
        # Pad row to ensure consistent columns
        max_cols = max(len(r) for r in values) if values else 0
        padded_row = row + [''] * (max_cols - len(row))
        # Safely convert to string, handling Unicode
        try:
            row_str = ' | '.join(str(cell) for cell in padded_row[:10])
            print(f"Row {i+1}: {row_str}")  # Show first 10 columns
        except UnicodeEncodeError:
            # Fallback for problematic characters
            row_str = ' | '.join(str(cell).encode('ascii', errors='replace').decode('ascii') for cell in padded_row[:10])
            print(f"Row {i+1}: {row_str}")
    
    if len(values) > max_display_rows:
        print(f"\n... ({len(values) - max_display_rows} more rows not shown)")
    
    print("\n" + "="*80)
    print(f"Total rows: {len(values)}")
    print("="*80)

def save_to_json(values, filename='penang_segmentation.json'):
    """Save the data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(values, f, indent=2, ensure_ascii=False)
    print(f"\nData saved to {filename}")

def main():
    print("="*80)
    print("PENANG MEX SEGMENTATION READER")
    print("="*80)
    print(f"Spreadsheet ID: {SPREADSHEET_ID}")
    print(f"Sheet GID: {SHEET_GID}")
    print()
    
    service = authenticate()
    if not service:
        return
    
    values, sheet_name = get_sheet_data(service, SPREADSHEET_ID, SHEET_GID)
    
    if values:
        display_segmentation_structure(values)
        save_to_json(values)
        
        # Also save as CSV for easy viewing
        import csv
        with open('penang_segmentation.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(values)
        print(f"Data also saved to penang_segmentation.csv")
    else:
        print("Failed to retrieve data")

if __name__ == '__main__':
    main()

