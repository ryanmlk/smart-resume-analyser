### Project Context
A mid-sized recruitment technology company is building an internal AI-driven platform to help recruiters quickly screen large volumes of resumes and match candidates with open roles. The company currently handles thousands of resumes every week and relies heavily on manual screening, which is slow, inconsistent, and prone to human bias. The leadership team wants to modernize the workflow using emerging AI tools and scalable software architecture.

### Problem Statement
Recruiters face significant challenges in identifying the right candidates due to unstructured resume formats, inconsistent skill representation, and the inability to efficiently match candidate profiles with job requirements. The manual process results in delayed hiring, increased operational costs, and missed high-quality candidates.

The company requires a real-time, intelligent system that can automatically analyze resumes, extract meaningful information, and generate basic job recommendations.

### Project Objectives
You will design and develop an intelligent system that:

1. Analyzes resumes based on skills and experience.
2. Stores structured candidate profiles in a database
3. Recommends basic job opportunities

The final solution must run locally using Streamlit and demonstrate practical, real-world AI software engineering skills.

### 3 Week Capstone Timeline

#### Week 1: Planning and System Design
- Focus: Turn the idea into a clear technical plan.
- Deliverables: Tech Spec Document containing:

- Problem overview
- User flow diagrams
- System architecture
- MongoDB schema design
- API design
- Streamlit UI Wireframe

Expected Output: Approved tech spec before coding begins.

#### Week 2: Core Development
- Focus: Build the working system.

Tasks

- Resume upload and parsing
- Skill extraction logic (Try following the ATS scheme for scoring)
- Candidate scoring algorithm
- MongoDB CRUD operations
- Core Streamlit UI

Expected Output: A functional local working version of the app.

#### Week 3: Testing, Pushing, and Final Presentation
- Focus: Stabilize the product, prepare for delivery, and present the final solution.

Tasks: 

- Bug fixes, code standardization and error handling
- UI and user experience improvements
- Performance tuning and optimization
- Local hosting using Streamlit
- Push code to Git
- Preparation of final presentation slides
Tools to Utilize:
Draw.io or Lucidchart for system architecture diagrams
Notion or Markdown for tech spec document
Jupyter Notebook for exploration and prototyping
spaCy for text processing and skill extraction
scikit learn for similarity and basic models

Optional Hugging Face for embeddings

FastAPI for building a basic API
Pydantic for data validation
MongoDB as the primary database
Streamlit for web application
Ruff for Linting
Grading Rubric
Total: 100 marks

### Grading Rubric

1. System Design, Tech Spec Document and Architecture – 20 marks
Quality of system architecture, clarity of data flow, and completeness of the technical specification document.

2. Implementation Quality – 25 marks
Functionality of features, code quality, modularity, and overall robustness of the implementation.

3. AI and Data Processing – 20 marks
Accuracy and correctness of resume parsing, skill extraction, and job recommendation logic.

4. Tool Usage – 10 marks
Appropriate and effective use of Streamlit, Notion, NLP libraries, and any other required tools.

5. Presentation, Teamwork and Demo – 25 marks
Clarity and professionalism of final presentation, live demo quality, and collaboration within the team.

### Final Deliverables
- GitHub repository link
- Fully working Streamlit application with demo
- README file with screenshots
- requirements.txt file
- .gitignore file
- Final presentation slides with a nice class presentation

### ATS GRADING (Reference)
Applicant Tracking Systems score resumes by analyzing several core parameters. While each platform uses its own algorithm, most rely on these key factors:

1. Keyword relevance
ATS looks for job specific keywords pulled from the job description. This includes required skills, tools, certifications, job titles, and industry terms. Higher keyword match usually raises the score.

2. Skills matching
Hard skills are weighted more heavily than soft skills. Technical tools, programming languages, methodologies, and certifications tend to carry the most value.

3. Work experience alignment
The system evaluates how closely your job titles, responsibilities, and career timeline match the role requirements. Consistency and relevance matter more than job prestige.

4. Education and certifications
Degrees, licenses, and certifications that match required or preferred qualifications improve scoring.

5. Formatting readability
ATS prefers simple, clean layouts. It scores higher when it can easily parse headings, bullet points, and standard section titles. Complex graphics, columns, tables, and text boxes can lower readability scores.

6. Job titles and industry terminology
Standard job titles and recognized industry language score better than creative or vague titles.

7. Recency of experience
More recent, relevant roles tend to carry greater weight than older or unrelated work.

8. Location and work authorization
Some ATS systems score or filter based on geographic proximity and legal work eligibility.

9. Accomplishment based content
Quantified achievements such as metrics, percentages, revenue impact, or efficiency gains score higher than generic task descriptions.

10. Consistency and completeness
Date gaps, missing information, and inconsistencies in job history can lower scores.

