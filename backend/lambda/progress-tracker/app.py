"""
Progress Tracker for AI Tutor South Africa
==========================================

Tracks learner progress over time, identifying improvement areas
and celebrating achievements.
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math


class Topic(Enum):
    """Mathematics topics aligned to CAPS/IEB curriculum"""
    # Grades 1-3
    COUNTING = "counting"
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    PATTERNS = "patterns"
    
    # Grades 4-6
    FRACTIONS = "fractions"
    DECIMALS = "decimals"
    GEOMETRY_BASICS = "geometry_basics"
    MEASUREMENT = "measurement"
    
    # Grades 7-9
    ALGEBRA_BASICS = "algebra_basics"
    LINEAR_EQUATIONS = "linear_equations"
    GEOMETRY = "geometry"
    RATIO_PERCENTAGE = "ratio_percentage"
    
    # Grades 10-12
    ALGEBRA = "algebra"
    FUNCTIONS = "functions"
    TRIGONOMETRY = "trigonometry"
    CALCULUS = "calculus"
    STATISTICS = "statistics"
    PROBABILITY = "probability"


class SkillLevel(Enum):
    """Learner skill levels"""
    BEGINNER = 1
    DEVELOPING = 2
    COMPETENT = 3
    PROFICIENT = 4
    ADVANCED = 5


@dataclass
class ProblemAttempt:
    """Record of a single problem attempt"""
    problem_id: str
    topic: Topic
    subtopic: str
    learner_response: str
    correct: bool
    hints_used: int
    time_taken_seconds: int
    misconceptions_detected: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class LearnerProgress:
    """Comprehensive progress tracking for a learner"""
    learner_id: str
    grade: int
    language: str
    
    # Overall stats
    total_attempts: int = 0
    correct_attempts: int = 0
    total_time_minutes: float = 0
    
    # Topic mastery (topic -> skill level)
    topic_mastery: Dict[str, int] = field(default_factory=dict)
    
    # Identified weak areas
    weak_areas: List[str] = field(default_factory=list)
    
    # Misconception patterns
    misconception_patterns: Dict[str, int] = field(default_factory=dict)
    
    # Recent attempts (last 10)
    recent_attempts: List[Dict] = field(default_factory=list)
    
    # Streak tracking
    current_streak: int = 0
    longest_streak: int = 0
    
    def get_accuracy(self) -> float:
        """Calculate overall accuracy percentage"""
        if self.total_attempts == 0:
            return 0
        return round((self.correct_attempts / self.total_attempts) * 100, 1)
    
    def get_skill_level(self, topic: Topic) -> SkillLevel:
        """Get skill level for a specific topic"""
        level = self.topic_mastery.get(topic.value, 0)
        return SkillLevel(min(max(level, 1), 5))


class ProgressTracker:
    """
    Tracks and analyzes learner progress over time.
    
    Features:
    - Topic mastery tracking
    - Misconception pattern identification
    - Streak tracking for motivation
    - Personalized recommendations
    """
    
    def __init__(self):
        self.learners: Dict[str, LearnerProgress] = {}
        
    def record_attempt(self, learner_id: str, attempt: ProblemAttempt) -> LearnerProgress:
        """
        Record a problem attempt and update progress.
        
        Args:
            learner_id: Learner's phone number or ID
            attempt: The problem attempt record
            
        Returns:
            Updated learner progress
        """
        
        # Get or create learner progress
        progress = self.learners.get(learner_id)
        if not progress:
            progress = LearnerProgress(
                learner_id=learner_id,
                grade=9,  # Default - should be set from profile
                language="en"
            )
            self.learners[learner_id] = progress
        
        # Update overall stats
        progress.total_attempts += 1
        if attempt.correct:
            progress.correct_attempts += 1
            progress.current_streak += 1
            progress.longest_streak = max(progress.longest_streak, progress.current_streak)
        else:
            progress.current_streak = 0
        
        progress.total_time_minutes += attempt.time_taken_seconds / 60
        
        # Update topic mastery
        topic = attempt.topic.value
        current_mastery = progress.topic_mastery.get(topic, 0)
        
        if attempt.correct and attempt.hints_used == 0:
            # Strong performance - increase mastery
            progress.topic_mastery[topic] = min(current_mastery + 1, 5)
        elif attempt.correct and attempt.hints_used <= 2:
            # Good performance with hints
            progress.topic_mastery[topic] = max(current_mastery, current_mastery + 0.5)
        elif not attempt.correct:
            # Wrong answer - note weak area
            if topic not in progress.weak_areas:
                progress.weak_areas.append(topic)
        
        # Track misconception patterns
        for misconception in attempt.misconceptions_detected:
            count = progress.misconception_patterns.get(misconception, 0)
            progress.misconception_patterns[misconception] = count + 1
        
        # Add to recent attempts
        attempt_dict = {
            "problem_id": attempt.problem_id,
            "topic": topic,
            "correct": attempt.correct,
            "hints_used": attempt.hints_used,
            "timestamp": attempt.timestamp
        }
        progress.recent_attempts.append(attempt_dict)
        
        # Keep only last 10 attempts
        if len(progress.recent_attempts) > 10:
            progress.recent_attempts = progress.recent_attempts[-10:]
        
        return progress
    
    def get_progress_report(self, learner_id: str) -> Dict:
        """
        Generate a comprehensive progress report for a learner.
        
        Args:
            learner_id: Learner's phone number or ID
            
        Returns:
            Progress report with stats and recommendations
        """
        
        progress = self.learners.get(learner_id)
        if not progress:
            return {
                "status": "no_data",
                "message": "No progress data yet. Start learning!"
            }
        
        # Calculate improvement trajectory
        recent = progress.recent_attempts[-5:] if len(progress.recent_attempts) >= 5 else progress.recent_attempts
        recent_accuracy = sum(1 for a in recent if a["correct"]) / len(recent) * 100 if recent else 0
        
        # Identify top misconceptions
        top_misconceptions = sorted(
            progress.misconception_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(progress)
        
        return {
            "overall": {
                "total_problems": progress.total_attempts,
                "correct": progress.correct_attempts,
                "accuracy": progress.get_accuracy(),
                "time_spent_minutes": round(progress.total_time_minutes, 1),
                "current_streak": progress.current_streak,
                "longest_streak": progress.longest_streak
            },
            "topics": {
                topic: {
                    "mastery_level": mastery,
                    "skill_level": SkillLevel(min(max(int(mastery), 1), 5)).name
                }
                for topic, mastery in progress.topic_mastery.items()
            },
            "weak_areas": progress.weak_areas,
            "misconception_patterns": dict(top_misconceptions),
            "recent_accuracy": round(recent_accuracy, 1),
            "recommendations": recommendations,
            "achievements": self._get_achievements(progress)
        }
    
    def _generate_recommendations(self, progress: LearnerProgress) -> List[Dict]:
        """Generate personalized recommendations based on progress"""
        
        recommendations = []
        
        # If accuracy is low, recommend easier problems
        if progress.get_accuracy() < 50:
            recommendations.append({
                "type": "practice_easier",
                "message": "Let's build your confidence! Try some easier problems first.",
                "action": "practice_basics"
            })
        
        # If weak areas identified, recommend focused practice
        if progress.weak_areas:
            recommendations.append({
                "type": "focus_area",
                "message": f"Let's work on {progress.weak_areas[0].replace('_', ' ')}",
                "action": f"practice_{progress.weak_areas[0]}"
            })
        
        # If streak is long, celebrate and encourage
        if progress.current_streak >= 5:
            recommendations.append({
                "type": "celebration",
                "message": f"🔥 Amazing! {progress.current_streak} problems in a row!",
                "action": "keep_going"
            })
        
        # If strong in a topic, recommend advancement
        strong_topics = [t for t, m in progress.topic_mastery.items() if m >= 4]
        if strong_topics:
            recommendations.append({
                "type": "advance",
                "message": f"You're crushing {strong_topics[0]}! Ready for harder problems?",
                "action": "challenge_mode"
            })
        
        return recommendations
    
    def _get_achievements(self, progress: LearnerProgress) -> List[Dict]:
        """Unlock achievements based on progress"""
        
        achievements = []
        
        # First problem
        if progress.total_attempts >= 1:
            achievements.append({
                "id": "first_step",
                "title": "First Step 🎯",
                "description": "Solved your first problem!",
                "unlocked": True
            })
        
        # 10 problems
        if progress.total_attempts >= 10:
            achievements.append({
                "id": "getting_started",
                "title": "Getting Started 📚",
                "description": "Attempted 10 problems",
                "unlocked": True
            })
        
        # 100 problems
        if progress.total_attempts >= 100:
            achievements.append({
                "id": "dedicated",
                "title": "Dedicated Learner 🌟",
                "description": "Attempted 100 problems!",
                "unlocked": True
            })
        
        # Streak achievements
        if progress.longest_streak >= 5:
            achievements.append({
                "id": "on_fire",
                "title": "On Fire! 🔥",
                "description": "5 correct answers in a row",
                "unlocked": True
            })
        
        if progress.longest_streak >= 10:
            achievements.append({
                "id": "unstoppable",
                "title": "Unstoppable! 🚀",
                "description": "10 correct answers in a row!",
                "unlocked": True
            })
        
        return achievements


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("PROGRESS TRACKER DEMO")
    print("=" * 60)
    
    tracker = ProgressTracker()
    
    # Simulate learner attempts
    learner_id = "+27123456789"
    
    attempts = [
        ProblemAttempt(
            problem_id="prob_001",
            topic=Topic.LINEAR_EQUATIONS,
            subtopic="solving_for_x",
            learner_response="x = 4",
            correct=True,
            hints_used=0,
            time_taken_seconds=45,
            misconceptions_detected=[]
        ),
        ProblemAttempt(
            problem_id="prob_002",
            topic=Topic.LINEAR_EQUATIONS,
            subtopic="solving_for_x",
            learner_response="x = 5",
            correct=False,
            hints_used=2,
            time_taken_seconds=90,
            misconceptions_detected=["inverse_operation_confusion"]
        ),
        ProblemAttempt(
            problem_id="prob_003",
            topic=Topic.LINEAR_EQUATIONS,
            subtopic="word_problems",
            learner_response="x = 12",
            correct=True,
            hints_used=1,
            time_taken_seconds=60,
            misconceptions_detected=[]
        ),
        ProblemAttempt(
            problem_id="prob_004",
            topic=Topic.FRACTIONS,
            subtopic="adding_fractions",
            learner_response="3/4",
            correct=True,
            hints_used=0,
            time_taken_seconds=30,
            misconceptions_detected=[]
        ),
        ProblemAttempt(
            problem_id="prob_005",
            topic=Topic.FRACTIONS,
            subtopic="multiplying_fractions",
            learner_response="2/6",
            correct=True,
            hints_used=0,
            time_taken_seconds=25,
            misconceptions_detected=[]
        ),
    ]
    
    for attempt in attempts:
        tracker.record_attempt(learner_id, attempt)
        status = "✓" if attempt.correct else "✗"
        print(f"\n{status} Problem {attempt.problem_id}: {attempt.topic.value}")
        print(f"   Response: {attempt.learner_response}")
        print(f"   Hints used: {attempt.hints_used}")
    
    # Generate progress report
    print("\n" + "=" * 60)
    print("PROGRESS REPORT")
    print("=" * 60)
    
    report = tracker.get_progress_report(learner_id)
    print(json.dumps(report, indent=2))
