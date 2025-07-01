# frontend/pages/mcq_generation.py

import streamlit as st
from backend.mcq_generator import MCQGenerator

def render_mcq_generation(job=None):
    st.markdown("## 📚 Generated MCQs")

    if not job or not job.required_skills:
        st.warning("⚠️ No skills found. Please analyze a job description first.")
        return

    st.markdown("⚙️ Generating MCQs for skills:")
    st.code(job.required_skills)

    mcq_gen = MCQGenerator()
    questions = mcq_gen.generate_mcqs(job.required_skills)

    if not questions:
        st.error("❌ No MCQs could be generated. Try with different or more common skills.")
        return

    for q in questions:
        st.markdown(f"**Q{q['id']}: {q['question']}**")
        for i, option in enumerate(q['options']):
            st.markdown(f"- ({chr(65+i)}) {option}")
        st.markdown(f"✅ Correct: **{q['options'][q['correct']]}**  \n📌 Category: {q.get('category', 'General')}")
        st.markdown("---")
