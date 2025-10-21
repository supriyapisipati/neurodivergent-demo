"""
Focus Techniques for Neurodivergent Users
Specialized techniques and accommodations for executive function challenges
"""

import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum

class FocusTechnique(Enum):
    POMODORO = "pomodoro"
    BODY_DOUBLING = "body_doubling"
    TIME_BLOCKING = "time_blocking"
    CHUNKING = "chunking"
    SENSORY_BREAKS = "sensory_breaks"
    VISUAL_TIMERS = "visual_timers"
    ACCOUNTABILITY = "accountability"

class FocusSession:
    """Represents a focus session with neurodivergent accommodations"""
    
    def __init__(self, technique: FocusTechnique, duration: int = 25, break_duration: int = 5):
        self.technique = technique
        self.duration = duration
        self.break_duration = break_duration
        self.start_time = None
        self.end_time = None
        self.completed = False
        self.accommodations = []
        
    def start(self):
        """Start the focus session"""
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=self.duration)
        self.completed = False
        
    def is_active(self) -> bool:
        """Check if session is currently active"""
        if not self.start_time:
            return False
        return datetime.now() < self.end_time
    
    def time_remaining(self) -> timedelta:
        """Get remaining time in session"""
        if not self.start_time or not self.end_time:
            return timedelta(0)
        remaining = self.end_time - datetime.now()
        return max(remaining, timedelta(0))
    
    def complete(self):
        """Mark session as completed"""
        self.completed = True

