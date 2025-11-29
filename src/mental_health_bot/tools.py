from typing import List, Dict, Any
import numpy as np

class MentalHealthTools:
    """Advanced custom tools for mental health analysis"""
    
    def __init__(self):
        self.crisis_keywords = {
            'suicidal': ['kill myself', 'end it all', 'suicide', 'want to die', 'not worth living'],
            'self_harm': ['cut myself', 'self harm', 'hurt myself', 'bleeding'],
            'panic': ['panic attack', 'cant breathe', 'heart racing', 'losing control'],
            'depression': ['hopeless', 'empty inside', 'no point', 'cant get out of bed']
        }
        
    def crisis_detector(self, text: str) -> Dict:
        """Advanced crisis detection with multi-layer analysis"""
        text_lower = text.lower()
        
        # Layer 1: Keyword matching
        crisis_level = "low"
        detected_issues = []
        
        for category, keywords in self.crisis_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_issues.append(category)
                if category in ['suicidal', 'self_harm']:
                    crisis_level = "high"
                elif crisis_level != "high" and category in ['panic']:
                    crisis_level = "medium"
        
        # Layer 2: Emotional intensity analysis
        emotional_intensity = self.analyze_emotional_intensity(text)
        if emotional_intensity > 0.8 and crisis_level == "low":
            crisis_level = "medium"
            
        # Layer 3: Contextual risk assessment
        risk_score = self.calculate_risk_score(text, detected_issues)
        
        return {
            "crisis_level": crisis_level,
            "detected_issues": detected_issues,
            "risk_score": risk_score,
            "emotional_intensity": emotional_intensity,
            "immediate_action_required": crisis_level in ["high", "medium"]
        }
    
    def analyze_emotional_intensity(self, text: str) -> float:
        """Analyze emotional intensity from text"""
        intensity_indicators = [
            len([w for w in text.split() if w in ['very', 'extremely', 'really', 'so', 'too']]),
            text.count('!'),
            len([w for w in text.split() if len(w) > 8]),  # Long words often indicate intensity
            text.count(' not ')  # Negations often indicate distress
        ]
        
        intensity = sum(intensity_indicators) / (len(text.split()) + 1)
        return min(intensity, 1.0)
    
    def calculate_risk_score(self, text: str, issues: List[str]) -> float:
        """Calculate comprehensive risk score"""
        base_score = 0.0
        
        # Issue-based scoring
        issue_weights = {'suicidal': 1.0, 'self_harm': 0.9, 'panic': 0.7, 'depression': 0.6}
        for issue in issues:
            base_score += issue_weights.get(issue, 0.5)
            
        # Text characteristics
        if 'help' in text.lower():
            base_score += 0.3  # Reaching out is positive but indicates need
        if 'alone' in text.lower() or 'lonely' in text.lower():
            base_score += 0.2
            
        return min(base_score, 1.0)
    
    def generate_coping_strategy(self, crisis_data: Dict) -> str:
        """Generate personalized coping strategies"""
        issues = crisis_data['detected_issues']
        
        strategies = {
            'suicidal': """🚨 **CRITICAL**: Please contact crisis support immediately:
• Call 988 (Suicide Prevention)
• Text HOME to 741741
• You are not alone - help is available NOW""",
            
            'panic': """💨 **Panic Attack Protocol**:
1. 5-4-3-2-1 Grounding Technique
2. Deep breathing: 4-4-6 pattern
3. Focus on one safe object in your environment""",
            
            'depression': """🤗 **Depression Support**:
• Break tasks into tiny steps
• Reach out to one person today  
• Remember: feelings aren't facts""",
            
            'default': """🌱 **General Wellness**:
• Practice mindfulness for 5 minutes
• Connect with nature or pets
• Engage in gentle physical activity"""
        }
        
        if 'suicidal' in issues:
            return strategies['suicidal']
        elif 'panic' in issues:
            return strategies['panic']
        elif 'depression' in issues:
            return strategies['depression']
        else:
            return strategies['default']

# Global tools instance
MENTAL_HEALTH_TOOLS = MentalHealthTools()
