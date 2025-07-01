# ✅ FINAL frontend/pages/analysis.py (Intelligent Resume Ranking + JD Upload)

import streamlit as st
import pandas as pd
import os
from backend.resume_parser import ResumeParser
from backend.job_matcher import JobMatcher
from config.settings import EXPORT_DIR
import re

parser = ResumeParser()
matcher = JobMatcher()

def render_analysis_page():
    st.subheader("📄 Upload Job Description (.txt)")
    jd_file = st.file_uploader("📂 Upload Job Description File", type=['txt'])

    if jd_file:
        jd_text = jd_file.read().decode("utf-8")
        st.text_area("📋 Job Description Preview", jd_text, height=180)

        # Extract job and skills
        job_skills = matcher.extract_skills_from_job_description(jd_text, job_title="AI Engineer")
        st.session_state['job_skills'] = job_skills

        st.markdown("### 📌 Extracted Skills:")
        if job_skills:
            # Create container for skill badges
            skill_container = st.container()
            with skill_container:
                # Display all skills in a fluid layout
                skills_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;'>"
                for skill in job_skills[:15]:
                    skills_html += f"""
                    <span style='
                        background-color: #f0f2f6;
                        padding: 4px 12px;
                        border-radius: 16px;
                        font-size: 12px;
                        border: 1px solid #e1e5e9;
                    '>
                        {skill}
                    </span>
                    """
                skills_html += "</div>"
                st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No relevant skills found. Include keywords like Python, SQL, Flask, etc.")

        resume_files = st.file_uploader("📂 Upload Candidate Resumes (PDF/DOCX)", accept_multiple_files=True)

        if resume_files:
            candidates = []
            for f in resume_files:
                candidate = parser.parse_resume(f.read(), f.name)
                if candidate:
                    candidates.append(candidate)

            if not candidates:
                st.error("❌ No valid resumes parsed.")
                return

            # Calculate project relevance
            for candidate in candidates:
                projects = candidate.get('projects', [])
                candidate['project_relevance'] = matcher.calculate_project_relevance(projects, job_skills)
                
                # Calculate overall score
                candidate['overall_score'] = matcher.calculate_overall_score(candidate)

            # Rank candidates
            ranked_candidates = matcher.rank_candidates(candidates)
            df = pd.DataFrame(ranked_candidates).sort_values(by="overall_score", ascending=False)

            st.markdown("## 🧠 Candidate Analysis Result")
            st.dataframe(df, use_container_width=True)

            # Save results
            out_path = EXPORT_DIR / "shortlist.csv"
            df.to_csv(out_path, index=False)
            st.success(f"✅ Shortlist saved to `{out_path.name}`")

            # Show top candidate details
            if not df.empty:
                top_candidate = df.iloc[0].to_dict()
                st.subheader(f"🏆 Top Candidate: {top_candidate['name']}")
                
                st.write(f"**Project Relevance Score:** {top_candidate.get('project_relevance', 0):.1f}/10")
                
                # Show their best project
                if 'projects' in top_candidate and top_candidate['projects']:
                    # Find the project with maximum length (as proxy for detail)
                    best_project = max(top_candidate['projects'], key=len)
                    with st.expander("🌟 Best Project Implementation"):
                        st.write(best_project)
                
                # Show score comparison
                st.subheader("📊 Score Comparison")
                chart_data = df[['name', 'overall_score', 'project_relevance', 'skill_match']].set_index('name')
                st.bar_chart(chart_data)
        else:
            st.info("⬆️ Please upload resumes to proceed.")