class FocusTechniqueManager:
    """Manages focus techniques and accommodations for neurodivergent users"""
    
    def __init__(self):
        self.techniques = {
            FocusTechnique.POMODORO: {
                "name": "Pomodoro Technique",
                "description": "25 minutes of focused work followed by a 5-minute break",
                "duration": 25,
                "break_duration": 5,
                "accommodations": [
                    "Use a visual timer",
                    "Set up a comfortable workspace",
                    "Have water and snacks nearby",
                    "Use noise-cancelling headphones if needed"
                ],
                "sensory_considerations": [
                    "Adjust lighting to reduce eye strain",
                    "Use fidget tools if helpful",
                    "Take movement breaks between sessions"
                ]
            },
            FocusTechnique.BODY_DOUBLING: {
                "name": "Body Doubling",
                "description": "Work alongside someone else for accountability and motivation",
                "duration": 30,
                "break_duration": 10,
                "accommodations": [
                    "Find a study/work partner",
                    "Use video calls for virtual body doubling",
                    "Join online focus groups",
                    "Set up regular check-ins"
                ],
                "sensory_considerations": [
                    "Choose a quiet, comfortable space",
                    "Use headphones to reduce distractions",
                    "Have backup plans if partner cancels"
                ]
            },
            FocusTechnique.TIME_BLOCKING: {
                "name": "Time Blocking",
                "description": "Dedicate specific time slots to different tasks",
                "duration": 45,
                "break_duration": 15,
                "accommodations": [
                    "Use calendar apps with visual blocks",
                    "Set multiple reminders",
                    "Color-code different task types",
                    "Build in buffer time between blocks"
                ],
                "sensory_considerations": [
                    "Use visual timers and calendars",
                    "Create a dedicated workspace for each block",
                    "Have transition rituals between blocks"
                ]
            },
            FocusTechnique.CHUNKING: {
                "name": "Task Chunking",
                "description": "Break large tasks into small, manageable pieces",
                "duration": 15,
                "break_duration": 5,
                "accommodations": [
                    "Use task management apps",
                    "Create visual progress trackers",
                    "Set micro-goals for each chunk",
                    "Celebrate completion of each chunk"
                ],
                "sensory_considerations": [
                    "Use visual progress indicators",
                    "Have sensory rewards for completed chunks",
                    "Take movement breaks between chunks"
                ]
            },
            FocusTechnique.SENSORY_BREAKS: {
                "name": "Sensory Breaks",
                "description": "Regular breaks that address sensory needs",
                "duration": 20,
                "break_duration": 10,
                "accommodations": [
                    "Set up a sensory break station",
                    "Use fidget tools and stress balls",
                    "Practice deep breathing exercises",
                    "Take short walks or stretches"
                ],
                "sensory_considerations": [
                    "Adjust lighting and temperature",
                    "Use weighted blankets or compression",
                    "Listen to calming music or white noise",
                    "Practice grounding techniques"
                ]
            }
        }
    
    def get_technique_info(self, technique: FocusTechnique) -> Dict[str, Any]:
        """Get detailed information about a focus technique"""
        return self.techniques.get(technique, {})
    
    def suggest_technique(self, task_type: str, user_preferences: Dict[str, Any] = None) -> FocusTechnique:
        """Suggest the best focus technique based on task type and user preferences"""
        
        suggestions = {
            "writing": FocusTechnique.POMODORO,
            "reading": FocusTechnique.CHUNKING,
            "planning": FocusTechnique.TIME_BLOCKING,
            "creative": FocusTechnique.SENSORY_BREAKS,
            "collaborative": FocusTechnique.BODY_DOUBLING,
            "overwhelming": FocusTechnique.CHUNKING,
            "repetitive": FocusTechnique.POMODORO,
            "complex": FocusTechnique.TIME_BLOCKING
        }
        
        # Check user preferences
        if user_preferences:
            if user_preferences.get('needs_accountability'):
                return FocusTechnique.BODY_DOUBLING
            if user_preferences.get('sensory_sensitive'):
                return FocusTechnique.SENSORY_BREAKS
            if user_preferences.get('gets_overwhelmed'):
                return FocusTechnique.CHUNKING
        
        return suggestions.get(task_type.lower(), FocusTechnique.POMODORO)
    
    def create_focus_session(self, technique: FocusTechnique, custom_duration: int = None) -> FocusSession:
        """Create a new focus session with the specified technique"""
        technique_info = self.get_technique_info(technique)
        
        duration = custom_duration or technique_info.get('duration', 25)
        break_duration = technique_info.get('break_duration', 5)
        
        session = FocusSession(technique, duration, break_duration)
        session.accommodations = technique_info.get('accommodations', [])
        
        return session
    
    def get_accommodations(self, challenge: str) -> List[str]:
        """Get accommodations for specific challenges"""
        
        accommodations = {
            "focus_difficulties": [
                "Use a visual timer with color changes",
                "Try the Pomodoro technique (25 min work, 5 min break)",
                "Use noise-cancelling headphones",
                "Create a distraction-free workspace",
                "Use focus apps like Forest or Freedom"
            ],
            "time_management": [
                "Use visual timers and calendars",
                "Set multiple alarms and reminders",
                "Use time estimation games",
                "Try body doubling for accountability",
                "Use calendar blocking techniques"
            ],
            "sensory_overload": [
                "Adjust lighting (natural light preferred)",
                "Use fidget tools or stress balls",
                "Try different seating options",
                "Use white noise or calming music",
                "Take regular movement breaks"
            ],
            "executive_function": [
                "Break tasks into smaller steps",
                "Use visual organization tools",
                "Create step-by-step checklists",
                "Use task management apps",
                "Ask for help when needed"
            ],
            "motivation": [
                "Set small, achievable goals",
                "Use rewards and celebrations",
                "Find an accountability partner",
                "Track progress visually",
                "Remember that progress, not perfection, matters"
            ]
        }
        
        return accommodations.get(challenge.lower(), accommodations["focus_difficulties"])
    
    def get_sensory_tips(self, sensory_needs: List[str]) -> List[str]:
        """Get sensory-friendly tips based on specific needs"""
        
        sensory_tips = {
            "visual": [
                "Use natural lighting when possible",
                "Adjust screen brightness and contrast",
                "Use color-coding for organization",
                "Create visual progress indicators",
                "Use large, clear fonts"
            ],
            "auditory": [
                "Use noise-cancelling headphones",
                "Try white noise or nature sounds",
                "Use instrumental music for focus",
                "Create a quiet workspace",
                "Use earplugs if needed"
            ],
            "tactile": [
                "Use fidget tools and stress balls",
                "Try different seating options",
                "Use weighted blankets or compression",
                "Have comfortable clothing",
                "Use textured materials for grounding"
            ],
            "movement": [
                "Take regular movement breaks",
                "Use a standing desk or exercise ball",
                "Practice stretching and yoga",
                "Take short walks",
                "Use fidget tools that allow movement"
            ],
            "proprioceptive": [
                "Use weighted blankets or compression",
                "Try deep pressure activities",
                "Use resistance bands or exercise",
                "Practice deep breathing",
                "Use grounding techniques"
            ]
        }
        
        all_tips = []
        for need in sensory_needs:
            all_tips.extend(sensory_tips.get(need.lower(), []))
        
        return list(set(all_tips))  # Remove duplicates
    
    def create_personalized_plan(self, task: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create a personalized focus plan based on user profile"""
        
        # Determine best technique
        technique = self.suggest_technique(
            user_profile.get('task_type', 'general'),
            user_profile.get('preferences', {})
        )
        
        # Create session
        session = self.create_focus_session(technique)
        
        # Get accommodations
        accommodations = []
        for challenge in user_profile.get('challenges', []):
            accommodations.extend(self.get_accommodations(challenge))
        
        # Get sensory tips
        sensory_tips = self.get_sensory_tips(user_profile.get('sensory_needs', []))
        
        return {
            "technique": technique.value,
            "session_duration": session.duration,
            "break_duration": session.break_duration,
            "accommodations": list(set(accommodations)),  # Remove duplicates
            "sensory_tips": sensory_tips,
            "technique_info": self.get_technique_info(technique),
            "encouragement": self.get_encouragement(user_profile.get('mood', 'neutral'))
        }
    
    def get_encouragement(self, mood: str) -> str:
        """Get encouraging messages based on current mood"""
        
        encouragements = {
            "overwhelmed": [
                "It's okay to feel overwhelmed. Take a deep breath and remember: you don't have to do everything at once.",
                "You're not alone in feeling this way. Many successful people face these challenges too.",
                "Start with just one small step. That's already progress worth celebrating."
            ],
            "frustrated": [
                "Frustration is a normal part of learning and growing. You're doing better than you think.",
                "It's okay to take breaks when you need them. Your well-being comes first.",
                "Every expert was once a beginner. You're learning and that's amazing."
            ],
            "motivated": [
                "You've got this! Your determination is inspiring.",
                "Look at you taking charge of your productivity. That's fantastic!",
                "Your commitment to finding what works for you is admirable."
            ],
            "neutral": [
                "You're taking steps to improve your productivity. That's worth celebrating.",
                "Every small step forward is progress. Keep going!",
                "You're building skills and strategies that will serve you well."
            ]
        }
        
        import random
        return random.choice(encouragements.get(mood, encouragements["neutral"]))

class PomodoroTimer:
    """A specialized Pomodoro timer with neurodivergent accommodations"""
    
    def __init__(self, work_duration: int = 25, break_duration: int = 5, long_break_duration: int = 15):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.long_break_duration = long_break_duration
        self.current_session = None
        self.session_count = 0
        self.is_work_session = True
        
    def start_work_session(self):
        """Start a work session"""
        self.current_session = FocusSession(FocusTechnique.POMODORO, self.work_duration, self.break_duration)
        self.current_session.start()
        self.is_work_session = True
        
    def start_break_session(self):
        """Start a break session"""
        # Determine break duration (long break every 4 sessions)
        break_duration = self.long_break_duration if self.session_count % 4 == 0 else self.break_duration
        
        self.current_session = FocusSession(FocusTechnique.POMODORO, break_duration, 0)
        self.current_session.start()
        self.is_work_session = False
        
    def complete_session(self):
        """Complete the current session"""
        if self.current_session:
            self.current_session.complete()
            if self.is_work_session:
                self.session_count += 1
            self.current_session = None
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        if not self.current_session:
            return {"status": "idle", "message": "No active session"}
        
        if self.current_session.is_active():
            remaining = self.current_session.time_remaining()
            session_type = "Work" if self.is_work_session else "Break"
            return {
                "status": "active",
                "type": session_type,
                "remaining_minutes": int(remaining.total_seconds() // 60),
                "remaining_seconds": int(remaining.total_seconds() % 60),
                "session_count": self.session_count
            }
        else:
            return {
                "status": "completed",
                "type": "Work" if self.is_work_session else "Break",
                "message": "Session completed! Time for a break." if self.is_work_session else "Break completed! Ready for work."
            }

if __name__ == "__main__":
    # Test the focus techniques
    manager = FocusTechniqueManager()
    
    # Test technique suggestion
    technique = manager.suggest_technique("writing", {"needs_accountability": True})
    print(f"Suggested technique: {technique.value}")
    
    # Test personalized plan
    user_profile = {
        "task_type": "writing",
        "challenges": ["focus_difficulties", "time_management"],
        "sensory_needs": ["visual", "auditory"],
        "preferences": {"needs_accountability": True},
        "mood": "overwhelmed"
    }
    
    plan = manager.create_personalized_plan("Write a report", user_profile)
    print("Personalized plan:")
    print(json.dumps(plan, indent=2))
