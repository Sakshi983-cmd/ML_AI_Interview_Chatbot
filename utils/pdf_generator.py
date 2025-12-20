"""
PDF Report Generator
Creates professional PDF reports
"""

from typing import List, Tuple
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import logging

logger = logging.getLogger(__name__)

class PDFReportGenerator:
    """Generate professional PDF reports"""
    
    @staticmethod
    def generate_report(name: str, role: str, scores: List[int],
                       questions: List[str], answers: List[str],
                       skills: List[str]) -> Tuple[bytes, str]:
        """Generate PDF report"""
        
        filename = f"{name}_Interview_Report.pdf"
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph("ML/AI Interview Report", styles['Heading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary
        total = sum(scores)
        summary_data = [
            ["Candidate", name],
            ["Position", role],
            ["Date", datetime.now().strftime("%B %d, %Y")],
            ["Total Score", f"{total}/100"],
            ["Status", "QUALIFIED" if total >= 70 else "REVIEW"]
        ]
        
        table = Table(summary_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Skills
        if skills:
            elements.append(Paragraph("Skills Identified", styles['Heading2']))
            elements.append(Paragraph(", ".join(skills[:8]), styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Q&A Breakdown
        elements.append(Paragraph("Question-wise Breakdown", styles['Heading2']))
        
        for i, (q, a, s) in enumerate(zip(questions, answers, scores), 1):
            elements.append(Paragraph(f"<b>Q{i}:</b> {q[:80]}...", styles['Normal']))
            elements.append(Paragraph(f"<b>A:</b> {a[:120]}...", styles['Normal']))
            elements.append(Paragraph(f"<b>Score:</b> {s}/20", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        doc.build(elements)
        return buffer.getvalue(), filename
