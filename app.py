import streamlit as st
import tempfile
import os
from datetime import datetime
from pathlib import Path

# Import backend classes
from backend.job_matcher import JobMatcher
from backend.resume_parser import ResumeParser
from backend.mcq_generator import MCQGenerator

# Import frontend components
from frontend.pages.home import render_home_page

# Page settings
st.set_page_config(
    page_title="AI HR Recruitment Assistant", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'job_title' not in st.session_state:
    st.session_state.job_title = ""
if 'candidates' not in st.session_state:
    st.session_state.candidates = []
if 'job_skills' not in st.session_state:
    st.session_state.job_skills = []

def render_analysis_page():
    """Render the candidate analysis page"""
    st.header("📊 Candidate Analysis")
    
    # Job Description Upload
    st.subheader("1. Upload Job Description")
    job_file = st.file_uploader("Upload Job Description (.txt)", type=['txt'])
    job_title = st.text_input("Job Title (Optional)", placeholder="e.g., Junior AI Engineer")
    
    if job_file:
        job_description = job_file.read().decode('utf-8')
        st.session_state.job_description = job_description
        st.session_state.job_title = job_title
        
        # Show preview
        with st.expander("📝 Job Description Preview"):
            st.text_area("Content", job_description, height=150, disabled=True)
    
    # Resume Upload
    st.subheader("2. Upload Resumes")
    resume_files = st.file_uploader(
        "Upload Resume Files (.pdf, .docx)", 
        type=['pdf', 'docx'], 
        accept_multiple_files=True
    )
    
    if resume_files and st.session_state.job_description:
        if st.button("🔍 Analyze Candidates", type="primary"):
            with st.spinner("Analyzing candidates..."):
                try:
                    # Initialize components
                    job_matcher = JobMatcher()
                    
                    # Save uploaded files temporarily
                    temp_files = []
                    with tempfile.TemporaryDirectory() as temp_dir:
                        for resume_file in resume_files:
                            temp_path = os.path.join(temp_dir, resume_file.name)
                            with open(temp_path, 'wb') as f:
                                f.write(resume_file.getbuffer())
                            temp_files.append(temp_path)
                        
                        # Perform analysis
                        results = job_matcher.match_resumes_to_job(
                            temp_files, 
                            st.session_state.job_description,
                            st.session_state.job_title
                        )
                    
                    if 'error' in results:
                        st.error(f"Error: {results['error']}")
                    else:
                        # Store results in session state
                        st.session_state.candidates = results['candidates']
                        st.session_state.job_skills = results['extracted_skills']
                        
                        # Display results
                        display_analysis_results(results)
                        
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
                    st.error("Please check your files and try again.")
    
    # Display previous results if available
    elif st.session_state.candidates:
        st.info("📋 Showing previous analysis results")
        results = {
            'candidates': st.session_state.candidates,
            'extracted_skills': st.session_state.job_skills,
            'shortlist': st.session_state.candidates[:3],
            'total_candidates': len(st.session_state.candidates)
        }
        display_analysis_results(results)

def display_analysis_results(results):
    """Display the analysis results"""
    st.success("✅ Analysis Complete!")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Candidates", results['total_candidates'])
    with col2:
        st.metric("Skills Identified", len(results['extracted_skills']))
    with col3:
        st.metric("Top Candidate Score", f"{results['candidates'][0]['overall_score']:.1f}/10" if results['candidates'] else "N/A")
    with col4:
        st.metric("Shortlisted", len(results.get('shortlist', [])))
    
    # Display extracted skills - FIXED: Removed type parameter
    st.subheader("🔧 Skills Required")
    if results['extracted_skills']:
        # Create a nice layout for skills using columns
        skills_to_show = results['extracted_skills'][:15]  # Show first 15 skills
        
        # Display skills in a more visual way using containers
        skill_container = st.container()
        with skill_container:
            # Create rows of skills (5 per row)
            for i in range(0, len(skills_to_show), 5):
                cols = st.columns(5)
                for j, skill in enumerate(skills_to_show[i:i+5]):
                    with cols[j]:
                        # Use markdown for better styling instead of st.badge
                        st.markdown(f"""
                        <div style="
                            background-color: #f0f2f6;
                            color: #1f2937;
                            padding: 4px 12px;
                            border-radius: 16px;
                            text-align: center;
                            margin: 2px;
                            font-size: 12px;
                            font-weight: 500;
                            border: 1px solid #e1e5e9;
                        ">
                            {skill}
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.warning("No technical skills detected in job description")
    
    # Display candidates
    st.subheader("👥 Candidate Rankings")
    
    for idx, candidate in enumerate(results['candidates']):
        with st.expander(f"#{idx+1} {candidate['name']} - Score: {candidate['overall_score']:.1f}/10"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Contact Information:**")
                st.write(f"📧 {candidate['email']}")
                st.write(f"📱 {candidate['phone']}")
                st.write(f"📄 {candidate['file_name']}")
                
                st.write("**Experience:**")
                st.write(f"🕐 {candidate['experience_years']} years")
                st.write(f"📊 Level: {candidate['experience_level']}")
                st.write(f"💼 Projects: {candidate['projects_count']}")
            
            with col2:
                st.write("**Skills Matched:**")
                if candidate['skills']:
                    # Display candidate skills using the same styling as job skills
                    skills_to_show = candidate['skills'][:10]  # Show first 10 skills
                    for i in range(0, len(skills_to_show), 3):
                        cols = st.columns(3)
                        for j, skill in enumerate(skills_to_show[i:i+3]):
                            with cols[j]:
                                st.markdown(f"""
                                <div style="
                                    background-color: #e8f5e8;
                                    color: #155724;
                                    padding: 3px 8px;
                                    border-radius: 12px;
                                    text-align: center;
                                    margin: 1px;
                                    font-size: 11px;
                                    font-weight: 500;
                                    border: 1px solid #d4edda;
                                ">
                                    {skill}
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.write("No matching skills found")
                
                st.write("**Scoring Breakdown:**")
                st.write(f"• **Skill Match:** {candidate['skill_match']}/10")
                st.write(f"• **Project Relevance:** {candidate.get('project_relevance', 0):.1f}/10")
                st.write(f"• **Experience Level:** {candidate.get('experience_score', 0):.1f}/10")
                st.write(f"• **Overall Score:** {candidate['overall_score']:.1f}/10")
                
                # Add relevance explanation
                st.write("**Why This Candidate Ranks Here:**")
                relevance_reasons = []
                if candidate['skill_match'] >= 7:
                    relevance_reasons.append("✅ Strong skill alignment with job requirements")
                elif candidate['skill_match'] >= 5:
                    relevance_reasons.append("⚠️ Moderate skill match with room for growth")
                else:
                    relevance_reasons.append("❌ Limited skill match - may need extensive training")
                
                if candidate['experience_years'] >= 3:
                    relevance_reasons.append("✅ Solid experience in relevant field")
                elif candidate['experience_years'] >= 1:
                    relevance_reasons.append("⚠️ Some experience, suitable for junior roles")
                else:
                    relevance_reasons.append("❌ Entry-level candidate - requires mentoring")
                
                if candidate['projects_count'] >= 3:
                    relevance_reasons.append("✅ Demonstrated project delivery capability")
                elif candidate['projects_count'] >= 1:
                    relevance_reasons.append("⚠️ Limited project experience shown")
                else:
                    relevance_reasons.append("❌ No clear project experience mentioned")
                
                for reason in relevance_reasons:
                    st.write(f"  {reason}")
            
            # Show projects if available
            if candidate.get('projects'):
                st.write("**Recent Projects:**")
                for project in candidate['projects'][:3]:
                    st.write(f"• {project}")
    
    # Export option
    st.subheader("📤 Export Results")
    if st.button("Download Results as CSV"):
        csv_data = generate_csv_export(results['candidates'])
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"candidate_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def generate_csv_export(candidates):
    """Generate CSV data for export"""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Rank', 'Name', 'Email', 'Phone', 'Experience_Years', 
        'Experience_Level', 'Projects_Count', 'Skill_Match', 
        'Project_Relevance', 'Overall_Score', 'Skills', 'File_Name'
    ])
    
    # Write data
    for idx, candidate in enumerate(candidates, 1):
        writer.writerow([
            idx,
            candidate['name'],
            candidate['email'],
            candidate['phone'],
            candidate['experience_years'],
            candidate['experience_level'],
            candidate['projects_count'],
            candidate['skill_match'],
            candidate.get('project_relevance', 0),
            candidate['overall_score'],
            '; '.join(candidate['skills']),
            candidate['file_name']
        ])
    
    return output.getvalue()

