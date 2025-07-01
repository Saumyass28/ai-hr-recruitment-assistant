# 🤖 AI HR Recruitment Assistant

An intelligent recruitment tool that analyzes resumes based on project relevance and skills—not just years of experience—and automatically generates MCQs based on the job description.

---

## 🚀 Features

✅ Upload Job Descriptions (`.txt`)  
✅ Upload Resumes (`.pdf`, `.docx`)  
✅ Extracts Skills, Projects, and Experience from each candidate  
✅ Smart Ranking based on:
- ✅ Skill Match (semantic matching using embeddings)
- ✅ Project Depth (technical indicators, keywords)
- ✅ Experience (weighted lesser than practical impact)

✅ Auto-generates MCQs based on required skills  
✅ Exports Shortlist as `.csv`  
✅ Built with love using GenAI logic and Streamlit 💡

---

## 🧠 How It Works

1. **Resume Parser**: Extracts name, contact info, skills, projects, and experience.
2. **Job Matcher**: Calculates skill match using Sentence Transformers and assigns a weighted score to each candidate.
3. **Project Depth**: Measures how deeply a candidate implemented key skills.
4. **MCQ Generator**: Creates questions from a skill-wise question bank for live candidate screening.

---

## 🛠️ Tech Stack

| Layer              | Tools Used                           |
|-------------------|---------------------------------------|
| Frontend           | Streamlit                            |
| Resume Parsing     | spaCy, PyMuPDF, python-docx           |
| Intelligence Scoring | sentence-transformers (MiniLM-L6-v2) |
| MCQ Engine         | Python (custom logic)                |
| Data Export        | Pandas, CSV                          |

---

## 🖼️ Sample Screens

| Job Upload | Resume Ranking | MCQ Generator |
|------------|----------------|---------------|
| ✅ Upload `.txt` JD | ✅ Top 10 candidates sorted | ✅ 5 smart MCQs auto generated |

---

## 🧪 How to Run

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
