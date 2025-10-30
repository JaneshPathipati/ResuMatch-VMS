"""
Google Sheets to SQLite Database Sync
Syncs volunteer data from Google Sheets to the database
Supports both manual and automatic syncing
"""

import gspread
from google.oauth2.service_account import Credentials
from database import Database
import time
from datetime import datetime

# Google Sheets API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

class GoogleSheetSync:
    def __init__(self, credentials_file='credentials.json'):
        """
        Initialize Google Sheets sync
        
        Args:
            credentials_file: Path to Google service account credentials JSON
        """
        self.credentials_file = credentials_file
        self.db = Database()
        self.client = None
    
    def connect(self):
        """Connect to Google Sheets API"""
        try:
            creds = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=SCOPES
            )
            self.client = gspread.authorize(creds)
            print("[SUCCESS] Connected to Google Sheets API")
            return True
        except FileNotFoundError:
            print(f"[ERROR] Credentials file not found: {self.credentials_file}")
            print("\nPlease follow the setup instructions in GOOGLE_SHEETS_SETUP.md")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            return False
    
    def sync_from_sheet(self, sheet_url_or_id, worksheet_name='Sheet1'):
        """
        Sync data from Google Sheet to database
        
        Args:
            sheet_url_or_id: Google Sheet URL or ID
            worksheet_name: Name of the worksheet (default: 'Sheet1')
        """
        if not self.client:
            if not self.connect():
                return False
        
        try:
            print(f"\n[INFO] Opening Google Sheet...")
            
            # Open the spreadsheet
            if sheet_url_or_id.startswith('http'):
                sheet = self.client.open_by_url(sheet_url_or_id)
            else:
                sheet = self.client.open_by_key(sheet_url_or_id)
            
            # Get the worksheet
            worksheet = sheet.worksheet(worksheet_name)
            
            # Get all records as list of dictionaries
            records = worksheet.get_all_records()
            
            print(f"[INFO] Found {len(records)} records in Google Sheet")
            
            # Sync to database
            inserted_count = 0
            updated_count = 0
            skipped_count = 0
            
            for record in records:
                volunteer_data = {
                    'name': str(record.get('Name', '')).strip(),
                    'email': str(record.get('Email', '')).strip(),
                    'phone': str(record.get('Phone', '')).strip(),
                    'skills': str(record.get('Skills', '')).strip(),
                    'experience': str(record.get('Experience', '')).strip(),
                    'education': str(record.get('Education', '')).strip(),
                    'availability': str(record.get('Availability', '')).strip(),
                    'languages': str(record.get('Languages', '')).strip(),
                    'certifications': str(record.get('Certifications', '')).strip(),
                    'interests': str(record.get('Interests', '')).strip()
                }
                
                # Validate required fields
                if not volunteer_data['name'] or not volunteer_data['email']:
                    skipped_count += 1
                    continue
                
                # Insert into database
                volunteer_id = self.db.insert_volunteer(volunteer_data)
                
                if volunteer_id:
                    inserted_count += 1
                    print(f"  [+] Added: {volunteer_data['name']}")
                else:
                    skipped_count += 1
                    print(f"  [=] Skipped: {volunteer_data['email']} (already exists)")
            
            print(f"\n[SUCCESS] Sync completed!")
            print(f"  - Inserted: {inserted_count} new volunteers")
            print(f"  - Skipped: {skipped_count} (duplicates or invalid)")
            print(f"  - Total in database: {len(self.db.get_all_volunteers())}")
            
            return True
            
        except gspread.exceptions.SpreadsheetNotFound:
            print("[ERROR] Spreadsheet not found. Check the URL/ID and sharing permissions.")
            return False
        except gspread.exceptions.WorksheetNotFound:
            print(f"[ERROR] Worksheet '{worksheet_name}' not found.")
            return False
        except Exception as e:
            print(f"[ERROR] Sync failed: {e}")
            return False
    
    def auto_sync(self, sheet_url_or_id, worksheet_name='Sheet1', interval_seconds=300):
        """
        Auto-sync from Google Sheet at regular intervals
        
        Args:
            sheet_url_or_id: Google Sheet URL or ID
            worksheet_name: Name of the worksheet
            interval_seconds: Sync interval in seconds (default: 300 = 5 minutes)
        """
        print(f"\n{'='*80}")
        print("AUTO-SYNC MODE")
        print(f"{'='*80}")
        print(f"Syncing every {interval_seconds} seconds ({interval_seconds/60:.1f} minutes)")
        print("Press Ctrl+C to stop\n")
        
        sync_count = 0
        
        try:
            while True:
                sync_count += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"\n[{timestamp}] Sync #{sync_count}")
                print("-" * 80)
                
                self.sync_from_sheet(sheet_url_or_id, worksheet_name)
                
                print(f"\nNext sync in {interval_seconds} seconds...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n\n[INFO] Auto-sync stopped. Total syncs: {sync_count}")

def main():
    """Interactive menu for Google Sheets sync"""
    print("\n" + "="*80)
    print(" GOOGLE SHEETS SYNC")
    print("="*80)
    
    syncer = GoogleSheetSync()
    
    print("\nOptions:")
    print("1. One-time sync from Google Sheet")
    print("2. Auto-sync (continuous)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        print("\nEnter your Google Sheet URL or ID:")
        sheet_id = input("Sheet URL/ID: ").strip()
        worksheet = input("Worksheet name (press Enter for 'Sheet1'): ").strip() or 'Sheet1'
        
        syncer.sync_from_sheet(sheet_id, worksheet)
    
    elif choice == '2':
        print("\nEnter your Google Sheet URL or ID:")
        sheet_id = input("Sheet URL/ID: ").strip()
        worksheet = input("Worksheet name (press Enter for 'Sheet1'): ").strip() or 'Sheet1'
        
        interval = input("Sync interval in seconds (press Enter for 300): ").strip()
        interval = int(interval) if interval else 300
        
        syncer.auto_sync(sheet_id, worksheet, interval)
    
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
