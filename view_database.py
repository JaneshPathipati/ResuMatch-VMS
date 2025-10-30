"""
Database Viewer and Management Script
View all data in the volunteer management database
"""

from database import Database
import json

def print_separator():
    print("\n" + "="*80 + "\n")

def view_all_volunteers():
    """Display all volunteers in the database"""
    db = Database()
    volunteers = db.get_all_volunteers()
    
    print_separator()
    print(f"ALL VOLUNTEERS (Total: {len(volunteers)})")
    print_separator()
    
    if not volunteers:
        print("No volunteers found in database.")
        return
    
    # Display in a nice table format
    for i, v in enumerate(volunteers, 1):
        print(f"\n[{i}] {v['name']}")
        print("-" * 60)
        print(f"  Email:          {v['email']}")
        print(f"  Phone:          {v['phone']}")
        print(f"  Skills:         {v['skills']}")
        print(f"  Experience:     {v['experience']}")
        print(f"  Education:      {v['education']}")
        print(f"  Availability:   {v['availability']}")
        print(f"  Languages:      {v['languages']}")
        print(f"  Certifications: {v['certifications']}")
        print(f"  Interests:      {v['interests']}")
        print(f"  Created At:     {v['created_at']}")

def view_shortlisted_volunteers():
    """Display all shortlisted volunteers"""
    db = Database()
    shortlisted = db.get_shortlisted_volunteers()
    
    print_separator()
    print(f"SHORTLISTED VOLUNTEERS (Total: {len(shortlisted)})")
    print_separator()
    
    if not shortlisted:
        print("No shortlisted volunteers found.")
        return
    
    for i, v in enumerate(shortlisted, 1):
        print(f"\n[{i}] {v['name']} - Match Score: {v['match_score']}%")
        print("-" * 60)
        print(f"  Email:          {v['email']}")
        print(f"  Phone:          {v['phone']}")
        print(f"  Skills:         {v['skills']}")
        print(f"  Experience:     {v['experience']}")
        
        # Parse matching skills
        try:
            matching_skills = json.loads(v['matching_skills'])
            if matching_skills:
                print(f"  Matching Skills: {', '.join(matching_skills)}")
        except:
            pass
        
        print(f"  Job Description: {v['job_description'][:100]}...")
        print(f"  Shortlisted At:  {v['shortlisted_at']}")

def export_to_json():
    """Export all data to JSON files"""
    db = Database()
    volunteers = db.get_all_volunteers()
    shortlisted = db.get_shortlisted_volunteers()
    
    # Export volunteers
    with open('volunteers_export.json', 'w', encoding='utf-8') as f:
        json.dump(volunteers, f, indent=2)
    
    # Export shortlisted
    with open('shortlisted_export.json', 'w', encoding='utf-8') as f:
        json.dump(shortlisted, f, indent=2)
    
    print_separator()
    print("EXPORT COMPLETED")
    print_separator()
    print(f"Volunteers exported to: volunteers_export.json ({len(volunteers)} records)")
    print(f"Shortlisted exported to: shortlisted_export.json ({len(shortlisted)} records)")

def get_database_stats():
    """Show database statistics"""
    db = Database()
    volunteers = db.get_all_volunteers()
    shortlisted = db.get_shortlisted_volunteers()
    
    print_separator()
    print("DATABASE STATISTICS")
    print_separator()
    print(f"Total Volunteers:        {len(volunteers)}")
    print(f"Shortlisted Volunteers:  {len(shortlisted)}")
    print(f"Database File:           volunteer_management.db")
    
    if volunteers:
        print(f"\nLatest Volunteer Added:  {volunteers[-1]['name']} ({volunteers[-1]['created_at']})")
    
    if shortlisted:
        # Get top match
        top_match = max(shortlisted, key=lambda x: x['match_score'])
        print(f"Top Match Score:         {top_match['match_score']}% ({top_match['name']})")

def search_volunteers(keyword):
    """Search volunteers by keyword"""
    db = Database()
    volunteers = db.get_all_volunteers()
    
    keyword_lower = keyword.lower()
    results = []
    
    for v in volunteers:
        # Search in multiple fields
        searchable = f"{v['name']} {v['email']} {v['skills']} {v['experience']} {v['education']}".lower()
        if keyword_lower in searchable:
            results.append(v)
    
    print_separator()
    print(f"SEARCH RESULTS FOR: '{keyword}' (Found: {len(results)})")
    print_separator()
    
    if not results:
        print("No matches found.")
        return
    
    for i, v in enumerate(results, 1):
        print(f"\n[{i}] {v['name']}")
        print(f"    Email: {v['email']}")
        print(f"    Skills: {v['skills']}")
        print(f"    Experience: {v['experience']}")

def main_menu():
    """Interactive menu for database access"""
    while True:
        print("\n" + "="*80)
        print(" VOLUNTEER DATABASE VIEWER")
        print("="*80)
        print("\n1. View All Volunteers")
        print("2. View Shortlisted Volunteers")
        print("3. Database Statistics")
        print("4. Search Volunteers")
        print("5. Export Data to JSON")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            view_all_volunteers()
        elif choice == '2':
            view_shortlisted_volunteers()
        elif choice == '3':
            get_database_stats()
        elif choice == '4':
            keyword = input("\nEnter search keyword: ").strip()
            if keyword:
                search_volunteers(keyword)
        elif choice == '5':
            export_to_json()
        elif choice == '6':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
