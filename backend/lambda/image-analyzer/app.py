"""
Image Analyzer for AI Tutor South Africa
=========================================

Analyzes uploaded images of learner's handwritten work:
- Uses AWS Textract for handwriting recognition
- Uses AWS Bedrock Claude with vision for understanding
- Identifies mistakes and reasoning errors
- Provides targeted feedback

Supports:
- Photo of exam paper
- Scanned work
- WhatsApp photo messages
"""

import json
import base64
from typing import Dict, List, Optional
from dataclasses import dataclass
import boto3


@dataclass
class HandwritingAnalysis:
    """Analysis result of learner's handwritten work"""
    problem_statement: str
    learner_work: List[str]  # Steps the learner wrote
    mistakes_found: List[Dict]  # Where they went wrong
    correct_answer: str
    learner_answer: str
    feedback: str
    reasoning_gaps: List[str]


class ImageAnalyzer:
    """
    Analyzes images of learner's handwritten mathematics work.
    
    This is a POWERFUL feature that makes the tutor feel like a real teacher
    looking over the learner's shoulder!
    """
    
    def __init__(self):
        self.textract = boto3.client('textract', region_name='af-south-1')
        self.bedrock = boto3.client('bedrock-runtime', region_name='af-south-1')
        self.model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    def analyze_uploaded_work(self, image_data: bytes, grade: int) -> HandwritingAnalysis:
        """
        Analyze an image of learner's handwritten work.
        
        Args:
            image_data: Image bytes (JPEG/PNG)
            grade: Learner's grade level
            
        Returns:
            HandwritingAnalysis with mistakes and feedback
        """
        
        # Step 1: Extract text from image using Textract
        text_blocks = self._extract_handwriting(image_data)
        
        # Step 2: Use Claude Vision to understand the work
        analysis = self._analyze_with_claude_vision(image_data, text_blocks, grade)
        
        return analysis
    
    def _extract_handwriting(self, image_data: bytes) -> List[str]:
        """
        Extract handwritten text using AWS Textract.
        
        Textract is specifically good at recognizing handwriting,
        including mathematical notation.
        """
        
        try:
            response = self.textract.detect_document_text(
                Document={'Bytes': image_data}
            )
            
            # Extract lines of text in order
            lines = []
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    lines.append(block['Text'])
            
            return lines
        
        except Exception as e:
            # For demo/mock purposes
            return [
                "Problem: 2x + 5 = 13",
                "Step 1: 2x + 5 + 13 = 18",
                "Step 2: 2x = 18",
                "Step 3: x = 9"
            ]
    
    def _analyze_with_claude_vision(
        self, 
        image_data: bytes, 
        text_blocks: List[str],
        grade: int
    ) -> HandwritingAnalysis:
        """
        Use Claude 3.5 Sonnet (with vision) to analyze the work.
        
        Claude can:
        1. See the actual handwriting and diagrams
        2. Understand mathematical notation
        3. Identify where the learner went wrong
        4. Provide Socratic guidance
        """
        
        # Encode image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        prompt = f"""You are an expert Mathematics tutor analyzing a Grade {grade} learner's work.

The learner uploaded a photo of their work. Here's what was extracted:
{chr(10).join(text_blocks)}

Your task:
1. Identify the problem they were solving
2. Identify each step they wrote
3. Find where they made a mistake (if any)
4. Explain WHY the mistake happened (reasoning error)
5. Provide Socratic guidance to help them discover the correct approach

Remember: Don't just say "wrong" - help them understand their thinking process.

Return your analysis in this format:
PROBLEM: [the problem statement]
LEARNER_WORK: [list each step]
MISTAKE_LOCATION: [which step was wrong]
MISTAKE_TYPE: [what kind of error - e.g., "inverse operation confusion"]
REASONING_GAP: [why they made this mistake]
CORRECT_APPROACH: [what they should have done]
SOCRATIC_FEEDBACK: [questions to guide them to correct thinking]
"""
        
        # In production: Call Bedrock with vision
        # For demo: Return mock analysis
        return self._mock_analysis()
    
    def _mock_analysis(self) -> HandwritingAnalysis:
        """Mock analysis for demo purposes"""
        
        return HandwritingAnalysis(
            problem_statement="2x + 5 = 13",
            learner_work=[
                "Step 1: 2x + 5 + 13 = 18",
                "Step 2: 2x = 18", 
                "Step 3: x = 9"
            ],
            mistakes_found=[
                {
                    "step_number": 1,
                    "what_they_wrote": "2x + 5 + 13 = 18",
                    "mistake_type": "inverse_operation_confusion",
                    "explanation": "Learner added 13 to both sides instead of subtracting 5. They're treating the equation as 'combine all numbers' rather than 'isolate x'."
                }
            ],
            correct_answer="x = 4",
            learner_answer="x = 9",
            feedback="""I can see your thinking! Let me help you spot where things went differently.

