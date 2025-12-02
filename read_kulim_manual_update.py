"""
Read Kulim manual update from Google Doc
Document ID: 1rFzTaqGZcZFM3BFIGH2v1G7fMHmt7OYiarNKr15ISWk
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

DOCUMENT_ID = '1rFzTaqGZcZFM3BFIGH2v1G7fMHmt7OYiarNKr15ISWk'
# Use combined scopes to allow both Sheets and Docs access
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/documents.readonly'
]

def authenticate():
    """Authenticate and return service object - try using existing token first"""
    creds = None
    # Try existing sheets token first
    token_file = 'token_sheets.pickle'
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Check if we need to add Docs scope
    if creds and creds.valid:
        # Check if token has Docs scope
        required_scope = 'https://www.googleapis.com/auth/documents.readonly'
        if not creds.has_scopes([required_scope]):
            print("Token doesn't have Docs API scope. Re-authenticating with combined scopes...")
            # Delete old token to force re-auth
            if os.path.exists(token_file):
                os.remove(token_file)
            creds = None  # Force re-auth with new scopes
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                creds = None
        
        if not creds:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found!")
                print("Please create OAuth 2.0 credentials in Google Cloud Console")
                print("and save as credentials.json")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save with combined scopes
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('docs', 'v1', credentials=creds)

def get_document_content(service, document_id):
    """Get content from Google Doc"""
    try:
        doc = service.documents().get(documentId=document_id).execute()
        
        # Extract text content
        content = []
        if 'body' in doc and 'content' in doc['body']:
            for element in doc['body']['content']:
                if 'paragraph' in element:
                    para_text = ''
                    if 'elements' in element['paragraph']:
                        for elem in element['paragraph']['elements']:
                            if 'textRun' in elem:
                                para_text += elem['textRun'].get('content', '')
                    if para_text.strip():
                        content.append(para_text)
                elif 'table' in element:
                    # Handle tables
                    table_rows = []
                    if 'tableRows' in element['table']:
                        for row in element['table']['tableRows']:
                            row_cells = []
                            if 'tableCells' in row:
                                for cell in row['tableCells']:
                                    cell_text = ''
                                    if 'content' in cell:
                                        for cell_elem in cell['content']:
                                            if 'paragraph' in cell_elem:
                                                if 'elements' in cell_elem['paragraph']:
                                                    for text_elem in cell_elem['paragraph']['elements']:
                                                        if 'textRun' in text_elem:
                                                            cell_text += text_elem['textRun'].get('content', '')
                                    row_cells.append(cell_text.strip())
                            table_rows.append(row_cells)
                        content.append('\n[TABLE START]')
                        for row in table_rows:
                            content.append(' | '.join(row))
                        content.append('[TABLE END]\n')
        
        return '\n'.join(content)
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def main():
    print("="*80)
    print("READING KULIM MANUAL UPDATE FROM GOOGLE DOC")
    print("="*80)
    print()
    
    # Authenticate
    print("Authenticating...")
    service = authenticate()
    if not service:
        print("Authentication failed!")
        return
    
    print("Successfully authenticated!")
    print()
    
    # Get document content
    print(f"Reading document: {DOCUMENT_ID}")
    content = get_document_content(service, DOCUMENT_ID)
    
    if content:
        print("="*80)
        print("DOCUMENT CONTENT:")
        print("="*80)
        print(content)
        print()
        
        # Save to file
        output_file = 'kulim_manual_update_content.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content saved to: {output_file}")
    else:
        print("Failed to retrieve document content")

if __name__ == '__main__':
    main()

