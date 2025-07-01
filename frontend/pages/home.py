import streamlit as st

def render_home_page():
    """Render the home page"""
    st.title("🏠 Home")
    st.write("Welcome to the AI HR Assistant! Upload a job description and resumes to get started.")
    
    # Add some helpful information
    st.markdown("""
    ### How to use this application:
    
    1. **Upload Job Description**: Start by uploading a job description file (.txt format)
    2. **Upload Resumes**: Upload multiple resume files (.pdf or .docx format)
    3. **Get Analysis**: The system will analyze and rank candidates based on:
       - Skill matching with job requirements
       - Project relevance and experience
       - Overall candidate fit
    4. **Generate MCQs**: Create interview questions based on the job requirements
    
    ### Features:
    - ✅ Smart resume parsing and skill extraction
    - ✅ Project-based relevance scoring
    - ✅ Comprehensive candidate ranking
    - ✅ Automated MCQ generation
    - ✅ Export results to CSV
    
    **Navigate using the sidebar to get started!**
    """)
    
    # Add some statistics or tips
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Supported Resume Formats", "PDF, DOCX")
    
    with col2:
        st.metric("Job Description Format", "TXT")
    
    with col3:
        st.metric("Max File Size", "200MB")

# Make this function available for import
if __name__ == "__main__":
    render_home_page()