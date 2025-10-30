from database import Database

db = Database()

# Get volunteers
volunteers = db.get_all_volunteers()
print(f"\n{'='*80}")
print(f"DATABASE CONTENTS")
print(f"{'='*80}\n")
print(f"Total Volunteers: {len(volunteers)}\n")

print("First 5 Volunteers:")
print("-" * 80)
for i, v in enumerate(volunteers[:5], 1):
    print(f"\n{i}. {v['name']}")
    print(f"   Email: {v['email']}")
    print(f"   Skills: {v['skills']}")

# Get shortlisted
shortlisted = db.get_shortlisted_volunteers()
print(f"\n\n{'='*80}")
print(f"Total Shortlisted: {len(shortlisted)}\n")

if shortlisted:
    print("Shortlisted Volunteers:")
    print("-" * 80)
    for i, s in enumerate(shortlisted[:5], 1):
        print(f"\n{i}. {s['name']} - Match Score: {s['match_score']}%")
        print(f"   Email: {s['email']}")
        print(f"   Skills: {s['skills']}")
else:
    print("No volunteers shortlisted yet. Use the web interface to shortlist!")

print(f"\n{'='*80}")
print("Database file: volunteer_management.db")
print(f"{'='*80}\n")
