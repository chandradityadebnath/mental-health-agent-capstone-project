import streamlit as st
import asyncio
import time
from datetime import datetime
import nest_asyncio
import google.generativeai as genai
import os

# Apply nest_asyncio to handle async in Streamlit
nest_asyncio.apply()

# =============================================
# 🧠 GEMINI AI INTEGRATION WITH USER API KEY
# =============================================

class GeminiAIIntegration:
    """Gemini AI Integration with user-provided API key"""
    
    def __init__(self):
        self.model = None
        self.fallback_mode = True  # Start in fallback mode
        self.api_key = None
        
    def configure_ai(self, api_key: str):
        """Configure AI with user-provided API key"""
        if not api_key:
            return False
            
        try:
            genai.configure(api_key=api_key)
            
            # Try different models in priority order
            models_to_try = [
                'gemini-2.0-flash-lite',
                'gemini-2.0-flash-lite-001', 
                'gemma-3-1b-it',
                'gemini-2.0-flash',
                'gemini-pro'
            ]
            
            for model_name in models_to_try:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    # Test the model
                    test_response = self.model.generate_content("Say 'AI Ready'")
                    self.fallback_mode = False
                    self.api_key = api_key
                    st.success(f"✅ Connected to {model_name}!")
                    return True
                except Exception as e:
                    continue
                    
            # If no models work
            st.error("❌ No working Gemini models found with this API key")
            self.fallback_mode = True
            return False
            
        except Exception as e:
            st.error(f"❌ API configuration failed: {e}")
            self.fallback_mode = True
            return False
    
    async def analyze_with_ai(self, text: str) -> dict:
        """Analyze text with real Gemini AI"""
        if self.model and not self.fallback_mode:
            try:
                prompt = f"""
                You are a compassionate mental health support assistant. Analyze this user message and provide emotional support.
                
                User Message: "{text}"
                
                Please provide:
                1. Primary emotions detected (comma-separated)
                2. Urgency level (low/medium/high) 
                3. Key support needs
                4. A compassionate, therapeutic response (2-3 paragraphs)
                
                Format your response as:
                EMOTIONS: [emotions]
                URGENCY: [urgency]
                NEEDS: [needs]
                RESPONSE: [your compassionate response here]
                """
                
                response = self.model.generate_content(prompt)
                return self._parse_ai_response(response.text)
                
            except Exception as e:
                st.error(f"❌ AI analysis failed: {e}")
                return self._simulated_analysis(text)
        else:
            return self._simulated_analysis(text)
    
    def _parse_ai_response(self, ai_text: str) -> dict:
        """Parse AI response into structured data"""
        lines = ai_text.split('\n')
        result = {
            'emotions': 'concerned',
            'urgency': 'medium', 
            'needs': 'emotional_support',
            'response': 'I hear you and I\'m here to support you through this.',
            'ai_generated': True
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith('EMOTIONS:'):
                result['emotions'] = line[9:].strip()
            elif line.startswith('URGENCY:'):
                result['urgency'] = line[8:].strip().lower()
            elif line.startswith('NEEDS:'):
                result['needs'] = line[6:].strip()
            elif line.startswith('RESPONSE:'):
                result['response'] = line[9:].strip()
                
        return result
    
    def _simulated_analysis(self, text: str) -> dict:
        """Advanced simulated AI analysis"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['die', 'suicide', 'kill myself', 'end it all', 'not worth living']):
            return {
                'emotions': 'desperate, hopeless, suicidal',
                'urgency': 'high',
                'needs': 'crisis_intervention',
                'response': """🚨 **I'm deeply concerned about what you're sharing**

I hear the pain and hopelessness in your words, and I want you to know that your life is precious. What you're experiencing right now is overwhelming, but these intense feelings, while very real, are temporary.

**Please reach out right now:**
• Call 988 - Suicide & Crisis Lifeline (24/7)
• Text HOME to 741741 - Crisis Text Line
• Call 911 if you're in immediate danger

You don't have to face this alone. There are people trained to help you through this exact moment. Your safety is the most important thing right now.""",
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['anxious', 'panic', 'overwhelmed', 'heart racing', 'cant breathe']):
            return {
                'emotions': 'anxious, overwhelmed, scared',
                'urgency': 'medium',
                'needs': 'anxiety_management', 
                'response': """💨 **I understand how overwhelming anxiety can feel**

That racing heart, difficulty breathing, and sense of losing control is your body's alarm system activated. While it feels terrifying, this is a false alarm - you are safe in this moment.

**Let's ground ourselves together:**
1. **Breathe with me**: Inhale for 4 counts, hold for 4, exhale for 6. Let's do this 3 times.
2. **5-4-3-2-1 Grounding**: Name 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, 1 thing you can taste.
3. **Remember**: This panic will pass. You've gotten through anxious moments before.

You're stronger than this feeling, even when it doesn't seem like it.""",
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['sad', 'depressed', 'hopeless', 'empty', 'nothing matters']):
            return {
                'emotions': 'sad, depressed, hopeless',
                'urgency': 'medium', 
                'needs': 'emotional_support',
                'response': """🤗 **I hear the heaviness you're carrying**

That empty, nothing-matters feeling can be one of the most isolating experiences. Please know that what you're describing matters deeply, and I'm here with you in it.

**What you're feeling is valid**, and it takes tremendous strength to articulate it. Depression often lies to us, making us believe this is how things will always be - but feelings, like weather, change and pass.

**Small steps for right now:**
- Be extra gentle with yourself today
- If getting out of bed feels impossible, that's okay
- Could you try one tiny comforting action? Maybe a sip of water or looking out a window

You're not alone in this, even when it feels that way.""",
                'ai_generated': False
            }
        else:
            return {
                'emotions': 'reflective, contemplative',
                'urgency': 'low',
                'needs': 'emotional_support',
                'response': """💫 **Thank you for sharing what's on your mind**

It takes courage to reach out and put your experiences into words. I'm here to listen without judgment, and whatever you're feeling right now is completely valid.

Sometimes just speaking our truth aloud can help lighten the load, even if just a little. You don't have to have everything figured out, and you don't have to face anything alone.

**I'm here to listen** and support you in whatever way feels helpful. Would you like to tell me more about what's been happening?""",
                'ai_generated': False
            }

