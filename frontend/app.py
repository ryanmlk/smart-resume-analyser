import streamlit as st
import sys
import os

# Add backend to path logic to ensure imports work whether running from root or frontend dir
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, '..', 'backend')
sys.path.append(backend_path)

try:
    from parser import parse_resume, parse_job_description
    from scorer import calculate_ats_score
    from database import db
except ImportError as e:
    st.error(f"Backend modules not found. Ensure you are running from the \
    project root or backend is in python path. Error: {e}")
    st.stop()

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

st.title("Smart Resume Analyzer")
st.markdown("Upload your resume and optionally paste a job description to score against.")

col_upload, col_jd = st.columns(2)

with col_upload:
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

with col_jd:
    job_description = st.text_area("Paste Job Description (Optional)", height=150)

if uploaded_file:
    # Use a unique key to detect if the file has changed
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"
    
    # Check if we already processed this exact file
    if "parsed_resume_data" not in st.session_state or st.session_state.get("current_file_key") != file_key:
        
        # Valid new file, process it
        temp_path = os.path.join(current_dir, f"temp_{uploaded_file.name}")
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Analyzing with Llama 3 (this may take 1-2 mins)..."):
            try:
                # Parse
                parsed_data = parse_resume(temp_path)
                
                # Store in session state
                st.session_state["parsed_resume_data"] = parsed_data
                st.session_state["current_file_key"] = file_key
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
                # Clear state on error to allow retry
                if "parsed_resume_data" in st.session_state:
                    del st.session_state["parsed_resume_data"]
                if "current_file_key" in st.session_state:
                    del st.session_state["current_file_key"]
            finally:
                # Cleanup temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    # Retrieve data from state (whether just parsed or cached)
    resume_data = st.session_state.get("parsed_resume_data")

    if resume_data:
        if "error" in resume_data:
            st.error(f"Error: {resume_data['error']}")
        else:
            # Display Parsed Profile (Col 1) ALWAYS
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Parsed Profile")
                st.info(f"**Email:** {resume_data.get('email', 'N/A')}")
                st.info(f"**Phone:** {resume_data.get('phone', 'N/A')}")
                
                st.write("**Detected Skills:**")
                skills = resume_data.get('skills', [])
                if skills:
                    st.success(", ".join(skills))
                else:
                    st.warning("No skills detected.")
                    
                st.markdown("---")
                st.subheader("Structure Breakdown")
                
                parsed_sections = resume_data.get('parsed_sections', {})
                
                with st.expander("Professional Summary", expanded=True):
                    st.write(parsed_sections.get('summary') or "*Not Found*")

                with st.expander("Experience"):
                    st.write(parsed_sections.get('experience') or "*Not Found*")
                    
                with st.expander("Projects"):
                    st.write(parsed_sections.get('projects') or "*Not Found*")
                    
                with st.expander("Education"):
                    st.write(parsed_sections.get('education') or "*Not Found*")
                    
                with st.expander("References"):
                    st.write(parsed_sections.get('references') or "*Not Found*")

            with col2:
                if job_description and job_description.strip():
                    # Extract JD Skills
                    with st.spinner("Analyzing Job Description (Llama 3)..."):
                        jd_result = parse_job_description(job_description)
                        jd_skills = set(jd_result.get("skills", []))
                    
                    # Score
                    score_data = calculate_ats_score(resume_data, 
                                                     job_description_keywords=jd_skills if jd_skills else None)
                    
                    # Save to DB (Fire and forget)
                    try:
                        db.insert_resume({**resume_data, **score_data})
                    except Exception as db_e:
                        print(f"DB Error: {db_e}") 
                    
                    st.subheader("ATS Score")
                    score = score_data['total_score']
                    
                    # Color code score
                    if score >= 80:
                        st.balloons()
                        st.success(f"Score: {score}/100")
                    elif score >= 50:
                        st.warning(f"Score: {score}/100")
                    else:
                        st.error(f"Score: {score}/100")
                        
                    st.progress(score)
                    
                    st.subheader("Feedback")
                    for item in score_data['breakdown']:
                        st.write(f"- {item}")
                else:
                    st.info("**Please enter a Job Description** to generate an ATS Score and feedback.")
        
        # Show raw text in expander
        with st.expander("View Raw Resume Text"):
             st.text(resume_data.get("text", ""))
