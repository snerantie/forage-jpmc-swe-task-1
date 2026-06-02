"""
AI Tutor South Africa - Reasoning Analyzer
==========================================

The core innovation: analyzing HOW learners think, not just WHAT they answer.
This module identifies reasoning gaps, misconceptions, and provides personalized guidance.
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class MisconceptionType(Enum):
    """Common mathematical misconceptions detected by the system"""
    INVERSE_OPERATION_CONFUSION = "inverse_operation_confusion"
    SIGN_ERROR = "sign_error"
    ORDER_OF_OPERATIONS = "order_of_operations"
    EQUALS_SIGN_MISUNDERSTANDING = "equals_sign_misunderstanding"
    VARIABLE_CONFUSION = "variable_confusion"
    PROCEDURAL_SKIP = "procedural_skip"
    CALCULATION_ERROR = "calculation_error"
    CONCEPTUAL_GAP = "conceptual_gap"


@dataclass
class ReasoningAnalysis:
    """Output of the reasoning analysis"""
    misconception_detected: Optional[MisconceptionType]
    reasoning_gap: str
    severity: str  # "foundational", "procedural", "minor"
    related_concepts: List[str]
    confidence: float
    suggested_response: str
    hint_level: int  # 1-3, progressive hints


class ReasoningAnalyzer:
    """
    Analyzes learner responses to understand their reasoning process.
    
    This is the heart of the AI tutor - it doesn't just check answers,
    it understands the learner's thinking pattern.
    """
    
    def __init__(self, grade_level: int, language: str = "en"):
        self.grade_level = grade_level
        self.language = language
        self.conversation_history = []
        
    def analyze_response(
        self, 
        problem: str, 
        learner_response: str,
        expected_approach: List[str]
    ) -> ReasoningAnalysis:
        """
        Analyze a learner's response to identify reasoning patterns.
        
        Args:
            problem: The math problem being solved
            learner_response: What the learner said/did
            expected_approach: Steps that represent correct reasoning
            
        Returns:
            ReasoningAnalysis with detected misconceptions and guidance
        """
        
        # In production, this would call AWS Bedrock Claude
        # For demo, we show the analysis logic
        
        self.conversation_history.append({
            "role": "learner",
            "content": learner_response
        })
        
        # Analyze the response
        analysis = self._detect_misconception(problem, learner_response, expected_approach)
        
        return analysis
    
    def _detect_misconception(
        self, 
        problem: str, 
        response: str, 
        expected: List[str]
    ) -> ReasoningAnalysis:
        """
        Detect misconceptions by comparing learner's approach to expected reasoning.
        """
        
        response_lower = response.lower()
        
        # Example detection logic (in production, this uses Claude on Bedrock)
        
        # Detect: Trying to combine terms across the equals sign
        if any(phrase in response_lower for phrase in ["add", "combine", "together"]):
            if "=" in problem and not any(step in response_lower for step in ["subtract", "move", "both sides"]):
                return ReasoningAnalysis(
                    misconception_detected=MisconceptionType.INVERSE_OPERATION_CONFUSION,
                    reasoning_gap="Learner is treating the equation as a left-to-right calculation rather than maintaining equality balance. They want to add numbers across the equals sign.",
                    severity="foundational",
                    related_concepts=["equation_balance", "inverse_operations", "maintaining_equality"],
                    confidence=0.85,
                    suggested_response=self._generate_socratic_response(
                        "inverse_operation_confusion",
                        hint_level=1
                    ),
                    hint_level=1
                )
        
        # Detect: Sign errors
        if "-" in problem and "negative" in response_lower:
            if "add" in response_lower and "-" not in response_lower.replace("negative", ""):
                return ReasoningAnalysis(
                    misconception_detected=MisconceptionType.SIGN_ERROR,
                    reasoning_gap="Learner may be confused about handling negative numbers in equations.",
                    severity="procedural",
                    related_concepts=["negative_numbers", "inverse_operations"],
                    confidence=0.75,
                    suggested_response=self._generate_socratic_response("sign_error", hint_level=1),
                    hint_level=1
                )
        
        # Default: Partial understanding, needs probing
        return ReasoningAnalysis(
            misconception_detected=MisconceptionType.CONCEPTUAL_GAP,
            reasoning_gap="Learner's approach doesn't match expected reasoning pattern. Need to probe further.",
            severity="minor",
            related_concepts=["problem_comprehension"],
            confidence=0.60,
            suggested_response=self._generate_probing_question(problem),
            hint_level=1
        )
    
    def _generate_socratic_response(self, misconception_type: str, hint_level: int) -> str:
        """
        Generate a Socratic question that guides the learner to discover the answer.
        
        This is the key differentiator - we don't give answers, we ask questions.
        """
        
        responses = {
            "inverse_operation_confusion": {
                1: "Interesting thinking! Let me help you see this differently.\n\nThink of an equation like a balance scale ⚖️. You have 2x + 5 on the left side, and 13 on the right side.\n\nIf you want to find x, what do you think is 'in the way' of x being by itself?",
                2: "Great progress! You noticed that +5 is 'in the way'. \n\nOn a balance scale, if you remove 5 from one side, what must you do to keep it balanced?",
                3: "Exactly! You subtract 5 from BOTH sides. So:\n2x + 5 - 5 = 13 - 5\n2x = 8\n\nNow, what's the next step to get x alone?"
            },
            "sign_error": {
                1: "I see you're thinking about the negative sign. Good awareness! \n\nLet's slow down. When you see 'subtract a negative number', what does that mean to you?",
                2: "Remember: subtracting a negative is the same as adding a positive! \n\nExample: 5 - (-3) = 5 + 3 = 8\n\nCan you apply this to your problem?",
                3: "Let's rewrite it step by step. What do you get when you simplify the signs?"
            }
        }
        
        return responses.get(misconception_type, {}).get(hint_level, "Tell me more about your thinking.")
    
    def _generate_probing_question(self, problem: str) -> str:
        """Generate a question to understand the learner's thinking better."""
        return "I'd love to understand your thinking! What made you choose that approach?"


# Demo Usage
if __name__ == "__main__":
    # Example: Grade 9 learner solving 2x + 5 = 13
    
    analyzer = ReasoningAnalyzer(grade_level=9, language="en")
    
    problem = "2x + 5 = 13"
    learner_response = "I think I should add 13 and 5 together"
    expected_approach = [
        "Identify the goal: isolate x",
        "Recognize +5 is added to 2x",
        "Apply inverse operation: subtract 5 from both sides",
        "Simplify: 2x = 8",
        "Divide both sides by 2",
        "Solution: x = 4"
    ]
    
    analysis = analyzer.analyze_response(problem, learner_response, expected_approach)
    
    print("=" * 60)
    print("AI TUTOR - REASONING ANALYSIS")
    print("=" * 60)
    print(f"\nProblem: {problem}")
    print(f"Learner said: '{learner_response}'")
    print(f"\nMisconception Detected: {analysis.misconception_detected.value}")
    print(f"Reasoning Gap: {analysis.reasoning_gap}")
    print(f"Severity: {analysis.severity}")
    print(f"Related Concepts: {analysis.related_concepts}")
    print(f"Confidence: {analysis.confidence * 100:.0f}%")
    print(f"\nSUGGESTED RESPONSE:\n{analysis.suggested_response}")
    print("=" * 60)
