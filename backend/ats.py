import re

def calculate_ats_score(resume_text):

    score = 0
    feedback = []

    resume = resume_text.lower()

    # -----------------------------
    # Contact Information (10)
    # -----------------------------
    email = bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text))
    phone = bool(re.search(r"\+?\d[\d\s\-]{8,}", resume_text))
    contact_score = 0
    if email and phone:
        contact_score = 10
        score += contact_score
        feedback.append("✅ Contact information detected.")
    else:
        feedback.append("❌ Add email and phone number.")

    # -----------------------------
    # Education (15)
    # -----------------------------
    education_keywords = [
        "education",
        "b.tech",
        "btech",
        "information technology",
        "computer science",
        "iiit",
        "cgpa",
        "gpa"
    ]
    education_score = 0

    if any(word in resume for word in education_keywords):
        education_score = 15
        score += education_score
        feedback.append("✅ Education section found.")
    else:
        feedback.append("❌ Add education details.")

    # -----------------------------
    # Skills (20)
    # -----------------------------
    skills = [
        "python","sql","machine learning","deep learning",
        "tensorflow","pytorch","keras","streamlit",
        "flask","fastapi","docker","git","github",
        "aws","azure","pandas","numpy","scikit-learn"
    ]

    skill_count = sum(1 for skill in skills if skill in resume)

    skill_score = min(skill_count, 10) * 2
    score += skill_score

    feedback.append(f"✅ {skill_count} technical skills detected.")

    # -----------------------------
    # Projects (20)
    # -----------------------------
    project_keywords = [
        "project",
        "developed",
        "built",
        "implemented",
        "created"
    ]
    project_score = 0

    if any(word in resume for word in project_keywords):
        project_score = 20
        score += project_score
        feedback.append("✅ Projects section detected.")
    else:
        feedback.append("❌ Add academic/personal projects.")

    # -----------------------------
    # Experience (20)
    # -----------------------------
    experience_keywords = [
        "intern",
        "experience",
        "worked",
        "software engineer",
        "developer"
    ]

    experience_score = 0
    if any(word in resume for word in experience_keywords):
        experience_score = 20
        score += experience_score
        feedback.append("✅ Experience section found.")
    else:
        feedback.append("🟡 No experience detected.")

    # -----------------------------
    # GitHub (5)
    # -----------------------------
    github_score = 0
    if "github" in resume:
        github_score = 5
        score += github_score
        feedback.append("✅ GitHub profile included.")
    else:
        feedback.append("🟡 Add GitHub profile.")

    # -----------------------------
    # LinkedIn (5)
    # -----------------------------
    linkedin_score = 0
    if "linkedin" in resume:
        linkedin_score = 5
        score += linkedin_score
        feedback.append("✅ LinkedIn profile included.")
    else:
        feedback.append("🟡 Add LinkedIn profile.")

    # -----------------------------
    # Certifications (5)
    # -----------------------------
    cert_keywords = [
        "certificate",
        "certification",
        "coursera",
        "udemy",
        "nptel"
    ]

    certificate_score = 0
    if any(word in resume for word in cert_keywords):
        certificate_score = 5
        score += certificate_score
        feedback.append("✅ Certifications detected.")
    else:
        feedback.append("🟡 Add certifications.")

    breakdown = {
    "Contact": contact_score,
    "Education": education_score,
    "Skills": skill_score,
    "Projects": project_score,
    "Experience": experience_score,
    "GitHub": github_score,
    "LinkedIn": linkedin_score,
    "Certificates": certificate_score
    }

    score = min(score, 100)

    return score, feedback, breakdown