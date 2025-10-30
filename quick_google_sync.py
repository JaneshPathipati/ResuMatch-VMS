"""
Quick Google Sheets Sync Script
Simple one-command sync without menu
"""

from google_sheets_sync import GoogleSheetSync
import sys

# CONFIGURATION
# ==============
# Replace these with your Google Sheet details:

SHEET_URL = "YOUR_GOOGLE_SHEET_URL_HERE"
WORKSHEET_NAME = "Sheet1"  # Change if different (e.g., "Form Responses 1")

# For auto-sync, set this to True
AUTO_SYNC = False
SYNC_INTERVAL_SECONDS = 300  # 5 minutes

# ==============

def main():
    print("\n" + "="*80)
    print(" QUICK GOOGLE SHEETS SYNC")
    print("="*80 + "\n")
    
    if SHEET_URL == "YOUR_GOOGLE_SHEET_URL_HERE":
        print("[ERROR] Please edit quick_google_sync.py and set your SHEET_URL")
        print("\nInstructions:")
        print("1. Open quick_google_sync.py in a text editor")
        print("2. Replace SHEET_URL with your actual Google Sheet URL")
        print("3. Optionally change WORKSHEET_NAME if needed")
        print("4. Run this script again")
        sys.exit(1)
    
    syncer = GoogleSheetSync()
    
    if AUTO_SYNC:
        print(f"Starting auto-sync mode (every {SYNC_INTERVAL_SECONDS} seconds)...")
        syncer.auto_sync(SHEET_URL, WORKSHEET_NAME, SYNC_INTERVAL_SECONDS)
    else:
        print("Starting one-time sync...")
        syncer.sync_from_sheet(SHEET_URL, WORKSHEET_NAME)

if __name__ == "__main__":
    main()
