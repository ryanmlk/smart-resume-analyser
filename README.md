# Smart Resume Analyzer

A Python-based Resume Parser and ATS Scorer using Spacy and Streamlit.
Built as a capstone project requirement.

## Features
- **PDF & DOCX Parsing**: Extracts text from resume files.
- **Skill Extraction**: Uses NLP (Spacy) and a skill database to identify key skills.
- **ATS Scoring**: Scores resumes (0-100) based on content, formatting, and keyword presence.
- **Instant Feedback**: Provides actionable advice to improve the resume.

## Installation

1. **Prerequisites**: Python 3.8+, MongoDB (optional but recommended).

2. **Setup Environment**:
   ```bash
   # Create venv (if not using ~/_venv)
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r smart-resume-analyzer/requirements.txt
   ```
   *Note: First run will download the Spacy `en_core_web_sm` model automatically.*

## Running the Application

Run the Streamlit frontend:

```bash
streamlit run smart-resume-analyzer/frontend/app.py
```

## Project Structure

- `backend/`: Core logic.
  - `parser.py`: Text extraction and validation.
  - `scorer.py`: ATS scoring algorithm.
  - `database.py`: MongoDB connection.
- `frontend/`: UI logic.
  - `app.py`: Main Streamlit application.