def render_mcq_generation():
    """Render the MCQ generation page"""
    st.header("❓ MCQ Generation")
    
    if not st.session_state.job_description:
        st.warning("Please upload a job description and analyze candidates first.")
        return
    
    st.subheader("📝 Job Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Job Title:** {st.session_state.job_title or 'Not specified'}")
    with col2:
        st.write(f"**Skills Required:** {len(st.session_state.job_skills)}")
    
    # MCQ Generation Options
    st.subheader("⚙️ MCQ Options")
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.selectbox("Number of Questions", [5, 10, 15, 20], index=1)
    with col2:
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)
    
    if st.button("🎯 Generate MCQs", type="primary"):
        with st.spinner("Generating MCQs..."):
            try:
                mcq_generator = MCQGenerator()
                
                # Generate MCQs with proper parameters
                mcqs = mcq_generator.generate_mcqs(
                    st.session_state.job_description,
                    st.session_state.job_skills,
                    num_questions,
                    difficulty
                )
                
                st.success(f"✅ Generated {len(mcqs)} MCQs!")
                
                # Display MCQs
                for idx, mcq in enumerate(mcqs, 1):
                    with st.expander(f"Question {idx}: {mcq['question'][:50]}..."):
                        st.write(f"**Question:** {mcq['question']}")
                        st.write("**Options:**")
                        for option_idx, option in enumerate(mcq['options'], 1):
                            prefix = "✅" if option_idx == mcq['correct_answer'] else "  "
                            st.write(f"{prefix} {chr(64+option_idx)}. {option}")
                        st.write(f"**Explanation:** {mcq.get('explanation', 'No explanation provided')}")
                
                # Export MCQs
                if st.button("📥 Download MCQs"):
                    mcq_text = format_mcqs_for_export(mcqs)
                    st.download_button(
                        label="Download MCQs as Text",
                        data=mcq_text,
                        file_name=f"mcqs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"Error generating MCQs: {str(e)}")

def format_mcqs_for_export(mcqs):
    """Format MCQs for text export"""
    output = []
    output.append("INTERVIEW QUESTIONS")
    output.append("=" * 50)
    output.append("")
    
    for idx, mcq in enumerate(mcqs, 1):
        output.append(f"Question {idx}: {mcq['question']}")
        output.append("")
        for option_idx, option in enumerate(mcq['options'], 1):
            output.append(f"{chr(64+option_idx)}. {option}")
        output.append("")
        output.append(f"Correct Answer: {chr(64+mcq['correct_answer'])}")
        if mcq.get('explanation'):
            output.append(f"Explanation: {mcq['explanation']}")
        output.append("")
        output.append("-" * 30)
        output.append("")
    
    return "\n".join(output)

# Main App
def main():
    # Sidebar Navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio("Select Page", ["🏠 Home", "📊 Candidate Analysis", "❓ Generate MCQs"])
    
    # App Title
    st.title("🤖 AI HR Recruitment Assistant")
    st.markdown(f"#### 🕒 Today is: `{datetime.today().strftime('%A, %d %B %Y')}`")
    
    # Route Pages
    if page == "🏠 Home":
        render_home_page()
    elif page == "📊 Candidate Analysis":
        render_analysis_page()
    elif page == "❓ Generate MCQs":
        render_mcq_generation()
    
    # Footer
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit | © 2025 AI HR Assistant")

if __name__ == "__main__":
    main()