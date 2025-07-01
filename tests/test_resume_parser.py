from backend.resume_parser import ResumeParser

def test_resume_parsing():
    parser = ResumeParser()
    with open("data/sample_resumes/sample_resume_1.pdf", "rb") as f:
        result = parser.parse_resume(f.read(), "sample_resume_1.pdf")
        assert result is not None
        assert result.name != "Unknown"
        assert len(result.skills) > 0