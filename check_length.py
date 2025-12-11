import sys
sys.path.append("/mnt/area51/Projects/ai-resume-parser/smart-resume-analyzer/backend")
from parser import extract_text_from_pdf
import os

pdf_path = "/mnt/area51/Projects/ai-resume-parser/smart-resume-analyzer/Resume (Ryan Moses).pdf"
text = extract_text_from_pdf(pdf_path)
print(f"Resume Length: {len(text)} chars")
print(f"Approx Tokens: {len(text)/4}")
print("First 200 chars:", text[:200])
