"""
Resume Parsing Utility
Extracts text from PDF and identifies skills
"""

import PyPDF2
from io import BytesIO
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class ResumeParser:
    """Extract resume text and skills from PDF"""
    
    @staticmethod
    def extract_pdf(file) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            pdf_bytes = BytesIO(file.getvalue())
            reader = PyPDF2.PdfReader(pdf_bytes)
            
            if not reader.pages:
                return None
            
            text = ""
            for page in reader.pages[:10]:
                text += page.extract_text() + "\n"
            
            return text.strip() if text.strip() else None
        except Exception as e:
            logger.error(f"PDF parse error: {e}")
            return None
    
    @staticmethod
    def extract_skills(resume_text: str) -> List[str]:
        """Extract ML/AI skills from resume"""
        skills_db = {
            "python": "Python",
            "pytorch": "PyTorch",
            "tensorflow": "TensorFlow",
            "keras": "Keras",
            "sklearn": "Scikit-Learn",
            "nlp": "NLP",
            "llm": "LLM",
            "transformers": "Transformers",
            "huggingface": "HuggingFace",
            "pandas": "Pandas",
            "numpy": "NumPy",
            "sql": "SQL",
            "docker": "Docker",
            "aws": "AWS",
            "gcp": "GCP",
            "azure": "Azure",
            "git": "Git",
            "linux": "Linux",
            "cv": "Computer Vision",
            "opencv": "OpenCV",
            "spark": "Spark",
            "hadoop": "Hadoop"
        }
        
        found = []
        resume_lower = resume_text.lower()
        
        for skill_key, skill_name in skills_db.items():
            if skill_key in resume_lower:
                found.append(skill_name)
        
        return list(set(found))[:10]
