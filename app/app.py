import streamlit as st
import asyncio
from src.mental_health_bot.ai_orchestrator import AIAgentOrchestrator

orchestrator = AIAgentOrchestrator()

st.set_page_config(page_title="MindMate AI", page_icon="🧠")

st.title("🧠 MindMate Mental Health Support AI")
st.write("Talk to me — I'm here to support you ❤️")

user_input = st.text_area("How are you feeling today?", height=150)

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        result = asyncio.run(orchestrator.process(user_input))

        st.subheader("🎭 Detected Emotions")
        st.write(result["emotions"])

        if result["crisis_level"] == "high":
            st.error("⚠️ Crisis Situation Detected")

        st.subheader("🤖 AI Response")
        st.write(result["response"])