# =============================================
# 🧠 MENTAL HEALTH AGENT SYSTEM
# =============================================

class MentalHealthAgent:
    """Mental Health Agent with configurable AI"""
    
    def __init__(self):
        self.ai = GeminiAIIntegration()
        self.crisis_keywords = {
            'suicidal': ['kill myself', 'end it all', 'suicide', 'want to die', 'not worth living'],
            'self_harm': ['cut myself', 'self harm', 'hurt myself', 'bleeding'],
            'panic': ['panic attack', 'cant breathe', 'heart racing', 'losing control'],
            'depression': ['hopeless', 'empty inside', 'no point', 'cant get out of bed']
        }
        
        self.resources = {
            "crisis": {
                "988 Suicide Prevention": "Call 988 - Available 24/7",
                "Crisis Text Line": "Text HOME to 741741", 
                "Emergency Services": "Call 911 for immediate help"
            },
            "therapy": {
                "BetterHelp": "Online therapy platform",
                "Psychology Today": "Find local therapists",
                "Open Path Collective": "Affordable therapy options"
            }
        }
    
    def configure_ai(self, api_key: str) -> bool:
        """Configure the AI with user API key"""
        return self.ai.configure_ai(api_key)
    
    async def chat(self, message: str, user_id: str = "anonymous") -> dict:
        """Main chat method"""
        start_time = time.time()
        
        # AI Analysis (real or simulated)
        ai_analysis = await self.ai.analyze_with_ai(message)
        
        # Crisis detection
        crisis_data = self._detect_crisis(message)
        
        # Generate enhanced response
        response_data = self._generate_enhanced_response(message, crisis_data, ai_analysis)
        
        processing_time = time.time() - start_time
        
        return {
            'user_id': user_id,
            'processing_time_seconds': round(processing_time, 2),
            'ai_analysis': ai_analysis,
            'crisis_assessment': crisis_data,
            'final_response': response_data,
            'timestamp': datetime.now().isoformat()
        }
    
    def _detect_crisis(self, text: str) -> dict:
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
    
    def _generate_enhanced_response(self, user_message: str, crisis_data: dict, ai_analysis: dict) -> dict:
        """Generate enhanced response"""
        crisis_level = crisis_data['crisis_level']
        emotions = ai_analysis['emotions']
        urgency = ai_analysis['urgency']
        ai_response = ai_analysis['response']
        
        # Add crisis resources if needed
        if crisis_level == 'high':
            enhanced_response = ai_response + self._get_crisis_resources()
        else:
            enhanced_response = ai_response
        
        return {
            "response_text": enhanced_response,
            "crisis_level": crisis_level,
            "emotions": emotions,
            "urgency": urgency,
            "resources": self._get_relevant_resources(crisis_level),
            "ai_used": ai_analysis['ai_generated'],
            "agents_involved": 4,
            "comprehensive_analysis": True
        }
    
    def _get_crisis_resources(self) -> str:
        """Get crisis resources text"""
        return """

🚨 **IMMEDIATE CRISIS SUPPORT:**
• 📞 **Call 988** - Suicide & Crisis Lifeline (24/7)
• 📱 **Text HOME** to 741741 - Crisis Text Line
• 🚑 **Call 911** - Emergency Services

Your safety is the absolute priority. Please reach out now."""
    
    def _get_relevant_resources(self, crisis_level: str) -> dict:
        """Get relevant resources"""
        if crisis_level == "high":
            return {k: v for k, v in self.resources.items() if k == "crisis"}
        else:
            return self.resources

