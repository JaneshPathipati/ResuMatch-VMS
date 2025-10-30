"""
Custom Google Sheets Sync for Geeta Sevi IT Interest Areas
Maps the specific columns from your Google Sheet to the volunteer database
"""

import gspread
from google.oauth2.service_account import Credentials
from database import Database
import time
from datetime import datetime

# Google Sheets Configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/16_SnaTYS0O5qvTBesXB5jEe3V0hk6nN2D8mvNWEBTDE/edit?usp=sharing"
WORKSHEET_NAME = "Form responses 1"  # or "Form Responses 2" depending on which one you want

# Google Sheets API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

class GeetaSheetSync:
    def __init__(self, credentials_file='credentials.json'):
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
            print(f"[ERROR] Credentials file '{self.credentials_file}' not found")
            print("\n=== SETUP REQUIRED ===")
            print("Please follow these steps:")
            print("1. Go to: https://console.cloud.google.com/")
            print("2. Create a project and enable Google Sheets API")
            print("3. Create a service account and download credentials.json")
            print("4. Share your Google Sheet with the service account email")
            print("\nSee GOOGLE_SHEETS_SETUP.md for detailed instructions")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            return False
    
    def map_expertise_to_skills(self, record):
        """Map expertise columns to skills string"""
        skills = []
        
        # Map all the expertise areas
        expertise_fields = {
            'PHP + MySQL': 'Experience in Expertise Area where you can contribute [PHP + MySQL]',
            'Wordpress': 'Experience in Expertise Area where you can contribute [Wordpress Management]',
            'Wordpress Coding': 'Experience in Expertise Area where you can contribute [Wordpress Coding]',
            'Graphic Design': 'Experience in Expertise Area where you can contribute [Graphic Design for Websites]',
            'Testing and QA': 'Experience in Expertise Area where you can contribute [Testing and QA]',
            'React Native': 'Experience in Expertise Area where you can contribute [React Native Developer for Android/iOS]',
            'Google Script': 'Experience in Expertise Area where you can contribute [Google Script]',
            'Process Management': 'Experience in Expertise Area where you can contribute [Process Manager / Implementation]',
            'ISO Documentation': 'Experience in Expertise Area where you can contribute [ISO and Process Documentation]',
            'HR in IT': 'Experience in Expertise Area where you can contribute [HR in IT]',
            'AI Programming': 'Experience in Expertise Area where you can contribute [AI Programming]',
            'Digital Marketing': 'Experience in Expertise Area where you can contribute [Digital Marketing Expert]'
        }
        
        for skill_name, column_name in expertise_fields.items():
            experience = str(record.get(column_name, '')).strip()
            if experience and experience not in ['None', 'No', '']:
                if 'month' in experience or 'year' in experience:
                    skills.append(f"{skill_name} ({experience})")
                else:
                    skills.append(skill_name)
        
        return ', '.join(skills) if skills else 'Not specified'
    
    def sync_from_sheet(self):
        """Sync data from the Geeta Sevi Google Sheet"""
        if not self.client:
            if not self.connect():
                return False
        
        try:
            print(f"\n{'='*80}")
            print("SYNCING GEETA SEVI IT INTEREST AREAS SHEET")
            print(f"{'='*80}\n")
            print(f"[INFO] Opening Google Sheet...")
            
            # Open the spreadsheet
            sheet = self.client.open_by_url(SHEET_URL)
            
            # Get the worksheet
            worksheet = sheet.worksheet(WORKSHEET_NAME)
            
            # Get all records
            records = worksheet.get_all_records()
            
            print(f"[INFO] Found {len(records)} records in Google Sheet")
            print(f"[INFO] Processing and syncing to database...\n")
            
            # Sync to database
            inserted_count = 0
            skipped_count = 0
            
            for i, record in enumerate(records, 1):
                # Extract and map fields
                name = str(record.get('Name', '')).strip()
                email = str(record.get('Email address', '')).strip()
                phone = str(record.get('Mobile Number', '')).strip()
                
                # Skip if no name or email
                if not name or not email:
                    skipped_count += 1
                    continue
                
                # Map expertise areas to skills
                skills = self.map_expertise_to_skills(record)
                
                # Get additional information
                linkedin = str(record.get('Linkedln Profile (if available)', '')).strip()
                association = str(record.get('Since when are you associated with Learngeeta in any capacity.', '')).strip()
                contribution_area = str(record.get('What area you would like to contribute in Geeta Parivar IT activities', '')).strip()
                
                # Get timestamp from sheet
                timestamp = str(record.get('Timestamp', '')).strip()
                
                # Create volunteer data (with expanded schema, empty values for unavailable fields)
                volunteer_data = {
                    # Core fields
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'skills': skills,
                    'experience': contribution_area[:500] if contribution_area else 'Not specified',
                    'education': 'Not specified',
                    'availability': association if association else 'Not specified',
                    'languages': 'Not specified',
                    'certifications': linkedin if linkedin else 'Not specified',
                    'interests': 'IT volunteer work, Geeta Parivar activities',
                    # Expanded fields (blank for Geeta Sevi sheet)
                    'timestamp': timestamp,
                    'linkedin_url': linkedin,
                    'join_date': association,
                    # All other expanded fields left blank (not in Geeta Sevi sheet)
                }
                
                # Insert into database
                volunteer_id = self.db.insert_volunteer(volunteer_data)
                
                if volunteer_id:
                    inserted_count += 1
                    print(f"  [{inserted_count}] Added: {name} ({email})")
                    print(f"      Skills: {skills[:80]}...")
                else:
                    skipped_count += 1
                    print(f"  [=] Skipped: {email} (already exists)")
            
            print(f"\n{'='*80}")
            print("[SUCCESS] Sync completed!")
            print(f"{'='*80}")
            print(f"  - New volunteers added: {inserted_count}")
            print(f"  - Skipped (duplicates): {skipped_count}")
            print(f"  - Total in database: {len(self.db.get_all_volunteers())}")
            print(f"{'='*80}\n")
            
            return True
            
        except gspread.exceptions.SpreadsheetNotFound:
            print("[ERROR] Spreadsheet not found.")
            print("Make sure you've shared the sheet with your service account email!")
            return False
        except gspread.exceptions.WorksheetNotFound:
            print(f"[ERROR] Worksheet '{WORKSHEET_NAME}' not found.")
            print("Available worksheets in the sheet:")
            try:
                worksheets = sheet.worksheets()
                for ws in worksheets:
                    print(f"  - {ws.title}")
            except:
                pass
            return False
        except Exception as e:
            print(f"[ERROR] Sync failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def auto_sync(self, interval_seconds=300):
        """Auto-sync at regular intervals"""
        print(f"\n{'='*80}")
        print("AUTO-SYNC MODE - Geeta Sevi Sheet")
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
                
                self.sync_from_sheet()
                
                print(f"\nNext sync in {interval_seconds} seconds...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n\n[INFO] Auto-sync stopped. Total syncs: {sync_count}")

def main():
    """Main function"""
    print("\n" + "="*80)
    print(" GEETA SEVI GOOGLE SHEETS SYNC")
    print("="*80)
    print(f"\nSheet URL: {SHEET_URL}")
    print(f"Worksheet: {WORKSHEET_NAME}")
    print("\nOptions:")
    print("1. One-time sync")
    print("2. Auto-sync (continuous - every 5 minutes)")
    print("3. Custom interval auto-sync")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    syncer = GeetaSheetSync()
    
    if choice == '1':
        syncer.sync_from_sheet()
    
    elif choice == '2':
        syncer.auto_sync(interval_seconds=300)  # 5 minutes
    
    elif choice == '3':
        interval = input("Enter sync interval in seconds (e.g., 60, 300, 600): ").strip()
        try:
            interval = int(interval)
            syncer.auto_sync(interval_seconds=interval)
        except ValueError:
            print("Invalid interval. Using default 300 seconds.")
            syncer.auto_sync(interval_seconds=300)
    
    elif choice == '4':
        print("Goodbye!")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()

