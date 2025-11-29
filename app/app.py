import streamlit as st
import sys
import os
import asyncio
from typing import List, Dict, Any

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

try:
    from mental_health_bot.main import mental_health_agent
    st.success("✅ MindMate - Mental Health Agent System Loaded Successfully!")
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.info("Please check that all dependencies are installed and files are properly structured.")

# Streamlit app
st.set_page_config(
    page_title="MindMate - Mental Health Support",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 MindMate - Mental Health Support</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("About MindMate")
    st.write("""
    MindMate provides 24/7 mental health support through AI-powered conversations.
    
    **Features:**
    - Crisis detection & intervention
    - Emotional analysis
    - Personalized support planning
    - Resource matching
    - 4 specialized AI agents working together
    """)
    
    st.header("Safety Notice")
    st.warning("""
    **For immediate crisis support:**
    - Call 988 (Suicide Prevention)
    - Text HOME to 741741
    - Call 911 for emergencies
    """)

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat with MindMate")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{hash(str(st.session_state)) % 10000}"
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analyzing with multiple AI agents..."):
                try:
                    # Process message through the agent system
                    result = asyncio.run(mental_health_agent.chat(prompt, st.session_state.user_id))
                    
                    # Display the response
                    response_text = result['final_response']['response_text']
                    crisis_level = result['final_response']['crisis_level']
                    
                    # Apply appropriate styling based on crisis level
                    if crisis_level == 'high':
                        st.markdown(f'<div class="response-box crisis-high">{response_text}</div>', unsafe_allow_html=True)
                    elif crisis_level == 'medium':
                        st.markdown(f'<div class="response-box crisis-medium">{response_text}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="response-box crisis-low">{response_text}</div>', unsafe_allow_html=True)
                    
                    # Add to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    st.error(f"Sorry, I encountered an error: {str(e)}")
                    st.info("Please try again or check the system configuration.")

with col2:
    st.subheader("📊 System Info")
    
    if st.session_state.messages:
        st.metric("Messages Exchanged", len(st.session_state.messages))
        
        # Show last response analysis if available
        if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "assistant":
            try:
                result = asyncio.run(mental_health_agent.chat("test", st.session_state.user_id))
                crisis_level = result['final_response']['crisis_level']
                emotions = result['final_response']['emotions']
                
                st.write("**Last Analysis:**")
                st.write(f"**Crisis Level:** {crisis_level.upper()}")
                st.write(f"**Emotions:** {emotions}")
                st.write(f"**Agents Used:** {result['final_response']['agents_involved']}")
                
            except:
                st.write("Analysis data unavailable")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>MindMate - Mental Health Support System | Always here to listen 🤗</p>
</div>
""", unsafe_allow_html=True)
