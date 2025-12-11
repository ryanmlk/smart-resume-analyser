import logging
import os
import re
import json
from typing import Dict, List, Union, Set
import PyPDF2
import docx
import spacy
import csv
import ast
import ollama
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
OLLAMA_MODEL_NAME = "llama3"

JSON_SCHEMA_DEFINITION = """
{
  "personal_information": {
    "name": "string | null",
    "email": "string | null",
    "phone": "string | null",
    "linkedin_url": "string | null",
    "github_url": "string | null"
  },
  "summary": "string | null",
  "work_experience": [
    {
      "job_title": "string | null",
      "company": "string | null",
      "start_date": "string | null",
      "end_date": "string | null",
      "description": "string | null"
    }
  ],
  "education": [
    {
      "institution": "string | null",
      "degree": "string | null",
      "start_date": "string | null",
      "end_date": "string | null"
    }
  ],
  "skills": ["string"],
  "projects": [
     {
       "name": "string | null",
       "description": "string | null",
       "technologies_used": ["string"]
     }
  ],
  "references": ["string"] 
}
"""

# Load Spacy Model (Fallback/JD)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# --- Constants & Helpers ---
MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = {'.pdf', '.docx'}

SKILLS_DB_PATH = "/mnt/area51/Projects/ai-resume-parser/backend/feedback_component/models/cleaned_job_data.csv"
SKILLS_SET = set()

def load_skills():
    """Type safe skill loading."""
    global SKILLS_SET
    try:
        if not os.path.exists(SKILLS_DB_PATH):
            logging.warning("Skills DB not found. Using default skill set.")
            SKILLS_SET = {"python", "java", "c++", "sql", "machine learning", "data analysis", "react", "node.js"}
            return

        with open(SKILLS_DB_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            
            skill_col_idx = -1
            if headers:
                if "core_skills" in headers:
                    skill_col_idx = headers.index("core_skills")
                elif "filtered_skills" in headers:
                     skill_col_idx = headers.index("filtered_skills")

            if skill_col_idx == -1:
                 skill_col_idx = 2

            for row in reader:
                if len(row) > skill_col_idx:
                    try:
                        skills_list = ast.literal_eval(row[skill_col_idx])
                        for skill in skills_list:
                            SKILLS_SET.add(skill.lower().strip())
                    except:
                        continue
        logging.info(f"Loaded {len(SKILLS_SET)} unique skills.")
    except Exception as e:
        logging.error(f"Error loading skills: {e}")
        SKILLS_SET = {"python", "java", "sql"} 

load_skills()

def validate_file(file_path: str) -> bool:
    if not os.path.exists(file_path):
        return False
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
        
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False
        
    return True

def extract_text_from_pdf(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        logging.error(f"Error reading PDF file {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logging.error(f"Error reading DOCX file {file_path}: {e}")
        return ""

def extract_skills(text: str) -> List[str]:
    """
    Extracts skills by matching noun chunks and tokens against the loaded SKILLS_SET.
    Useful for JD Skill Extraction.
    """
    text_lower = text.lower()
    found_skills = set()
    doc = nlp(text_lower)
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()
        if chunk_text in SKILLS_SET:
            found_skills.add(chunk_text)
    for token in doc:
        if token.text in SKILLS_SET:
            found_skills.add(token.text)
    return list(found_skills)


def parse_job_description(text: str) -> Dict[str, List[str]]:
    """
    Parses a Job Description using Ollama (Llama 3) to extract specific skills.
    Replaces the basic Spacy extraction for JDs.
    """
    schema = """
    {
        "technical_skills": ["string"],
        "soft_skills": ["string"]
    }
    """
    
    prompt = f"""
    Analyze the following Job Description and extract the key skills required.
    Focus on specific technologies (e.g., Python, AWS, SQL), methodologies (e.g., Agile), and professional qualities.
    Do NOT include generic nouns like "components", "insurance", "wellness", "admin" unless they are specific tools/certs.
    
    Job Description:
    {text}
    
    JSON Schema:
    {schema}
    """
    
    try:
        logging.info(f"Sending JD to Ollama ({OLLAMA_MODEL_NAME})...")
        logging.info("Generic: Local processing can take 1-2 minutes depending on your hardware. Please wait...")
        response = ollama.chat(model=OLLAMA_MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt}
        ], format='json')
        
        content = response['message']['content']
        data = json.loads(content)
        
        # Combine and clean
        tech = data.get("technical_skills", []) or []
        soft = data.get("soft_skills", []) or []
        all_skills = [s for s in tech + soft if s]
        
        return {"skills": all_skills}
        
    except Exception as e:
        logging.error(f"Ollama JD Parsing Error: {e}")
        # Fallback to existing regex/spacy
        return {"skills": extract_skills(text)}


# --- Ollama Parsing ---

def call_llama(text: str) -> Dict:
    prompt = f"""
    Analyze the following resume text and extract the key information precisely according to the JSON schema provided.
    
    Resume Text:
    {text}
    
    JSON Schema:
    {JSON_SCHEMA_DEFINITION}
    """
    
    try:
        logging.info(f"Sending request to Ollama ({OLLAMA_MODEL_NAME})...")
        logging.info("Generic: Local processing can take 1-2 minutes depending on your hardware. Please wait...")
        response = ollama.chat(model=OLLAMA_MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt}
        ], format='json')
        
        content = response['message']['content']
        return json.loads(content)
    except Exception as e:
        logging.error(f"Ollama API Error: {e}")
        return None

