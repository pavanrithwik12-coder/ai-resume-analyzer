"""Module 7: Streamlit dashboard for the AI Resume Analyzer and Job Recommendation System."""
import io
import os

import pandas as pd
import plotly.express as px
import streamlit as st

from resume_parser import extract_text, validate_file
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills, group_by_category
from job_matcher import load_roles, match_roles, skill_gap
from roadmap_generator import generate_roadmap, build_report

BASE = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("AI Resume Analyzer and Job Recommendation System")
st.caption("Upload your resume, pick a target role and see your match score, missing skills and a learning roadmap.")


@st.cache_data
def load_data():
    roles = load_roles(os.path.join(BASE, "data", "job_roles.csv"))
    skills = load_skill_dictionary(os.path.join(BASE, "data", "skill_dictionary.csv"))
    return roles, skills


roles_df, skill_df = load_data()

with st.sidebar:
    st.header("1. Upload and choose")
    uploaded = st.file_uploader("Resume (PDF or DOCX, max 5 MB)", type=["pdf", "docx"])
    target = st.selectbox("Target role", roles_df["role"].tolist())
    st.info("Your resume is processed in memory only and is not stored.")

if uploaded is None:
    st.write("Upload a resume from the sidebar to begin.")
    st.stop()

ok, message = validate_file(uploaded.name, uploaded.size)
if not ok:
    st.error(message)
    st.stop()
st.success(f"Uploaded file: {uploaded.name}")

try:
    raw_text = extract_text(io.BytesIO(uploaded.getvalue()), uploaded.name)
except Exception as exc:
    st.error(f"Could not read this file: {exc}")
    st.stop()

clean = clean_text(raw_text)
if len(clean) < 50:
    st.warning("Very little text was found. The file may be a scanned image, so skills may be missed.")

found = extract_skills(clean, skill_df)
grouped = group_by_category(found)
ranking = match_roles(clean, list(found), roles_df)
gap = skill_gap(found, roles_df, target)
roadmap = generate_roadmap(gap["missing"], gap["weak"])
target_score = ranking.loc[ranking["Role"] == target, "Score"].iloc[0]

tab1, tab2, tab3, tab4 = st.tabs(["Extracted skills", "Match scores", "Gap and roadmap", "Report"])

with tab1:
    st.subheader(f"{len(found)} skills found")
    for category, skills in grouped.items():
        st.markdown(f"**{category}:** " + ", ".join(skills))

with tab2:
    st.metric(f"Match score for {target}", f"{target_score}%")
    fig = px.bar(ranking, x="Score", y="Role", orientation="h", range_x=[0, 100], text="Score")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Top 3 recommended roles")
    for i, row in enumerate(ranking.head(3).itertuples(), 1):
        st.write(f"{i}. **{row.Role}** - {row.Score}%")
    st.caption("Scores are estimates for learning guidance, not recruiter decisions.")

with tab3:
    c1, c2 = st.columns(2)
    c1.subheader("Already in your resume")
    c1.write(", ".join(gap["present"]) or "None")
    c2.subheader("Missing skills")
    c2.write(", ".join(gap["missing"]) or "None - great coverage!")
    if gap["weak"]:
        st.write("Weak (mentioned only once): " + ", ".join(gap["weak"]))
    st.subheader("Learning roadmap")
    for week, text in roadmap:
        st.write(f"**{week}:** {text}")
    st.caption("Missing keywords do not always mean missing ability.")

with tab4:
    report = build_report(target, ranking, grouped, gap, roadmap)
    st.text(report)
    st.download_button("Download analysis report", report, file_name="resume_analysis_report.txt")