# =============================================
# 🎨 STREAMLIT APP WITH API KEY INPUT
# =============================================

# Initialize the agent
mental_health_agent = MentalHealthAgent()

# Streamlit app configuration
st.set_page_config(
    page_title="MindMate - AI Mental Health Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .api-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .ai-status {
        text-align: center;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .ai-active {
        background-color: #e6f7f2;
        color: #00cc96;
        border: 2px solid #00cc96;
    }
    .ai-simulated {
        background-color: #fff4e6;
        color: #ffa500;
        border: 2px solid #ffa500;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 MindMate AI</div>', unsafe_allow_html=True)

# API Key Section (like Kaggle)
with st.expander("🔑 Connect Your Google AI API Key", expanded=True):
    st.markdown("""
    **Get your FREE API key:**
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Create a new API key (free)
    3. Paste it below to enable real AI
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        api_key = st.text_input(
            "Google AI API Key:",
            type="password",
            placeholder="Enter your API key here...",
            help="Get free API key from https://makersuite.google.com/app/apikey"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("🔗 Connect AI", use_container_width=True):
            if api_key:
                with st.spinner("Connecting to Gemini AI..."):
                    success = mental_health_agent.configure_ai(api_key)
                    if success:
                        st.success("✅ AI Connected Successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to connect. Check your API key.")
            else:
                st.warning("⚠️ Please enter an API key")

# AI Status Display
if mental_health_agent.ai.model and not mental_health_agent.ai.fallback_mode:
    st.markdown('<div class="ai-status ai-active">🤖 REAL GEMINI AI ACTIVE</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ai-status ai-simulated">🔄 ADVANCED SIMULATED AI ACTIVE</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🤖 AI System Status")
    
    if mental_health_agent.ai.model and not mental_health_agent.ai.fallback_mode:
        st.success("""
        **✅ Real Gemini AI Active**
        
        Your messages are being analyzed by Google's advanced AI models.
        """)
        st.metric("AI Mode", "Real AI")
        st.metric("API Status", "Connected")
    else:
        st.warning("""
        **🔄 Advanced Simulated AI**
        
        Using sophisticated mental health algorithms.
        Connect your API key for real AI.
        """)
        st.metric("AI Mode", "Simulated")
        st.metric("API Status", "Not Connected")
    
    st.header("🚨 Crisis Support")
    st.error("""
    **Emergency Contacts:**
    - 🆘 **Call 988** (24/7 Crisis Line)
    - 📱 **Text HOME** to 741741
    - 🚑 **Call 911** for emergencies
    """)
    
    st.header("💡 How to Get API Key")
    st.info("""
    1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with Google account
    3. Click "Create API Key"
    4. Copy and paste above
    5. It's **FREE** for limited use
    """)

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat with MindMate")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_id' not in st.session_state:
        import random
        st.session_state.user_id = f"user_{random.randint(10000, 99999)}"
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show AI status for assistant messages
            if message["role"] == "assistant" and "ai_used" in message:
                if message["ai_used"]:
                    st.caption("🤖 Generated by Real Gemini AI")
                else:
                    st.caption("🔄 Advanced Simulated Response")
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analyzing with AI..."):
                try:
                    # Process message
                    result = asyncio.run(mental_health_agent.chat(prompt, st.session_state.user_id))
                    
                    # Extract response
                    response_data = result['final_response']
                    response_text = response_data['response_text']
                    ai_used = response_data['ai_used']
                    
                    # Display response
                    st.markdown(response_text)
                    
                    # Show AI usage
                    if ai_used:
                        st.caption("🤖 Generated by Real Gemini AI")
                    else:
                        st.caption("🔄 Advanced Simulated AI")
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_text,
                        "ai_used": ai_used,
                        "crisis_level": response_data.get('crisis_level', 'low')
                    })
                    
                except Exception as e:
                    st.error(f"System error: {str(e)}")
                    fallback = "🤗 I'm here to listen and support you. Your feelings are valid and important."
                    st.markdown(fallback)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": fallback,
                        "ai_used": False
                    })

with col2:
    st.subheader("📊 Session Info")
    
    if st.session_state.messages:
        st.metric("Total Messages", len(st.session_state.messages))
        
        # Count AI vs simulated
        ai_count = len([m for m in st.session_state.messages if m.get("ai_used")])
        sim_count = len([m for m in st.session_state.messages if m.get("ai_used") == False])
        
        st.metric("AI Responses", ai_count)
        st.metric("Simulated Responses", sim_count)
    
    st.subheader("🔧 API Info")
    if mental_health_agent.ai.api_key:
        st.success("API Key: ✅ Connected")
        st.code(f"Key: {mental_health_agent.ai.api_key[:8]}...")
    else:
        st.warning("API Key: ❌ Not Connected")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>🧠 MindMate AI Mental Health Support</strong></p>
    <p><small>Connect your Google AI API key for enhanced AI-powered support</small></p>
</div>
""", unsafe_allow_html=True)
