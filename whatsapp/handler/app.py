"""
WhatsApp Webhook Handler for AI Tutor South Africa
===================================================

Handles incoming WhatsApp messages and routes them to the AI tutor engine.
Designed to work with WhatsApp Business API.
"""

import json
from typing import Dict, Optional
from dataclasses import dataclass
import re


@dataclass
class WhatsAppMessage:
    """Incoming WhatsApp message structure"""
    from_number: str
    message_id: str
    message_type: str  # text, image, audio, document
    content: str
    timestamp: str
    profile_name: Optional[str] = None


@dataclass
class WhatsAppResponse:
    """Outgoing WhatsApp message structure"""
    to: str
    message_type: str
    content: str
    preview_url: bool = False


class WhatsAppHandler:
    """
    Handles WhatsApp webhook events and messages.
    
    Features:
    - Text message processing
    - Image handling (for math problems with diagrams)
    - Voice message support (future: speech-to-text)
    - Session management
    - Rate limiting
    """
    
    def __init__(self):
        self.sessions = {}  # In production: DynamoDB
        self.supported_languages = ["en", "zu", "xh", "af", "st", "tn", "ts", "ve"]
        
    def process_webhook(self, event: Dict) -> Optional[WhatsAppResponse]:
        """
        Process incoming webhook event from WhatsApp Business API.
        
        Args:
            event: The webhook payload from WhatsApp
            
        Returns:
            WhatsAppResponse if a reply is needed, None otherwise
        """
        
        # Validate webhook
        if not self._validate_webhook(event):
            return None
        
        # Extract message
        message = self._parse_message(event)
        if not message:
            return None
        
        # Get or create session
        session = self._get_session(message.from_number)
        
        # Update session with learner info
        if message.profile_name:
            session["learner_name"] = message.profile_name
        
        # Handle different message types
        if message.message_type == "text":
            return self._handle_text_message(message, session)
        elif message.message_type == "image":
            return self._handle_image_message(message, session)
        elif message.message_type == "audio":
            return self._handle_audio_message(message, session)
        else:
            return self._send_help_message(message.from_number)
    
    def _parse_message(self, event: Dict) -> Optional[WhatsAppMessage]:
        """Extract message details from webhook payload"""
        
        try:
            entry = event.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            
            if "messages" not in value:
                return None
            
            msg = value["messages"][0]
            
            return WhatsAppMessage(
                from_number=msg.get("from", ""),
                message_id=msg.get("id", ""),
                message_type=msg.get("type", "text"),
                content=self._extract_content(msg),
                timestamp=msg.get("timestamp", ""),
                profile_name=value.get("contacts", [{}])[0].get("profile", {}).get("name")
            )
        except (IndexError, KeyError):
            return None
    
    def _extract_content(self, msg: Dict) -> str:
        """Extract text content from different message types"""
        
        msg_type = msg.get("type", "text")
        
        if msg_type == "text":
            return msg.get("text", {}).get("body", "")
        elif msg_type == "image":
            return msg.get("image", {}).get("caption", "[Image received]")
        elif msg_type == "audio":
            return "[Voice message received]"
        
        return ""
    
    def _handle_text_message(self, message: WhatsAppMessage, session: Dict) -> WhatsAppResponse:
        """
        Process text message and generate AI tutor response.
        
        This is where the magic happens - the message goes to the
        Reasoning Analyzer, then the Hint Engine.
        """
        
        text = message.content.strip().lower()
        
        # Check for commands
        if text in ["hi", "hello", "start", "heita", "sawubona", "hallo"]:
            return self._send_welcome_message(message.from_number, session)
        
        if text in ["help", "help me", "nceda", "help asseblief"]:
            return self._send_help_message(message.from_number)
        
        if text in ["progress", "my progress", "impilo yami"]:
            return self._send_progress_report(message.from_number, session)
        
        if text.startswith("grade "):
            grade = self._extract_grade(text)
            if grade:
                session["grade"] = grade
                return self._confirm_grade_set(message.from_number, grade)
        
        # It's a math question or response - send to AI tutor engine
        # In production: Call Lambda function with Reasoning Analyzer
        response = self._get_ai_response(message.content, session)
        
        return WhatsAppResponse(
            to=message.from_number,
            message_type="text",
            content=response
        )
    
    def _send_welcome_message(self, to: str, session: Dict) -> WhatsAppResponse:
        """Send personalized welcome message"""
        
        name = session.get("learner_name", "learner")
        grade = session.get("grade")
        
        welcome = f"""👋 Hello {name}! Welcome to AI Tutor! 🎓

I'm your personal Mathematics tutor. I'll help you learn to solve problems step by step.

"""
        
        if not grade:
            welcome += """First, tell me your grade. Reply with:
• Grade 1  (or just type: grade 1)
• Grade 2
• ...
• Grade 12

You can also:
• Ask me a math question anytime
• Type 'help' for assistance
• Type 'progress' to see how you're improving

Let's learn together! 📚"""
        else:
            welcome += f"""You're in Grade {grade}. Ready to learn!

What would you like help with today?

Examples:
• "Help me solve: 2x + 5 = 13"
• "I don't understand fractions"
• "Practice algebra"

Let's go! 🚀"""
        
        return WhatsAppResponse(
            to=to,
            message_type="text",
            content=welcome
        )
    
    def _send_help_message(self, to: str) -> WhatsAppResponse:
        """Send help information"""
        
        help_text = """🆘 AI Tutor Help

HOW TO USE:
1. Just type your math question
2. I'll guide you step by step
3. I won't give answers - I'll help YOU find them!

EXAMPLES:
• "Solve: 2x + 5 = 13"
• "What is 15% of 200?"
• "Help with fractions"

COMMANDS:
• grade [1-12] - Set your grade
• progress - See your improvement
• help - Show this message

LANGUAGES:
I understand English, IsiZulu, IsiXhosa, Afrikaans, and more!

Questions? Just type them! 📝"""
        
        return WhatsAppResponse(
            to=to,
            message_type="text",
            content=help_text
        )
    
    def _send_progress_report(self, to: str, session: Dict) -> WhatsAppResponse:
        """Send learner's progress report"""
        
        # In production: Fetch from DynamoDB
        progress = session.get("progress", {
            "problems_attempted": 12,
            "problems_solved": 9,
            "accuracy": 75,
            "topics_covered": ["linear_equations", "fractions"],
            "improvement_areas": ["word_problems"]
        })
        
        report = f"""📊 Your Progress Report

🎯 Problems Attempted: {progress['problems_attempted']}
✅ Problems Solved: {progress['problems_solved']}
📈 Accuracy: {progress['accuracy']}%

📚 Topics Covered:
{chr(10).join(f"• {t.replace('_', ' ').title()}" for t in progress['topics_covered'])}

💪 Keep Practicing:
{chr(10).join(f"• {t.replace('_', ' ').title()}" for t in progress['improvement_areas'])}

You're doing great! Let's keep learning! 🚀"""
        
        return WhatsAppResponse(
            to=to,
            message_type="text",
            content=report
        )
    
    def _confirm_grade_set(self, to: str, grade: int) -> WhatsAppResponse:
        """Confirm grade selection"""
        
        return WhatsAppResponse(
            to=to,
            message_type="text",
            content=f"""✅ Grade {grade} set!

Now you'll get questions and hints suited for your level.

What would you like to learn today?

Examples:
• "Help me solve: 2x + 5 = 13"
• "I want to practice fractions"
• "Explain percentages to me"

Let's go! 🎓"""
        )
    
    def _extract_grade(self, text: str) -> Optional[int]:
        """Extract grade number from text"""
        
        match = re.search(r'grade\s*(\d{1,2})', text)
        if match:
            grade = int(match.group(1))
            if 1 <= grade <= 12:
                return grade
        return None
    
    def _get_ai_response(self, message: str, session: Dict) -> str:
        """
        Get AI tutor response.
        
        In production: Call the Reasoning Analyzer Lambda
        For demo: Return mock progressive responses
        """
        
        # Demo: Mock AI responses for presentation
        message_lower = message.lower()
        
        if "2x + 5 = 13" in message_lower or "2x+5=13" in message_lower:
            return """Great question! Let's solve this together. 🎯

I won't give you the answer - instead, I'll help YOU find it.

First, tell me: What do you think is the goal when solving this equation?

💡 Hint: Think about what we're trying to find."""
        
        if any(word in message_lower for word in ["add 13", "add them", "combine"]):
            return """Interesting thinking! Let me help you see this differently.

An equation is like a balance scale ⚖️. You have 2x + 5 on the left, and 13 on the right.

If you add 13 and 5, which side would change?

🤔 Think about it: We want to get x by itself. What's 'in the way' of x?"""
        
        if "subtract 5" in message_lower or "minus 5" in message_lower:
            return """Exactly right! 🌟

When you subtract 5 from both sides:
2x + 5 - 5 = 13 - 5
2x = 8

Great job! Now, what's the next step to find x?

💡 Remember: x is multiplied by 2 right now."""
        
        if "divide by 2" in message_lower or "divide" in message_lower:
            return """Perfect! You've got it! 🎉

2x ÷ 2 = 8 ÷ 2
x = 4

Let's check: 2(4) + 5 = 8 + 5 = 13 ✓

You solved it! The key skills you used:
1. Maintaining balance (same operation on both sides)
2. Using inverse operations (subtract to undo addition)

Would you like to try another problem? Type 'next' for practice!"""
        
        # Default response
        return """I'm here to help! Tell me more about your thinking.

What problem are you working on? Just type it out and we'll solve it together! 📝"""
    
    def _get_session(self, phone_number: str) -> Dict:
        """Get or create session for learner"""
        
        if phone_number not in self.sessions:
            self.sessions[phone_number] = {
                "phone": phone_number,
                "grade": None,
                "language": "en",
                "progress": {
                    "problems_attempted": 0,
                    "problems_solved": 0,
                    "topics_covered": [],
                    "improvement_areas": []
                }
            }
        
        return self.sessions[phone_number]
    
    def _validate_webhook(self, event: Dict) -> bool:
        """Validate webhook is from WhatsApp"""
        
        # In production: Verify signature
        # For demo: Just check structure
        return "entry" in event


