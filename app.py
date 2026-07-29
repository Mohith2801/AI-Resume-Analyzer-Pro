import streamlit as st
from backend.parser import extract_text_from_pdf
from backend.ats import calculate_ats_score
from backend.ai import analyze_resume, generate_interview_questions
from backend.skills import extract_skills
from backend.matcher import match_resume_with_jd
from backend.report import create_report
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
# 📄 AI Resume Analyzer Pro

### 🚀 AI-Powered Resume Intelligence Platform

Analyze your resume using AI and improve your chances of getting shortlisted.

---
""")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📄 Resume", "PDF")
col2.metric("🤖 AI", "Enabled")
col3.metric("📊 ATS", "100 Points")
col4.metric("💼 JD Match", "Supported")
# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:

    st.image("assets/logo.png", width=120)

    st.title("AI Resume Analyzer")

    st.success("Version 1.0")

    st.markdown("---")

    st.subheader("✨ Features")

    st.write("✅ ATS Score")
    st.write("✅ AI Resume Review")
    st.write("✅ Skill Extraction")
    st.write("✅ Job Description Matching")
    st.write("✅ Interview Questions")
    st.write("✅ PDF Report")

    st.markdown("---")

    st.subheader("🛠 Tech Stack")

    st.write("Python")
    st.write("Streamlit")
    st.write("OpenRouter")
    st.write("Plotly")
    st.write("PyMuPDF")
    st.write("ReportLab")
# --------------------------------------------------
# File Upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Your Resume",
    type=["pdf"],
    help="Supported format: PDF"
)

# --------------------------------------------------
# Process Resume
# --------------------------------------------------
if uploaded_file is not None:

    st.success("✅ Resume Uploaded Successfully!")
    st.balloons()

    st.subheader("📂 File Details")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📄 **{uploaded_file.name}**")
    with col2:
        st.info(f"📦 **{round(uploaded_file.size/1024,2)} KB**")

    # Extract Resume Text
    resume_text = extract_text_from_pdf(uploaded_file)
    # Extract Skills
    skills = extract_skills(resume_text)
    # Count Resume Pages
    pages = max(1, len(resume_text.split("\f")))
    # Calculate ATS Score
    score, feedback, breakdown = calculate_ats_score(resume_text)

    # Create Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 ATS Score",
        "🤖 AI Analysis",
        "🛠 Skills",
        "💼 JD Match",
        "🎤 Interview",
        "📄 Resume Preview"
    ])

    # ==================================================
    # TAB 1 : ATS
    # ==================================================
    with tab1:

        st.subheader("📊 ATS Analysis")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("ATS", f"{score}/100")
        with col2:
            st.metric("Skills", len(skills))
        with col3:
            st.metric("Pages", pages)
        with col4:
            st.metric("Suggestions", len(feedback))

        fig = go.Figure(go.Indicator(
             mode="gauge+number",
             value=score,
             title={'text': "ATS Score"},
             gauge={
                  'axis': {'range': [0, 100]},
                  'bar': {'color': "darkgreen"},
                  'steps': [
                       {'range': [0, 40], 'color': "#ffcccc"},
                       {'range': [40, 70], 'color': "#fff2cc"},
                       {'range': [70, 100], 'color': "#d9ead3"}
                    ]
            }
        ))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        # ATS Breakdown Chart
        labels = list(breakdown.keys())
        values = list(breakdown.values())
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, values)
        ax.set_ylabel("Score")
        ax.set_title("ATS Score Breakdown")
        st.pyplot(fig)
        st.subheader("📌 Suggestions")
        for item in feedback:
            st.success(item)

    # ==================================================
    # TAB 2 : AI
    # ==================================================
    with tab2:
        st.subheader("🤖 AI Resume Analysis")
        if st.button("🤖 Analyze Resume with AI"):
            with st.spinner("Analyzing Resume... Please wait..."):
                ai_response = analyze_resume(resume_text)
            st.toast("✅ Analysis Completed!")
            with st.container(border=True):
                st.markdown(ai_response)
            # Generate PDF Report
            create_report(
                "resume_report.pdf",
                score,
                ai_response
            )
            # Download Button
            with open("resume_report.pdf", "rb") as pdf:
                st.download_button(
                    "📥 Download Report",
                    pdf,
                    file_name="AI_Resume_Report.pdf",
                    mime="application/pdf"
                    )
    # ==================================================
    # TAB 3 : Skills
    # ==================================================
    with tab3:
        st.subheader("🛠 Extracted Skills")
        if skills:
            cols = st.columns(3)
            for i, skill in enumerate(skills):
                cols[i % 3].success(skill)
        else:
            st.warning("No skills detected.")

    # ==================================================
    # TAB 4 : Job Description Matching  
    # ==================================================
    with tab4:
        st.subheader("💼 Job Description Matching")
        job_description = st.text_area(
            "Paste Job Description",
            height=250
        )

        if st.button("🎯 Match Resume"):
            jd_score, matched, missing = match_resume_with_jd(
                resume_text,
                job_description
            )

            st.metric("Resume Match", f"{jd_score}%")
            st.progress(jd_score / 100)
            st.subheader("✅ Matching Skills")
            if matched:
                for skill in matched:
                    st.success(skill)
            else:
                st.warning("No matching skills found.")
            st.subheader("❌ Missing Skills")
            if missing:
                for skill in missing:
                    st.error(skill)
            else:
                st.success("No missing skills.")

    # ==================================================
    # TAB 5 : Interview Questions   
    # ==================================================
    with tab5:
        st.subheader("🎤 AI Interview Questions")
        if st.button("Generate Interview Questions"):
            with st.spinner("Generating Interview Questions..."):
                questions = generate_interview_questions(resume_text)
            st.success("Questions Generated!")
            with st.container(border=True):
                st.markdown(questions)

    # ==================================================
    # TAB 6 : Resume Preview
    # ==================================================
    with tab6:

        st.subheader("📄 Resume Preview")

        st.text_area(
            "Extracted Resume Text",
            resume_text,
            height=450
        )
st.markdown("---")

st.caption(
    "Developed by Narra Mohith Charan | AI Resume Analyzer Pro | 2026"
)