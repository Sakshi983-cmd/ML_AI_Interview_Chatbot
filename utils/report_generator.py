from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(name, score, feedback):
    filename = f"{name}_ML_Interview_Report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFillColorRGB(0.2, 0.2, 0.8)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 100, "ML/AI Interview Report")
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0,0,0)
    c.drawString(50, height - 150, f"Candidate: {name}")
    c.drawString(50, height - 180, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    c.drawString(50, height - 220, f"Score: {score}/100")
    c.drawString(50, height - 270, "Feedback:")
    text = c.beginText(70, height - 300)
    text.setFont("Helvetica", 12)
    for line in feedback.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()
    with open(filename, "rb") as f:
        return f.read(), filename