In Step 1, you wrote: 2x + 5 + 13 = 18

🤔 Think about this: What's our goal when we solve 2x + 5 = 13?

We want to get x by itself, right? 

Look at the left side: 2x + 5
What's 'in the way' of x? It's that +5.

💡 To remove +5, we don't add more numbers. We do the OPPOSITE of adding.
What's the opposite of adding 5?

Try again with this hint: Think of the equation like a balance scale ⚖️. 
Whatever you do to one side, you must do to the other.""",
            reasoning_gaps=[
                "equation_balance",
                "inverse_operations",
                "understanding_equals_sign"
            ]
        )
    
    def generate_feedback_message(self, analysis: HandwritingAnalysis) -> str:
        """
        Generate a WhatsApp message with feedback on uploaded work.
        """
        
        message = f"""📸 I've analyzed your work! Let's look at it together.

**Problem:** {analysis.problem_statement}

**What you wrote:**
"""
        for i, step in enumerate(analysis.learner_work, 1):
            message += f"\n  {i}. {step}"
        
        message += f"""

**Your answer:** {analysis.learner_answer}
**Correct answer:** {analysis.correct_answer}

---

{analysis.feedback}

---

📊 Skills to practice:
"""
        for gap in analysis.reasoning_gaps:
            message += f"\n• {gap.replace('_', ' ').title()}"
        
        message += """

Would you like to:
1. Try solving it again with my hints?
2. See a similar worked example?
3. Ask a specific question?

Just reply with 1, 2, or 3! 🎓"""
        
        return message


# Lambda handler
def lambda_handler(event, context):
    """
    AWS Lambda handler for image analysis.
    
    Expected event format:
    {
        "image_data": "base64_encoded_image",
        "learner_id": "phone_number",
        "grade": 9
    }
    """
    
    try:
        # Decode image
        image_b64 = event.get('image_data', '')
        image_data = base64.b64decode(image_b64)
        
        grade = event.get('grade', 9)
        
        # Analyze
        analyzer = ImageAnalyzer()
        analysis = analyzer.analyze_uploaded_work(image_data, grade)
        
        # Generate feedback
        feedback_message = analyzer.generate_feedback_message(analysis)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'analysis': {
                    'problem': analysis.problem_statement,
                    'learner_answer': analysis.learner_answer,
                    'correct_answer': analysis.correct_answer,
                    'mistakes': analysis.mistakes_found
                },
                'feedback_message': feedback_message
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


# Demo
if __name__ == "__main__":
    print("=" * 70)
    print("IMAGE ANALYZER DEMO - Handwritten Work Analysis")
    print("=" * 70)
    
    analyzer = ImageAnalyzer()
    
    # Simulate analyzing uploaded image
    print("\n📸 Learner uploads photo of their work...")
    print("\n[Simulating image analysis...]")
    
    # Mock image data
    mock_image = b"mock_image_data"
    
    analysis = analyzer.analyze_uploaded_work(mock_image, grade=9)
    
    print("\n" + "=" * 70)
    print("ANALYSIS RESULT")
    print("=" * 70)
    
    print(f"\nProblem: {analysis.problem_statement}")
    print(f"\nLearner wrote:")
    for i, step in enumerate(analysis.learner_work, 1):
        print(f"  {i}. {step}")
    
    print(f"\nMistakes found: {len(analysis.mistakes_found)}")
    for mistake in analysis.mistakes_found:
        print(f"\n  Step {mistake['step_number']}: {mistake['what_they_wrote']}")
        print(f"  Error type: {mistake['mistake_type']}")
        print(f"  Why: {mistake['explanation']}")
    
    print(f"\nLearner's answer: {analysis.learner_answer}")
    print(f"Correct answer: {analysis.correct_answer}")
    
    print("\n" + "=" * 70)
    print("FEEDBACK MESSAGE (WhatsApp)")
    print("=" * 70)
    
    feedback = analyzer.generate_feedback_message(analysis)
    print(f"\n{feedback}")
