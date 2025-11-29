from typing import List, Dict, Any
import asyncio
import time
from datetime import datetime

class SimpleMentalHealthOrchestrator:
    """Simplified orchestrator that works without complex dependencies"""
    
    def __init__(self):
        self.crisis_keywords = {
            'suicidal': ['kill myself', 'end it all', 'suicide', 'want to die', 'not worth living'],
            'self_harm': ['cut myself', 'self harm', 'hurt myself', 'bleeding'],
            'panic': ['panic attack', 'cant breathe', 'heart racing', 'losing control'],
            'depression': ['hopeless', 'empty inside', 'no point', 'cant get out of bed']
        }
    
    async def process_user_message(self, user_message: str, user_id: str = None, session_id: str = None) -> Dict:
        """Process user message with simplified logic"""
        start_time = time.time()
        
        print(f"🎯 Processing message: {user_message[:50]}...")
        
        # Crisis detection
        crisis_data = self._detect_crisis(user_message)
        
        # Emotion analysis
        emotion_data = self._analyze_emotions(user_message)
        
        # Generate response
        final_response = self._generate_response(user_message, crisis_data, emotion_data)
        
        processing_time = time.time() - start_time
        
        return {
            'user_id': user_id,
            'session_id': session_id,
            'processing_time_seconds': round(processing_time, 2),
            'crisis_assessment': crisis_data,
            'final_response': final_response,
            'system_metrics': {
                'crisis_detected': crisis_data['crisis_level'] in ['medium', 'high'],
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _detect_crisis(self, text: str) -> Dict:
        """Detect crisis level from text"""
        text_lower = text.lower()
        
        crisis_level = "low"
        detected_issues = []
        
        for category, keywords in self.crisis_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_issues.append(category)
                if category in ['suicidal', 'self_harm']:
                    crisis_level = "high"
                elif crisis_level != "high" and category in ['panic']:
                    crisis_level = "medium"
        
        return {
            "crisis_level": crisis_level,
            "detected_issues": detected_issues,
            "immediate_action_required": crisis_level in ["high", "medium"]
        }
    
    def _analyze_emotions(self, text: str) -> Dict:
        """Analyze emotions from text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['die', 'suicide', 'kill myself']):
            return {"emotions": "desperate, hopeless, suicidal", "urgency": "high"}
        elif any(word in text_lower for word in ['anxious', 'panic', 'overwhelmed']):
            return {"emotions": "anxious, overwhelmed, scared", "urgency": "medium"}
        elif any(word in text_lower for word in ['sad', 'depressed', 'hopeless']):
            return {"emotions": "sad, depressed, hopeless", "urgency": "medium"}
        else:
            return {"emotions": "concerned, attentive", "urgency": "low"}
    
    def _generate_response(self, user_message: str, crisis_data: Dict, emotion_data: Dict) -> Dict:
        """Generate appropriate response based on analysis"""
        crisis_level = crisis_data['crisis_level']
        emotions = emotion_data['emotions']
        
        if crisis_level == 'high':
            response_text = """🚨 **CRITICAL**: I'm deeply concerned about what you're sharing. Your life is precious and there are people who want to help. Please contact crisis support immediately:\n\n• Call 988 (Suicide Prevention Lifeline)\n• Text HOME to 741741 (Crisis Text Line)\n• Call 911 for immediate emergency help\n\nYou are not alone - help is available right now. Please reach out."""
            
        elif crisis_level == 'medium':
            response_text = """💨 I understand this feels overwhelming right now. Let's work through this together:\n\n1. **Grounding Exercise**: Name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, 1 thing you can taste\n\n2. **Breathing**: Inhale for 4 counts, hold for 4, exhale for 6\n\n3. **Remember**: This feeling is temporary, and you've gotten through difficult moments before."""
            
        else:
            response_text = """🤗 Thank you for sharing what's on your mind. It takes courage to reach out, and I'm here to listen and support you. Whatever you're experiencing right now is valid, and you don't have to face it alone. Would you like to tell me more about what's been going on?"""
        
        return {
            "response_text": response_text,
            "crisis_level": crisis_level,
            "emotions": emotions,
            "agents_involved": 1,  # Simplified version
            "support_resources": {
                "crisis": "988 Suicide Prevention, Crisis Text Line: 741741",
                "therapy": "BetterHelp, Psychology Today therapist directory",
                "support": "7 Cups, Support Groups Central"
            }
        }

# Global instance
simple_orchestrator = SimpleMentalHealthOrchestrator()