# Lambda handler for AWS
def lambda_handler(event, context):
    """AWS Lambda entry point"""
    
    handler = WhatsAppHandler()
    response = handler.process_webhook(event)
    
    if response:
        # In production: Send via WhatsApp Business API
        return {
            "statusCode": 200,
            "body": json.dumps({
                "to": response.to,
                "type": response.message_type,
                "content": response.content
            })
        }
    
    return {"statusCode": 200, "body": json.dumps({"status": "ok"})}


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("WHATSAPP HANDLER DEMO")
    print("=" * 60)
    
    handler = WhatsAppHandler()
    
    # Simulate webhook payload
    webhook = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "+27123456789",
                        "id": "msg_123",
                        "type": "text",
                        "text": {"body": "Hi"},
                        "timestamp": "1234567890"
                    }],
                    "contacts": [{
                        "profile": {"name": "Thabo"}
                    }]
                }
            }]
        }]
    }
    
    response = handler.process_webhook(webhook)
    print("\n📱 Incoming: 'Hi'")
    print(f"\n🤖 AI Tutor Response:\n{response.content}")
    
    # Simulate setting grade
    webhook["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"] = "grade 9"
    response = handler.process_webhook(webhook)
    print(f"\n📱 Incoming: 'grade 9'")
    print(f"\n🤖 AI Tutor Response:\n{response.content}")
    
    # Simulate math question
    webhook["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"] = "Help me solve: 2x + 5 = 13"
    response = handler.process_webhook(webhook)
    print(f"\n📱 Incoming: 'Help me solve: 2x + 5 = 13'")
    print(f"\n🤖 AI Tutor Response:\n{response.content}")
