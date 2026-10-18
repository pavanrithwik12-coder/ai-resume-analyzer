# AI Resume Analyzer and Job Recommendation System

An NLP-based Streamlit application that helps students see how well their resume matches selected job roles. It extracts text from PDF/DOCX resumes, identifies technical skills, scores the resume against job roles, recommends the top 3 roles, lists missing skills and generates a simple learning roadmap.

> Built for the Unlox AI Program - Major Project 1.

## Features
- Upload a PDF or DOCX resume (file type and size validated, nothing stored permanently)
- Text extraction (`pypdf`, `python-docx`) and cleaning (regex; keeps C++, C#, .NET)
- Skill extraction from a controlled dictionary of 58 skills in 11 categories
- Comparison with 7 job roles (Data Analyst, ML Engineer, AI Engineer, NLP Engineer, Computer Vision Engineer, Python Developer, Data Scientist)
- Match score, ranked roles, top-3 recommendation and chart
- Skill-gap analysis (present / weak / missing) and a rule-based weekly roadmap
- Downloadable text report

## Workflow
Upload resume -> Extract text -> Clean text -> Extract skills -> Load role requirements -> TF-IDF + cosine similarity -> Match score -> Recommend roles -> Missing skills + roadmap

## How the match score works
`Score = 70% x skill coverage + 30% x TF-IDF cosine similarity (candidate skills vs role skills)`
- Skill coverage = required skills found in the resume / required skills for the role
- TF-IDF cosine similarity gives more weight to less common skills
- Full-text TF-IDF similarity between the resume and the role description is also shown for reference

## Setup
```
git clone https://github.com/pavanrithwik12-coder/ai-resume-analyzer.git
cd ai-resume-analyzer/ai_resume_analyzer
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```
ai_resume_analyzer/
|-- app.py                 Streamlit dashboard
|-- resume_parser.py       PDF/DOCX extraction and validation
|-- text_cleaner.py        Cleaning and personal-information removal
|-- skill_extractor.py     Dictionary skill extraction, categories, sections
|-- job_matcher.py         TF-IDF, cosine similarity, skill-gap analysis
|-- roadmap_generator.py   Learning roadmap and report
|-- requirements.txt
|-- data/ (job_roles.csv, skill_dictionary.csv)
|-- sample_resumes/        Synthetic resumes (no real personal data)
|-- reports/
|-- tests/test_cases.csv   Testing sheet
```

## Testing
Three sample resumes were tested; each returns the expected top role (see `tests/test_cases.csv`). Score-consistency and fairness checks are in the Colab notebook.

## Responsible AI
- Guidance tool only, not for hiring or rejection decisions
- Gender, age, religion, nationality, marital status, photo and disability are never scored (such lines are removed before analysis)
- Only job-related skills, education, projects and experience are evaluated
- Scores are estimates; missing keywords do not always mean missing ability
- Uploaded resumes are processed in memory and not stored

## Limitations
- Keyword/dictionary matching misses skills that are not in the dictionary or are written differently
- Only 7 roles and 58 skills; role requirements are manually defined
- Scanned (image) PDFs cannot be read without OCR
- TF-IDF does not understand meaning (Sentence Transformers could be added as an improvement)

## Deployment
Push the repository to GitHub and deploy on Streamlit Community Cloud (main file: `app.py`).

## Author
Avilala Pavan Rithwik (2600031557) - Unlox AI Program
