import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for the mental health agent system"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # System Settings
    MAX_RESPONSE_TIME = 5.0  # seconds
    ENABLE_ANALYTICS = True
    CRISIS_THRESHOLD = 0.7
    
    # Agent Settings
    AGENT_TIMEOUT = 10.0
    PARALLEL_PROCESSING = True
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configurations are present"""
        if not cls.GOOGLE_API_KEY:
            print("⚠️  Google API key not found. Using simulated AI mode.")
        return True
