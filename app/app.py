import streamlit as st
import asyncio
import time
from datetime import datetime
import random
import google.generativeai as genai

# =========================
# 🧠 GEMINI AI INTEGRATION
# =========================
class GeminiAIIntegration:
    """Gemini AI Integration with proper async handling"""

    def __init__(self):
        self.model = None
        self.fallback_mode = True
        self.api_key = None

    def configure_ai(self, api_key: str):
        """Configure AI with API key"""
        if not api_key or not api_key.strip():
            st.error("❌ Please enter a valid API key")
            return False

        try:
            api_key = api_key.strip()
            self.api_key = api_key
            genai.configure(api_key=api_key)

            try:
                self.model = genai.GenerativeModel("gemini-pro")
                test_response = self.model.generate_content("Hello")
                self.fallback_mode = False
                st.session_state.api_key_connected = True
                st.session_state.ai_model = "gemini-pro"
                st.success("✅ API Key Valid! Real AI Activated!")
                return True
            except Exception as e:
                st.error(f"❌ API Connection Failed: {e}")
                self.fallback_mode = True
                st.session_state.api_key_connected = False
                return False

        except Exception as e:
            st.error(f"❌ Configuration Failed: {e}")
            self.fallback_mode = True
            st.session_state.api_key_connected = False
            return False

    async def analyze_with_ai(self, text: str) -> dict:
        """Analyze text with AI or fallback simulated AI"""
        use_real_ai = (self.model is not None and not self.fallback_mode and st.session_state.get("api_key_connected", False))
        if use_real_ai:
            try:
                prompt = f"""Please provide a compassionate response to this: "{text}" """
                response = self.model.generate_content(prompt)
                return {
                    "emotions": "ai_analyzed",
                    "urgency": "medium",
                    "needs": "ai_determined",
                    "response": response.text,
                    "ai_generated": True
                }
            except Exception as e:
                return self._simulated_analysis(text)
        else:
            return self._simulated_analysis(text)

    def _simulated_analysis(self, text: str) -> dict:
        """Fallback simulated AI responses based on emotion keywords"""
        text_lower = text.lower()

        # CRISIS
        if any(word in text_lower for word in ['kill myself', 'suicide', 'end my life']):
            responses = [
                "🚨 Immediate Support Available: Call 988 or Text HOME to 741741",
                "🚨 Crisis: Professionals can help. Call 911 or 988 now."
            ]
            return {"emotions":"desperate","urgency":"high","needs":"crisis_intervention",
                    "response": random.choice(responses), "ai_generated": False}

        # SAD
        elif any(word in text_lower for word in ['sad','depressed','hopeless']):
            responses = [
                "I hear your sadness. Can you share what’s weighing on you?",
                "It’s okay to feel low. I’m here to listen."
            ]
            return {"emotions":"sad","urgency":"medium","needs":"emotional_support",
                    "response": random.choice(responses), "ai_generated": False}

        # HAPPY
        elif any(word in text_lower for word in ['happy','good','great','joy']):
            responses = [
                "That’s wonderful! What’s bringing you joy today?",
                "I’m glad to hear you’re happy! Celebrate the moment."
            ]
            return {"emotions":"happy","urgency":"low","needs":"celebration",
                    "response": random.choice(responses), "ai_generated": False}

        # ANGRY
        elif any(word in text_lower for word in ['angry','mad','furious']):
            responses = [
                "I hear your anger. Let’s explore what’s causing it.",
                "Anger is valid. How can we channel it constructively?"
            ]
            return {"emotions":"angry","urgency":"medium","needs":"anger_management",
                    "response": random.choice(responses), "ai_generated": False}

        # ANXIOUS
        elif any(word in text_lower for word in ['anxious','worried','panic']):
            responses = [
                "Anxiety can be overwhelming. Let’s try to ground ourselves.",
                "I understand your worry. Take a deep breath with me."
            ]
            return {"emotions":"anxious","urgency":"medium","needs":"anxiety_management",
                    "response": random.choice(responses), "ai_generated": False}

        # DEFAULT
        else:
            responses = [
                "Thank you for sharing. How can I best support you?",
                "I’m here to listen. Tell me more about what’s on your mind."
            ]
            return {"emotions":"neutral","urgency":"low","needs":"connection",
                    "response": random.choice(responses), "ai_generated": False}


