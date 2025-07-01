import re
from typing import List, Dict, Any
from backend.resume_parser import ResumeParser

class JobMatcher:
    def __init__(self):
        self.resume_parser = ResumeParser()
        
    def extract_skills_from_job_description(self, job_description: str, job_title: str = None) -> List[str]:
        """Extract skills from job description with enhanced matching"""
        if not job_description or not job_description.strip():
            return []
            
        skill_keywords = [
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
            'bootstrap', 'tailwind', 'sass', 'webpack', 'npm', 'yarn', 'vite',
            'rest api', 'restful', 'oauth', 'jwt', 'authentication', 'authorization'
        ]
        
        # Add job-title specific skills if provided
        if job_title:
            job_title_lower = job_title.lower()
            if 'ai' in job_title_lower or 'artificial intelligence' in job_title_lower:
                skill_keywords.extend(['ai', 'artificial intelligence', 'nlp', 'computer vision', 'deep learning'])
            elif 'data' in job_title_lower:
                skill_keywords.extend(['pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'r'])
            elif 'devops' in job_title_lower:
                skill_keywords.extend(['ci/cd', 'monitoring', 'logging', 'infrastructure'])
        
        extracted_skills = []
        job_text_lower = job_description.lower()
        
        for skill in skill_keywords:
            # Use word boundary regex for better matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, job_text_lower):
                extracted_skills.append(skill)
        
        return list(set(extracted_skills))  # Remove duplicates

    def calculate_project_depth(self, project_text: str, job_skills: List[str]) -> float:
        """Calculate project depth score based on implementation evidence"""
        score = 0
        project_lower = project_text.lower()
        
        # Implementation complexity (technical verbs)
        tech_verbs = ["developed", "built", "engineered", "implemented", "optimized", "designed", "architected"]
        for verb in tech_verbs:
            if verb in project_lower:
                score += 1
        
        # Technical specificity (mentions of frameworks/libraries)
        if any(word in project_lower for word in ["using", "with", "utilizing", "via"]):
            score += 2
        
        # Quantifiable results
        if re.search(r'\d+%|\$\d+|\d+x', project_text):
            score += 3
        
        # Skill relevance
        for skill in job_skills:
            if skill.lower() in project_lower:
                score += 2
        
        return min(score, 10)  # Cap at 10
    
    def calculate_project_relevance(self, projects: List[str], job_skills: List[str]) -> float:
        """Calculate how relevant candidate's projects are to job requirements"""
        if not projects or not job_skills:
            return 0.0
        
        total_score = 0
        for project in projects:
            total_score += self.calculate_project_depth(project, job_skills)
        
        # Normalize and weight recent projects higher
        return min(total_score / len(projects) * 2, 10)  # Scale to 10
    
    def calculate_overall_score(self, candidate: Dict[str, Any]) -> float:
        """Calculate weighted overall score prioritizing project relevance"""
        # New weights prioritizing project implementation
        PROJECT_WEIGHT = 0.6  # 60% weight to projects
        SKILL_WEIGHT = 0.3    # 30% to skills
        EXP_WEIGHT = 0.1      # 10% to experience
        
        skill_score = candidate.get('skill_match', 0)
        project_score = candidate.get('project_relevance', 0)
        experience_score = min(candidate.get('experience_years', 0), 10)  # Cap at 10
        
        overall_score = (
            (skill_score * SKILL_WEIGHT) +
            (project_score * PROJECT_WEIGHT) +
            (experience_score * EXP_WEIGHT)
        )
        
        return round(overall_score, 1)
    
    def rank_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank candidates with improved multi-criteria sorting"""
        # Calculate overall scores
        for candidate in candidates:
            candidate['overall_score'] = self.calculate_overall_score(candidate)
        
        # Multi-level sorting
        sorted_candidates = sorted(candidates, key=lambda x: (
            -x['overall_score'],           # Primary: Overall score (descending)
            -x.get('project_relevance', 0), # Secondary: Project relevance (descending)
            -x['skill_match'],             # Tertiary: Skill match (descending)
            -x['experience_years']         # Quaternary: Experience (descending)
        ))
        
        return sorted_candidates
    
    def match_resumes_to_job(self, resume_files: List[str], job_description: str, job_title: str = None) -> Dict[str, Any]:
        """Main function to match resumes to job description"""
        try:
            # Validate inputs
            if not job_description or not job_description.strip():
                return {
                    'error': 'Job description is required',
                    'extracted_skills': [],
                    'candidates': [],
                    'shortlist': []
                }
            
            if not resume_files:
                return {
                    'error': 'At least one resume file is required',
                    'extracted_skills': [],
                    'candidates': [],
                    'shortlist': []
                }
            
            # Extract skills from job description
            job_skills = self.extract_skills_from_job_description(job_description, job_title)
            
            if not job_skills:
                print("Warning: No technical skills detected in job description")
            
            # Parse all resumes with job-specific skills
            candidates = self.resume_parser.parse_multiple_resumes(resume_files, job_skills)
            
            # Filter out candidates that could not be parsed
            valid_candidates = [c for c in candidates if c.get('raw_text') != 'Failed to parse resume']
            
            if not valid_candidates:
                return {
                    'error': 'No resumes could be parsed successfully',
                    'extracted_skills': job_skills,
                    'candidates': [],
                    'shortlist': []
                }
            
            # Calculate project relevance for each candidate
            for candidate in valid_candidates:
                projects = candidate.get('projects', [])
                candidate['project_relevance'] = self.calculate_project_relevance(projects, job_skills)
                candidate['overall_score'] = self.calculate_overall_score(candidate)
            
            # Rank candidates
            ranked_candidates = self.rank_candidates(valid_candidates)
            
            # Create shortlist (top 3 candidates)
            shortlist = ranked_candidates[:3]
            
            return {
                'extracted_skills': job_skills,
                'candidates': ranked_candidates,
                'shortlist': shortlist,
                'total_candidates': len(ranked_candidates),
                'skills_found': len(job_skills),
                'job_description_length': len(job_description.split()),
                'job_title': job_title or 'Not specified'
            }
            
        except Exception as e:
            print(f"Error in job matching: {e}")
            return {
                'error': f'Error processing job matching: {str(e)}',
                'extracted_skills': [],
                'candidates': [],
                'shortlist': []
            }
    
    def get_candidate_analysis(self, candidate: Dict[str, Any], job_skills: List[str]) -> Dict[str, Any]:
        """Get detailed analysis for a specific candidate"""
        matched_skills = candidate.get('skills', [])
        missing_skills = [skill for skill in job_skills if skill not in matched_skills]
        
        skill_match_percentage = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
        
        # Determine candidate recommendation based on overall score
        overall_score = candidate.get('overall_score', 0)
        if overall_score >= 8:
            recommendation = "Highly Recommended"
        elif overall_score >= 6:
            recommendation = "Recommended"
        elif overall_score >= 4:
            recommendation = "Consider with Caution"
        else:
            recommendation = "Not Recommended"
        
        return {
            'candidate': candidate,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'skill_match_percentage': round(skill_match_percentage, 1),
            'recommendation': recommendation,
            'strengths': self._identify_strengths(candidate),
            'areas_for_improvement': missing_skills[:5],  # Top 5 missing skills
            'project_summary': self._get_project_summary(candidate)
        }
    
    def _identify_strengths(self, candidate: Dict[str, Any]) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        
        # Experience-based strengths
        if candidate['experience_years'] >= 5:
            strengths.append("Extensive experience")
        elif candidate['experience_years'] >= 2:
            strengths.append("Good experience level")
        
        # Project-based strengths
        project_score = candidate.get('project_relevance', 0)
        if project_score >= 8:
            strengths.append("Strong project portfolio")
        elif project_score >= 5:
            strengths.append("Decent project experience")
        
        # Skill-based strengths
        if candidate['skill_match'] >= 10:
            strengths.append("Excellent skill alignment")
        elif candidate['skill_match'] >= 5:
            strengths.append("Good skill match")
        
        # Overall performance
        overall_score = candidate.get('overall_score', 0)
        if overall_score >= 8:
            strengths.append("Top performer")
        elif overall_score >= 6:
            strengths.append("Strong candidate")
        
        if not strengths:
            strengths.append("Entry-level candidate with potential")
        
        return strengths
    
    def _get_project_summary(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Get summary of candidate's project experience"""
        projects = candidate.get('projects', [])
        
        return {
            'total_projects': len(projects),
            'detailed_projects': len([p for p in projects if len(p) > 50]),
            'project_relevance_score': candidate.get('project_relevance', 0),
            'has_recent_projects': len(projects) > 0
        }
    
    def calculate_skill_gap(self, candidate: Dict[str, Any], job_skills: List[str]) -> Dict[str, Any]:
        """Calculate skill gap analysis for a candidate"""
        candidate_skills = set(skill.lower() for skill in candidate.get('skills', []))
        job_skills_set = set(skill.lower() for skill in job_skills)
        
        matched_skills = candidate_skills.intersection(job_skills_set)
        missing_skills = job_skills_set - candidate_skills
        
        skill_coverage = len(matched_skills) / len(job_skills_set) * 100 if job_skills_set else 0
        
        return {
            'skill_coverage_percentage': round(skill_coverage, 1),
            'matched_skills_count': len(matched_skills),
            'missing_skills_count': len(missing_skills),
            'critical_missing_skills': list(missing_skills)[:3],  # Top 3 missing
            'skill_gap_severity': 'Low' if skill_coverage >= 80 else 'Medium' if skill_coverage >= 60 else 'High'
        }