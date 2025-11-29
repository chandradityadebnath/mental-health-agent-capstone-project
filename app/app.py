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
# 🧠 GEMINI AI INTEGRATION - FIXED CRISIS DETECTION
# =============================================

class GeminiAIIntegration:
    """Gemini AI Integration with proper crisis detection"""
    
    def __init__(self):
        self.model = None
        self.fallback_mode = True
        self.api_key = None
        
    def configure_ai(self, api_key: str):
        """Configure AI with user-provided API key"""
        if not api_key:
            return False
            
        try:
            genai.configure(api_key=api_key)
            
            # Try different models in priority order
            models_to_try = [
                'models/gemini-2.0-flash-lite',
                'models/gemini-2.0-flash-lite-001', 
                'models/gemma-3-1b-it',
                'models/gemini-2.0-flash',
                'models/gemini-pro'
            ]
            
            for model_name in models_to_try:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    # Test the model with a simple prompt
                    test_response = self.model.generate_content("Say 'AI Ready'")
                    self.fallback_mode = False
                    self.api_key = api_key
                    
                    # Store in session state
                    st.session_state.api_key_connected = True
                    st.session_state.api_key = api_key
                    st.session_state.ai_model = model_name
                    
                    return True
                except Exception as e:
                    continue
                    
            # If no models work
            st.session_state.api_key_connected = False
            self.fallback_mode = True
            return False
            
        except Exception as e:
            st.session_state.api_key_connected = False
            self.fallback_mode = True
            return False
    
    async def analyze_with_ai(self, text: str) -> dict:
        """Analyze text with real Gemini AI - FIXED TO ACTUALLY USE AI"""
        print(f"🔍 Analyzing: {text}")  # Debug
        
        # Check if we should use real AI
        if self.model and not self.fallback_mode and st.session_state.api_key_connected:
            try:
                # **FIXED: Better prompt for crisis situations**
                prompt = f"""
                USER MESSAGE: "{text}"
                
                As a mental health support assistant, analyze this message and provide:
                
                1. EMOTIONS: Comma-separated primary emotions
                2. URGENCY: low/medium/high based on suicide risk
                3. NEEDS: Key support needs
                4. RESPONSE: A compassionate, appropriate response
                
                If the user mentions suicide, self-harm, or wanting to die, respond with URGENCY: high and provide immediate crisis resources.
                """
                
                response = self.model.generate_content(prompt)
                print(f"🤖 AI Response: {response.text}")  # Debug
                return self._parse_ai_response(response.text)
                
            except Exception as e:
                print(f"❌ AI Error: {e}")  # Debug
                return self._simulated_analysis(text)
        else:
            print("🔄 Using simulated AI")  # Debug
            return self._simulated_analysis(text)
    
    def _parse_ai_response(self, ai_text: str) -> dict:
        """Parse AI response into structured data"""
        print(f"📝 Parsing AI response: {ai_text}")  # Debug
        
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
        """Advanced simulated AI analysis - FIXED CRISIS DETECTION"""
        text_lower = text.lower()
        print(f"🔍 Simulated analysis for: {text_lower}")  # Debug
        
        # **FIXED: Better crisis detection**
        if any(word in text_lower for word in ['kill myself', 'suicide', 'end my life', 'want to die', 'not worth living']):
            print("🚨 HIGH CRISIS DETECTED")  # Debug
            return {
                'emotions': 'desperate, hopeless, suicidal',
                'urgency': 'high',
                'needs': 'crisis_intervention',
                'response': """🚨 **I'm deeply concerned about what you're sharing**

I hear that you're feeling hopeless and considering ending your life. Please know that your life is precious and there are people who want to help you right now.

**IMMEDIATE CRISIS SUPPORT:**
• 📞 **Call 988** - Suicide & Crisis Lifeline (24/7)
• 📱 **Text HOME** to 741741 - Crisis Text Line
• 🚑 **Call 911** if you're in immediate danger

You don't have to face this alone. These intense feelings, while overwhelming, are temporary. Professional help is available right now.

**Please reach out immediately.** Your safety is the most important thing.""",
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['sad', 'depressed', 'hopeless', 'empty', 'crying']):
            print("🟡 MEDIUM CRISIS DETECTED")  # Debug
            return {
                'emotions': 'sad, depressed, hopeless',
                'urgency': 'medium', 
                'needs': 'emotional_support',
                'response': """🤗 **I hear the pain in your words**

That heavy, hopeless feeling can be incredibly overwhelming. Thank you for having the courage to share what you're going through.

**You're not alone in this.** What you're feeling is valid, and it takes strength to acknowledge when we're struggling.

**Some gentle suggestions:**
- Be extra kind to yourself today
- Reach out to one trusted person
- Try a small comforting activity
- Remember: feelings are temporary, even when they feel permanent

Would you like to talk more about what's been weighing on you?""",
                'ai_generated': False
            }
        elif any(word in text_lower for word in ['anxious', 'panic', 'overwhelmed', 'stress']):
            print("🟡 ANXIETY DETECTED")  # Debug
            return {
                'emotions': 'anxious, overwhelmed, scared',
                'urgency': 'medium',
                'needs': 'anxiety_management', 
                'response': """💨 **I understand how overwhelming anxiety can feel**

That racing mind and physical tension is your body's alarm system. While it feels scary, you are safe in this moment.

**Let's try some grounding together:**
1. **Breathe with me**: Inhale 4 counts, hold 4, exhale 6
2. **5-4-3-2-1**: 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste
3. **Remember**: This anxiety will pass. You've gotten through anxious moments before.

You're stronger than this feeling, even when it doesn't seem like it.""",
                'ai_generated': False
            }
        else:
            print("🟢 LOW CRISIS - GENERAL RESPONSE")  # Debug
            return {
                'emotions': 'reflective, contemplative',
                'urgency': 'low',
                'needs': 'emotional_support',
                'response': """💫 **Thank you for sharing**

I appreciate you opening up about what's on your mind. It takes courage to reach out, and I'm here to listen without judgment.

Whatever you're experiencing right now is valid, and you don't have to face it alone. Sometimes just putting our experiences into words can help lighten the load.

**I'm here to listen** and support you in whatever way feels helpful. Would you like to tell me more about what's been happening?""",
                'ai_generated': False
            }

