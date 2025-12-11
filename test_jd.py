import sys
sys.path.append("/mnt/area51/Projects/ai-resume-parser/smart-resume-analyzer/backend")

from parser import extract_skills
from scorer import calculate_ats_score

def test_jd_comparison():
    print("--- Testing JD Comparison ---")
    
    # Mock Resume Data
    resume_data = {
        "text": "Experienced Python Developer with SQL knowledge.",
        "skills": ["python", "sql", "java", "communication"],
        "email": "test@test.com",
        "phone": "123"
    }
    
    # Mock JD
    jd_text = "We need a Python developer who knows SQL and React."
    jd_skills = set(extract_skills(jd_text))
    print(f"Extracted JD Skills: {jd_skills}")
    
    # Score Without JD
    score_no_jd = calculate_ats_score(resume_data)
    print(f"Score (No JD): {score_no_jd['total_score']}")
    
    # Score With JD
    score_with_jd = calculate_ats_score(resume_data, job_description_keywords=jd_skills)
    print(f"Score (With JD): {score_with_jd['total_score']}")
    print("Breakdown:", score_with_jd['breakdown'])
    
    # Verify Weight Shift
    # With JD, skill weight is higher (45). Resume has 2/3 matches (python, sql).
    # Without JD, based on count (4 skills -> ~half score if threshold is 5).
    
if __name__ == "__main__":
    test_jd_comparison()
