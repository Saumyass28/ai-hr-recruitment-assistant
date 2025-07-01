## Manual Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

## Docker Setup
```bash
docker-compose up --build
```
