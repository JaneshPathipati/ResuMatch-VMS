"""
Test if credentials.json file exists and is valid
"""

import os
import json

def test_credentials():
    print("\n" + "="*80)
    print(" CREDENTIALS CHECK")
    print("="*80 + "\n")
    
    cred_file = "credentials.json"
    
    # Check if file exists
    if not os.path.exists(cred_file):
        print(f"[ERROR] File not found: {cred_file}")
        print("\nThe file should be at:")
        print(f"  {os.path.abspath(cred_file)}")
        print("\nPlease:")
        print("1. Download credentials.json from Google Cloud Console")
        print("2. Save it in this folder")
        print("\nSee setup_google_sync.md for detailed instructions")
        return False
    
    print(f"[OK] File found: {cred_file}")
    
    # Check if it's valid JSON
    try:
        with open(cred_file, 'r') as f:
            data = json.load(f)
        
        # Check for required fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing = [field for field in required_fields if field not in data]
        
        if missing:
            print(f"[ERROR] Missing required fields: {', '.join(missing)}")
            return False
        
        print(f"[OK] Valid JSON format")
        print(f"\n[INFO] Service Account Details:")
        print(f"  Project ID: {data.get('project_id')}")
        print(f"  Client Email: {data.get('client_email')}")
        print(f"\n[IMPORTANT] Make sure you shared your Google Sheet with:")
        print(f"  {data.get('client_email')}")
        print("\nTo share:")
        print("1. Open your Google Sheet")
        print("2. Click 'Share' button")
        print("3. Add the email above")
        print("4. Give 'Viewer' or 'Editor' access")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON file: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == "__main__":
    success = test_credentials()
    
    if success:
        print("\n" + "="*80)
        print("[SUCCESS] Credentials file is ready!")
        print("="*80)
        print("\nYou can now run:")
        print("  python auto_sync_geeta.py")
    else:
        print("\n" + "="*80)
        print("[FAILED] Please fix the issues above")
        print("="*80)

