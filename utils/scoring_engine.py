
"""
Scoring Engine
Evaluates answers with transparent reasoning
"""

from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Score answers with detailed breakdown"""
    
    def score_answer(self, question: str, answer: str, resume: str) -> Dict:
        """
        Calculate score with transparent reasoning
        Returns: {score, feedback, reasoning, breakdown}
        """
        
        # Validation
        if len(answer.strip()) < 20:
            return {
                "score": 5,
                "feedback": "Answer too brief",
                "reasoning": "Insufficient content",
                "breakdown": {"clarity": 1, "depth": 1, "relevance": 1}
            }
        
        score = 10
        breakdown = {"clarity": 0, "depth": 0, "relevance": 0}
        
        # Technical Depth (0-7 points)
        depth_keywords = [
            "algorithm", "complexity", "optimize", "pattern",
            "design", "approach", "logic", "example", "code",
            "tradeoff", "efficient"
        ]
        depth_score = min(7, sum(1 for kw in depth_keywords if kw in answer.lower()) * 2)
        breakdown["depth"] = depth_score
        score += depth_score
        
        # Clarity (0-3 points)
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        clarity_score = min(3, len(sentences))
        breakdown["clarity"] = clarity_score
        score += clarity_score
        
        # Relevance (0-3 points)
        resume_words = set(resume.lower().split())
        answer_words = set(answer.lower().split())
        overlap = len(resume_words & answer_words)
        relevance_score = min(3, overlap // 10)
        breakdown["relevance"] = relevance_score
        score += relevance_score
        
        feedback = "Excellent" if score >= 18 else "Good" if score >= 14 else "Needs improvement"
        
        return {
            "score": min(20, score),
            "feedback": feedback,
            "reasoning": f"Depth: {breakdown['depth']}/7 | Clarity: {clarity_score}/3 | Relevance: {relevance_score}/3",
            "breakdown": breakdown
        }
