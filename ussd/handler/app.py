"""
USSD Session Handler for AI Tutor South Africa
==============================================

Handles USSD sessions for learners without smartphones or data.
USSD works on any phone and doesn't require internet.

Key Constraints:
- 160 characters per screen
- Session timeout ~3 minutes
- Menu-driven navigation
- No rich media (text only)
"""

import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class USSDState(Enum):
    """Possible states in USSD session flow"""
    WELCOME = "welcome"
    SELECT_GRADE = "select_grade"
    SELECT_TOPIC = "select_topic"
    SELECT_ACTION = "select_action"
    ASK_QUESTION = "ask_question"
    PRACTICE = "practice"
    VIEW_PROGRESS = "view_progress"


@dataclass
class USSDRequest:
    """Incoming USSD request structure"""
    session_id: str
    service_code: str
    phone_number: str
    text: str
    network_code: str  # Vodacom, MTN, Cell C, Telkom


@dataclass
class USSDResponse:
    """Outgoing USSD response structure"""
    message: str
    continue_session: bool  # True = continue, False = end


class USSDHandler:
    """
    Handles USSD sessions for AI Tutor.
    
    Designed for:
    - Low-end phones (Nokia, etc.)
    - Zero-rated access on Vodacom
    - Quick, menu-driven interactions
    """
    
    # USSD codes (Vodacom format)
    USSD_CODE = "*120*TUTOR#"  # In production: Get actual code from Vodacom
    
    # Menus organized by state
    MENUS = {
        "welcome": """Welcome to AI Tutor!
1. Mathematics
2. Help
3. My Progress""",
        
        "select_grade": """Select your grade:
1. Gr 1-3
2. Gr 4-6
3. Gr 7-9
4. Gr 10-12""",
        
        "select_topic_primary": """Topic:
1. Numbers
2. Addition
3. Subtraction
4. Patterns
5. Back""",
        
        "select_topic_senior": """Topic:
1. Algebra
2. Geometry
3. Fractions
4. Equations
5. Back""",
        
        "select_topic_fet": """Topic:
1. Algebra
2. Calculus
3. Trigonometry
4. Functions
5. Statistics
6. Back"""
    }
    
    def __init__(self):
        self.sessions = {}  # In production: DynamoDB with TTL
        self.max_message_length = 160  # USSD limit
        
    def process_request(self, request: USSDRequest) -> USSDResponse:
        """
        Process USSD request and return appropriate response.
        
        Args:
            request: The incoming USSD request
            
        Returns:
            USSDResponse with menu or result
        """
        
        # Get or create session
        session = self._get_session(request.session_id)
        session["phone"] = request.phone_number
        session["network"] = request.network_code
        
        # Parse user input
        user_input = request.text.strip() if request.text else ""
        steps = user_input.split("*") if user_input else []
        
        # Determine current state and respond
        if not steps or steps[-1] == "":
            # Initial request or empty input
            return self._handle_state(USSDState.WELCOME, "", session)
        
        # Process based on navigation path
        current_step = steps[-1]
        
        # Welcome menu
        if len(steps) == 1:
            if current_step == "1":
                session["subject"] = "mathematics"
                return self._handle_state(USSDState.SELECT_GRADE, "", session)
            elif current_step == "2":
                return self._show_help()
            elif current_step == "3":
                return self._show_progress(session)
        
        # Grade selection
        elif len(steps) == 2:
            grade_group = int(current_step)
            session["grade_group"] = grade_group
            return self._show_topics(grade_group)
        
        # Topic selection
        elif len(steps) == 3:
            topic_index = int(current_step)
            topics = self._get_topics_for_grade(session.get("grade_group", 1))
            if 1 <= topic_index <= len(topics):
                session["topic"] = topics[topic_index - 1]
                return self._show_topic_menu(session)
            elif topic_index == len(topics) + 1:  # Back
                return self._handle_state(USSDState.WELCOME, "", session)
        
        # Topic action
        elif len(steps) == 4:
            if current_step == "1":  # Learn
                return self._start_lesson(session)
            elif current_step == "2":  # Practice
                return self._start_practice(session)
            elif current_step == "3":  # Ask Question
                return USSDResponse(
                    message="Type your question (160 chars max):",
                    continue_session=True
                )
            elif current_step == "4":  # Back
                return self._show_topics(session.get("grade_group", 1))
        
        return self._show_error()
    
    def _handle_state(self, state: USSDState, input_text: str, session: Dict) -> USSDResponse:
        """Handle session state and return appropriate menu"""
        
        if state == USSDState.WELCOME:
            return USSDResponse(
                message=self._truncate(self.MENUS["welcome"]),
                continue_session=True
            )
        
        elif state == USSDState.SELECT_GRADE:
            return USSDResponse(
                message=self._truncate(self.MENUS["select_grade"]),
                continue_session=True
            )
        
        return self._show_error()
    
    def _show_topics(self, grade_group: int) -> USSDResponse:
        """Show topics based on grade group"""
        
        if grade_group == 1:  # Grade 1-3
            menu = self.MENUS["select_topic_primary"]
        elif grade_group in [2, 3]:  # Grade 4-9
            menu = self.MENUS["select_topic_senior"]
        else:  # Grade 10-12
            menu = self.MENUS["select_topic_fet"]
        
        return USSDResponse(
            message=self._truncate(menu),
            continue_session=True
        )
    
    def _get_topics_for_grade(self, grade_group: int) -> List[str]:
        """Get topic list for grade group"""
        
        topics_map = {
            1: ["Numbers", "Addition", "Subtraction", "Patterns"],
            2: ["Numbers", "Addition", "Fractions", "Geometry"],
            3: ["Algebra", "Geometry", "Fractions", "Equations"],
            4: ["Algebra", "Calculus", "Trigonometry", "Functions", "Statistics"]
        }
        
        return topics_map.get(grade_group, topics_map[1])
    
    def _show_topic_menu(self, session: Dict) -> USSDResponse:
        """Show actions for selected topic"""
        
        topic = session.get("topic", "Mathematics")
        
        menu = f"""{topic}:
1. Learn
2. Practice
3. Ask Question
4. Back"""
        
        return USSDResponse(
            message=self._truncate(menu),
            continue_session=True
        )
    
    def _start_lesson(self, session: Dict) -> USSDResponse:
        """Start a mini-lesson on the topic"""
        
        topic = session.get("topic", "Algebra")
        
        lessons = {
            "Algebra": """Algebra Basics:
x is a mystery number.
If 2x = 10,
then x = 5.

Try: 3x = 15
Answer: x = ?

Reply with answer:""",
            
            "Equations": """Equations:
Both sides must be equal.
2x + 4 = 12
Step 1: -4 from both
2x = 8
Step 2: Divide by 2
x = 4

Ready to try?""",
            
            "Fractions": """Fractions:
1/2 = 0.5
1/4 = 0.25

To add fractions:
Make same bottom number
1/2 + 1/4 = ?
= 2/4 + 1/4 = 3/4

Continue? (1=Yes 2=No)"""
        }
        
        lesson = lessons.get(topic, f"Lesson: {topic}\nComing soon!\n1. Back")
        
        return USSDResponse(
            message=self._truncate(lesson),
            continue_session=True
        )
    
    def _start_practice(self, session: Dict) -> USSDResponse:
        """Start practice problems"""
        
        topic = session.get("topic", "Algebra")
        
        problems = {
            "Algebra": """Practice:
Solve: 2x = 10
What is x?

Reply with number:""",
            
            "Equations": """Practice:
Solve: x + 5 = 12
What is x?

Reply with number:""",
            
            "Fractions": """Practice:
1/2 + 1/4 = ?

1. 2/4
2. 3/4
3. 1/6

Reply with 1, 2, or 3:"""
        }
        
        problem = problems.get(topic, "Practice coming soon!\n1. Back")
        
        return USSDResponse(
            message=self._truncate(problem),
            continue_session=True
        )
    
    def _show_help(self) -> USSDResponse:
        """Show help information (USSD format, 160 chars)"""
        
        help_text = """AI Tutor Help:
1. Pick a subject
2. Pick your grade
3. Learn or Practice

No data needed!
Works on any phone.
Call support: 0800..."""
        
        return USSDResponse(
            message=self._truncate(help_text),
            continue_session=False  # End session
        )
    
    def _show_progress(self, session: Dict) -> USSDResponse:
        """Show learner progress (compact)"""
        
        # In production: Fetch from DynamoDB
        problems = session.get("problems_solved", 7)
        accuracy = session.get("accuracy", 71)
        
        progress = f"""Your Progress:
Problems: {problems}
Accuracy: {accuracy}%
Keep learning!"""
        
        return USSDResponse(
            message=self._truncate(progress),
            continue_session=False
        )
    
    def _show_error(self) -> USSDResponse:
        """Show error message"""
        
        return USSDResponse(
            message="Invalid option. Please try again.",
            continue_session=False
        )
    
    def _truncate(self, text: str) -> str:
        """Truncate text to USSD limit"""
        
        if len(text) <= self.max_message_length:
            return text
        
        return text[:self.max_message_length - 3] + "..."
    
    def _get_session(self, session_id: str) -> Dict:
        """Get or create session"""
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "id": session_id,
                "state": USSDState.WELCOME.value,
                "subject": None,
                "grade_group": None,
                "topic": None
            }
        
        return self.sessions[session_id]


