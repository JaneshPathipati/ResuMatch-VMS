"""
Quick setup script for Volunteer Management System
Runs all necessary setup steps in sequence
"""

import subprocess
import sys

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print('='*60)
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False, text=True)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 VOLUNTEER MANAGEMENT SYSTEM - SETUP")
    print("="*60)
    
    steps = [
        ("pip install -r requirements.txt", "Installing dependencies"),
        ("python create_sample_data.py", "Creating sample volunteer data"),
        ("python excel_sync.py", "Syncing data to database"),
    ]
    
    success_count = 0
    for command, description in steps:
        if run_command(command, description):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"📊 SETUP SUMMARY")
    print("="*60)
    print(f"Completed: {success_count}/{len(steps)} steps")
    
    if success_count == len(steps):
        print("\n✓ Setup completed successfully!")
        print("\n🌐 To start the application, run:")
        print("   python app.py")
        print("\n   Then open http://localhost:5000 in your browser")
    else:
        print("\n✗ Setup incomplete. Please check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

