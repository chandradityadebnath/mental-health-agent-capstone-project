import streamlit as st
import sys
import os
import asyncio
import nest_asyncio

# Apply nest_asyncio to handle async in Streamlit
nest_asyncio.apply()

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

try:
    from mental_health_bot import mental_health_agent
    st.success("✅ Mental Health Agent System Loaded Successfully!")
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.info("Trying alternative import...")
    
    # Fallback: Create a simple version directly
    class FallbackMentalHealthAgent:
        async def chat(self, message: str, user_id: str = "anonymous"):
            return {
                'final_response': {
                    'response_text': f"🤗 I hear you saying: '{message}'. While the full AI system is loading, please know that your feelings are valid. If you're in crisis, please call 988 immediately.",
                    'crisis_level': 'low',
                    'emotions': 'processing',
                    'agents_involved': 1
                }
            }
    
    mental_health_agent = FallbackMentalHealthAgent()
    st.warning("⚠️ Using fallback mode - some features may be limited")

# Streamlit app configuration
st.set_page_config(
    page_title="MindMate - Mental Health Support",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
        white-space: pre-line;
    }
    .crisis-high {
        border-left: 5px solid #ff4b4b;
        background-color: #ffe6e6;
    }
    .crisis-medium {
        border-left: 5px solid #ffa500;
        background-color: #fff4e6;
    }
    .crisis-low {
        border-left: 5px solid #00cc96;
        background-color: #e6f7f2;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 MindMate - Mental Health Support</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">24/7 AI-powered mental health support with crisis detection</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About MindMate")
    st.write("""
    **MindMate** provides compassionate mental health support through AI technology.
    
    **Key Features:**
    - 🤖 Intelligent crisis detection
    - 🎯 Emotional analysis
    - 🛡️ Safety-first approach
    - 💝 24/7 availability
    
    **How it works:**
    1. Share what you're feeling
    2. AI analyzes emotions and crisis level
    3. Get personalized support
    4. Access resources if needed
    """)
    
    st.header("🚨 Immediate Help")
    st.error("""
    **If you're in crisis:**
    - 🆘 Call 988 (Suicide Prevention)
    - 📱 Text HOME to 741741
    - 🚑 Call 911 for emergencies
    - 🏥 Go to nearest emergency room
    """)
    
    st.header("🔒 Privacy")
    st.info("""
    Your conversations are:
    - Private and secure
    - Anonymous
    - Never stored permanently
    - Always respectful
    """)

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Start Conversation")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_id' not in st.session_state:
        import random
        st.session_state.user_id = f"user_{random.randint(1000, 9999)}"
    
    # Display chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            # Determine crisis level for styling
            crisis_level = message.get("crisis_level", "low")
            css_class = f"response-box crisis-{crisis_level}"
            st.markdown(f'<div class="{css_class}"><strong>MindMate:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        with st.spinner("🧠 Analyzing your message..."):
            try:
                # Process message through the agent system
                result = asyncio.run(mental_health_agent.chat(prompt, st.session_state.user_id))
                
                # Extract response
                response_data = result['final_response']
                response_text = response_data['response_text']
                crisis_level = response_data.get('crisis_level', 'low')
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "crisis_level": crisis_level
                })
                
                # Rerun to update display
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                # Fallback response
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "🤗 I'm here to listen. Please know that your feelings are valid. If you're in crisis, please call 988 immediately.",
                    "crisis_level": "low"
                })
                st.rerun()

with col2:
    st.subheader("📊 Conversation Info")
    
    if st.session_state.messages:
        st.metric("Messages", len(st.session_state.messages))
        
        # Show crisis level of last message
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
            last_crisis = st.session_state.messages[-1].get("crisis_level", "low")
            crisis_display = {
                "high": "🔴 High",
                "medium": "🟡 Medium", 
                "low": "🟢 Low"
            }
            st.metric("Current Crisis Level", crisis_display.get(last_crisis, "🟢 Low"))
    
    st.subheader("💡 Quick Examples")
    example_messages = [
        "I've been feeling really sad lately",
        "I'm having a panic attack",
        "I feel lonely and isolated",
        "I'm stressed about work",
        "I just need someone to talk to"
    ]
    
    for example in example_messages:
        if st.button(example, key=example):
            # Simulate clicking this message
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🧠 <strong>MindMate</strong> - Your AI Mental Health Companion | Always here to listen 🤗</p>
    <p><small>This is an AI support system. For medical emergencies, please contact professional healthcare providers.</small></p>
</div>
""", unsafe_allow_html=True)
