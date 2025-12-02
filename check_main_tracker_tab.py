"""
Check the "Main Tracker v2" tab in the Google Sheets to see column J
and verify if segmentation is mapped to all Penang MEX merchants
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

def list_all_sheets(service, spreadsheet_id):
    """List all sheets in the spreadsheet"""
    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = []
        for sheet in spreadsheet.get('sheets', []):
            sheet_info = {
                'title': sheet['properties']['title'],
                'sheetId': sheet['properties']['sheetId'],
                'gid': sheet['properties']['sheetId']
            }
            sheets.append(sheet_info)
        return sheets
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def get_column_j_from_tab(service, spreadsheet_id, sheet_name):
    """Get column J from the specified tab"""
    try:
        # Read column J (index 10, 1-based)
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!J:J"  # Column J
        ).execute()
        
        values = result.get('values', [])
        return values
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def main():
    print("="*80)
    print("CHECKING MAIN TRACKER V2 TAB")
    print("="*80)
    print()
    
    service = authenticate()
    if not service:
        return
    
    # List all sheets
    print("Listing all sheets in the spreadsheet...")
    sheets = list_all_sheets(service, SPREADSHEET_ID)
    
    print(f"\nFound {len(sheets)} sheets:")
    for sheet in sheets:
        print(f"  - {sheet['title']} (GID: {sheet['gid']})")
    
    # Find "Main Tracker v2" tab
    main_tracker = None
    for sheet in sheets:
        if 'Main Tracker v2' in sheet['title'] or 'main tracker v2' in sheet['title'].lower():
            main_tracker = sheet
            break
    
    if not main_tracker:
        print("\nERROR: 'Main Tracker v2' tab not found!")
        print("Available tabs:")
        for sheet in sheets:
            print(f"  - {sheet['title']}")
        return
    
    print(f"\nFound 'Main Tracker v2' tab: {main_tracker['title']} (GID: {main_tracker['gid']})")
    
    # Get column J
    print(f"\nReading column J from '{main_tracker['title']}'...")
    column_j = get_column_j_from_tab(service, SPREADSHEET_ID, main_tracker['title'])
    
    if column_j:
        print(f"\nColumn J has {len(column_j)} rows")
        print("\nFirst 20 rows of Column J:")
        for i, cell in enumerate(column_j[:20]):
            print(f"  Row {i+1}: {cell[0] if cell else '(empty)'}")
        
        # Check for non-empty values
        non_empty = [cell[0] for cell in column_j if cell and cell[0].strip()]
        print(f"\nNon-empty values in Column J: {len(non_empty)}")
        print(f"Unique values: {len(set(non_empty))}")
        if non_empty:
            print(f"Sample values: {set(non_empty[:10])}")
    else:
        print("Failed to read column J")

if __name__ == '__main__':
    main()


