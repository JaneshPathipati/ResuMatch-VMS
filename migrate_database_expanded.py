"""
Database Migration: Add Expanded Columns
Adds new columns from VMS Volunteers sheet to existing database
"""

import sqlite3
from datetime import datetime

DB_NAME = 'volunteer_management.db'

def backup_database():
    """Create a backup of the database before migration"""
    import shutil
    backup_name = f"volunteer_management_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    try:
        shutil.copy2(DB_NAME, backup_name)
        print(f"[SUCCESS] Database backed up to: {backup_name}")
        return True
    except Exception as e:
        print(f"[ERROR] Backup failed: {e}")
        return False

def add_new_columns():
    """Add new columns to volunteers table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # List of new columns to add
    new_columns = [
        ('timestamp', 'TEXT'),
        ('prefix', 'TEXT'),
        ('alternate_phone', 'TEXT'),
        ('date_of_birth', 'TEXT'),
        ('anniversary_date', 'TEXT'),
        ('gender', 'TEXT'),
        ('country', 'TEXT'),
        ('state', 'TEXT'),
        ('city', 'TEXT'),
        ('address', 'TEXT'),
        ('pin_code', 'TEXT'),
        ('zip_code', 'TEXT'),
        ('education_field', 'TEXT'),
        ('job_sector', 'TEXT'),
        ('profession', 'TEXT'),
        ('job_position', 'TEXT'),
        ('years_experience', 'TEXT'),
        ('linkedin_url', 'TEXT'),
        ('facebook_url', 'TEXT'),
        ('instagram_url', 'TEXT'),
        ('previous_experience', 'TEXT'),
        ('primary_skills', 'TEXT'),
        ('secondary_skills', 'TEXT'),
        ('volunteering_mode', 'TEXT'),
        ('availability_days', 'TEXT'),
        ('time_availability', 'TEXT'),
        ('commitment_duration', 'TEXT'),
        ('join_date', 'TEXT'),
        ('hear_about_source', 'TEXT'),
        ('passed_examination', 'TEXT'),
        ('departments_served', 'TEXT'),
        ('journey_description', 'TEXT'),
    ]
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(volunteers)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    print("\n" + "="*80)
    print(" DATABASE MIGRATION - ADDING EXPANDED COLUMNS")
    print("="*80)
    print(f"\nExisting columns: {len(existing_columns)}")
    print(f"New columns to add: {len(new_columns)}\n")
    
    added_count = 0
    skipped_count = 0
    
    for column_name, column_type in new_columns:
        if column_name in existing_columns:
            print(f"  [SKIP] {column_name:30} (already exists)")
            skipped_count += 1
        else:
            try:
                sql = f"ALTER TABLE volunteers ADD COLUMN {column_name} {column_type}"
                cursor.execute(sql)
                print(f"  [ADD]  {column_name:30} {column_type}")
                added_count += 1
            except Exception as e:
                print(f"  [ERROR] {column_name:30} - {e}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*80)
    print(" MIGRATION COMPLETE")
    print("="*80)
    print(f"  - Columns added: {added_count}")
    print(f"  - Columns skipped: {skipped_count}")
    print(f"  - Total columns now: {len(existing_columns) + added_count}")
    print("="*80 + "\n")
    
    return True

def verify_migration():
    """Verify the migration was successful"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(volunteers)")
    columns = cursor.fetchall()
    
    print("\n" + "="*80)
    print(" VERIFICATION - ALL COLUMNS IN VOLUNTEERS TABLE")
    print("="*80 + "\n")
    
    for col in columns:
        col_id, name, col_type, not_null, default_val, pk = col
        nullable = "NOT NULL" if not_null else "NULL"
        primary = " (PRIMARY KEY)" if pk else ""
        print(f"  {col_id+1:2}. {name:30} {col_type:15} {nullable:10}{primary}")
    
    print(f"\n  Total columns: {len(columns)}")
    print("="*80 + "\n")
    
    conn.close()

def main():
    print("\n" + "="*80)
    print(" DATABASE MIGRATION TOOL")
    print("="*80)
    print("\nThis will add new columns to your volunteers table.")
    print("A backup will be created before migration.")
    print("\n" + "="*80)
    
    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n[CANCELLED] Migration cancelled by user.\n")
        return
    
    # Step 1: Backup
    print("\n[STEP 1/3] Creating backup...")
    if not backup_database():
        print("\n[ERROR] Cannot proceed without backup.")
        return
    
    # Step 2: Add columns
    print("\n[STEP 2/3] Adding new columns...")
    if not add_new_columns():
        print("\n[ERROR] Migration failed.")
        return
    
    # Step 3: Verify
    print("[STEP 3/3] Verifying migration...")
    verify_migration()
    
    print("\n" + "="*80)
    print("[SUCCESS] MIGRATION COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nNext steps:")
    print("  1. The sync scripts will now use the expanded schema")
    print("  2. Run RUN_DUAL_SYNC.bat to sync both sheets")
    print("  3. New columns will be populated for VMS Volunteers sheet")
    print("  4. Geeta Sevi sheet will have blank values for extra columns")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