# =============================================
# 🧠 MENTAL HEALTH AGENT SYSTEM - FIXED
# =============================================

class MentalHealthAgent:
    """Mental Health Agent with proper crisis handling"""
    
    def __init__(self):
        self.ai = GeminiAIIntegration()
        
        # **FIXED: More comprehensive crisis keywords**
        self.crisis_keywords = {
            'suicidal': ['kill myself', 'suicide', 'end my life', 'want to die', 'not worth living', 'end it all', 'better off dead'],
            'self_harm': ['cut myself', 'self harm', 'hurt myself', 'bleeding', 'harm myself'],
            'panic': ['panic attack', 'cant breathe', 'heart racing', 'losing control', 'going crazy'],
            'depression': ['hopeless', 'empty inside', 'no point', 'cant get out of bed', 'nothing matters']
        }
        
        # Initialize session state if not exists
        if 'api_key_connected' not in st.session_state:
            st.session_state.api_key_connected = False
        if 'api_key' not in st.session_state:
            st.session_state.api_key = None
        if 'ai_model' not in st.session_state:
            st.session_state.ai_model = None
        
        self.resources = {
            "crisis": {
                "988 Suicide Prevention": "Call 988 - Available 24/7",
                "Crisis Text Line": "Text HOME to 741741", 
                "Emergency Services": "Call 911 for immediate help"
            }
        }
    
    def configure_ai(self, api_key: str) -> bool:
        """Configure the AI with user API key"""
        return self.ai.configure_ai(api_key)
    
    def is_ai_connected(self) -> bool:
        """Check if AI is connected"""
        return st.session_state.api_key_connected
    
    async def chat(self, message: str, user_id: str = "anonymous") -> dict:
        """Main chat method - FIXED TO USE AI PROPERLY"""
        start_time = time.time()
        print(f"💬 Processing: {message}")  # Debug
        
        # **FIXED: Always use AI analysis first if connected**
        ai_analysis = await self.ai.analyze_with_ai(message)
        
        # **FIXED: Enhanced crisis detection**
        crisis_data = self._detect_crisis(message)
        
        # **FIXED: Generate appropriate response based on analysis**
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
        """Enhanced crisis detection - FIXED"""
        text_lower = text.lower()
        print(f"🔍 Crisis detection for: {text_lower}")  # Debug
        
        crisis_level = "low"
        detected_issues = []
        
        # **FIXED: Better keyword matching**
        for category, keywords in self.crisis_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_issues.append(category)
                    if category in ['suicidal', 'self_harm']:
                        crisis_level = "high"
                        break  # Immediate high crisis
                    elif crisis_level != "high" and category in ['panic']:
                        crisis_level = "medium"
        
        print(f"🚨 Crisis level: {crisis_level}")  # Debug
        return {
            "crisis_level": crisis_level,
            "detected_issues": detected_issues,
            "immediate_action_required": crisis_level in ["high", "medium"]
        }
    
    def _generate_enhanced_response(self, user_message: str, crisis_data: dict, ai_analysis: dict) -> dict:
        """Generate enhanced response - FIXED"""
        crisis_level = crisis_data['crisis_level']
        emotions = ai_analysis['emotions']
        urgency = ai_analysis['urgency']
        ai_response = ai_analysis['response']
        
        print(f"🎯 Generating response - Crisis: {crisis_level}, AI: {ai_analysis['ai_generated']}")  # Debug
        
        # **FIXED: Use AI response directly, only enhance for high crisis**
        if crisis_level == 'high':
            # Add crisis resources to AI response
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

