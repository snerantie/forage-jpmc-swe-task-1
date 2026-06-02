"""
Personalized Hint Engine
========================

Generates progressive hints based on learner's current understanding.
Hints get more specific as the learner needs more help.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class HintLevel(Enum):
    """Progressive hint levels - from subtle to specific"""
    PROBING_QUESTION = 1      # "What do you think is the first step?"
    CONCEPTUAL_HINT = 2       # "Remember, equations are like balance scales..."
    PROCEDURAL_HINT = 3       # "Try subtracting 5 from both sides..."
    WORKED_EXAMPLE = 4        # Show a similar problem solved step-by-step


@dataclass
class Hint:
    level: HintLevel
    content: str
    analogy: Optional[str] = None
    related_problem: Optional[str] = None


class HintEngine:
    """
    Generates personalized hints that guide learners without giving answers.
    
    The key innovation: hints are NOT one-size-fits-all. They're tailored to:
    - The learner's grade level
    - Their detected misconception
    - Their progress in the current session
    - Their historical weak areas
    """
    
    def __init__(self, learner_profile: Dict):
        self.learner_profile = learner_profile
        self.hints_given = 0
        
    def get_next_hint(self, problem: Dict, misconception: str) -> Hint:
        """
        Get the next appropriate hint level.
        
        Hints progress from subtle to more specific as learner needs more help.
        """
        self.hints_given += 1
        
        # Determine hint level based on how many hints already given
        if self.hints_given == 1:
            return self._generate_probing_question(problem, misconception)
        elif self.hints_given == 2:
            return self._generate_conceptual_hint(problem, misconception)
        elif self.hints_given == 3:
            return self._generate_procedural_hint(problem, misconception)
        else:
            return self._generate_worked_example(problem, misconception)
    
    def _generate_probing_question(self, problem: Dict, misconception: str) -> Hint:
        """Level 1: Ask a question to understand learner's thinking"""
        
        probing_questions = {
            "inverse_operation_confusion": [
                "What do you think is the goal when solving this equation?",
                "What does the equals sign tell us about both sides?",
                "If you had 2x apples + 5 apples on one side and 13 apples on the other, how could you find out how many apples are in each 'x' group?"
            ],
            "sign_error": [
                "What do you remember about subtracting negative numbers?",
                "Let's think about temperature. If it's 5 degrees and drops by 3 degrees, what's the temperature? What if it drops by -3 degrees?"
            ],
            "order_of_operations": [
                "What do you remember about BODMAS/BIDMAS?",
                "Which operation should we do first in this expression?"
            ]
        }
        
        questions = probing_questions.get(misconception, ["Tell me about your thinking."])
        question = questions[min(self.hints_given - 1, len(questions) - 1)]
        
        return Hint(
            level=HintLevel.PROBING_QUESTION,
            content=question,
            analogy=self._get_analogy(misconception)
        )
    
    def _generate_conceptual_hint(self, problem: Dict, misconception: str) -> Hint:
        """Level 2: Provide conceptual understanding without procedure"""
        
        conceptual_hints = {
            "inverse_operation_confusion": 
                "Think of an equation like a balance scale ⚖️. Whatever you do to one side, "
                "you must do to the other to keep it balanced.\n\n"
                "To 'undo' an operation, you use its inverse:\n"
                "• Addition ↔ Subtraction\n"
                "• Multiplication ↔ Division\n\n"
                "What operation do you need to 'undo' +5?",
            
            "sign_error":
                "Remember: When you subtract a negative number, it's like adding a positive!\n\n"
                "Think of it like debt: If someone takes away your debt of R50 (-50), "
                "you now have R50 more! So: 10 - (-5) = 10 + 5 = 15 🎯",
            
            "order_of_operations":
                "BODMAS tells us the order:\n"
                "B - Brackets first\n"
                "O - Orders (powers, roots)\n"
                "D - Division\n"
                "M - Multiplication\n"
                "A - Addition\n"
                "S - Subtraction\n\n"
                "Which part should we calculate first?"
        }
        
        return Hint(
            level=HintLevel.CONCEPTUAL_HINT,
            content=conceptual_hints.get(misconception, "Let's think about this concept together."),
            analogy=self._get_analogy(misconception)
        )
    
    def _generate_procedural_hint(self, problem: Dict, misconception: str) -> Hint:
        """Level 3: Give more specific procedural guidance"""
        
        procedural_hints = {
            "inverse_operation_confusion":
                f"Let's break it down:\n\n"
                f"Original equation: {problem.get('expression', '2x + 5 = 13')}\n\n"
                f"Step 1: Identify what's 'attached' to x. Here it's '×2' and '+5'.\n"
                f"Step 2: We need to 'peel away' these operations in REVERSE order.\n"
                f"        - Last operation was +5, so first we subtract 5 from BOTH sides.\n"
                f"        - Then we divide by 2.\n\n"
                f"What do you get when you subtract 5 from both sides?",
            
            "sign_error":
                "Let's simplify the signs step by step:\n\n"
                "Example: -(-3) = +3\n"
                "Example: 5 - (-2) = 5 + 2 = 7\n\n"
                "Try applying this to your problem. What happens when you have two negatives?"
        }
        
        return Hint(
            level=HintLevel.PROCEDURAL_HINT,
            content=procedural_hints.get(misconception, "Let me guide you through this step by step.")
        )
    
    def _generate_worked_example(self, problem: Dict, misconception: str) -> Hint:
        """Level 4: Show a similar problem solved step-by-step"""
        
        worked_examples = {
            "inverse_operation_confusion":
                "Let me show you a similar problem:\n\n"
                "Problem: 3x + 7 = 19\n\n"
                "Step 1: Subtract 7 from BOTH sides\n"
                "   3x + 7 - 7 = 19 - 7\n"
                "   3x = 12\n\n"
                "Step 2: Divide BOTH sides by 3\n"
                "   3x ÷ 3 = 12 ÷ 3\n"
                "   x = 4\n\n"
                "Check: 3(4) + 7 = 12 + 7 = 19 ✓\n\n"
                "Now try your problem: 2x + 5 = 13\n"
                "What's your first step?"
        }
        
        return Hint(
            level=HintLevel.WORKED_EXAMPLE,
            content=worked_examples.get(misconception, "Let me show you an example."),
            related_problem=problem.get('expression')
        )
    
    def _get_analogy(self, misconception: str) -> Optional[str]:
        """Get a real-world analogy relevant to South African learners"""
        
        analogies = {
            "inverse_operation_confusion":
                "💡 Think of it like a taxi: To undo going from Johannesburg to Pretoria (+70km), "
                "you need to go back (-70km). Each operation has an 'undo' button!",
            
            "sign_error":
                "💡 Think of negative numbers like owing money. If you owe someone R20 (-20), "
                "and they say 'forget about the debt' (subtract the -20), you actually GAIN R20!",
            
            "order_of_operations":
                "💡 Think of BODMAS like getting dressed. You put on underwear before pants, "
                "not the other way around! Order matters."
        }
        
        return analogies.get(misconception)


# Demo
if __name__ == "__main__":
    learner_profile = {
        "grade": 9,
        "language": "en",
        "weak_areas": ["linear_equations", "inverse_operations"]
    }
    
    problem = {
        "type": "linear_equation",
        "expression": "2x + 5 = 13",
        "grade_level": 9
    }
    
    engine = HintEngine(learner_profile)
    
    print("=" * 60)
    print("PROGRESSIVE HINT DEMO")
    print("=" * 60)
    print(f"\nProblem: {problem['expression']}")
    print("Learner misconception: inverse_operation_confusion")
    print("\n" + "=" * 60)
    
    for i in range(4):
        hint = engine.get_next_hint(problem, "inverse_operation_confusion")
        print(f"\n📌 HINT LEVEL {hint.level.value}: {hint.level.name}")
        print("-" * 60)
        print(hint.content)
        if hint.analogy:
            print(f"\n{hint.analogy}")
        print()
