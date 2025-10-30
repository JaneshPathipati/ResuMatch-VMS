"""
Resume Parser - Extract data from PDF and DOCX resumes
Extracts: Name, Email, Phone, Skills, Experience, Education
"""

import re
import PyPDF2
import docx
from io import BytesIO

class ResumeParser:
    def __init__(self):
        # Common skills keywords
        self.skills_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'django', 'flask', 'spring', 'sql', 'mysql', 'postgresql', 'mongodb',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'html', 'css',
            'php', 'ruby', 'go', 'rust', 'c++', 'c#', 'swift', 'kotlin',
            'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch',
            'testing', 'qa', 'agile', 'scrum', 'devops', 'ci/cd', 'jenkins',
            'wordpress', 'graphic design', 'ui/ux', 'figma', 'photoshop',
            'digital marketing', 'seo', 'content writing', 'project management'
        ]
    
    def extract_text_from_pdf(self, file_content):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_content):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def extract_email(self, text):
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def extract_phone(self, text):
        """Extract phone number from text"""
        # Match various phone formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-234-567-8900
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (234) 567-8900
            r'\d{10}',  # 2345678900
            r'\+?\d{1,3}\s?\d{10}',  # +91 1234567890
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return ""
    
    def extract_name(self, text):
        """Extract name from resume (usually first line or after specific headers)"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) > 3 and len(line) < 50:
                # Skip lines with email or phone
                if '@' not in line and not re.search(r'\d{3}[-.\s]?\d{3}', line):
                    # Check if it looks like a name (2-4 words, mostly alphabetic)
                    words = line.split()
                    if 1 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                        return line
        return "Unknown"
    
    def extract_skills(self, text):
        """Extract skills from resume"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skills_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        # Also look for skills section
        skills_section_pattern = r'(?:skills?|technical skills?|expertise|technologies)[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)'
        skills_match = re.search(skills_section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if skills_match:
            skills_text = skills_match.group(1)
            # Extract comma-separated or bullet-pointed skills
            additional_skills = re.findall(r'[•\-\*]?\s*([A-Za-z0-9+#.\s]{2,30})(?:[,\n]|$)', skills_text)
            found_skills.extend([s.strip() for s in additional_skills if len(s.strip()) > 2])
        
        # Remove duplicates and return
        return ', '.join(list(dict.fromkeys(found_skills))[:15])  # Limit to 15 skills
    
    def extract_experience(self, text):
        """Extract experience summary"""
        # Look for experience section
        exp_pattern = r'(?:experience|work experience|employment)[:\s]+(.*?)(?=\n\n[A-Z]|education|skills|$)'
        exp_match = re.search(exp_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if exp_match:
            exp_text = exp_match.group(1).strip()
            # Limit to first 500 characters
            return exp_text[:500] if exp_text else "Not specified"
        
        # Try to find years of experience
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_match = re.search(years_pattern, text, re.IGNORECASE)
        
        if years_match:
            return f"{years_match.group(1)} years of experience"
        
        return "Not specified"
    
    def extract_education(self, text):
        """Extract education information"""
        # Look for education section first
        edu_section_pattern = r'(?:education|academic|qualification)[:\s]+(.*?)(?=\n\n|certification|language|reference|$)'
        edu_match = re.search(edu_section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if edu_match:
            edu_text = edu_match.group(1).strip()
            # Clean up and limit
            edu_lines = [line.strip() for line in edu_text.split('\n') if line.strip()][:3]
            return ' | '.join(edu_lines) if edu_lines else "Not specified"
        
        # Fallback: Look for degree keywords
        degree_pattern = r'(?:bachelor|master|phd|doctorate|mba|b\.?tech|m\.?tech|b\.?sc|m\.?sc|b\.?e|m\.?e).*?(?=\n|$)'
        degree_match = re.search(degree_pattern, text, re.IGNORECASE)
        
        if degree_match:
            return degree_match.group(0).strip()[:200]
        
        return "Not specified"
    
    def parse_resume(self, file_content, filename):
        """
        Main function to parse resume and extract all information
        
        Args:
            file_content: Binary content of the file
            filename: Name of the file
        
        Returns:
            Dictionary with extracted volunteer data
        """
        # Extract text based on file type
        if filename.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(file_content)
        elif filename.lower().endswith(('.docx', '.doc')):
            text = self.extract_text_from_docx(file_content)
        else:
            return None
        
        if not text:
            return None
        
        # Extract all fields
        volunteer_data = {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text),
            'education': self.extract_education(text),
            'availability': 'Not specified',
            'languages': 'Not specified',
            'certifications': 'Not specified',
            'interests': 'Not specified'
        }
        
        return volunteer_data

