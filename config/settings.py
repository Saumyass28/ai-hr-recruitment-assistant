from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Model and File Config
SENTENCE_MODEL = 'all-MiniLM-L6-v2'
SPACY_MODEL = 'en_core_web_sm'

# File Upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = ['pdf', 'docx', 'txt']

# Scoring Weights
SCORING_WEIGHTS = {
    'skill_match': 0.4,
    'project_depth': 0.5,
    'experience_factor': 0.1
}

# Experience Thresholds (years)
EXPERIENCE_THRESHOLDS = {
    'beginner': 2,
    'intermediate': 5
}

# Output
EXPORT_DIR = BASE_DIR / 'exports'
EXPORT_DIR.mkdir(exist_ok=True)

SHORTLIST_THRESHOLD = 60