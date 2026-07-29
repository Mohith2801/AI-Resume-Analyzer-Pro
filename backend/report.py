from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(filename, ats_score, ai_analysis):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>ATS Score:</b> {ats_score}/100", styles["Normal"]))

    story.append(Paragraph("<br/><b>AI Analysis</b>", styles["Heading2"]))

    story.append(Paragraph(ai_analysis.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(story)