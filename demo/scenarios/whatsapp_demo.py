"""
AI Tutor South Africa - Interactive Demo Script
================================================

Run this script to simulate a live WhatsApp interaction.
Perfect for hackathon presentation demo.

Usage: python demo/scenarios/whatsapp_demo.py
"""

import time
import json
from datetime import datetime


def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_message(sender: str, message: str):
    """Print a chat message"""
    icon = "👤 LEARNER" if sender == "learner" else "🤖 AI TUTOR"
    print(f"\n{icon}:")
    print("-" * 40)
    print(message)
    print("-" * 40)


def simulate_typing():
    """Simulate typing delay"""
    print("\n⏳ AI Tutor is typing...", end="", flush=True)
    time.sleep(1.5)
    print("\r" + " " * 30 + "\r", end="")


def run_demo():
    """
    Run the interactive WhatsApp demo.
    Simulates a real conversation with the AI tutor.
    """
    
    print_header("AI TUTOR SOUTH AFRICA - LIVE DEMO")
    print("\n📱 Simulating WhatsApp conversation...")
    print("👤 Learner: Thabo, Grade 9")
    print("📚 Topic: Linear Equations")
    print("\nPress Enter to continue through each step...")
    
    # ==========================================
    # STEP 1: Welcome
    # ==========================================
    input("\n[Press Enter to start...]")
    
    print_message("learner", "Hi")
    
    simulate_typing()
    
    print_message("tutor", """👋 Hello Thabo! Welcome to AI Tutor! 🎓

I'm your personal Mathematics tutor. I'll help you learn to solve problems step by step.

You're in Grade 9. Ready to learn!

What would you like help with today?

Examples:
• "Help me solve: 2x + 5 = 13"
• "I don't understand fractions"
• "Practice algebra"

Let's go! 🚀""")
    
    # ==========================================
    # STEP 2: The Problem
    # ==========================================
    input("\n[Press Enter for learner's question...]")
    
    print_message("learner", "Help me solve: 2x + 5 = 13")
    
    simulate_typing()
    
    print_message("tutor", """Great question! Let's solve this together. 🎯

I won't give you the answer - instead, I'll help YOU find it.

First, tell me: What do you think is the goal when solving this equation?

💡 Hint: Think about what we're trying to find.""")
    
    # ==========================================
    # STEP 3: The Misconception (KEY MOMENT!)
    # ==========================================
    input("\n[Press Enter for learner's misconception...]")
    
    print_message("learner", "I think I should add 13 and 5 together")
    
    simulate_typing()
    
    print_message("tutor", """Interesting thinking! Let me help you see this differently.

An equation is like a balance scale ⚖️. You have 2x + 5 on the left, and 13 on the right.

If you add 13 and 5, which side would change?

🤔 Think about it: We want to get x by itself. What's 'in the way' of x?""")
    
    # Show reasoning analysis
    input("\n[Press Enter to see the Reasoning Analysis...]")
    
    print_header("🧠 BEHIND THE SCENES: REASONING ANALYSIS")
    
    analysis = {
        "learner_response": "I think I should add 13 and 5 together",
        "misconception_detected": "inverse_operation_confusion",
        "reasoning_gap": "Learner is treating the equation as a left-to-right calculation rather than maintaining equality balance. They want to combine numbers across the equals sign.",
        "severity": "foundational",
        "confidence": 0.85,
        "related_concepts": ["equation_balance", "inverse_operations", "maintaining_equality"],
        "suggested_approach": "Use balance scale analogy to help learner visualize equality. Ask what's 'in the way' of x."
    }
    
    print(json.dumps(analysis, indent=2))
    
    # ==========================================
    # STEP 4: The Correction
    # ==========================================
    input("\n[Press Enter for learner's correction...]")
    
    print_message("learner", "Oh, I need to subtract 5 from both sides!")
    
    simulate_typing()
    
    print_message("tutor", """Exactly right! 🌟

When you subtract 5 from both sides:
2x + 5 - 5 = 13 - 5
2x = 8

Great job! Now, what's the next step to find x?

💡 Remember: x is multiplied by 2 right now.""")
    
    # ==========================================
    # STEP 5: Success!
    # ==========================================
    input("\n[Press Enter for learner's solution...]")
    
    print_message("learner", "Divide by 2, so x = 4")
    
    simulate_typing()
    
    print_message("tutor", """Perfect! You've got it! 🎉

2x ÷ 2 = 8 ÷ 2
x = 4

Let's check our answer:
2(4) + 5 = 8 + 5 = 13 ✓

You solved it! The key skills you used:
1. Maintaining balance (same operation on both sides)
2. Using inverse operations (subtract to undo addition)

Would you like to try another problem? Type 'next' for practice!""")
    
    # ==========================================
    # STEP 6: Progress Report
    # ==========================================
    input("\n[Press Enter to see Progress Report...]")
    
    print_message("learner", "Progress")
    
    simulate_typing()
    
    print_message("tutor", """📊 Your Progress Report

🎯 Problems Attempted: 12
✅ Problems Solved: 9
📈 Accuracy: 75%

📚 Topics Covered:
• Linear Equations
• Fractions

💪 Keep Practicing:
• Word Problems

🔥 Current Streak: 3 correct!

You're doing great! Let's keep learning! 🚀""")
    
    # ==========================================
    # SUMMARY
    # ==========================================
    input("\n[Press Enter for demo summary...]")
    
    print_header("DEMO SUMMARY")
    
    print("""
✅ WHAT WE DEMONSTRATED:

1. 🎯 REASONING ANALYSIS
   - Detected learner's misconception (inverse operation confusion)
   - Provided targeted guidance instead of just saying "wrong"
   
2. 🗣️ SOCRATIC METHOD
   - Asked questions to guide learner to the answer
   - Never gave the solution directly
   
3. 📊 PROGRESS TRACKING
   - Tracked problems attempted, solved, and accuracy
   - Identified improvement areas
   
4. 🎓 PERSONALIZATION
   - Adapted to Grade 9 level
   - Used appropriate analogies (balance scale)

KEY INNOVATION:
Traditional AI tutors check answers. We analyze THINKING.
This is how we build independent problem-solvers.
    """)
    
    print_header("THANK YOU! 🇿🇦")
    print("""
Built for South African learners:
• Zero-rated on Vodacom
• WhatsApp + USSD channels
• CAPS & IEB aligned
• Multi-language support

Questions? Let's chat!
    """)


if __name__ == "__main__":
    run_demo()
