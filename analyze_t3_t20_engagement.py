"""
Analyze T3/T20 engagement metrics for last 6 months:
1. Campaigns/Ads Participation %
2. DoD (Deals of the Day) Participation %
3. Merchant tagging/engagement rate
"""

import json
from datetime import datetime, timedelta
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

def get_t20_t3_merchants(service):
    """Get T20 and T3 merchant IDs from Main Tracker V2"""
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Main Tracker V2!C4:J10000'
    ).execute()
    
    values = result.get('values', [])
    
    t20_merchants = []
    t3_merchants = []
    
    for row in values:
        if len(row) >= 8 and row[0]:  # Has merchant_id
            merchant_id = row[0].strip()
            segmentation = row[7] if len(row) > 7 else ''
            
            if segmentation:
                if 'T20' in segmentation:
                    t20_merchants.append(merchant_id)
                if 'T3' in segmentation:
                    t3_merchants.append(merchant_id)
    
    return list(set(t20_merchants)), list(set(t3_merchants))

def main():
    print("="*80)
    print("T3/T20 ENGAGEMENT ANALYSIS - LAST 6 MONTHS")
    print("="*80)
    print()
    
    service = authenticate()
    
    # Get merchant lists
    print("Getting T20 and T3 merchant lists from Main Tracker V2...")
    t20_merchants, t3_merchants = get_t20_t3_merchants(service)
    
    print(f"T20 merchants: {len(t20_merchants)}")
    print(f"T3 merchants: {len(t3_merchants)}")
    print()
    
    # Save merchant lists
    with open('t20_merchant_ids.json', 'w', encoding='utf-8') as f:
        json.dump(t20_merchants, f, indent=2)
    print("T20 merchant IDs saved to: t20_merchant_ids.json")
    
    with open('t3_merchant_ids.json', 'w', encoding='utf-8') as f:
        json.dump(t3_merchants, f, indent=2)
    print("T3 merchant IDs saved to: t3_merchant_ids.json")
    
    # Calculate date range (last 6 months)
    today = datetime(2025, 11, 7)  # Current date from Midas
    six_months_ago = today - timedelta(days=180)
    
    print(f"\nAnalysis Period: {six_months_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")
    print()
    print("="*80)
    print("QUERY SETUP")
    print("="*80)
    print("\n1. Campaigns/Ads Participation %")
    print("   - Need to query campaign participation data")
    print("   - Compare participation rate over 6 months")
    print()
    print("2. DoD Participation %")
    print("   - Use: analytics_food.pre_purchased_deals_base")
    print("   - Use: ocd_adw.f_food_prepurchased_deals")
    print("   - Filter by T3/T20 merchant IDs")
    print()
    print("3. Merchant Tagging/Engagement Rate")
    print("   - Check d_merchant.am_name, mgs fields")
    print("   - Calculate % of T3/T20 merchants with assigned AM/MGS")

if __name__ == '__main__':
    main()