---
🚨 **IMMEDIATE CRISIS SUPPORT:**
• 📞 **Call 988** - Suicide & Crisis Lifeline (24/7)
• 📱 **Text HOME** to 741741 - Crisis Text Line  
• 🚑 **Call 911** - Emergency Services

**Your safety is the absolute priority. Please reach out now.**"""
    
    def _get_relevant_resources(self, crisis_level: str) -> dict:
        """Get relevant resources"""
        if crisis_level == "high":
            return {k: v for k, v in self.resources.items() if k == "crisis"}
        else:
            return self.resources

# =============================================
# 🎨 STREAMLIT APP - FIXED
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
    .crisis-high {
        border-left: 6px solid #ff4b4b;
        background-color: #ffe6e6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .crisis-medium {
        border-left: 6px solid #ffa500;
        background-color: #fff4e6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .crisis-low {
        border-left: 6px solid #00cc96;
        background-color: #e6f7f2;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 MindMate AI</div>', unsafe_allow_html=True)

# API Key Section
with st.expander("🔑 Connect Your Google AI API Key", expanded=not st.session_state.get('api_key_connected', False)):
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
            help="Get free API key from https://makersuite.google.com/app/apikey",
            key="api_key_input"
        )
    
    with col2:
        st.write("") 
        st.write("") 
        connect_button = st.button("🔗 Connect AI", use_container_width=True, type="primary")
    
    if connect_button:
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
if st.session_state.get('api_key_connected', False):
    st.success(f"🤖 **REAL GEMINI AI ACTIVE** - Connected to: {st.session_state.get('ai_model', 'Unknown')}")
else:
    st.info("🔄 **ADVANCED SIMULATED AI ACTIVE** - Connect API key for real AI")

# Main chat interface
st.subheader("💬 Chat with MindMate")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        crisis_level = message.get("crisis_level", "low")
        css_class = f"crisis-{crisis_level}"
        with st.chat_message("assistant"):
            st.markdown(f'<div class="{css_class}">{message["content"]}</div>', unsafe_allow_html=True)
            
            # Show AI status
            if message.get("ai_used"):
                st.caption("🤖 Generated by Real Gemini AI")
            else:
                st.caption("🔄 Advanced Simulated Response")

# Chat input
if prompt := st.chat_input("How are you feeling today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🧠 Analyzing with AI..."):
            try:
                # Process message
                result = asyncio.run(mental_health_agent.chat(prompt))
                
                # Extract response
                response_data = result['final_response']
                response_text = response_data['response_text']
                ai_used = response_data['ai_used']
                crisis_level = response_data.get('crisis_level', 'low')
                
                # Display with appropriate styling
                css_class = f"crisis-{crisis_level}"
                st.markdown(f'<div class="{css_class}">{response_text}</div>', unsafe_allow_html=True)
                
                # Show AI usage
                if ai_used:
                    st.caption("🤖 Generated by Real Gemini AI")
                else:
                    st.caption("🔄 Advanced Simulated Response")
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "ai_used": ai_used,
                    "crisis_level": crisis_level
                })
                
            except Exception as e:
                st.error(f"System error: {str(e)}")
                fallback = "🤗 I'm here to listen and support you. Your feelings are valid and important."
                st.markdown(fallback)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": fallback,
                    "ai_used": False,
                    "crisis_level": "low"
                })
    
    st.rerun()
