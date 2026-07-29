def extract_skills(resume_text):

    skills_database = [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Streamlit",
        "Flask",
        "FastAPI",
        "Git",
        "GitHub",
        "Docker",
        "AWS",
        "Azure",
        "Power BI",
        "Excel",
        "RAG",
        "LangChain",
        "Transformers",
        "LLM",
        "OpenCV"
    ]

    found_skills = []

    resume_lower = resume_text.lower()

    for skill in skills_database:
        if skill.lower() in resume_lower:
            found_skills.append(skill)

    return found_skills