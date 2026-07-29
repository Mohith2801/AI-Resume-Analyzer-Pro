import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from backend.parser import extract_text_from_pdf
from backend.ats import calculate_ats_score
from backend.ai import analyze_resume, generate_interview_questions
from backend.skills import extract_skills
from backend.matcher import match_resume_with_jd
from backend.report import create_report

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.markdown(
        """
# 🧠 Resume AI

### Intelligent Resume Analysis

---
""")

    st.success("Version 1.0")

    st.markdown("## 🚀 Features")

    st.markdown("""
✅ ATS Score

✅ AI Resume Review

✅ Skill Detection

✅ JD Matching

✅ Interview Questions

✅ PDF Report
""")

    st.divider()

    st.markdown("## 🛠 Tech Stack")

    st.markdown("""
- Python

- Streamlit

- OpenRouter

- Plotly

- PyMuPDF

- ReportLab
""")

    st.divider()

    st.caption("Made with ❤️ by Mohith")

# -------------------------------------------------
# HERO SECTION
# -------------------------------------------------

st.markdown("""
<div class="hero">

<h1>🧠 AI Resume Analyzer Pro</h1>

<p>
AI Powered Resume Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TOP METRICS
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 ATS Engine",
        "100%"
    )

with col2:
    st.metric(
        "🤖 AI Analysis",
        "Enabled"
    )

with col3:
    st.metric(
        "💼 JD Match",
        "Supported"
    )

with col4:
    st.metric(
        "🎤 Interview",
        "AI Generated"
    )

st.markdown("---")

# -------------------------------------------------
# UPLOAD
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload Resume",
    type=["pdf"],
    help="Upload your resume in PDF format"
)
if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    skills = extract_skills(resume_text)

    pages = max(1, len(resume_text.split("\f")))

    score, feedback, breakdown = calculate_ats_score(resume_text)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 ATS",
        "🤖 AI Analysis",
        "🛠 Skills",
        "💼 JD Match",
        "🎤 Interview",
        "📄 Resume"
    ])
    # ==================================================
    # TAB 1 : ATS DASHBOARD
    # ==================================================
    with tab1:
        st.markdown("## 📊 ATS Dashboard")
        st.caption("Professional Applicant Tracking System Analysis")
        # ------------------------------------------
        # Top Metrics
        # ------------------------------------------
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("🎯 ATS Score", f"{score}/100")
        with c2:
            st.metric("🛠 Skills",len(skills))
        with c3:
            st.metric("📄 Resume Pages",pages)
        with c4:
            st.metric("💡 Suggestions",len(feedback))
        st.markdown("---")
        # ------------------------------------------
        # Charts
        # ------------------------------------------
        left, right = st.columns([1,1])
        with left:
            st.subheader("🎯 ATS Score")
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={"text":"Overall Score"},
                    gauge={
                        "axis":{"range":[0,100]},
                        "bar":{"color":"#3B82F6"},
                        "steps":[
                            {"range":[0,40],"color":"#3b0d11"},
                            {"range":[40,70],"color":"#665c00"},
                            {"range":[70,100],"color":"#1b4332"}
                        ]
                    }
                )
            )
            gauge.update_layout(
                height=350,
                margin=dict(l=20,r=20,t=40,b=20)
            )
            st.plotly_chart(gauge, use_container_width=True)
        with right:
            st.subheader("📈 Score Breakdown")
            labels = list(breakdown.keys())
            values = list(breakdown.values())
            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(labels, values)
            ax.set_ylim(0,20)
            ax.set_ylabel("Marks")
            plt.xticks(rotation=30)
            st.pyplot(fig)
        st.markdown("---")
        # ------------------------------------------
        # Suggestions
        # ------------------------------------------
        st.subheader("📌 Resume Suggestions")
        for item in feedback:
            if item.startswith("✅"):
                st.success(item)
            elif item.startswith("❌"):
                st.error(item)
            else:
                st.warning(item)
        # ==================================================
        # TAB 2 : AI ANALYSIS
        # ==================================================
        with tab2:
            st.markdown("## 🤖 AI Resume Analysis")
            st.caption("Powered by OpenRouter AI")
            if st.button("🚀 Analyze Resume",use_container_width=True):
                with st.spinner("Analyzing your resume..."):
                    ai_response = analyze_resume(resume_text)
                st.success("Analysis Completed Successfully!")
                # -------------------------------
                # AI Result Card
                # -------------------------------
                with st.container(border=True):
                    st.markdown(ai_response)
                st.markdown("---")
                # -------------------------------
                # Download Report
                # -------------------------------
                create_report("resume_report.pdf",score,ai_response)
                with open(
                    "resume_report.pdf",
                    "rb"
                ) as pdf:
                    st.download_button(
                    "📥 Download PDF Report",
                    pdf,
                    file_name="AI_Resume_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                    )
        # ==================================================
        # TAB 3 : SKILLS
        # ==================================================
        with tab3:
            st.markdown("## 🛠 Skills Analysis")
            st.caption("Skills detected from your resume")
            if len(skills) == 0:
                st.warning("No skills detected.")
            else:
                st.success(f"Detected {len(skills)} Skills")
                st.markdown("### 💻 Technical Skills")
                cols = st.columns(4)
                for i, skill in enumerate(skills):
                    with cols[i % 4]:
                        st.info(f"✅ {skill}")
                st.markdown("---")
                st.subheader("📊 Skills Distribution")
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=skills,
                        y=[1] * len(skills),
                        text=skills,
                        textposition="outside"
                    )
                )
                fig.update_layout(
                    height=400,
                    xaxis_title="Skills",
                    yaxis=dict(showticklabels=False),
                    title="Detected Skills",
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig,use_container_width=True)
        # ==================================================
        # TAB 4 : JOB DESCRIPTION MATCH
        # ==================================================
        with tab4:
            st.markdown("## 💼 Job Description Match")
            st.caption("Compare your resume with a job description")
            job_description = st.text_area(
                "📋 Paste Job Description",
                height=250,
                placeholder="Paste the complete job description here..."
            )
            if st.button("🎯 Match Resume",use_container_width=True):
                if job_description.strip() == "":
                    st.warning("Please paste a Job Description.")
                else:
                    jd_score, matching_skills, missing_skills = match_resume_with_jd(
                        resume_text,
                        job_description
                    )
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("🎯 Match %",f"{jd_score}%")
                with c2:
                    st.metric("✅ Matching",len(matching_skills))
                with c3:
                    st.metric("❌ Missing",len(missing_skills))
                st.markdown("---")
                # -------------------------
                # Match Gauge
                # -------------------------
                gauge = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=jd_score,
                        title={"text": "Resume Match"},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#3B82F6"},
                            "steps": [
                                {"range": [0, 40], "color": "#3b0d11"},
                                {"range": [40, 70], "color": "#665c00"},
                                {"range": [70, 100], "color": "#1b4332"},
                            ],
                        },
                    )
                )
                gauge.update_layout(height=320)
                st.plotly_chart(gauge,use_container_width=True)
                st.markdown("---")
                left, right = st.columns(2)
                with left:
                    st.subheader("✅ Matching Skills")
                    if matching_skills:
                        for skill in matching_skills:
                            st.success(skill)
                    else:
                        st.info("No matching skills found.")
                with right:
                    st.subheader("❌ Missing Skills")
                    if missing_skills:
                        for skill in missing_skills:
                            st.error(skill)
                    else:
                        st.info("No missing skills found.")
                st.markdown("---")
                st.subheader("💡 Recommendation")
                if jd_score >= 80:
                    st.success(
                        "Excellent match! Your resume is well aligned with this job."
                    )
                elif jd_score >= 60:
                    st.warning(
                        "Good match. Improve the missing skills to increase your chances."
                    )
                else:
                    st.error(
                        "Low match score. Consider updating your resume to include relevant skills."
                    )
        # ==================================================
        # TAB 5 : INTERVIEW PREPARATION
        # ==================================================
        with tab5:
            st.markdown("## 🎤 AI Interview Preparation")
            st.caption("Generate interview questions based on your resume")
            col1, col2 = st.columns([3,1])
            with col1:
                st.info(
                    "Get personalized interview questions generated from your resume."
                )
            with col2:
                st.metric("Questions", "AI Generated")
            st.markdown("---")
            if st.button(
                "🚀 Generate Interview Questions",
                use_container_width=True
            ):
                with st.spinner("Generating interview questions..."):
                    questions = generate_interview_questions(resume_text)
                st.success("Interview Questions Generated!")
                st.markdown("---")
                with st.container(border=True):
                    st.markdown(questions)
                st.markdown("---")
                with st.expander("💡 Interview Tips"):
                    st.markdown("""
### Before the Interview

- Revise all projects thoroughly.
- Prepare a short self-introduction.
- Know every skill listed on your resume.
- Practice explaining your projects.
- Be ready for coding questions.

### During the Interview

- Think before answering.
- Explain your approach clearly.
- If you don't know an answer, explain how you would solve it.
- Stay confident and communicate effectively.

### After the Interview

- Thank the interviewer.
- Ask relevant questions about the role.
- Reflect on your performance.
""")

        # ==================================================
        # TAB 6 : RESUME PREVIEW
        # ==================================================
        with tab6:
            st.markdown("## 📄 Resume Preview")
            st.caption("Preview the extracted content from your uploaded resume")
            # ------------------------------------------
            # Resume Statistics
            # ------------------------------------------
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("📄 Pages",pages)
            with c2:
                st.metric("🛠 Skills",len(skills))
            with c3:
                st.metric("📝 Characters",len(resume_text))
            with c4:
                st.metric("📚 Words",len(resume_text.split()))
            st.markdown("---")
            # ------------------------------------------
            # Resume Text
            # ------------------------------------------
            with st.container(border=True):
                st.text_area(
                    "Extracted Resume",
                    resume_text,
                    height=500
                )
            st.markdown("---")
            # ------------------------------------------
            # Resume Quality
            # ------------------------------------------
            st.subheader("📊 Resume Statistics")
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=[
                        "Words",
                        "Characters",
                        "Skills"
                    ],
                    y=[
                        len(resume_text.split()),
                        len(resume_text),
                        len(skills)
                    ],
                    text=[
                        len(resume_text.split()),
                        len(resume_text),
                        len(skills)
                    ],
                    textposition="outside"
                )
            )
            fig.update_layout(
                height=400,
                title="Resume Overview",
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("---")
            # ------------------------------------------
            # Download Resume Text
            # ------------------------------------------
            st.download_button(
                label="📥 Download Extracted Resume Text",
                data=resume_text,
                file_name="Extracted_Resume.txt",
                mime="text/plain",
                use_container_width=True
            )