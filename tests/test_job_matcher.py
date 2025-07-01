from backend.job_matcher import JobMatcher
from backend.data_models import Candidate, JobRequirements, ContactInfo

def test_candidate_scoring():
    matcher = JobMatcher()
    job = JobRequirements(
        title="ML Engineer",
        description="Python, ML, APIs",
        required_skills=["python", "ml", "api"],
        min_experience=1
    )
    candidate = Candidate(
        name="Alice",
        contact_info=ContactInfo(email="a@a.com", phone="123456"),
        skills=["python", "ml"],
        experience_years=2,
        projects=["Built ML model", "Developed API"],
        raw_text="Some text"
    )
    score = matcher.score_candidate(candidate, job)
    assert score.overall_score > 0