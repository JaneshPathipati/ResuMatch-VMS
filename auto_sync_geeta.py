"""
Automatic Google Sheets Sync for Geeta Sevi Sheet
Runs sync immediately without menus
"""

from sync_geeta_sheet import GeetaSheetSync

def main():
    print("\n" + "="*80)
    print(" AUTO SYNC - GEETA SEVI GOOGLE SHEET")
    print("="*80 + "\n")
    
    syncer = GeetaSheetSync()
    
    # Run one-time sync
    print("Starting sync from Google Sheet...")
    success = syncer.sync_from_sheet()
    
    if success:
        print("\n" + "="*80)
        print("SYNC COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nYou can now:")
        print("1. View volunteers: python show_data.py")
        print("2. Use web interface: http://localhost:5000")
        print("3. Run auto-sync: python auto_sync_geeta.py --continuous")
    else:
        print("\n" + "="*80)
        print("SYNC FAILED - Please check the errors above")
        print("="*80)
        print("\nMake sure you have:")
        print("1. Created credentials.json file")
        print("2. Shared your Google Sheet with the service account email")
        print("\nSee setup_google_sync.md for instructions")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        # Auto-sync mode
        syncer = GeetaSheetSync()
        syncer.auto_sync(interval_seconds=300)  # Every 5 minutes
    else:
        # One-time sync
        main()

