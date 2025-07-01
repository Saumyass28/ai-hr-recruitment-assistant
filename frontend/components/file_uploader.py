import streamlit as st

def upload_job_and_resumes():
    jd_file = st.file_uploader("📄 Upload Job Description", type=["pdf", "txt", "docx"])
    resumes = st.file_uploader("📑 Upload Resumes", type=["pdf"], accept_multiple_files=True)
    return jd_file, resumes
