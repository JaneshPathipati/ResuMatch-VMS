"""
Remove sample volunteers and keep only Google Sheet volunteers
"""

from database import Database

# List of sample volunteer emails to remove
SAMPLE_EMAILS = [
    'john.smith@email.com',
    'sarah.j@email.com',
    'mchen@email.com',
    'emily.r@email.com',
    'dwilson@email.com',
    'lisa.t@email.com',
    'jmartinez@email.com',
    'rachel.kim@email.com',
    'canderson@email.com',
    'awhite@email.com',
    'kbrown@email.com',
    'jlee@email.com',
    'rtaylor@email.com',
    'ngarcia@email.com',
    'tdavis@email.com'
]

def clean_sample_volunteers():
    """Remove sample volunteers from database"""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("CLEANING SAMPLE VOLUNTEERS")
    print("="*80 + "\n")
    
    # Get count before
    cursor.execute("SELECT COUNT(*) FROM volunteers")
    before_count = cursor.fetchone()[0]
    print(f"Total volunteers before cleaning: {before_count}")
    
    # Delete sample volunteers
    deleted_count = 0
    for email in SAMPLE_EMAILS:
        cursor.execute("SELECT id, name FROM volunteers WHERE email = ?", (email,))
        result = cursor.fetchone()
        
        if result:
            volunteer_id, name = result
            
            # Delete from shortlisted_volunteers first (foreign key)
            cursor.execute("DELETE FROM shortlisted_volunteers WHERE volunteer_id = ?", (volunteer_id,))
            
            # Delete from volunteers
            cursor.execute("DELETE FROM volunteers WHERE id = ?", (volunteer_id,))
            
            deleted_count += 1
            print(f"  [X] Deleted: {name} ({email})")
    
    conn.commit()
    
    # Get count after
    cursor.execute("SELECT COUNT(*) FROM volunteers")
    after_count = cursor.fetchone()[0]
    
    print(f"\n" + "="*80)
    print("CLEANUP COMPLETED")
    print("="*80)
    print(f"Volunteers before: {before_count}")
    print(f"Deleted: {deleted_count}")
    print(f"Volunteers after: {after_count}")
    print(f"\nOnly Google Sheet volunteers remain!")
    print("="*80 + "\n")
    
    conn.close()

if __name__ == "__main__":
    clean_sample_volunteers()

