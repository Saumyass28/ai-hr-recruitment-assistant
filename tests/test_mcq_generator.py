from backend.mcq_generator import MCQGenerator

def test_mcq_generator():
    gen = MCQGenerator()
    mcqs = gen.generate_mcqs(["python"])
    assert len(mcqs) > 0
    assert mcqs[0].question.startswith("What is")
