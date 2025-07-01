import re
import json
from typing import List, Dict, Any
import PyPDF2
import docx
from pathlib import Path

class ResumeParser:
    def __init__(self):
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb', 
            'html', 'css', 'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'machine learning', 'data science', 'tensorflow', 'pytorch', 'flask',
            'django', 'express', 'angular', 'vue', 'typescript', 'c++', 'c#',
            'php', 'ruby', 'go', 'rust', 'scala', 'kotlin', 'swift', 'mysql',
            'postgresql', 'redis', 'elasticsearch', 'jenkins', 'terraform',
            'ansible', 'linux', 'unix', 'bash', 'powershell', 'api', 'rest',
            'graphql', 'microservices', 'devops', 'ci/cd', 'agile', 'scrum',
            'springboot', 'spring', 'hibernate', 'jpa', 'maven', 'gradle',
            'junit', 'mockito', 'selenium', 'postman', 'swagger', 'json',
            'xml', 'yaml', 'nosql', 'firebase', 'heroku', 'netlify', 'vercel',
            'bootstrap', 'tailwind', 'sass', 'webpack', 'npm', 'yarn', 'vite'
        ]
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text based on file extension"""
        file_ext = Path(file_path).suffix.lower()
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            return self.extract_text_from_docx(file_path)
        else:
            return ""
    
    def extract_email(self, text: str) -> str:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "Not provided"
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        phone_patterns = [
            r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            r'\+?[0-9]{1,4}[-.\s]?[0-9]{10}',
            r'[0-9]{10}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0].strip()
        return "Not provided"
    
    def extract_skills_from_text(self, text: str, job_skills: List[str] = None) -> List[str]:
        """Extract skills from text with improved matching"""
        extracted_skills = []
        text_lower = text.lower()
        
        # Use job skills if provided, otherwise use default skill keywords
        skills_to_check = job_skills if job_skills else self.skill_keywords
        
        for skill in skills_to_check:
            # Use word boundary regex for better matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.append(skill)
        
        return list(set(extracted_skills))  # Remove duplicates
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        experience_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*(?:years?|yrs?)',
            r'experience\s*:?\s*(\d+)\s*(?:years?|yrs?)',
        ]
        
        years = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(match) for match in matches])
        
        return max(years) if years else 0
    
    def extract_projects(self, text: str) -> List[str]:
        """Extract project information from resume"""
        projects = []
        project_keywords = ['project', 'built', 'developed', 'created', 'implemented', 'designed']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in project_keywords):
                if len(line.strip()) > 20:  # Meaningful project descriptions
                    projects.append(line.strip())
        
        return projects[:5]  # Return top 5 projects
    
    def count_projects(self, text: str) -> int:
        """Count project mentions in resume"""
        project_keywords = [
            'project', 'developed', 'built', 'created', 'implemented', 
            'designed', 'developed', 'programmed', 'coded', 'engineered'
        ]
        
        text_lower = text.lower()
        project_count = 0
        
        for keyword in project_keywords:
            # Count occurrences of each keyword
            matches = len(re.findall(r'\b' + keyword + r'\b', text_lower))
            project_count += matches
        
        # Cap at reasonable number to avoid inflated scores
        return min(project_count, 15)
    
    def parse_resume(self, file_path: str, job_skills: List[str] = None) -> Dict[str, Any]:
        """Parse resume and extract all relevant information"""
        try:
            # Extract text from file
            text = self.extract_text(file_path)
            if not text:
                return self._create_empty_candidate(file_path)
            
            # Extract candidate information
            filename = Path(file_path).stem
            candidate_name = filename.replace('_', ' ').replace('-', ' ').title()
            
            # Extract skills (with job-specific skills if provided)
            skills = self.extract_skills_from_text(text, job_skills)
            
            # Extract projects
            projects = self.extract_projects(text)
            
            # Calculate metrics
            experience_years = self.extract_experience_years(text)
            project_count = self.count_projects(text)
            
            # Determine experience level
            if experience_years == 0:
                experience_level = 'Fresher'
            elif experience_years <= 2:
                experience_level = 'Beginner'
            elif experience_years <= 5:
                experience_level = 'Intermediate'
            else:
                experience_level = 'Expert'
            
            return {
                'name': candidate_name,
                'email': self.extract_email(text),
                'phone': self.extract_phone(text),
                'skills': skills,
                'projects': projects,  # Added projects list
                'experience_years': experience_years,
                'projects_count': min(project_count, 10),
                'file_name': Path(file_path).name,
                'skill_match': len(skills),
                'project_depth': min(project_count * 2, 10),
                'experience_level': experience_level,
                'raw_text': text[:500] + "..." if len(text) > 500 else text  # Store snippet for debugging
            }
            
        except Exception as e:
            print(f"Error parsing resume {file_path}: {e}")
            return self._create_empty_candidate(file_path)
    
    def _create_empty_candidate(self, file_path: str) -> Dict[str, Any]:
        """Create empty candidate data structure for failed parsing"""
        filename = Path(file_path).stem
        return {
            'name': filename.replace('_', ' ').replace('-', ' ').title(),
            'email': 'Not provided',
            'phone': 'Not provided',
            'skills': [],
            'projects': [],  # Added empty projects list
            'experience_years': 0,
            'projects_count': 0,
            'file_name': Path(file_path).name,
            'skill_match': 0,
            'project_depth': 0,
            'experience_level': 'Fresher',
            'raw_text': 'Failed to parse resume'
        }
    
    def parse_multiple_resumes(self, file_paths: List[str], job_skills: List[str] = None) -> List[Dict[str, Any]]:
        """Parse multiple resumes"""
        candidates = []
        for file_path in file_paths:
            candidate = self.parse_resume(file_path, job_skills)
            candidates.append(candidate)
        return candidates