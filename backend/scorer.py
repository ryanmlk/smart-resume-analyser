import logging
from typing import Dict, List, Set

def calculate_ats_score(resume_data: Dict, job_description_keywords: Set[str] = None) -> Dict:
    """
    Calculates an ATS score (0-100) based on various factors.
    Returns the score and a breakdown of feedback.
    """
    score = 0
    feedback = []
    
    # Weights configuration
    if job_description_keywords:
        MAX_SKILL_SCORE = 45
        MAX_SECTION_SCORE = 15
        MAX_CONTACT_SCORE = 5
        MAX_QUANT_SCORE = 15
        MAX_FORMAT_SCORE = 20
    else:
        MAX_SKILL_SCORE = 30
        MAX_SECTION_SCORE = 20
        MAX_CONTACT_SCORE = 10
        MAX_QUANT_SCORE = 20
        MAX_FORMAT_SCORE = 20

    # 1. Skill Match
    text_lower = resume_data.get("text", "").lower()
    skills = set(resume_data.get("skills", []))
    if job_description_keywords:
        # Convert all to lower for comparison
        jd_keywords = set(k.lower() for k in job_description_keywords)
        resume_skills_lower = set(s.lower() for s in skills)
        
        matches = resume_skills_lower.intersection(jd_keywords)
        match_count = len(matches)
        total_keywords = len(jd_keywords)
        
        if total_keywords > 0:
            # Score is proportional to match rate
            skill_score = min(MAX_SKILL_SCORE, (match_count / total_keywords) * MAX_SKILL_SCORE)
            score += skill_score
            feedback.append(f"JD Skill Match: {int(skill_score)}/{MAX_SKILL_SCORE} ({match_count}/{total_keywords} keywords matched)")
            
            missing = list(jd_keywords - resume_skills_lower)
            if missing:
                # Show top 5 missing skills
                feedback.append(f"Missing Key Skills from JD: {', '.join(missing[:5])}")
        else:
             score += MAX_SKILL_SCORE # If JD has no keywords extracted, give full points purely for not failing
    else:
        # General scoring if no specific JD provided
        skill_count = len(skills)
        if skill_count >= 10:
            score += MAX_SKILL_SCORE
            feedback.append(f"Skill Match: {MAX_SKILL_SCORE}/{MAX_SKILL_SCORE} (Good number of skills detected)")
        elif skill_count >= 5:
            score += MAX_SKILL_SCORE / 2
            feedback.append(f"Skill Match: {MAX_SKILL_SCORE / 2}/{MAX_SKILL_SCORE} (Could add more relevant skills)")
        else:
            score += 5
            feedback.append(f"Skill Match: 5/{MAX_SKILL_SCORE} (Very few skills detected)")


    # 2. Section Presence
    # Use parsed sections from Gemini if available, otherwise fallback to regex
    parsed_sections = resume_data.get("parsed_sections")
    
    sections_domains = {
        "experience": ["experience", "work history", "employment"],
        "education": ["education", "university", "college", "degree"],
        "projects": ["projects", "portfolio"],
        "summary": ["summary", "objective", "profile"]
    }
    
    section_score = 0
    missing_sections = []
    points_per_section = MAX_SECTION_SCORE / 4
    
    if parsed_sections:
        # Use structured data check
        for section in sections_domains.keys():
            # Check if section content exists and is not empty or "None"
            content = parsed_sections.get(section)
            if content and len(str(content).strip()) > 10: # Basic length check
                section_score += points_per_section
            else:
                missing_sections.append(section)
    else:
        # Fallback to Text Search
        text_lower = resume_data.get("text", "").lower()
        for section, keywords in sections_domains.items():
            if any(k in text_lower for k in keywords):
                section_score += points_per_section
            else:
                missing_sections.append(section)
    
    # Rounding for cleanliness
    section_score = int(section_score) 
    score += section_score
    feedback.append(f"Section Structure: {section_score}/{MAX_SECTION_SCORE}")
    if missing_sections:
        feedback.append(f"Missing sections likely: {', '.join(missing_sections)}")

    # 3. Contact Info
    contact_score = 0
    points_per_contact = MAX_CONTACT_SCORE / 2
    
    if resume_data.get("email"):
        contact_score += points_per_contact
    else:
        feedback.append("Missing Email Address")
        
    if resume_data.get("phone"):
        contact_score += points_per_contact
    else:
        feedback.append("Missing Phone Number")
    
    contact_score = int(contact_score)
    score += contact_score
    feedback.append(f"Contact Info: {contact_score}/{MAX_CONTACT_SCORE}")

    # 4. Content Quality / Quantifiable Results
    # check for digits (simple heuristic for metrics like "50%", "10 years", "$1M")
    import re
    digit_count = len(re.findall(r'\d+', text_lower))
    if digit_count > 10:
        score += MAX_QUANT_SCORE
        feedback.append(f"Quantifiable Results: {MAX_QUANT_SCORE}/{MAX_QUANT_SCORE} (Good use of numbers/metrics)")
    elif digit_count > 5:
        sub_score = int(MAX_QUANT_SCORE / 2)
        score += sub_score
        feedback.append(f"Quantifiable Results: {sub_score}/{MAX_QUANT_SCORE} (Try to quantify more achievements)")
    else:
        score += 0
        feedback.append(f"Quantifiable Results: 0/{MAX_QUANT_SCORE} (Lack of measurable results)")
        
    # 5. Length / Formatting
    # Simple check on text length
    word_count = len(text_lower.split())
    if 200 <= word_count <= 2000:
        score += MAX_FORMAT_SCORE
        feedback.append(f"Length/Formatting: {MAX_FORMAT_SCORE}/{MAX_FORMAT_SCORE} (Good length)")
    elif word_count < 200:
        sub_score = int(MAX_FORMAT_SCORE / 4)
        score += sub_score
        feedback.append(f"Length/Formatting: {sub_score}/{MAX_FORMAT_SCORE} (Too short)")
    else:
        sub_score = int(MAX_FORMAT_SCORE / 2)
        score += sub_score
        feedback.append(f"Length/Formatting: {sub_score}/{MAX_FORMAT_SCORE} (Likely too long)")

    return {
        "total_score": int(score),
        "breakdown": feedback
    }

