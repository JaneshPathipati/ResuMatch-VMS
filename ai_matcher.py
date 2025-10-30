"""
AI-Powered Volunteer Matching using Azure OpenAI GPT-4
Intelligent semantic matching between job descriptions and volunteer profiles
"""

import json
from openai import AzureOpenAI
from database import Database
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
    MAX_VOLUNTEERS_TO_ANALYZE,
    TOP_MATCHES_TO_RETURN,
    MIN_MATCH_SCORE
)

class AIVolunteerMatcher:
    def __init__(self):
        self.db = Database()
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
    
    def _create_volunteer_summary(self, volunteer):
        """Create a concise summary of volunteer's profile"""
        summary = f"""
Name: {volunteer.get('name', 'N/A')}
Email: {volunteer.get('email', 'N/A')}
Phone: {volunteer.get('phone', 'N/A')}
Skills: {volunteer.get('skills', 'N/A')}
Primary Skills: {volunteer.get('primary_skills', 'N/A')}
Secondary Skills: {volunteer.get('secondary_skills', 'N/A')}
Experience: {volunteer.get('experience', 'N/A')}
Years of Experience: {volunteer.get('years_experience', 'N/A')}
Previous Experience: {volunteer.get('previous_experience', 'N/A') or 'N/A'}
Education: {volunteer.get('education', 'N/A')}
Education Field: {volunteer.get('education_field', 'N/A')}
Profession: {volunteer.get('profession', 'N/A')}
Job Sector: {volunteer.get('job_sector', 'N/A')}
Job Position: {volunteer.get('job_position', 'N/A')}
Languages: {volunteer.get('languages', 'N/A')}
Availability: {volunteer.get('availability', 'N/A')}
Volunteering Mode: {volunteer.get('volunteering_mode', 'N/A')}
Location: {volunteer.get('city', 'N/A')}, {volunteer.get('state', 'N/A')}
Interests: {volunteer.get('interests', 'N/A')}
        """.strip()
        return summary
    
    def _analyze_single_match(self, volunteer, job_description):
        """Use GPT-4 to analyze a single volunteer-job match"""
        
        volunteer_summary = self._create_volunteer_summary(volunteer)
        
        prompt = f"""You are an expert HR recruiter analyzing volunteer-job matches.

JOB DESCRIPTION:
{job_description}

VOLUNTEER PROFILE:
{volunteer_summary}

Analyze how well this volunteer matches the job requirements. Provide your assessment in the following JSON format:

{{
    "match_score": <number 0-100>,
    "skills_match": {{
        "score": <number 0-100>,
        "matching_skills": ["skill1", "skill2", ...],
        "missing_skills": ["skill1", "skill2", ...],
        "explanation": "Brief explanation"
    }},
    "experience_match": {{
        "score": <number 0-100>,
        "relevant_experience": "What relevant experience they have",
        "explanation": "Brief explanation"
    }},
    "education_match": {{
        "score": <number 0-100>,
        "explanation": "Brief explanation"
    }},
    "availability_match": {{
        "score": <number 0-100>,
        "explanation": "Brief explanation"
    }},
    "overall_assessment": "2-3 sentence summary of why this is a good/bad match",
    "strengths": ["strength1", "strength2", "strength3"],
    "concerns": ["concern1", "concern2"] or []
}}

Be objective and thorough. Score 90-100 for excellent matches, 70-89 for good matches, 50-69 for moderate matches, below 50 for poor matches."""

        try:
            response = self.client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are an expert HR recruiter and talent matcher. Provide accurate, objective assessments in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent scoring
                max_tokens=1000
            )
            
            # Parse GPT-4 response
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response (in case GPT-4 adds extra text)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(content)
            
            return {
                'volunteer_id': volunteer.get('id'),
                'volunteer_name': volunteer.get('name'),
                'volunteer_email': volunteer.get('email'),
                'volunteer_phone': volunteer.get('phone'),
                'match_score': analysis.get('match_score', 0),
                'analysis': analysis
            }
            
        except Exception as e:
            print(f"[ERROR] AI analysis failed for volunteer {volunteer.get('id')}: {e}")
            return None
    
    def _batch_analyze_volunteers(self, volunteers, job_description):
        """Analyze multiple volunteers efficiently"""
        
        # For very large datasets, we can batch volunteers
        # For now, analyze individually for detailed results
        results = []
        
        for i, volunteer in enumerate(volunteers[:MAX_VOLUNTEERS_TO_ANALYZE], 1):
            print(f"[AI] Analyzing volunteer {i}/{min(len(volunteers), MAX_VOLUNTEERS_TO_ANALYZE)}: {volunteer.get('name')}")
            
            result = self._analyze_single_match(volunteer, job_description)
            
            if result and result['match_score'] >= MIN_MATCH_SCORE:
                results.append(result)
        
        # Sort by match score (descending)
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return results[:TOP_MATCHES_TO_RETURN]
    
    def find_matching_volunteers(self, job_description):
        """
        Main method: Find and rank volunteers matching a job description
        
        Args:
            job_description (str): The job description text
        
        Returns:
            list: Top matching volunteers with detailed analysis
        """
        
        print("\n" + "="*80)
        print(" AI-POWERED VOLUNTEER MATCHING")
        print("="*80)
        print(f"\nJob Description Length: {len(job_description)} characters")
        
        # Get all volunteers from database
        all_volunteers = self.db.get_all_volunteers()
        print(f"Total Volunteers in Database: {len(all_volunteers)}")
        
        if not all_volunteers:
            print("[ERROR] No volunteers found in database")
            return []
        
        # Filter volunteers with minimum data
        eligible_volunteers = [
            v for v in all_volunteers 
            if v.get('name') and v.get('email') and (v.get('skills') or v.get('profession'))
        ]
        print(f"Eligible Volunteers (with basic info): {len(eligible_volunteers)}")
        
        if not eligible_volunteers:
            print("[ERROR] No eligible volunteers found")
            return []
        
        # Use GPT-4 to analyze matches
        print(f"\n[AI] Starting GPT-4 analysis (processing top {min(len(eligible_volunteers), MAX_VOLUNTEERS_TO_ANALYZE)} candidates)...")
        print("-" * 80)
        
        matches = self._batch_analyze_volunteers(eligible_volunteers, job_description)
        
        print("\n" + "="*80)
        print(f" MATCHING COMPLETE - Found {len(matches)} qualified matches")
        print("="*80)
        
        # Display summary
        if matches:
            print("\nTop Matches:")
            for i, match in enumerate(matches[:5], 1):
                print(f"  {i}. {match['volunteer_name']} - Score: {match['match_score']}/100")
        
        return matches
    
    def save_shortlisted_volunteers(self, job_description, matches):
        """Save shortlisted volunteers to database"""
        
        # Clear previous shortlisted volunteers
        self.db.clear_shortlisted_volunteers()
        
        saved_count = 0
        for match in matches:
            analysis = match.get('analysis', {})
            
            # Format matching skills
            skills_match = analysis.get('skills_match', {})
            matching_skills = ', '.join(skills_match.get('matching_skills', []))
            
            if not matching_skills:
                matching_skills = 'General fit based on profile'
            
            # Save to database
            try:
                self.db.insert_shortlisted_volunteer(
                    volunteer_id=match['volunteer_id'],
                    job_description=job_description[:500],  # Truncate if too long
                    match_score=match['match_score'],
                    matching_skills=matching_skills[:500]  # Truncate if too long
                )
                saved_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to save volunteer {match['volunteer_id']}: {e}")
        
        print(f"\n[SUCCESS] Saved {saved_count} shortlisted volunteers to database")
        return saved_count

