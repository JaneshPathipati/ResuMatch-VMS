import re
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ResumeMatcher:
    """
    Resume matching and parsing engine for volunteer shortlisting
    Uses TF-IDF and cosine similarity for matching volunteers to job descriptions
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not text or text == 'nan':
            return ""
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\s+#.,]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_keywords(self, text):
        """Extract important keywords from text"""
        if not text:
            return []
        
        # Common tech skills and keywords
        keywords = []
        text_lower = text.lower()
        
        # Programming languages
        prog_langs = ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 
                     'swift', 'kotlin', 'go', 'rust', 'typescript', 'sql', 'r']
        
        # Frameworks and tools
        frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'spring', 
                     'node.js', 'express', 'fastapi', 'tensorflow', 'pytorch']
        
        # Soft skills
        soft_skills = ['leadership', 'communication', 'teamwork', 'problem solving',
                      'analytical', 'creative', 'organized', 'detail-oriented']
        
        # Check for matches
        all_terms = prog_langs + frameworks + soft_skills
        for term in all_terms:
            if term in text_lower:
                keywords.append(term)
        
        return keywords
    
    def create_volunteer_profile(self, volunteer):
        """Create a comprehensive text profile from volunteer data"""
        profile_parts = []
        
        fields = ['skills', 'experience', 'education', 'certifications', 
                 'interests', 'languages']
        
        for field in fields:
            value = volunteer.get(field, '')
            if value and value != 'nan':
                profile_parts.append(str(value))
        
        profile = ' '.join(profile_parts)
        return self.preprocess_text(profile)
    
    def match_volunteers(self, volunteers: List[Dict], job_description: str, 
                        top_n: int = 10) -> List[Tuple[Dict, float, List[str]]]:
        """
        Match volunteers to job description using TF-IDF and cosine similarity
        
        Args:
            volunteers: List of volunteer dictionaries
            job_description: Job description text
            top_n: Number of top matches to return
        
        Returns:
            List of tuples (volunteer, match_score, matching_skills)
        """
        if not volunteers:
            return []
        
        # Preprocess job description
        job_desc_clean = self.preprocess_text(job_description)
        
        # Create volunteer profiles
        volunteer_profiles = []
        for volunteer in volunteers:
            profile = self.create_volunteer_profile(volunteer)
            volunteer_profiles.append(profile)
        
        # Create TF-IDF matrix
        all_texts = [job_desc_clean] + volunteer_profiles
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # Calculate cosine similarity
            job_vector = tfidf_matrix[0:1]
            volunteer_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(job_vector, volunteer_vectors)[0]
            
            # Get matching keywords for each volunteer
            results = []
            for idx, (volunteer, score) in enumerate(zip(volunteers, similarities)):
                volunteer_profile = volunteer_profiles[idx]
                matching_skills = self.find_matching_skills(
                    job_desc_clean, 
                    volunteer_profile, 
                    volunteer
                )
                results.append((volunteer, float(score), matching_skills))
            
            # Sort by score and return top N
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_n]
            
        except Exception as e:
            print(f"Error in matching: {e}")
            # Fallback to simple keyword matching
            return self.simple_keyword_match(volunteers, job_description, top_n)
    
    def find_matching_skills(self, job_desc, volunteer_profile, volunteer):
        """Find skills that match between job description and volunteer"""
        job_keywords = set(self.extract_keywords(job_desc))
        
        # Extract from volunteer's skills field
        volunteer_skills_text = str(volunteer.get('skills', ''))
        volunteer_keywords = set(self.extract_keywords(volunteer_skills_text))
        
        # Find intersection
        matching = list(job_keywords.intersection(volunteer_keywords))
        
        # If no exact matches, find partial matches
        if not matching:
            job_words = set(job_desc.split())
            volunteer_words = set(volunteer_profile.split())
            common_words = job_words.intersection(volunteer_words)
            # Filter out very common words
            matching = [w for w in common_words if len(w) > 3][:5]
        
        return matching[:10]  # Return top 10 matching skills
    
    def simple_keyword_match(self, volunteers, job_description, top_n):
        """Fallback simple keyword matching"""
        job_keywords = set(self.extract_keywords(job_description))
        
        results = []
        for volunteer in volunteers:
            profile = self.create_volunteer_profile(volunteer)
            volunteer_keywords = set(self.extract_keywords(profile))
            
            # Count matching keywords
            matching = list(job_keywords.intersection(volunteer_keywords))
            score = len(matching) / max(len(job_keywords), 1)
            
            results.append((volunteer, score, matching))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]
    
    def shortlist_volunteers(self, volunteers: List[Dict], job_description: str,
                           min_score: float = 0.1, max_results: int = 10) -> List[Dict]:
        """
        Shortlist volunteers based on job description
        
        Returns:
            List of dictionaries with volunteer info, match score, and matching skills
        """
        matches = self.match_volunteers(volunteers, job_description, max_results)
        
        shortlisted = []
        for volunteer, score, matching_skills in matches:
            if score >= min_score:
                shortlisted.append({
                    'volunteer': volunteer,
                    'match_score': round(score * 100, 2),  # Convert to percentage
                    'matching_skills': matching_skills
                })
        
        return shortlisted

