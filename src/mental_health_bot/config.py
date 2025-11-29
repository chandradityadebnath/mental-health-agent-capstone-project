from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiAIConfigurator:
    """Intelligent API configuration that finds working models automatically"""
    
    def __init__(self):
        self.working_models = []
        self.primary_model = None
        self.fallback_mode = False
        
    def discover_models(self):
        """Discover all available Gemini models"""
        try:
            # Get API key from environment variable
            api_key = os.getenv('GOOGLE_API_KEY')
            
            if not api_key:
                raise ValueError("🔑 No GOOGLE_API_KEY found in environment variables!")
                
            genai.configure(api_key=api_key)
            
            print("🔍 Discovering available AI models...")
            
            # For local development, use a simpler approach
            try:
                # Try to use Gemini 2.0 Flash Lite (free tier)
                self.primary_model = genai.GenerativeModel('gemini-2.0-flash-lite')
                test_response = self.primary_model.generate_content("Say 'AI Ready'")
                self.primary_model_name = 'gemini-2.0-flash-lite'
                print("✅ Gemini AI configured successfully!")
                self.fallback_mode = False
                return True
            except Exception as e:
                print(f"❌ Gemini AI failed: {e}")
                print("🔄 Switching to Advanced Simulated AI Mode...")
                self.fallback_mode = True
                return False
                
        except Exception as e:
            print(f"❌ AI Configuration Failed: {e}")
            print("🔄 Switching to Advanced Simulated AI Mode...")
            self.fallback_mode = True
            return False

# Global configuration
AI_CONFIG = GeminiAIConfigurator()
AI_CONFIG.discover_models()