# =========================
# Mental Health Agent
# =========================
class MentalHealthAgent:
    def __init__(self):
        self.ai = GeminiAIIntegration()
        if 'api_key_connected' not in st.session_state:
            st.session_state.api_key_connected = False
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def configure_ai(self, api_key: str) -> bool:
        return self.ai.configure_ai(api_key)

    async def chat(self, message: str, user_id: str = "anonymous") -> dict:
        start_time = time.time()
        ai_analysis = await self.ai.analyze_with_ai(message)
        processing_time = time.time() - start_time
        return {
            "user_id": user_id,
            "processing_time_seconds": round(processing_time, 2),
            "final_response": {
                "response_text": ai_analysis['response'],
                "crisis_level": ai_analysis['urgency'],
                "emotions": ai_analysis['emotions'],
                "ai_used": ai_analysis['ai_generated'],
                "agents_involved": 4
            },
            "timestamp": datetime.now().isoformat()
        }


# =========================
# Streamlit App
# =========================
mental_health_agent = MentalHealthAgent()

st.set_page_config(page_title="MindMate", page_icon="🧠", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main-header { font-size:2.5rem; color:#1f77b4; text-align:center; font-weight:bold; }
.ai-active { background:#e6f7f2; color:#00cc96; padding:1rem; border-radius:10px; text-align:center; border:2px solid #00cc96; margin:1rem 0;}
.ai-simulated { background:#fff4e6; color:#ffa500; padding:1rem; border-radius:10px; text-align:center; border:2px solid #ffa500; margin:1rem 0;}
.crisis-high { border-left:5px solid #ff4b4b; background:#ffe6e6; padding:1.5rem; border-radius:10px; margin:1rem 0;}
.user-message { background:#e3f2fd; padding:1rem; border-radius:10px; margin:0.5rem 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧠 MindMate</div>', unsafe_allow_html=True)

# API Key Section
with st.expander("🔑 API Key Setup (Optional)", expanded=not st.session_state.get('api_key_connected', False)):
    st.markdown("**Get FREE API Key:** [Google AI Studio](https://makersuite.google.com/app/apikey)")
    api_key = st.text_input("API Key:", type="password", key="api_key_input")
    if st.button("🔗 Connect AI"):
        if api_key:
            success = mental_health_agent.configure_ai(api_key)
            if success:
                st.balloons()
                st.experimental_rerun()
        else:
            st.warning("⚠️ Please enter an API key")

# AI Status
if st.session_state.get('api_key_connected', False):
    st.markdown('<div class="ai-active">🤖 REAL AI ACTIVE</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ai-simulated">🔄 ADVANCED SIMULATED AI ACTIVE</div>', unsafe_allow_html=True)

# Chat interface
st.subheader("💬 Chat with MindMate")

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        if message.get("crisis_level") == "high":
            st.markdown(f'<div class="crisis-high">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])
        st.caption("🤖 Real AI" if message["ai_used"] else "🔄 Simulated AI")

# Chat input
if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.spinner("🧠 Thinking..."):
        response = asyncio.run(mental_health_agent.chat(prompt))
        resp_data = response['final_response']
        st.session_state.messages.append({
            "role":"assistant",
            "content": resp_data['response_text'],
            "ai_used": resp_data['ai_used'],
            "crisis_level": resp_data['crisis_level']
        })
        st.experimental_rerun()

# Clear chat
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()

# Quick examples
st.subheader("💡 Try These Examples")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("😔 I'm feeling sad"): st.session_state.messages.append({"role":"user","content":"I'm feeling sad"}); st.experimental_rerun()
with col2:
    if st.button("😊 I'm happy today"): st.session_state.messages.append({"role":"user","content":"I'm happy today"}); st.experimental_rerun()
with col3:
    if st.button("😡 I'm so angry"): st.session_state.messages.append({"role":"user","content":"I'm so angry"}); st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;'><p><strong>🧠 MindMate Mental Health Support</strong></p><p><small>Always here to listen 🤗 | Emergency: Call 988</small></p></div>", unsafe_allow_html=True)