# Lambda handler for AWS
def lambda_handler(event, context):
    """AWS Lambda entry point for USSD gateway"""
    
    # Parse USSD gateway request (format varies by provider)
    request = USSDRequest(
        session_id=event.get("sessionId", "session_123"),
        service_code=event.get("serviceCode", "*120*TUTOR#"),
        phone_number=event.get("phoneNumber", "+27123456789"),
        text=event.get("text", ""),
        network_code=event.get("networkCode", "VODACOM")
    )
    
    handler = USSDHandler()
    response = handler.process_request(request)
    
    # Format response for USSD gateway
    return {
        "sessionId": request.session_id,
        "message": response.message,
        "continueSession": response.continue_session
    }


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("USSD HANDLER DEMO")
    print("=" * 60)
    
    handler = USSDHandler()
    
    # Simulate USSD session
    print("\n📱 Dialing *120*TUTOR#...")
    
    request = USSDRequest(
        session_id="sess_001",
        service_code="*120*TUTOR#",
        phone_number="+27123456789",
        text="",
        network_code="VODACOM"
    )
    
    response = handler.process_request(request)
    print(f"\n🤖 RESPONSE:\n{response.message}")
    
    # User selects Mathematics (1)
    request.text = "1"
    response = handler.process_request(request)
    print(f"\n📱 User inputs: 1")
    print(f"\n🤖 RESPONSE:\n{response.message}")
    
    # User selects Grade 10-12 (4)
    request.text = "1*4"
    response = handler.process_request(request)
    print(f"\n📱 User inputs: 4")
    print(f"\n🤖 RESPONSE:\n{response.message}")
    
    # User selects Algebra (1)
    request.text = "1*4*1"
    response = handler.process_request(request)
    print(f"\n📱 User inputs: 1")
    print(f"\n🤖 RESPONSE:\n{response.message}")
    
    # User selects Practice (2)
    request.text = "1*4*1*2"
    response = handler.process_request(request)
    print(f"\n📱 User inputs: 2")
    print(f"\n🤖 RESPONSE:\n{response.message}")
