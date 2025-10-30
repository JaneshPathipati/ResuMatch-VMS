"""
Sync Script for VMS Volunteers Google Sheet
Maps columns from the "Copy of Volunteers data for VMS" sheet to the database
"""

import gspread
from google.oauth2.service_account import Credentials
from database import Database
import time
from datetime import datetime

# Google Sheets Configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1qSqLPy5Q6mLA6Q1nUTKtlKx1kLAagFsrPCZ5x8vKjW8/edit?usp=sharing"
WORKSHEET_NAME = "Copy of Form Responses 1"  # Adjust if needed

# Google Sheets API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

class VMSVolunteerSync:
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
            print("\nPlease ensure credentials.json exists in the project directory")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            return False
    
    
    def sync_from_sheet(self):
        """Sync data from the VMS Volunteers Google Sheet"""
        if not self.client:
            if not self.connect():
                return False
        
        try:
            print(f"\n{'='*80}")
            print("SYNCING VMS VOLUNTEERS SHEET")
            print(f"{'='*80}\n")
            print(f"[INFO] Opening Google Sheet...")
            
            # Open the spreadsheet
            sheet = self.client.open_by_url(SHEET_URL)
            
            # Get the first worksheet (adjust if needed)
            try:
                worksheet = sheet.worksheet(WORKSHEET_NAME)
            except:
                # If worksheet name doesn't match, get the first sheet
                worksheet = sheet.get_worksheet(0)
                print(f"[INFO] Using worksheet: {worksheet.title}")
            
            # Get all data (handling duplicate column names)
            all_values = worksheet.get_all_values()
            
            if len(all_values) < 2:
                print("[ERROR] Sheet is empty or has no data rows")
                return False
            
            # Get headers from first row
            headers = all_values[0]
            data_rows = all_values[1:]  # Skip header row
            
            print(f"[INFO] Found {len(data_rows)} records in Google Sheet")
            print(f"[INFO] Processing and syncing to database...\n")
            
            # Create a mapping of column names to indices
            def find_column_index(header_name):
                """Find the first occurrence of a column header"""
                try:
                    return headers.index(header_name)
                except ValueError:
                    return -1
            
            # Map column indices - ALL columns
            idx_timestamp = find_column_index('Timestamp')
            idx_email = find_column_index('Email Address')
            idx_prefix = find_column_index('Prefix')
            idx_full_name = find_column_index('Full Name')
            idx_phone = find_column_index('WhatsApp Number')
            idx_alternate_phone = find_column_index('Alternate Contact No.')
            idx_dob = find_column_index('Date of Birth')
            idx_anniversary = find_column_index('Wedding Anniversary Date')
            idx_gender = find_column_index('Gender')
            idx_country_other = find_column_index('Select Country (Other than Bharat)')
            idx_state = find_column_index('State')
            idx_city = find_column_index('Current City')
            idx_address = 12  # "Address" column (first occurrence at index 12)
            idx_pin_code = find_column_index('PIN Code')
            idx_zip_code = find_column_index('ZIP code')
            idx_education = find_column_index('Highest Educational Qualification')
            idx_education_field = find_column_index('Highest Educational Qualification – Field/Stream')
            idx_job_sector = find_column_index('Current Job Sector')
            idx_profession = find_column_index('Profession')
            idx_job_position = find_column_index('Current Job Position / Role')
            idx_experience = find_column_index('Years of Experience in Current Position')
            idx_linkedin = find_column_index('LinkedIn Profile URL')
            idx_facebook = find_column_index('Facebook Profile URL')
            idx_instagram = find_column_index('Instagram Profile URL')
            idx_prev_exp = find_column_index('Previous Work / Volunteer Experience')
            idx_primary_skills = find_column_index('Primary Skill Set')
            idx_secondary_skills = find_column_index('Secondary Skill Sets')
            idx_languages = find_column_index('Languages Spoken (Fluently)')
            idx_volunteer_mode = find_column_index('Preferred Volunteering Mode')
            idx_availability_days = find_column_index('Availability (Days)')
            idx_time_availability = find_column_index('Time Availability (Indian Standard Time IST)')
            idx_commitment = find_column_index('Minimum Commitment Duration')
            idx_join_date = find_column_index('When did you join Learngeeta?')
            idx_hear_about = find_column_index('How did you hear about LearnGeeta?')
            idx_examination = find_column_index('Have you successfully passed any LearnGeeta examination?')
            idx_departments = find_column_index('In how many departments you have served so far?')
            idx_journey = find_column_index('Few Words on Journey in Learngeeta so far')
            idx_country = find_column_index('Country')
            
            # Sync to database
            inserted_count = 0
            skipped_count = 0
            
            for i, row in enumerate(data_rows, 1):
                # Helper function to safely extract cell value
                def get_val(idx):
                    return row[idx].strip() if idx >= 0 and idx < len(row) else ''
                
                # Extract ALL fields
                timestamp = get_val(idx_timestamp)
                email = get_val(idx_email)
                prefix = get_val(idx_prefix)
                full_name = get_val(idx_full_name)
                phone = get_val(idx_phone)
                alternate_phone = get_val(idx_alternate_phone)
                date_of_birth = get_val(idx_dob)
                anniversary_date = get_val(idx_anniversary)
                gender = get_val(idx_gender)
                country_other = get_val(idx_country_other)
                state = get_val(idx_state)
                city = get_val(idx_city)
                address = get_val(idx_address)
                pin_code = get_val(idx_pin_code)
                zip_code = get_val(idx_zip_code)
                education = get_val(idx_education)
                education_field = get_val(idx_education_field)
                job_sector = get_val(idx_job_sector)
                profession = get_val(idx_profession)
                job_position = get_val(idx_job_position)
                years_experience = get_val(idx_experience)
                linkedin_url = get_val(idx_linkedin)
                facebook_url = get_val(idx_facebook)
                instagram_url = get_val(idx_instagram)
                previous_experience = get_val(idx_prev_exp)
                primary_skills = get_val(idx_primary_skills)
                secondary_skills = get_val(idx_secondary_skills)
                languages_spoken = get_val(idx_languages)
                volunteering_mode = get_val(idx_volunteer_mode)
                availability_days = get_val(idx_availability_days)
                time_availability = get_val(idx_time_availability)
                commitment_duration = get_val(idx_commitment)
                join_date = get_val(idx_join_date)
                hear_about_source = get_val(idx_hear_about)
                passed_examination = get_val(idx_examination)
                departments_served = get_val(idx_departments)
                journey_description = get_val(idx_journey)
                country = get_val(idx_country)
                
                # Skip if no name
                if not full_name:
                    skipped_count += 1
                    continue
                
                # Generate synthetic email if missing
                if not email:
                    # Create email from name + row number
                    name_part = full_name.lower().replace(' ', '.').replace(',', '')
                    # Remove special characters
                    name_part = ''.join(c for c in name_part if c.isalnum() or c == '.')
                    email = f"{name_part}.{i}@vms.volunteer.temp"
                
                # Combine skills from multiple sources
                skills_list = []
                if profession:
                    skills_list.append(profession)
                if job_position:
                    skills_list.append(job_position)
                if job_sector:
                    skills_list.append(job_sector)
                skills = ', '.join(skills_list) if skills_list else 'Not specified'
                
                # Format education
                if education_field:
                    education_full = f"{education} - {education_field}" if education else education_field
                else:
                    education_full = education if education else 'Not specified'
                
                # Format experience
                experience_full = years_experience if years_experience else 'Not specified'
                
                # Availability
                availability_full = f"{availability_days} | {time_availability}" if availability_days or time_availability else 'Not specified'
                
                # Determine country
                country_final = country if country else (country_other if country_other else 'India')
                
                # Create volunteer data with ALL fields
                volunteer_data = {
                    'name': full_name,
                    'email': email,
                    'phone': phone,
                    'skills': skills,
                    'experience': experience_full,
                    'education': education_full,
                    'availability': availability_full,
                    'languages': languages_spoken if languages_spoken else 'Not specified',
                    'certifications': linkedin_url if linkedin_url else 'Not specified',
                    'interests': profession if profession else 'Volunteer work',
                    # Expanded fields
                    'timestamp': timestamp,
                    'prefix': prefix,
                    'alternate_phone': alternate_phone,
                    'date_of_birth': date_of_birth,
                    'anniversary_date': anniversary_date,
                    'gender': gender,
                    'country': country_final,
                    'state': state,
                    'city': city,
                    'address': address,
                    'pin_code': pin_code,
                    'zip_code': zip_code,
                    'education_field': education_field,
                    'job_sector': job_sector,
                    'profession': profession,
                    'job_position': job_position,
                    'years_experience': years_experience,
                    'linkedin_url': linkedin_url,
                    'facebook_url': facebook_url,
                    'instagram_url': instagram_url,
                    'previous_experience': previous_experience[:500] if previous_experience and len(previous_experience) > 500 else previous_experience,
                    'primary_skills': primary_skills,
                    'secondary_skills': secondary_skills,
                    'volunteering_mode': volunteering_mode,
                    'availability_days': availability_days,
                    'time_availability': time_availability,
                    'commitment_duration': commitment_duration,
                    'join_date': join_date,
                    'hear_about_source': hear_about_source,
                    'passed_examination': passed_examination,
                    'departments_served': departments_served,
                    'journey_description': journey_description[:1000] if journey_description and len(journey_description) > 1000 else journey_description,
                }
                
                # Insert into database
                volunteer_id = self.db.insert_volunteer(volunteer_data)
                
                if volunteer_id:
                    inserted_count += 1
                    print(f"  [{inserted_count}] Added: {full_name} ({email})")
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
        print("AUTO-SYNC MODE - VMS Volunteers Sheet")
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
    print(" VMS VOLUNTEERS GOOGLE SHEETS SYNC")
    print("="*80)
    print(f"\nSheet URL: {SHEET_URL}")
    print(f"Worksheet: {WORKSHEET_NAME}")
    print("\nOptions:")
    print("1. One-time sync")
    print("2. Auto-sync (continuous - every 5 minutes)")
    print("3. Custom interval auto-sync")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    syncer = VMSVolunteerSync()
    
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

