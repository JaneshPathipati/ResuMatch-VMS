import pandas as pd
from database import Database

def sync_excel_to_database(excel_file_path):
    """
    Sync volunteer data from Excel file to SQL database
    
    Expected Excel columns:
    - Name
    - Email
    - Phone
    - Skills
    - Experience
    - Education
    - Availability
    - Languages
    - Certifications
    - Interests
    """
    db = Database()
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        
        print(f"Reading Excel file: {excel_file_path}")
        print(f"Found {len(df)} volunteers in Excel file")
        
        # Normalize column names (remove spaces, lowercase)
        df.columns = df.columns.str.strip()
        
        inserted_count = 0
        skipped_count = 0
        
        for index, row in df.iterrows():
            volunteer_data = {
                'name': str(row.get('Name', '')).strip(),
                'email': str(row.get('Email', '')).strip(),
                'phone': str(row.get('Phone', '')).strip(),
                'skills': str(row.get('Skills', '')).strip(),
                'experience': str(row.get('Experience', '')).strip(),
                'education': str(row.get('Education', '')).strip(),
                'availability': str(row.get('Availability', '')).strip(),
                'languages': str(row.get('Languages', '')).strip(),
                'certifications': str(row.get('Certifications', '')).strip(),
                'interests': str(row.get('Interests', '')).strip()
            }
            
            # Validate required fields
            if not volunteer_data['name'] or not volunteer_data['email']:
                print(f"Skipping row {index + 1}: Missing name or email")
                skipped_count += 1
                continue
            
            volunteer_id = db.insert_volunteer(volunteer_data)
            
            if volunteer_id:
                inserted_count += 1
                print(f"Inserted: {volunteer_data['name']} ({volunteer_data['email']})")
            else:
                skipped_count += 1
                print(f"Skipped: {volunteer_data['email']} (already exists)")
        
        print(f"\n[SUCCESS] Sync completed!")
        print(f"  - Inserted: {inserted_count} volunteers")
        print(f"  - Skipped: {skipped_count} volunteers")
        
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_file_path}")
    except Exception as e:
        print(f"Error syncing data: {e}")

if __name__ == "__main__":
    # Example usage
    excel_file = "volunteers_data.xlsx"
    sync_excel_to_database(excel_file)

