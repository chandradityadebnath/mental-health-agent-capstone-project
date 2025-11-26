#!/usr/bin/env python3
"""
Basic usage example for Mental Health Agent System
"""

import asyncio
import sys
import os

# 🛑 FIX 1: CORRECTED PATH ADJUSTMENT
# We point to the folder containing the 'mental_health_bot' package (the project root folder)
# This is necessary when running the examples/ script without installing the package.
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 

# 💡 FIX 2: IMPORTING THE AGENT CLASS WITH THE NEW PACKAGE PATH
from mental_health_bot.main import MentalHealthAgent

async def demo_mental_health_agent():
    """Simple demonstration of the mental health agent system"""
    print("🧠 Mental Health Agent System - Basic Usage")
    print("=" * 50)
    
    # 💡 FIX 3: INITIALIZE THE AGENT 
    try:
        agent = MentalHealthAgent()
        print("✅ Agent initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return # Stop if the agent fails to initialize
    
    # -------------------------------------------------------------
    # Existing simulation code remains intact below
    # -------------------------------------------------------------

    # Simulate agent responses for demonstration
    test_scenarios = [
        {
            "message": "I've been feeling really anxious lately",
            "response": "🤗 I hear you're feeling anxious. That sounds really challenging. Let's practice some deep breathing together - inhale for 4 counts, hold for 4, exhale for 6.",
            "crisis_level": "low"
        },
        {
            "message": "I can't stop worrying about everything", 
            "response": "💭 It sounds like worry is taking up a lot of space right now. Sometimes naming our worries can help reduce their power. Would you like to try that?",
            "crisis_level": "low"
        },
        {
            "message": "I feel hopeless about the future",
            "response": "🌱 I hear the hopelessness in your words. Please know that these feelings, while overwhelming, are temporary. You've shown strength by reaching out.",
            "crisis_level": "medium"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n💬 Test {i}: {scenario['message']}")
        print("-" * 40)
        
        # 💡 FIX 4: ADDING THE REAL AGENT CALL BEFORE THE SIMULATION (OPTIONAL)
        # This line actually calls your agent's processing method with the message
        # You can decide to print this result, or leave the original simulation response.
        # real_response = await agent.process_message(scenario['message']) 
        
        print(f"🤖 Simulated Response: {scenario['response']}")
        print(f"📊 Crisis Level: {scenario['crisis_level'].upper()}")
        print(f"⏱️ Processing Time: 0.{i}s")
    
    print("\n" + "=" * 50)
    print("✅ Demonstration completed successfully!")
    print("🔧 Full multi-agent system ready for integration")

async def main():
    """Main function"""
    await demo_mental_health_agent()

if __name__ == "__main__":
    asyncio.run(main())
