import pytest
import asyncio
from src.agents.crisis_detector import CrisisDetectionAgent
from src.agents.emotion_analyzer import EmotionAnalysisAgent

class TestCrisisDetectionAgent:
    """Test crisis detection agent functionality"""
    
    @pytest.fixture
    def agent(self):
        return CrisisDetectionAgent()
    
    @pytest.mark.asyncio
    async def test_crisis_detection_high(self, agent):
        result = await agent.analyze("I want to kill myself")
        assert result['crisis_level'] == 'high'
        assert 'suicidal' in result['detected_issues']
    
    @pytest.mark.asyncio
    async def test_crisis_detection_low(self, agent):
        result = await agent.analyze("I had a good day today")
        assert result['crisis_level'] == 'low'

class TestEmotionAnalysisAgent:
    """Test emotion analysis agent functionality"""
    
    @pytest.fixture
    def agent(self):
        return EmotionAnalysisAgent()
    
    @pytest.mark.asyncio
    async def test_emotion_detection(self, agent):
        result = await agent.analyze("I feel anxious and worried")
        assert 'anxiety' in result['detected_emotions']
        assert result['emotional_intensity'] >= 0
