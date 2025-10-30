"""
AI-Powered Keyword Extractor for Job Descriptions
Uses GPT-4 to intelligently extract keywords from job descriptions
"""

from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION
)
import json

class KeywordExtractor:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
    
    def extract_keywords(self, job_description):
        """
        Extract relevant keywords from job description using GPT-4
        
        Args:
            job_description (str): The job description text
        
        Returns:
            dict: Extracted keywords categorized by type
        """
        
        prompt = f"""Analyze this job description and extract key information in JSON format:

JOB DESCRIPTION:
{job_description}

Extract and return ONLY a JSON object with these fields:
{{
    "skills": ["skill1", "skill2", ...],
    "experience_keywords": ["keyword1", "keyword2", ...],
    "education_keywords": ["keyword1", "keyword2", ...],
    "location_keywords": ["keyword1", "keyword2", ...],
    "availability_keywords": ["keyword1", "keyword2", ...],
    "all_keywords": ["all", "relevant", "keywords", ...]
}}

Rules:
- Extract technical skills, soft skills, tools, technologies
- Include synonyms and related terms (e.g., "Python" → also include "Python developer", "backend")
- Extract experience-related terms (years, level, type)
- Extract education requirements
- Extract location/remote work preferences
- Extract availability needs (part-time, full-time, volunteer hours)
- The "all_keywords" should be a comprehensive list of ALL important terms

Return ONLY valid JSON, no other text."""

        try:
            response = self.client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are a skilled HR assistant that extracts keywords from job descriptions. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            keywords = json.loads(content)
            
            print(f"\n[AI] Extracted {len(keywords.get('all_keywords', []))} keywords from job description")
            
            return keywords
            
        except Exception as e:
            print(f"[ERROR] Keyword extraction failed: {e}")
            # Fallback: basic keyword extraction
            words = job_description.lower().split()
            return {
                "skills": [],
                "experience_keywords": [],
                "education_keywords": [],
                "location_keywords": [],
                "availability_keywords": [],
                "all_keywords": list(set(words))
            }

def test_keyword_extractor():
    """Test the keyword extractor"""
    
    extractor = KeywordExtractor()
    
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
    print(" TESTING KEYWORD EXTRACTOR")
    print("="*80)
    print(f"\nJob Description:\n{job_description}")
    
    keywords = extractor.extract_keywords(job_description)
    
    print("\n" + "="*80)
    print(" EXTRACTED KEYWORDS")
    print("="*80)
    
    print("\nSkills:")
    for skill in keywords.get('skills', []):
        print(f"  - {skill}")
    
    print("\nExperience Keywords:")
    for kw in keywords.get('experience_keywords', []):
        print(f"  - {kw}")
    
    print("\nAll Keywords:")
    print(f"  {', '.join(keywords.get('all_keywords', []))}")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_keyword_extractor()

