import asyncio
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class C2PSScores:
    def __init__(self, credibility=0, commonality=0, problem=0, solution=0):
        self.credibility = credibility
        self.commonality = commonality
        self.problem = problem
        self.solution = solution
        self.timestamp = datetime.utcnow().isoformat()
        self.confidence = 0.85

class SimpleC2PSAnalyzer:
    """Simplified C2PS analyzer for initial testing"""
    
    def __init__(self):
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize analyzer"""
        self.is_initialized = True
        logger.info("✅ C2PS analyzer initialized (simple mode)")
    
    async def analyze_transcript(self, text: str, speaker: str = None) -> Dict:
        """Analyze transcript text"""
        if not self.is_initialized:
            await self.initialize()
        
        # Simple keyword-based scoring for demo
        text_lower = text.lower()
        
        # Score based on keyword presence
        credibility = self._score_keywords(text_lower, [
            'experience', 'expert', 'proven', 'clients', 'years'
        ])
        
        commonality = self._score_keywords(text_lower, [
            'understand', 'similar', 'agree', 'exactly', 'common'
        ])
        
        problem = self._score_keywords(text_lower, [
            'problem', 'challenge', 'issue', 'pain', 'struggle', 'difficult'
        ])
        
        solution = self._score_keywords(text_lower, [
            'solution', 'benefit', 'improve', 'save', 'reduce', 'optimize'
        ])
        
        scores = C2PSScores(credibility, commonality, problem, solution)
        
        # Simple conversion probability calculation
        avg_score = (credibility + commonality + problem + solution) / 4
        conversion_probability = min(0.95, avg_score / 10.0)
        
        # Generate recommendations
        recommendations = []
        if credibility < 5:
            recommendations.append("💼 Share more expertise or case studies")
        if commonality < 5:
            recommendations.append("🤝 Build more rapport with the prospect")
        if problem < 5:
            recommendations.append("❗ Explore pain points more deeply")
        if solution < 5:
            recommendations.append("💡 Present clearer value proposition")
        
        return {
            "scores": scores,
            "conversion_probability": conversion_probability,
            "recommendations": recommendations,
            "sentiment_score": 0.5  # Neutral for demo
        }
    
    def _score_keywords(self, text: str, keywords: List[str]) -> float:
        """Score text based on keyword presence"""
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 2
        return min(10.0, score)

class ConversationTracker:
    """Track ongoing conversations"""
    
    def __init__(self):
        self.analyzer = SimpleC2PSAnalyzer()
        self.conversation_history: Dict[str, List[str]] = {}
    
    async def add_transcript_segment(self, call_id: str, text: str, speaker: str):
        """Add transcript segment and analyze"""
        if call_id not in self.conversation_history:
            self.conversation_history[call_id] = []
        
        self.conversation_history[call_id].append(f"{speaker}: {text}")
        
        # Analyze the latest segment
        return await self.analyzer.analyze_transcript(text, speaker)
    
    def cleanup_conversation(self, call_id: str):
        """Clean up conversation data"""
        if call_id in self.conversation_history:
            del self.conversation_history[call_id]
