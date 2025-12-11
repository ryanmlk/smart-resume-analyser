from parser import extract_text_from_pdf
import re

def make_wide_pattern(keyword):
    words = keyword.split()
    wide_words = [r"\s*".join(list(w)) for w in words]
    return r"\s+".join(wide_words)

def extract_sections_debug(text):
    header_patterns = {
        "summary": [r"summary", r"professional\s+summary", r"profile", r"about\s+me"],
        "experience": [r"experience", r"work\s+experience", r"employment", r"work\s+history"],
        "education": [r"education", r"academic\s+background", r"qualifications"],
        "projects": [r"projects", r"personal\s+projects", r"portfolio"],
        "skills": [r"skills", r"technical\s+skills", r"core\s+competencies", r"technologies"],
        "references": [r"references"]
    }
    
    found_headers = []
    lines = text.split('\n')
    
    print(f"Total lines: {len(lines)}")
    
    for i, line in enumerate(lines):
        clean_line = line.strip()
        if len(clean_line) < 3:
            continue
            
        for section, keywords in header_patterns.items():
            for kw in keywords:
                # 1. Standard
                if re.search(r'(?i)^' + kw + r'$', clean_line) or \
                   re.search(r'(?i)^' + kw + r'[:\-]?$', clean_line):
                    print(f"MATCH (Standard) Line {i}: '{clean_line}' -> {section}")
                    found_headers.append((i, section))
                    break
                
                # 2. Wide
                wide_pat = r'(?i)^' + make_wide_pattern(kw) + r'[:\-]?$'
                if re.search(wide_pat, clean_line):
                     print(f"MATCH (Wide) Line {i}: '{clean_line}' -> {section}")
                     found_headers.append((i, section))
                     break
    
    found_headers.sort(key=lambda x: x[0])
    print("Found Headers:", found_headers)
    
    sections = {}
    for j in range(len(found_headers)):
        start_idx, section_name = found_headers[j]
        if j < len(found_headers) - 1:
            end_idx = found_headers[j+1][0]
        else:
            end_idx = len(lines)
            
        content = "\n".join(lines[start_idx+1 : end_idx]).strip()
        print(f"Section {section_name} (Lines {start_idx+1}-{end_idx}): Length {len(content)}")
        sections[section_name] = content
        
    return sections

def debug_pdf():
    pdf_path = "/mnt/area51/Projects/ai-resume-parser/smart-resume-analyzer/Resume (Ryan Moses).pdf"
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    text = extract_text_from_pdf(pdf_path)
    # print("Raw Text Preview:", text[:500])
    extract_sections_debug(text)



if __name__ == "__main__":
    debug_pdf()
