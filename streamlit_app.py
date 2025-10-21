"""
Streamlit Cloud deployment version of FocusCoach
Optimized for public sharing and demo purposes
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from focus_techniques import FocusTechniqueManager, PomodoroTimer

# Page configuration
st.set_page_config(
    page_title="FocusCoach - Neurodivergent Productivity Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for neurodivergent-friendly design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .step-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .break-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .encouragement-box {
        background: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .sensory-tip {
        background: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .focus-session {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #9c27b0;
        margin: 1rem 0;
    }
    
    .demo-notice {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'focus_manager' not in st.session_state:
        st.session_state.focus_manager = FocusTechniqueManager()
    
    if 'task_breakdown' not in st.session_state:
        st.session_state.task_breakdown = None
    
    if 'user_context' not in st.session_state:
        st.session_state.user_context = ""

def demo_task_breakdown(task: str, user_context: str = "") -> dict:
    """Demo version of task breakdown (no API key required)"""
    
    # Pre-defined breakdowns for common tasks
    demo_breakdowns = {
        "prepare quarterly report": {
            "steps": [
                {"description": "Set up your document and add the title", "estimated_time": "5", "tips": "Start with 'Q[1-4] [Year] Quarterly Report' - don't overthink it!"},
                {"description": "Gather all necessary data and documents", "estimated_time": "15", "tips": "Use a timer and take breaks every 15 minutes"},
                {"description": "Create an outline with main sections", "estimated_time": "10", "tips": "Use bullet points: Executive Summary, Key Metrics, Challenges, Next Steps"},
                {"description": "Write the Executive Summary (2-3 paragraphs)", "estimated_time": "20", "tips": "Start with key points, details can come later"},
                {"description": "Add your key metrics section with numbers", "estimated_time": "15", "tips": "Use bullet points and simple tables"},
                {"description": "Write about challenges and solutions", "estimated_time": "15", "tips": "Be honest and specific - what went wrong and how you fixed it"},
                {"description": "Add charts and graphs to visualize data", "estimated_time": "20", "tips": "Use simple charts - bar graphs and pie charts work well"},
                {"description": "Write the 'Next Quarter Goals' section", "estimated_time": "10", "tips": "Keep it simple - 3-5 specific goals"},
                {"description": "Review and edit the final report", "estimated_time": "15", "tips": "Read it out loud to catch any issues"},
                {"description": "Add your signature and date", "estimated_time": "2", "tips": "You're almost done! Just add your name and today's date"}
            ],
            "focus_techniques": ["Pomodoro technique (25 min work, 5 min break)", "Body doubling with a colleague", "Use a focus app like Forest"],
            "accommodations": ["Use noise-cancelling headphones", "Set up a comfortable workspace", "Take sensory breaks when needed", "Ask for help if you get stuck"],
            "sensory_tips": ["Use natural lighting if possible", "Try instrumental music for focus", "Have fidget tools nearby", "Take movement breaks every hour"],
            "encouragement": "You've got this! Remember, progress not perfection. Every small step counts!"
        },
        "clean my room": {
            "steps": [
                {"description": "Start by making your bed", "estimated_time": "3", "tips": "This gives you an instant sense of accomplishment!"},
                {"description": "Pick up and put away 5 items", "estimated_time": "10", "tips": "Start small - even 5 items is progress"},
                {"description": "Sort clothes into clean/dirty piles", "estimated_time": "15", "tips": "Use a timer and take breaks"},
                {"description": "Put dirty clothes in hamper, hang clean ones", "estimated_time": "10", "tips": "Don't worry about folding perfectly - just get them off the floor"},
                {"description": "Organize one surface (desk, dresser, etc.)", "estimated_time": "20", "tips": "Focus on one area at a time"},
                {"description": "Take a 5-minute break", "estimated_time": "5", "tips": "Hydrate and stretch"},
                {"description": "Tackle one more area", "estimated_time": "15", "tips": "Celebrate what you've accomplished so far"},
                {"description": "Do a final sweep - put away any remaining items", "estimated_time": "10", "tips": "You're almost done! Just a few more items to go"}
            ],
            "focus_techniques": ["Chunking technique", "Body doubling with a friend", "Use a timer for each step"],
            "accommodations": ["Play music you enjoy", "Use a comfortable outfit", "Take breaks when needed", "Ask for help if you get overwhelmed"],
            "sensory_tips": ["Open windows for fresh air", "Use gloves if textures bother you", "Take movement breaks", "Use a comfortable pace"],
            "encouragement": "Every small step makes a difference! You're doing great!"
        },
        "study for exam": {
            "steps": [
                {"description": "Gather all your study materials (books, notes, laptop)", "estimated_time": "5", "tips": "Set up your study space first - it helps your brain get ready"},
                {"description": "Review the study guide or syllabus", "estimated_time": "15", "tips": "Don't try to memorize everything at once"},
                {"description": "Create a study schedule for the week", "estimated_time": "10", "tips": "Break it into manageable chunks"},
                {"description": "Start with the easiest topic first", "estimated_time": "20", "tips": "Build confidence by starting with what you know"},
                {"description": "Take a 5-minute break", "estimated_time": "5", "tips": "Move around and hydrate"},
                {"description": "Study one challenging topic for 25 minutes", "estimated_time": "25", "tips": "Use the Pomodoro technique"},
                {"description": "Take another 5-minute break", "estimated_time": "5", "tips": "Stretch and have a snack"},
                {"description": "Review what you just studied", "estimated_time": "10", "tips": "Summarize in your own words"},
                {"description": "Create flashcards or summary notes", "estimated_time": "15", "tips": "Writing helps you remember better"},
                {"description": "Test yourself on what you studied", "estimated_time": "10", "tips": "Quiz yourself - it's the best way to see what you know"}
            ],
            "focus_techniques": ["Pomodoro technique", "Active recall methods", "Study with a friend"],
            "accommodations": ["Use noise-cancelling headphones", "Find a quiet study space", "Take regular breaks", "Use study apps if helpful"],
            "sensory_tips": ["Good lighting is important", "Comfortable seating", "Have water and snacks nearby", "Take movement breaks"],
            "encouragement": "You're building knowledge step by step. You've got this!"
        },
        "write a blog post": {
            "steps": [
                {"description": "Open your document and add a working title", "estimated_time": "3", "tips": "Don't worry about the perfect title - you can change it later"},
                {"description": "Brainstorm 5-7 key points you want to cover", "estimated_time": "10", "tips": "Use bullet points - don't overthink it"},
                {"description": "Write the introduction paragraph", "estimated_time": "15", "tips": "Start with a hook - why should people read this?"},
                {"description": "Write the first main point", "estimated_time": "20", "tips": "Just start writing - you can edit later"},
                {"description": "Take a 5-minute break", "estimated_time": "5", "tips": "Step away and stretch"},
                {"description": "Write the second main point", "estimated_time": "20", "tips": "Keep the momentum going"},
                {"description": "Add the third main point", "estimated_time": "20", "tips": "You're getting into the flow now"},
                {"description": "Write a conclusion paragraph", "estimated_time": "10", "tips": "Summarize your main points and add a call to action"},
                {"description": "Read through and edit for clarity", "estimated_time": "15", "tips": "Read it out loud to catch any awkward phrases"},
                {"description": "Add a final title and publish", "estimated_time": "5", "tips": "You did it! Time to share your thoughts with the world"}
            ],
            "focus_techniques": ["Pomodoro technique", "Free writing", "Body doubling with a writing partner"],
            "accommodations": ["Use a distraction-free writing app", "Set up a comfortable writing space", "Have water and snacks nearby", "Take breaks when you get stuck"],
            "sensory_tips": ["Good lighting is important", "Comfortable seating", "Background music if helpful", "Take movement breaks"],
            "encouragement": "Your voice matters! Every word you write is progress."
        },
        "plan a presentation": {
            "steps": [
                {"description": "Open a new document and write your topic at the top", "estimated_time": "2", "tips": "Keep it simple - just the main topic"},
                {"description": "Write down your main message in one sentence", "estimated_time": "5", "tips": "What do you want people to remember?"},
                {"description": "Create an outline with 3-5 main points", "estimated_time": "15", "tips": "Use bullet points - keep it simple"},
                {"description": "Write a brief introduction", "estimated_time": "10", "tips": "Tell them what you're going to tell them"},
                {"description": "Develop your first main point", "estimated_time": "20", "tips": "Add examples or stories to make it interesting"},
                {"description": "Take a 5-minute break", "estimated_time": "5", "tips": "Step away and think about your audience"},
                {"description": "Develop your second main point", "estimated_time": "20", "tips": "Keep it relevant to your main message"},
                {"description": "Add your third main point", "estimated_time": "20", "tips": "You're building a strong case"},
                {"description": "Write a conclusion that summarizes your points", "estimated_time": "10", "tips": "End with a clear takeaway"},
                {"description": "Practice your presentation out loud", "estimated_time": "15", "tips": "Practice makes perfect - you've got this!"}
            ],
            "focus_techniques": ["Time blocking", "Practice with a friend", "Record yourself practicing"],
            "accommodations": ["Use presentation software you're comfortable with", "Practice in a quiet space", "Have notes as backup", "Ask for feedback from trusted people"],
            "sensory_tips": ["Practice in the actual space if possible", "Wear comfortable clothes", "Have water nearby", "Take deep breaths before starting"],
            "encouragement": "You have valuable insights to share. Your audience is lucky to hear from you!"
        }
    }
    
    # Try to find a matching breakdown
    task_lower = task.lower()
    for key, breakdown in demo_breakdowns.items():
        if key in task_lower:
            return breakdown
    
    # Default breakdown for any task
    return {
        "steps": [
            {"description": f"Start with: {task}", "estimated_time": "15", "tips": "Break it into smaller pieces"},
            {"description": "Take a 5-minute break", "estimated_time": "5", "tips": "Rest and recharge"},
            {"description": "Continue with the next part", "estimated_time": "15", "tips": "Keep going at your own pace"},
            {"description": "Review what you've accomplished", "estimated_time": "10", "tips": "Celebrate your progress"}
        ],
        "focus_techniques": ["Pomodoro technique", "Body doubling", "Time blocking"],
        "accommodations": ["Use timers", "Take frequent breaks", "Ask for help when needed"],
        "sensory_tips": ["Comfortable lighting", "Noise-cancelling headphones", "Fidget tools"],
        "encouragement": "Remember: progress, not perfection. You're doing great!"
    }

def display_task_breakdown(breakdown):
    """Display the task breakdown in a user-friendly format"""
    if 'error' in breakdown:
        st.error(breakdown['error'])
        return
    
    # Steps
    st.subheader("📝 Your Step-by-Step Plan")
    for i, step in enumerate(breakdown.get('steps', []), 1):
        with st.container():
            st.markdown(f"""
            <div class="step-card">
                <h4>Step {i}: {step.get('description', 'No description')}</h4>
                <p><strong>⏱️ Time:</strong> {step.get('estimated_time', '15')} minutes</p>
                <p><strong>💡 Tips:</strong> {step.get('tips', 'Take your time and be patient with yourself')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Focus techniques
    if breakdown.get('focus_techniques'):
        st.subheader("🎯 Suggested Focus Techniques")
        for technique in breakdown['focus_techniques']:
            st.markdown(f"• {technique}")
    
    # Accommodations
    if breakdown.get('accommodations'):
        st.subheader("🛠️ Accommodations & Tools")
        for accommodation in breakdown['accommodations']:
            st.markdown(f"• {accommodation}")
    
    # Sensory tips
    if breakdown.get('sensory_tips'):
        st.subheader("🌿 Sensory-Friendly Tips")
        for tip in breakdown['sensory_tips']:
            st.markdown(f"""
            <div class="sensory-tip">
                {tip}
            </div>
            """, unsafe_allow_html=True)
    
    # Encouragement
    if breakdown.get('encouragement'):
        st.markdown(f"""
        <div class="encouragement-box">
            <h4>💪 Encouragement</h4>
            <p>{breakdown['encouragement']}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application interface"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 FocusCoach</h1>
        <p>Your supportive productivity assistant for executive function challenges</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo notice
    st.markdown("""
    <div class="demo-notice">
        <h4>🎬 Demo Mode</h4>
        <p>This is a demo version of FocusCoach. In the full version, you can connect your OpenAI API key for personalized AI responses and Google Calendar for automatic scheduling.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.selectbox("Choose a page:", [
            "Task Breakdown",
            "Focus Sessions", 
            "Focus Techniques",
            "About FocusCoach"
        ])
        
        st.header("⚙️ Settings")
        st.session_state.user_context = st.text_area(
            "Tell me about your needs:",
            value=st.session_state.user_context,
            help="Share any specific challenges, preferences, or accommodations you need"
        )
        
        # Quick tips
        st.header("💡 Quick Tips")
        st.markdown("""
        - Break tasks into 5-15 minute chunks
        - Use timers for focus sessions
        - Take breaks when you need them
        - Celebrate small wins!
        """)
    
    # Main content based on selected page
    if page == "Task Breakdown":
        task_breakdown_page()
    elif page == "Focus Sessions":
        focus_sessions_page()
    elif page == "Focus Techniques":
        focus_techniques_page()
    elif page == "About FocusCoach":
        about_page()

def task_breakdown_page():
    """Task breakdown and planning interface"""
    st.header("📋 Task Breakdown")
    st.markdown("Describe a task you'd like help with, and I'll break it down into manageable steps!")
    
    # Task input
    task = st.text_area(
        "What task would you like help with?",
        placeholder="e.g., Prepare quarterly report, Clean my room, Study for exam...",
        height=100
    )
    
    if st.button("🚀 Break Down This Task", type="primary"):
        if task.strip():
            with st.spinner("Creating a neurodivergent-friendly plan..."):
                breakdown = demo_task_breakdown(task, st.session_state.user_context)
                st.session_state.task_breakdown = breakdown
            
            display_task_breakdown(breakdown)
        else:
            st.warning("Please enter a task to break down!")

def focus_sessions_page():
    """Focus session management"""
    st.header("⏰ Focus Sessions")
    st.markdown("Manage your focus sessions with neurodivergent-friendly techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Start a Focus Session")
        task_type = st.selectbox("What type of task?", [
            "general", "writing", "reading", "planning"
        ])
        
        duration = st.slider("Session duration (minutes)", 5, 60, 25)
        break_time = st.slider("Break duration (minutes)", 2, 15, 5)
        
        if st.button("🚀 Start Focus Session", type="primary"):
            session_info = st.session_state.focus_manager.suggest_focus_session(task_type)
            st.session_state.current_session = {
                'type': task_type,
                'duration': duration,
                'break_time': break_time,
                'start_time': datetime.now()
            }
            st.success(f"Focus session started! Duration: {duration} minutes")
    
    with col2:
        st.subheader("📊 Session Statistics")
        if 'current_session' in st.session_state:
            session = st.session_state.current_session
            elapsed = datetime.now() - session['start_time']
            remaining = timedelta(minutes=session['duration']) - elapsed
            
            st.metric("Elapsed Time", f"{elapsed.seconds // 60} minutes")
            st.metric("Remaining", f"{remaining.seconds // 60} minutes")
            
            if remaining.total_seconds() <= 0:
                st.success("🎉 Focus session complete! Time for a break!")
                if st.button("☕ Take a Break"):
                    st.info("Great job! Take a {break_time} minute break.".format(
                        break_time=session['break_time']
                    ))
    
    # Focus techniques
    st.subheader("🧠 Focus Techniques")
    techniques = [
        "Pomodoro Technique (25 min work, 5 min break)",
        "Body Doubling (work alongside someone else)",
        "Time Blocking (dedicated time slots)",
        "Chunking (break work into small pieces)",
        "Sensory Breaks (movement, fidgeting, etc.)"
    ]
    
    for technique in techniques:
        st.markdown(f"• {technique}")

def focus_techniques_page():
    """Focus techniques and accommodations"""
    st.header("🧠 Focus Techniques & Accommodations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Focus Techniques")
        
        techniques = {
            "Pomodoro Technique": {
                "description": "25 minutes of focused work followed by a 5-minute break",
                "best_for": "Writing, studying, repetitive tasks",
                "accommodations": ["Use a visual timer", "Set up a comfortable workspace", "Have water and snacks nearby"]
            },
            "Body Doubling": {
                "description": "Work alongside someone else for accountability and motivation",
                "best_for": "Overwhelming tasks, staying focused, motivation",
                "accommodations": ["Find a study/work partner", "Use video calls for virtual body doubling", "Join online focus groups"]
            },
            "Time Blocking": {
                "description": "Dedicate specific time slots to different tasks",
                "best_for": "Planning, complex projects, time management",
                "accommodations": ["Use calendar apps with visual blocks", "Set multiple reminders", "Color-code different task types"]
            },
            "Task Chunking": {
                "description": "Break large tasks into small, manageable pieces",
                "best_for": "Overwhelming projects, executive function challenges",
                "accommodations": ["Use task management apps", "Create visual progress trackers", "Set micro-goals for each chunk"]
            }
        }
        
        for technique, info in techniques.items():
            with st.expander(f"🎯 {technique}"):
                st.write(f"**Description:** {info['description']}")
                st.write(f"**Best for:** {info['best_for']}")
                st.write("**Accommodations:**")
                for accommodation in info['accommodations']:
                    st.write(f"• {accommodation}")
    
    with col2:
        st.subheader("🌿 Sensory Accommodations")
        
        sensory_tips = {
            "Visual": [
                "Use natural lighting when possible",
                "Adjust screen brightness and contrast",
                "Use color-coding for organization",
                "Create visual progress indicators"
            ],
            "Auditory": [
                "Use noise-cancelling headphones",
                "Try white noise or nature sounds",
                "Use instrumental music for focus",
                "Create a quiet workspace"
            ],
            "Tactile": [
                "Use fidget tools and stress balls",
                "Try different seating options",
                "Use weighted blankets or compression",
                "Have comfortable clothing"
            ],
            "Movement": [
                "Take regular movement breaks",
                "Use a standing desk or exercise ball",
                "Practice stretching and yoga",
                "Take short walks"
            ]
        }
        
        for sense, tips in sensory_tips.items():
            with st.expander(f"🌿 {sense} Accommodations"):
                for tip in tips:
                    st.write(f"• {tip}")

def about_page():
    """About FocusCoach"""
    st.header("🧠 About FocusCoach")
    
    st.markdown("""
    ## What is FocusCoach?
    
    FocusCoach is a supportive AI-powered productivity assistant designed specifically for neurodivergent individuals who face executive function challenges like task overwhelm, time blindness, and focus maintenance.
    
    ## Key Features
    
    ### 🧠 Neurodivergent-Friendly Design
    - **Gentle Language**: Non-judgmental, encouraging prompts throughout
    - **Sensory Accommodations**: Tips for lighting, noise, movement, and comfort
    - **Flexible Options**: Adapts to individual needs and preferences
    - **Progress Over Perfection**: Celebrates small wins and progress
    
    ### 🎯 Focus Techniques
    - **Pomodoro Technique**: 25 min work, 5 min break
    - **Body Doubling**: Work alongside someone else for accountability
    - **Time Blocking**: Dedicated time slots for different tasks
    - **Task Chunking**: Break large tasks into small, manageable pieces
    - **Sensory Breaks**: Regular breaks addressing sensory needs
    
    ### 📱 User-Friendly Interface
    - **Visual Design**: High contrast, clear fonts, color-coded elements
    - **Accessibility**: Keyboard navigation, screen reader compatibility
    - **Customization**: Settings that adapt to your specific needs
    - **Encouragement**: Supportive messaging that builds confidence
    
    ## Who Can Benefit?
    
    - Neurodivergent individuals (ADHD, autism, etc.)
    - People with executive function challenges
    - Anyone who benefits from structured task management
    - Users who need sensory accommodations
    - People who prefer gentle, supportive tools
    
    ## How It Works
    
    1. **Describe Your Task**: Tell FocusCoach what you need help with
    2. **Get a Plan**: Receive a step-by-step breakdown with accommodations
    3. **Choose Techniques**: Select focus methods that work for you
    4. **Stay Supported**: Get encouragement and tips throughout
    
    ## Demo vs Full Version
    
    **This Demo Version:**
    - Shows how FocusCoach works
    - Pre-defined task breakdowns
    - Focus technique suggestions
    - Sensory accommodation tips
    
    **Full Version Includes:**
    - Personalized AI responses with OpenAI GPT-4
    - Google Calendar integration for automatic scheduling
    - Custom task breakdowns for any task
    - Advanced focus session management
    - Progress tracking and analytics
    
    ## Getting Started
    
    To use the full version:
    1. Set up your OpenAI API key
    2. (Optional) Connect Google Calendar
    3. Start breaking down tasks and managing focus sessions
    4. Customize settings for your specific needs
    
    ## Remember
    
    This tool is designed to support you, not to add pressure. Use it in whatever way works best for your brain and your needs. Progress, not perfection! 🌟
    """)
    
    st.markdown("""
    <div class="encouragement-box">
        <h4>💪 You've Got This!</h4>
        <p>Every small step is progress. Every challenge is an opportunity to learn and grow. You're not alone in this journey, and FocusCoach is here to support you every step of the way.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
