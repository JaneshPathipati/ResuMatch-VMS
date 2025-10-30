"""
Verify Expanded Schema Data
"""

from database import Database

db = Database()

print("\n" + "="*80)
print(" VERIFICATION - EXPANDED SCHEMA DATA")
print("="*80)

# Get total volunteers
all_volunteers = db.get_all_volunteers()
print(f"\nTotal volunteers in database: {len(all_volunteers)}")

# Show Geeta Sevi volunteer (first one)
print("\n" + "-"*80)
print("SAMPLE: GEETA SEVI VOLUNTEER (Volunteer #1)")
print("-"*80)
if all_volunteers:
    v = all_volunteers[0]
    print(f"  ID: {v.get('id')}")
    print(f"  Name: {v.get('name')}")
    print(f"  Email: {v.get('email')}")
    print(f"  Phone: {v.get('phone')}")
    print(f"  Skills: {v.get('skills', '')[:80]}...")
    print(f"  Timestamp: {v.get('timestamp', 'N/A')}")
    print(f"  LinkedIn: {v.get('linkedin_url', 'N/A')}")
    print(f"  Gender: {v.get('gender', 'N/A')}")
    print(f"  City: {v.get('city', 'N/A')}")
    print(f"  Profession: {v.get('profession', 'N/A')}")

# Show VMS volunteer
print("\n" + "-"*80)
print("SAMPLE: VMS VOLUNTEER (Volunteer #150)")
print("-"*80)
if len(all_volunteers) > 149:
    v = all_volunteers[149]
    print(f"  ID: {v.get('id')}")
    print(f"  Name: {v.get('name')}")
    print(f"  Email: {v.get('email')}")
    print(f"  Phone: {v.get('phone')}")
    print(f"  Timestamp: {v.get('timestamp', 'N/A')}")
    print(f"  Prefix: {v.get('prefix', 'N/A')}")
    print(f"  Gender: {v.get('gender', 'N/A')}")
    print(f"  Date of Birth: {v.get('date_of_birth', 'N/A')}")
    print(f"  City: {v.get('city', 'N/A')}")
    print(f"  State: {v.get('state', 'N/A')}")
    print(f"  Address: {v.get('address', 'N/A')[:60]}...")
    print(f"  Education: {v.get('education', 'N/A')[:60]}...")
    print(f"  Profession: {v.get('profession', 'N/A')}")
    print(f"  Job Sector: {v.get('job_sector', 'N/A')}")
    print(f"  Primary Skills: {v.get('primary_skills', 'N/A')[:60]}...")
    print(f"  Languages: {v.get('languages', 'N/A')[:60]}...")
    print(f"  Volunteering Mode: {v.get('volunteering_mode', 'N/A')}")
    print(f"  Join Date: {v.get('join_date', 'N/A')}")

print("\n" + "="*80)
print(" SUMMARY")
print("="*80)

# Count volunteers by source
geeta_count = sum(1 for v in all_volunteers if '@vms.volunteer.temp' not in v.get('email', ''))
vms_count = sum(1 for v in all_volunteers if '@vms.volunteer.temp' in v.get('email', ''))

print(f"\nVolunteers by source:")
print(f"  - Geeta Sevi IT Interest Areas: {geeta_count}")
print(f"  - VMS Volunteers (synthetic emails): {vms_count}")
print(f"  - Total: {len(all_volunteers)}")

# Count populated fields
expanded_fields = ['prefix', 'gender', 'date_of_birth', 'city', 'state', 'profession', 'job_sector']
print(f"\nExpanded fields populated:")
for field in expanded_fields:
    count = sum(1 for v in all_volunteers if v.get(field))
    print(f"  - {field}: {count} / {len(all_volunteers)} ({count*100/len(all_volunteers):.1f}%)")

print("\n" + "="*80)
print("[SUCCESS] Verification complete!")
print("="*80 + "\n")

