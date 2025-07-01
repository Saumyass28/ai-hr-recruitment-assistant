from dataclasses import dataclass, field
from typing import List

@dataclass
class ContactInfo:
    email: str = ""
    phone: str = ""

@dataclass
class Candidate:
    name: str
    contact_info: ContactInfo
    skills: List[str]
    experience_years: int
    projects: List[str]
    raw_text: str
    file_name: str = ""

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.contact_info.email,
            'phone': self.contact_info.phone,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'projects_count': len(self.projects),
            'file_name': self.file_name
        }

@dataclass
class JobRequirements:
    title: str
    description: str
    required_skills: List[str]
    min_experience: int

@dataclass
class CandidateScore:
    overall_score: float
    skill_match: float
    project_depth: float
    experience_level: str

    def to_dict(self):
        return {
            'overall_score': round(self.overall_score, 2),
            'skill_match': round(self.skill_match, 2),
            'project_depth': round(self.project_depth, 2),
            'experience_level': self.experience_level
        }

@dataclass
class MCQQuestion:
    question: str
    options: List[str]
    correct: int
    difficulty: str
    skill: str = ""
    explanation: str = ""
