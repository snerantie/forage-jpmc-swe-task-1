"""
AWS Bedrock Integration for AI Tutor South Africa

This module integrates with AWS Bedrock (Claude) for production AI responses.
For demo purposes, it includes mock responses.
"""

import json
from typing import Dict, List, Optional
import os


class BedrockTutorClient:
    """
    Client for AWS Bedrock - Claude 3.5 Sonnet
    """
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    def generate_response(self, messages: List[Dict], system_prompt: str) -> str:
        if self.use_mock:
            return self._get_mock_response(messages[-1]["content"] if messages else "")
        # Production: Call Bedrock API here
        return "Mock response"
    
    def _get_mock_response(self, last_message: str) -> str:
        responses = {
            "stuck": "I'd love to help you think through this! Tell me: what do you think the first step should be?",
            "add 13 and 5": "Interesting! Think of it like a balance scale. What's 'in the way' of x?",
            "subtract 5": "Excellent! Now what's the next step to find x?",
            "divide by 2": "Perfect! You solved it! x = 4"
        }
        for key, response in responses.items():
            if key in last_message.lower():
                return response
        return "Tell me more about your thinking."


TUTOR_SYSTEM_PROMPT = """
You are an AI Mathematics Tutor for South African learners (Grades 1-12).
You use the Socratic method - guide learners to discover answers through questions.
NEVER give the answer directly.
"""


if __name__ == "__main__":
    client = BedrockTutorClient(use_mock=True)
    messages = [{"role": "user", "content": "I'm stuck on: 2x + 5 = 13"}]
    response = client.generate_response(messages, TUTOR_SYSTEM_PROMPT)
    print("AI TUTOR:", response)