def test_ai_matcher():
    """Test function for the AI matcher"""
    
    matcher = AIVolunteerMatcher()
    
    # Test job description
    job_description = """
    We are looking for a Python developer with experience in web development.
    
    Requirements:
    - 2+ years of Python experience
    - Experience with Flask or Django
    - Knowledge of databases (SQL)
    - Good communication skills
    - Available for part-time remote work
    
    Responsibilities:
    - Develop web applications
    - Write clean, maintainable code
    - Collaborate with the team
    """
    
    print("\n" + "="*80)
    print(" TESTING AI MATCHER")
    print("="*80)
    
    # Find matches
    matches = matcher.find_matching_volunteers(job_description)
    
    # Display detailed results
    print("\n" + "="*80)
    print(" DETAILED RESULTS")
    print("="*80)
    
    for i, match in enumerate(matches, 1):
        print(f"\n--- MATCH #{i} ---")
        print(f"Name: {match['volunteer_name']}")
        print(f"Email: {match['volunteer_email']}")
        print(f"Overall Score: {match['match_score']}/100")
        
        analysis = match['analysis']
        print(f"\nAssessment: {analysis.get('overall_assessment', 'N/A')}")
        
        print("\nStrengths:")
        for strength in analysis.get('strengths', []):
            print(f"  + {strength}")
        
        concerns = analysis.get('concerns', [])
        if concerns:
            print("\nConcerns:")
            for concern in concerns:
                print(f"  - {concern}")
        
        print("\nDetailed Scores:")
        print(f"  Skills Match: {analysis.get('skills_match', {}).get('score', 'N/A')}/100")
        print(f"  Experience Match: {analysis.get('experience_match', {}).get('score', 'N/A')}/100")
        print(f"  Education Match: {analysis.get('education_match', {}).get('score', 'N/A')}/100")
        print(f"  Availability Match: {analysis.get('availability_match', {}).get('score', 'N/A')}/100")
        
        print("-" * 80)
    
    # Save to database
    if matches:
        matcher.save_shortlisted_volunteers(job_description, matches)
    
    print("\n" + "="*80)
    print(" TEST COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_ai_matcher()