def flatten_experience(experience_list: List[Dict]) -> str:
    """Helper to convert structured experience to string block."""
    if not experience_list: return ""
    output = []
    for exp in experience_list:
        title = exp.get('job_title') or "N/A"
        company = exp.get('company') or "N/A"
        dates = f"{exp.get('start_date', '')} - {exp.get('end_date', '')}"
        desc = exp.get('description') or ""
        output.append(f"{title} at {company} ({dates})\n{desc}")
    return "\n\n".join(output)

def flatten_education(edu_list: List[Dict]) -> str:
    """Helper to convert structured education to string block."""
    if not edu_list: return ""
    output = []
    for edu in edu_list:
        degree = edu.get('degree') or "Degree"
        inst = edu.get('institution') or "Institution"
        dates = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
        output.append(f"{degree} from {inst} ({dates})")
    return "\n\n".join(output)

def flatten_projects(proj_list: List[Dict]) -> str:
    """Helper to convert structured projects to string block."""
    if not proj_list: return ""
    output = []
    for proj in proj_list:
        name = proj.get('name') or "Project"
        desc = proj.get('description') or ""
        tech = ", ".join(proj.get('technologies_used', []))
        output.append(f"{name}: {desc}\nTech: {tech}")
    return "\n\n".join(output)

def clean_email(email_str: str) -> str:
    """Cleans email string removing spaces and artifacts."""
    if not email_str: return None
    # Remove all spaces
    clean = email_str.replace(" ", "")
    # Find email pattern in the cleaned string (in case of "email|email")
    # Simple pattern
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', clean)
    return match.group(0) if match else clean

def parse_resume(file_path: str) -> Dict[str, Union[str, List[str]]]:
    """
    Main parsing function using Ollama (Llama 3).
    """
    if not validate_file(file_path):
        return {"error": "Invalid file"}

    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        text = extract_text_from_docx(file_path)
    
    if not text:
        return {"error": "Could not extract text from file"}

    # Ollama Parsing
    llama_data = call_llama(text)
    
    if not llama_data:
        return {"error": "AI Parsing Failed (Ollama)"}

    # Map to our standard format
    personal = llama_data.get('personal_information', {})
    
    # Flatten sections for frontend string display
    parsed_sections = {
        "summary": llama_data.get('summary', ''),
        "experience": flatten_experience(llama_data.get('work_experience', [])),
        "education": flatten_education(llama_data.get('education', [])),
        "projects": flatten_projects(llama_data.get('projects', [])),
        "references": str(llama_data.get('references', []))
    }

    parsed_data = {
        "text": text,
        "email": clean_email(personal.get('email')),
        "phone": personal.get('phone'),
        "skills": llama_data.get('skills', []),
        "parsed_sections": parsed_sections,
        # Keep raw structured data too if needed in future
        "structured_data": llama_data 
    }
    
    return parsed_data

