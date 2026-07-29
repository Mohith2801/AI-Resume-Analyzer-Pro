from backend.skills import extract_skills

def match_resume_with_jd(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matching = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) == 0:
        score = 0
    else:
        score = round((len(matching) / len(jd_skills)) * 100)

    return score, matching, missing