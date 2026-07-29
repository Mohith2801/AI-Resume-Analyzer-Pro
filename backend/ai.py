import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = (
    st.secrets.get("OPENROUTER_API_KEY", None)
    or os.getenv("OPENROUTER_API_KEY")
)

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def analyze_resume(resume_text):
    prompt = f"""
You are an expert ATS Resume Reviewer and Career Coach.

Analyze the following resume and return your response in Markdown.

Use EXACTLY these headings:

# 📄 Professional Summary

# 💪 Strengths

# ⚠ Weaknesses

# 🛠 Missing Skills

# 💡 Resume Improvement Suggestions

# 🎯 Placement Readiness

Give a score out of 10 with a short explanation.

Resume:

{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model="inclusionai/ling-3.0-flash:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ {e}"

    
def generate_interview_questions(resume_text):

    prompt = f"""
You are an experienced Technical Interviewer.

Based on the following resume, generate:

# Technical Questions
(10 questions)

# HR Questions
(5 questions)

# Project-Based Questions
(5 questions)

Resume:

{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model="inclusionai/ling-3.0-flash:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ {e}"