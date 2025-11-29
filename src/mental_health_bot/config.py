from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
from kaggle_secrets import UserSecretsClient

class GeminiAIConfigurator:
    """Intelligent API configuration that finds working models automatically"""
    
    def __init__(self):
        self.working_models = []
        self.primary_model = None
        self.fallback_mode = False
        
    def discover_models(self):
        """Discover all available Gemini models"""
        try:
            user_secrets = UserSecretsClient()
            api_key = user_secrets.get_secret('GOOGLE_API_KEY')
            
            if not api_key:
                api_key = user_secrets.get_secret('GOOGLE_API_KEY')
                
            if not api_key:
                # For local development, use environment variable
                api_key = os.getenv('GOOGLE_API_KEY')
                if not api_key:
                    raise ValueError("🔑 No API key found!")
                    
            genai.configure(api_key=api_key)
            
            print("🔍 Discovering available AI models...")
            available_models = []
            
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
                    print(f"   🤖 {model.name}")
            
            # Priority order for models
            priority_models = [
                'models/gemini-2.0-flash-lite',
                'models/gemini-2.0-flash-lite-001',
                'models/gemma-3-1b-it',
                'models/gemini-2.0-flash',
                'models/gemini-2.5-flash',
                'models/gemini-pro-latest'
            ]
            
            # Test models in priority order
            for model_name in priority_models:
                if model_name in available_models:
                    try:
                        print(f"🧪 Testing: {model_name}")
                        model = genai.GenerativeModel(model_name)
                        test_response = model.generate_content("Say 'AI Ready'")
                        self.working_models.append(model_name)
                        print(f"   ✅ {model_name} - SUCCESS!")
                        
                        if not self.primary_model:
                            self.primary_model = model
                            self.primary_model_name = model_name
                            
                    except Exception as e:
                        print(f"   ❌ {model_name} - Failed")
                        continue
            
            if self.primary_model:
                print(f"🎯 PRIMARY MODEL SELECTED: {self.primary_model_name}")
                return True
            else:
                print("🚨 No working AI models found - Using Advanced Simulated AI")
                self.fallback_mode = True
                return False
                
        except Exception as e:
            print(f"❌ AI Configuration Failed: {e}")
            print("🔄 Switching to Advanced Simulated AI Mode...")
            self.fallback_mode = True
            return False

# Global configuration
AI_CONFIG = GeminiAIConfigurator()
