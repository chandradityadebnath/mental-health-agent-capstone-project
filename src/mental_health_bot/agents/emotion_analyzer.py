"""
Emotion Analysis Agent
"""

from typing import List, Dict  # <-- Fixed import
import re

class EmotionAnalysisAgent:
    """Analyzes user messages for emotional content"""

    def __init__(self):
        self.emotion_keywords = {
            "sad": ["sad", "unhappy", "depressed", "down"],
            "happy": ["happy", "joyful", "excited", "glad"],
            "anxious": ["anxious", "nervous", "worried", "stressed"],
            "angry": ["angry", "mad", "frustrated"]
        }

    async def analyze(self, message: str) -> Dict:
        detected_emotions = self._detect_emotions(message)
        support_needs = self._determine_support_needs(detected_emotions)
        return {
            "detected_emotions": detected_emotions,
            "support_needs": support_needs
        }

    def _detect_emotions(self, message: str) -> List[str]:
        emotions_found = []
        for emotion, keywords in self.emotion_keywords.items():
            for kw in keywords:
                if re.search(rf"\b{kw}\b", message, re.IGNORECASE):
                    emotions_found.append(emotion)
        return list(set(emotions_found))  # Remove duplicates

    def _determine_support_needs(self, emotions: List[str]) -> List[str]:
        needs = []
        if "sad" in emotions:
            needs.append("emotional_support")
        if "anxious" in emotions:
            needs.append("calming_guidance")
        if "angry" in emotions:
            needs.append("anger_management")
        if "happy" in emotions:
            needs.append("positive_reinforcement")
        return list(set(needs)) or ["general_support"]
