import streamlit as st
from src.mental_health_bot.emotion_analyzer import EmotionAnalyzer
from src.mental_health_bot.agents.chat_agent import ChatAgent

# Load your ML/NLP models
emotion_model = EmotionAnalyzer()
chat_agent = ChatAgent()

st.set_page_config(page_title="MindMate - Mental Health AI", page_icon="🧠")

st.title("🧠 MindMate - Mental Health Support Agent")
st.write("Type how you feel below and the AI will respond with empathy and support.")

# User input
user_input = st.text_area("How are you feeling today?", height=150)

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please type something.")
    else:
        # Emotion detection
        emotion = emotion_model.predict(user_input)

        # AI response generation
        response = chat_agent.generate_response(user_input, emotion)

        # Display
        st.subheader("😔 Detected Emotion:")
        st.write(f"**{emotion}**")

        st.subheader("🤖 MindMate AI Response:")
        st.write(response)
