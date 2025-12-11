import sys
sys.path.append("/mnt/area51/Projects/ai-resume-parser/smart-resume-analyzer/backend")
from parser import parse_resume, extract_text_from_pdf
import os
import json

def test_llama_parser():
    pdf_path = "/mnt/area51/Projects/ai-resume-parser/smart-resume-analyzer/Resume (Ryan Moses).pdf"
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    print(f"Testing Ollama Parser with: {pdf_path}")
    
    # 1. Parse
    data = parse_resume(pdf_path)
    if "error" in data:
        print("Error:", data["error"])
        return
        
    # 2. Inspect Output
    print("\n--- OLLAMA EXTRACTED DATA ---")
    print(f"Email: {data.get('email')}")
    print(f"Phone: {data.get('phone')}")
    print(f"Skills: {data.get('skills')[:10] if data.get('skills') else 'None'}...") 
    
    print("\n--- PARSED SECTIONS (Strings) ---")
    sections = data.get('parsed_sections', {})
    print("\n[EXPERIENCE]")
    print(sections.get('experience')[:200] + "..." if sections.get('experience') else "None")
    
    print("\n[PROJECTS]")
    print(sections.get('projects')[:200] + "..." if sections.get('projects') else "None")

if __name__ == "__main__":
    test_llama_parser()
