"""
High-level orchestrator for a chatbot-style AI response.
"""

import asyncio
from mental_health_bot.agents.crisis_detector import CrisisDetectionAgent
from mental_health_bot.agents.emotion_analyzer import EmotionAnalysisAgent
from mental_health_bot.agents.chat_agent import ChatAgent
from typing import Dict, List

class AIAgentOrchestrator:

    def __init__(self):
        self.crisis_agent = CrisisDetectionAgent()
        self.emotion_agent = EmotionAnalysisAgent()
        self.chat_agent = ChatAgent()

    async def process(self, message: str) -> Dict:
        crisis_task = asyncio.create_task(self.crisis_agent.analyze(message))
        emotion_task = asyncio.create_task(self.emotion_agent.analyze(message))

        crisis_result, emotion_result = await asyncio.gather(crisis_task, emotion_task)

        crisis_level = crisis_result.get("crisis_level", "low")
        emotions: List[str] = emotion_result.get("detected_emotions", [])

        final_response = self.chat_agent.generate(
            message=message,
            emotions=emotions,
            crisis_level=crisis_level
        )

        return {
            "response": final_response,
            "crisis_level": crisis_level,
            "emotions": emotions
        }
