"""
Find merchant_id and merchant_name columns in Main Tracker V2
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import sys
import io

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

def main():
    service = authenticate()
    # Read first few rows to understand structure
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Main Tracker V2!A1:Z10'
    ).execute()
    
    values = result.get('values', [])
    print("First 10 rows:")
    for i, row in enumerate(values[:10]):
        print(f"Row {i+1}: {row}")

if __name__ == '__main__':
    main()


