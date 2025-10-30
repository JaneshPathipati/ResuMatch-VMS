"""
Test Resume Upload Feature
Creates a sample resume in text format and tests the parser
"""

from resume_parser import ResumeParser

# Sample resume text (as if extracted from PDF)
SAMPLE_RESUME = """
JOHN DOE
john.doe@example.com | (555) 123-4567

SUMMARY
Experienced software developer with 5+ years of expertise in web development and database management.

SKILLS
- Programming Languages: Python, JavaScript, Java, PHP
- Web Frameworks: Django, Flask, React, Node.js
- Databases: MySQL, PostgreSQL, MongoDB
- Tools: Git, Docker, AWS, Jenkins
- Soft Skills: Team Leadership, Problem Solving, Agile Development

EXPERIENCE
Senior Software Developer
Tech Company Inc. | 2020 - Present
- Developed and maintained web applications using Python and Django
- Led a team of 5 developers in agile environment
- Implemented CI/CD pipelines using Jenkins and Docker

Software Developer
StartUp Corp | 2018 - 2020
- Built RESTful APIs using Flask
- Worked with MySQL and PostgreSQL databases
- Collaborated with cross-functional teams

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2014 - 2018

CERTIFICATIONS
- AWS Certified Developer
- Scrum Master Certification

LANGUAGES
English (Native), Spanish (Intermediate)
"""

def test_email_extraction():
    parser = ResumeParser()
    email = parser.extract_email(SAMPLE_RESUME)
    print(f"[TEST] Email Extraction: {email}")
    assert email == "john.doe@example.com", "Email extraction failed"
    print("  [PASSED]")

def test_phone_extraction():
    parser = ResumeParser()
    phone = parser.extract_phone(SAMPLE_RESUME)
    print(f"[TEST] Phone Extraction: {phone}")
    assert phone, "Phone extraction failed"
    print("  [PASSED]")

def test_name_extraction():
    parser = ResumeParser()
    name = parser.extract_name(SAMPLE_RESUME)
    print(f"[TEST] Name Extraction: {name}")
    assert "JOHN DOE" in name.upper(), "Name extraction failed"
    print("  [PASSED]")

def test_skills_extraction():
    parser = ResumeParser()
    skills = parser.extract_skills(SAMPLE_RESUME)
    print(f"[TEST] Skills Extraction: {skills[:100]}...")
    assert "Python" in skills or "python" in skills.lower(), "Skills extraction failed"
    print("  [PASSED]")

def test_experience_extraction():
    parser = ResumeParser()
    experience = parser.extract_experience(SAMPLE_RESUME)
    print(f"[TEST] Experience Extraction: {experience[:100]}...")
    assert experience != "Not specified", "Experience extraction failed"
    print("  [PASSED]")

def test_education_extraction():
    parser = ResumeParser()
    education = parser.extract_education(SAMPLE_RESUME)
    print(f"[TEST] Education Extraction: {education}")
    assert "bachelor" in education.lower() or "computer science" in education.lower(), "Education extraction failed"
    print("  [PASSED]")

def main():
    print("\n" + "="*80)
    print(" TESTING RESUME PARSER")
    print("="*80 + "\n")
    
    try:
        test_email_extraction()
        test_phone_extraction()
        test_name_extraction()
        test_skills_extraction()
        test_experience_extraction()
        test_education_extraction()
        
        print("\n" + "="*80)
        print(" ALL TESTS PASSED [SUCCESS]")
        print("="*80)
        print("\nResume parser is working correctly!")
        print("You can now upload resumes through the web interface.")
        print("\nGo to: http://localhost:5000")
        print("="*80 + "\n")
        
    except AssertionError as e:
        print(f"\n[FAILED] {e}")
        print("="*80 + "\n")

if __name__ == "__main__":
    main()

