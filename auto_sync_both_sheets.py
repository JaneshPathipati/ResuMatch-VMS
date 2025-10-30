"""
Auto-Sync Both Google Sheets Continuously
Syncs both Geeta Sevi and VMS Volunteers sheets at regular intervals
"""

import time
from datetime import datetime
from sync_geeta_sheet import GeetaSheetSync
from sync_vms_volunteers import VMSVolunteerSync
from database import Database

class DualSheetAutoSync:
    def __init__(self, credentials_file='credentials.json'):
        self.geeta_syncer = GeetaSheetSync(credentials_file)
        self.vms_syncer = VMSVolunteerSync(credentials_file)
        self.db = Database()
    
    def sync_both_sheets(self):
        """Sync both Google Sheets"""
        print(f"\n{'='*80}")
        print("SYNCING BOTH GOOGLE SHEETS")
        print(f"{'='*80}\n")
        
        success_count = 0
        
        # Sync Sheet 1: Geeta Sevi
        print("[1/2] Syncing Geeta Sevi IT Interest Areas...")
        print("-" * 80)
        if self.geeta_syncer.sync_from_sheet():
            success_count += 1
        
        print("\n")
        
        # Sync Sheet 2: VMS Volunteers
        print("[2/2] Syncing VMS Volunteers...")
        print("-" * 80)
        if self.vms_syncer.sync_from_sheet():
            success_count += 1
        
        print(f"\n{'='*80}")
        print(f"SYNC SUMMARY - {success_count}/2 sheets synced successfully")
        print(f"{'='*80}")
        print(f"Total volunteers in database: {len(self.db.get_all_volunteers())}")
        print(f"{'='*80}\n")
        
        return success_count == 2
    
    def auto_sync(self, interval_seconds=300):
        """Auto-sync both sheets at regular intervals"""
        print(f"\n{'='*80}")
        print("DUAL AUTO-SYNC MODE")
        print(f"{'='*80}")
        print("Syncing BOTH Google Sheets:")
        print("  1. Geeta Sevi IT Interest Areas")
        print("  2. VMS Volunteers Data")
        print(f"\nSync interval: {interval_seconds} seconds ({interval_seconds/60:.1f} minutes)")
        print("Press Ctrl+C to stop\n")
        print(f"{'='*80}\n")
        
        sync_count = 0
        
        try:
            while True:
                sync_count += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"\n{'#'*80}")
                print(f"SYNC CYCLE #{sync_count} - {timestamp}")
                print(f"{'#'*80}")
                
                self.sync_both_sheets()
                
                print(f"\n[INFO] Next sync cycle in {interval_seconds} seconds...")
                print(f"[INFO] Waiting... (Press Ctrl+C to stop)\n")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n\n{'='*80}")
            print("AUTO-SYNC STOPPED")
            print(f"{'='*80}")
            print(f"Total sync cycles completed: {sync_count}")
            print(f"Final volunteer count: {len(self.db.get_all_volunteers())}")
            print(f"{'='*80}\n")

def main():
    """Main function"""
    print("\n" + "="*80)
    print(" DUAL GOOGLE SHEETS AUTO-SYNC")
    print("="*80)
    print("\nThis will sync BOTH spreadsheets:")
    print("  1. Geeta Sevi IT Interest Areas")
    print("  2. VMS Volunteers Data")
    print("\nOptions:")
    print("1. One-time sync (both sheets)")
    print("2. Auto-sync (continuous - every 5 minutes)")
    print("3. Custom interval auto-sync")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    syncer = DualSheetAutoSync()
    
    if choice == '1':
        syncer.sync_both_sheets()
    
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
        print("\nGoodbye!")
    else:
        print("\nInvalid choice.")

if __name__ == "__main__":
    main()

