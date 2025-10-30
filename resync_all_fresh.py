"""
Fresh Re-sync: Clear and sync both sheets with expanded schema
"""

from database import Database
from sync_geeta_sheet import GeetaSheetSync
from sync_vms_volunteers import VMSVolunteerSync

def main():
    print("\n" + "="*80)
    print(" FRESH RE-SYNC WITH EXPANDED SCHEMA")
    print("="*80)
    print("\nThis will:")
    print("  1. Clear ALL volunteer data from database")
    print("  2. Re-sync Geeta Sevi sheet (with expanded columns)")
    print("  3. Re-sync VMS Volunteers sheet (with ALL expanded columns)")
    print("\n" + "="*80)
    
    response = input("\nProceed? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n[CANCELLED] Re-sync cancelled.\n")
        return
    
    db = Database()
    
    # Step 1: Clear volunteer data
    print("\n[STEP 1/3] Clearing existing volunteer data...")
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM volunteers')
    conn.commit()
    conn.close()
    print("[SUCCESS] Cleared all volunteers\n")
    
    # Step 2: Sync Geeta Sevi sheet
    print("[STEP 2/3] Syncing Geeta Sevi IT Interest Areas...")
    print("-" * 80)
    geeta_syncer = GeetaSheetSync()
    if geeta_syncer.sync_from_sheet():
        print("[SUCCESS] Geeta Sevi sheet synced!")
    else:
        print("[ERROR] Geeta Sevi sync failed")
        return
    
    print("\n")
    
    # Step 3: Sync VMS Volunteers sheet
    print("[STEP 3/3] Syncing VMS Volunteers...")
    print("-" * 80)
    vms_syncer = VMSVolunteerSync()
    if vms_syncer.sync_from_sheet():
        print("[SUCCESS] VMS Volunteers sheet synced!")
    else:
        print("[ERROR] VMS Volunteers sync failed")
        return
    
    # Final summary
    total_volunteers = len(db.get_all_volunteers())
    
    print("\n" + "="*80)
    print("[SUCCESS] FRESH SYNC COMPLETE!")
    print("="*80)
    print(f"Total volunteers in database: {total_volunteers}")
    print("\nAll volunteers now have the expanded schema:")
    print("  - VMS Volunteers: All 44 columns populated")
    print("  - Geeta Sevi: Core columns + timestamp/linkedin/join_date")
    print("  - Other columns blank where data not available")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

