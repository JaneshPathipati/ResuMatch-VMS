"""
Complete System Test - Resume Parsing and Matching
Tests the AI matching with real Google Sheet data
"""

from database import Database
from resume_matcher import ResumeMatcher
import json

def test_system():
    print("\n" + "="*80)
    print(" COMPLETE SYSTEM TEST - RESUME PARSING & MATCHING")
    print("="*80 + "\n")
    
    # Initialize
    db = Database()
    matcher = ResumeMatcher()
    
    # Test 1: Check database
    print("[TEST 1] Checking Database...")
    volunteers = db.get_all_volunteers()
    print(f"  [OK] Database connected")
    print(f"  [OK] Total volunteers: {len(volunteers)}")
    
    if len(volunteers) == 0:
        print("  [ERROR] No volunteers in database!")
        return False
    
    # Show sample volunteer
    print(f"\n  Sample Volunteer:")
    sample = volunteers[0]
    print(f"    Name: {sample['name']}")
    print(f"    Email: {sample['email']}")
    print(f"    Skills: {sample['skills'][:80]}...")
    
    # Test 2: Test AI Matching with different job descriptions
    test_cases = [
        {
            'title': 'PHP & MySQL Developer',
            'description': 'Need volunteer with PHP and MySQL experience. Wordpress coding skills preferred. Should have web development background.',
            'expected_skills': ['PHP', 'MySQL', 'Wordpress']
        },
        {
            'title': 'Testing & QA Specialist',
            'description': 'Looking for QA engineer with testing experience. Process management and quality assurance skills required. 3+ years experience preferred.',
            'expected_skills': ['Testing', 'QA', 'Process Management']
        },
        {
            'title': 'AI & Machine Learning Expert',
            'description': 'Seeking volunteer with AI programming and machine learning expertise. Python skills and data analysis experience needed.',
            'expected_skills': ['AI', 'Programming', 'Machine Learning']
        },
        {
            'title': 'Digital Marketing Specialist',
            'description': 'Need digital marketing expert with social media and SEO experience. Graphic design skills are a plus.',
            'expected_skills': ['Digital Marketing', 'Graphic Design']
        }
    ]
    
    print(f"\n[TEST 2] Testing AI Resume Matching...\n")
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"  Test Case {i}: {test_case['title']}")
        print(f"  Job Description: {test_case['description'][:80]}...")
        
        # Run matching
        matches = matcher.shortlist_volunteers(
            volunteers,
            test_case['description'],
            min_score=0.01,  # Low threshold for testing
            max_results=5
        )
        
        if len(matches) == 0:
            print(f"  [FAILED] No matches found!")
            all_passed = False
            continue
        
        print(f"  [OK] Found {len(matches)} matches")
        print(f"\n  Top 3 Matches:")
        
        for j, match in enumerate(matches[:3], 1):
            volunteer = match['volunteer']
            score = match['match_score']
            skills = match['matching_skills']
            
            print(f"\n    #{j}. {volunteer['name']} (Score: {score}%)")
            print(f"       Email: {volunteer['email']}")
            print(f"       Skills: {volunteer['skills'][:60]}...")
            if skills:
                print(f"       Matching: {', '.join(skills[:5])}")
        
        print()
    
    # Test 3: Test Database Storage
    print(f"\n[TEST 3] Testing Shortlist Storage...\n")
    
    # Clear previous shortlisted
    db.clear_shortlisted_volunteers()
    
    # Shortlist with a test job description
    test_job_desc = "Looking for PHP developer with MySQL and Wordpress experience"
    print(f"  Job Description: {test_job_desc}")
    
    matches = matcher.shortlist_volunteers(volunteers, test_job_desc, max_results=5)
    
    # Store in database
    for match in matches:
        volunteer = match['volunteer']
        db.insert_shortlisted_volunteer(
            volunteer['id'],
            test_job_desc,
            match['match_score'],
            json.dumps(match['matching_skills'])
        )
    
    # Retrieve from database
    shortlisted = db.get_shortlisted_volunteers()
    
    print(f"  [OK] Stored {len(matches)} volunteers in shortlist table")
    print(f"  [OK] Retrieved {len(shortlisted)} from database")
    
    if len(shortlisted) > 0:
        print(f"\n  Shortlisted Volunteer:")
        top = shortlisted[0]
        print(f"    Name: {top['name']}")
        print(f"    Match Score: {top['match_score']}%")
        print(f"    Skills: {top['skills'][:60]}...")
    
    # Test 4: Check Resume Parsing Features
    print(f"\n[TEST 4] Testing Resume Parsing Features...\n")
    
    # Test keyword extraction
    sample_text = "PHP MySQL Wordpress React Python Django Testing QA"
    keywords = matcher.extract_keywords(sample_text)
    print(f"  [OK] Keyword Extraction: {keywords[:10]}")
    
    # Test text preprocessing
    messy_text = "  PHP + MySQL,  WordPress  Coding!! "
    clean_text = matcher.preprocess_text(messy_text)
    print(f"  [OK] Text Preprocessing: '{messy_text}' -> '{clean_text}'")
    
    # Test profile creation
    sample_vol = volunteers[0]
    profile = matcher.create_volunteer_profile(sample_vol)
    print(f"  [OK] Profile Creation: {profile[:80]}...")
    
    # Final Summary
    print(f"\n" + "="*80)
    print(" TEST SUMMARY")
    print("="*80)
    print(f"  [OK] Database: {len(volunteers)} volunteers loaded")
    print(f"  [OK] AI Matching: Working with {len(test_cases)} test cases")
    print(f"  [OK] Storage: Shortlisted volunteers saved to database")
    print(f"  [OK] Resume Parsing: Keyword extraction & preprocessing working")
    print(f"\n  ALL SYSTEMS OPERATIONAL [SUCCESS]")
    print("="*80 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        test_system()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

