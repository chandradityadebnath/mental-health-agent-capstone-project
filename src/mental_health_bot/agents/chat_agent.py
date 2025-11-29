import random

class ChatAgent:
    """
    A supportive AI agent that generates emotionally aware responses
    using emotion + crisis detection + generative patterns.
    """

    def __init__(self):
        # fallback supportive phrases
        self.supportive_responses = {
            "sad": [
                "I’m really sorry you're feeling this way. I'm here for you.",
                "It’s okay to feel sad. You’re not alone.",
                "Your feelings are valid. Do you want to talk more about it?"
            ],
            "anxious": [
                "It sounds like you’re feeling overwhelmed. Take a deep breath—I'm with you.",
                "Anxiety can be tough, but talking about it helps.",
                "You’re doing your best, and that’s enough. Let’s work through this together."
            ],
            "angry": [
                "It’s okay to feel angry. Something must have really affected you.",
                "If you want, you can tell me what triggered your anger.",
                "Anger often hides deeper hurt. I’m listening."
            ],
            "neutral": [
                "I'm glad you're sharing this with me.",
                "Thanks for opening up. Tell me more.",
                "I’m here to support you however I can."
            ],
            "happy": [
                "That's amazing! I'm genuinely happy for you!",
                "Love hearing positive things from you. Keep it going!",
                "Great! Want to tell me more about it?"
            ]
        }

    def generate_ai_style_response(self, message, emotion):
        """
        GENERATIVE-LIKE AI RESPONSE (offline)
        This simulates intelligent conversation WITHOUT using an external API.
        """        
        base = {
            "sad": "It sounds like you’re really hurt right now. That must be heavy on your heart.",
            "anxious": "Your mind seems really active, maybe overloaded. That can be exhausting.",
            "angry": "Your frustration is loud, and it means something important happened.",
            "neutral": "I hear you. Thanks for expressing yourself.",
            "happy": "Your positive energy really comes through. That’s wonderful!"
        }

        return f"{base.get(emotion, 'I hear you.')}\n\nFrom what you said: \"{message}\", it seems like this emotion is affecting you strongly. I'm here to support you step by step."

    def generate_response(self, user_message, emotion, crisis_flag=False):
        """
        FINAL RESPONSE GENERATOR
        Combines:
        ✔ crisis detection
        ✔ emotion detection
        ✔ generative feeling response
        ✔ supportive fallback lines
        """

        # Crisis mode
        if crisis_flag:
            return (
                "⚠️ **IMPORTANT NOTICE**\n\n"
                "It seems like you're going through a very intense or potentially harmful situation.\n"
                "You deserve immediate support and someone to talk to right now.\n\n"
                "**Please consider reaching out:**\n"
                "- Someone you deeply trust\n"
                "- A mental health professional\n"
                "- A local helpline in your country\n\n"
                "You are NOT alone. I'm here with you as well."
            )

        # Mix generative + supportive
        supportive = random.choice(self.supportive_responses.get(emotion, ["I'm here with you."]))
        ai_generated = self.generate_ai_style_response(user_message, emotion)

        return f"{supportive}\n\n---\n\n{ai_generated}"
