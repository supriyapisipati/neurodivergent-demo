"""
Streamlit Cloud deployment version of FocusCoach
Optimized for public sharing and demo purposes
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from focus_techniques import FocusTechniqueManager, PomodoroTimer
import requests
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    
    if 'gmail_connected' not in st.session_state:
        st.session_state.gmail_connected = False
    
    if 'user_deadlines' not in st.session_state:
        st.session_state.user_deadlines = []
    
    if 'calendar_events' not in st.session_state:
        st.session_state.calendar_events = []

def get_gmail_deadlines(gmail_address):
    """Simulate getting deadlines from Gmail (demo version)"""
    # In a real implementation, this would use Gmail API
    # For demo purposes, we'll return sample deadlines
    sample_deadlines = [
        {
            "title": "Quarterly Report Due",
            "date": "2024-01-15",
            "priority": "high",
            "source": "email from SEC"
        },
        {
            "title": "Board Meeting Preparation",
            "date": "2024-01-20",
            "priority": "medium",
            "source": "calendar invite"
        },
        {
            "title": "Audit Review Meeting",
            "date": "2024-01-25",
            "priority": "high",
            "source": "email from auditor"
        },
        {
            "title": "Tax Filing Deadline",
            "date": "2024-01-31",
            "priority": "high",
            "source": "IRS reminder email"
        }
    ]
    
    return sample_deadlines

def analyze_deadlines_for_task(task, deadlines):
    """Analyze deadlines to provide personalized task breakdown"""
    relevant_deadlines = []
    urgency_level = "medium"
    
    # Check for relevant deadlines
    for deadline in deadlines:
        if any(keyword in task.lower() for keyword in ["report", "quarterly", "audit", "tax", "meeting"]):
            if any(keyword in deadline["title"].lower() for keyword in ["report", "quarterly", "audit", "tax", "meeting"]):
                relevant_deadlines.append(deadline)
    
    # Determine urgency
    if relevant_deadlines:
        high_priority_count = sum(1 for d in relevant_deadlines if d["priority"] == "high")
        if high_priority_count > 0:
            urgency_level = "high"
        elif len(relevant_deadlines) > 2:
            urgency_level = "high"
    
    return relevant_deadlines, urgency_level

def personalize_task_breakdown(task, breakdown, deadlines, urgency):
    """Personalize task breakdown based on deadlines and urgency"""
    personalized_breakdown = breakdown.copy()
    
    # Add deadline context
    if deadlines:
        deadline_context = f"📅 **Upcoming Deadlines:**\n"
        for deadline in deadlines[:3]:  # Show top 3 relevant deadlines
            deadline_context += f"• {deadline['title']} - {deadline['date']} ({deadline['priority']} priority)\n"
        
        personalized_breakdown["deadline_context"] = deadline_context
    
    # Adjust time estimates based on urgency
    if urgency == "high":
        # Reduce time estimates for urgent tasks
        for step in personalized_breakdown["steps"]:
            current_time = int(step["estimated_time"])
            step["estimated_time"] = str(max(5, current_time - 5))  # Reduce by 5 minutes, minimum 5
        personalized_breakdown["urgency_note"] = "⚡ **High Priority Task** - Time estimates have been adjusted for urgency"
    elif urgency == "low":
        # Increase time estimates for less urgent tasks
        for step in personalized_breakdown["steps"]:
            current_time = int(step["estimated_time"])
            step["estimated_time"] = str(current_time + 5)  # Add 5 minutes
        personalized_breakdown["urgency_note"] = "🐌 **Low Priority Task** - You have more time to work on this"
    
    # Add deadline-specific tips
    if deadlines:
        personalized_breakdown["deadline_tips"] = [
            "Set up calendar reminders for each step",
            "Break work into smaller chunks to meet deadlines",
            "Ask for help if you're falling behind",
            "Prioritize the most critical sections first"
        ]
    
    return personalized_breakdown

def demo_task_breakdown(task: str, user_context: str = "", gmail_address: str = None) -> dict:
    """Demo version of task breakdown (no API key required)"""
    
    # Get deadlines if Gmail is connected
    deadlines = []
    urgency = "medium"
    if gmail_address:
        try:
            # Check if session state is available (when running in Streamlit)
            if hasattr(st.session_state, 'gmail_connected') and st.session_state.gmail_connected:
                deadlines = get_gmail_deadlines(gmail_address)
                relevant_deadlines, urgency = analyze_deadlines_for_task(task, deadlines)
                st.session_state.user_deadlines = deadlines
            else:
                # Demo mode - simulate Gmail connection
                deadlines = get_gmail_deadlines(gmail_address)
                relevant_deadlines, urgency = analyze_deadlines_for_task(task, deadlines)
        except:
            # Fallback for when session state is not available
            deadlines = get_gmail_deadlines(gmail_address)
            relevant_deadlines, urgency = analyze_deadlines_for_task(task, deadlines)
    
    # Pre-defined breakdowns for common tasks
    demo_breakdowns = {
        "prepare quarterly report": {
            "steps": [
                {"description": "Create the Cover Page with company details", "estimated_time": "10", "tips": "Add company name, ticker symbol, CIK, quarter/year, filing date, and SEC file number"},
                {"description": "Set up Part I - Financial Information section", "estimated_time": "5", "tips": "Create headers for Item 1 (Financial Statements) and Item 2 (MD&A)"},
                {"description": "Add Condensed Consolidated Balance Sheets", "estimated_time": "30", "tips": "Include assets, liabilities, and shareholders' equity for current quarter and prior year-end"},
                {"description": "Create Income Statement (Operations)", "estimated_time": "25", "tips": "Show revenue, expenses, net income/loss for current quarter and YTD vs. prior year"},
                {"description": "Add Comprehensive Income Statement", "estimated_time": "20", "tips": "Include net income plus other comprehensive income (foreign currency, unrealized gains/losses)"},
                {"description": "Create Cash Flow Statement", "estimated_time": "25", "tips": "Show cash from operating, investing, and financing activities (current quarter and YTD vs. prior year)"},
                {"description": "Add Shareholders' Equity Statement", "estimated_time": "20", "tips": "Document changes in stock, retained earnings, treasury stock, etc."},
                {"description": "Write Notes to Financial Statements", "estimated_time": "45", "tips": "Include critical accounting policies, segment info, debt, legal proceedings, risks, subsequent events"},
                {"description": "Write Management's Discussion & Analysis (MD&A)", "estimated_time": "60", "tips": "Explain results of operations, liquidity, trends, risks, uncertainties, and critical accounting estimates"},
                {"description": "Add Market Risk Disclosures (Item 3)", "estimated_time": "20", "tips": "Document exposure to interest rate, foreign currency, commodity price, or equity price risks"},
                {"description": "Complete Controls and Procedures (Item 4)", "estimated_time": "15", "tips": "Evaluate disclosure controls and internal controls, get CEO and CFO signatures"},
                {"description": "Add Part II - Other Information", "estimated_time": "30", "tips": "Include legal proceedings, risk factors, unregistered sales, defaults, other material events"},
                {"description": "Create Exhibits section", "estimated_time": "20", "tips": "List certifications, press releases, material contracts, XBRL data files"},
                {"description": "Add required signatures", "estimated_time": "5", "tips": "Get signatures from principal executive and financial officers"},
                {"description": "Final review and compliance check", "estimated_time": "30", "tips": "Ensure GAAP compliance, check filing deadlines (40-45 days after quarter-end), review for completeness"}
            ],
            "focus_techniques": ["Time blocking for each financial statement", "Pomodoro technique (25 min work, 5 min break)", "Body doubling with accounting team", "Use focus app like Forest", "Break into morning/afternoon sessions"],
            "accommodations": ["Use noise-cancelling headphones", "Set up a comfortable workspace with dual monitors", "Take sensory breaks when needed", "Ask for help from accounting team", "Use templates and checklists", "Have backup data sources ready"],
            "sensory_tips": ["Use natural lighting if possible", "Try instrumental music for focus", "Have fidget tools nearby", "Take movement breaks every hour", "Use comfortable ergonomic setup", "Keep water and healthy snacks nearby"],
            "encouragement": "Quarterly reports are complex but you've got this! Take it one financial statement at a time. Remember, progress not perfection - every section completed is a win!"
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
    breakdown = None
    for key, bd in demo_breakdowns.items():
        if key in task_lower:
            breakdown = bd
            break
    
    # Default breakdown for any task
    if not breakdown:
        breakdown = {
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
    
    # Personalize based on deadlines and urgency
    if gmail_address and deadlines:
        relevant_deadlines, urgency = analyze_deadlines_for_task(task, deadlines)
        breakdown = personalize_task_breakdown(task, breakdown, relevant_deadlines, urgency)
    
    return breakdown

def display_task_breakdown(breakdown):
    """Display the task breakdown in a user-friendly format"""
    if 'error' in breakdown:
        st.error(breakdown['error'])
        return
    
    # Show deadline context if available
    if 'deadline_context' in breakdown:
        st.markdown(f"""
        <div class="demo-notice">
            <h4>📅 Deadline Information</h4>
            <p>{breakdown['deadline_context']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show urgency note if available
    if 'urgency_note' in breakdown:
        st.markdown(f"""
        <div class="encouragement-box">
            <h4>⚡ Priority Level</h4>
            <p>{breakdown['urgency_note']}</p>
        </div>
        """, unsafe_allow_html=True)
    
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
    
    # Deadline-specific tips
    if breakdown.get('deadline_tips'):
        st.subheader("⏰ Deadline Management Tips")
        for tip in breakdown['deadline_tips']:
            st.markdown(f"• {tip}")
    
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
            "Gmail Integration",
            "About FocusCoach"
        ])
        
        st.header("⚙️ Settings")
        st.session_state.user_context = st.text_area(
            "Tell me about your needs:",
            value=st.session_state.user_context,
            help="Share any specific challenges, preferences, or accommodations you need"
        )
        
        # Gmail Integration
        st.header("📧 Gmail Integration")
        gmail_address = st.text_input(
            "Gmail Address (Optional):",
            placeholder="your.email@gmail.com",
            help="Connect your Gmail to get personalized deadline information"
        )
        
        if st.button("🔗 Connect Gmail", type="secondary"):
            if gmail_address and "@gmail.com" in gmail_address:
                st.session_state.gmail_connected = True
                st.success("✅ Gmail connected! I'll analyze your deadlines.")
                # Get deadlines
                st.session_state.user_deadlines = get_gmail_deadlines(gmail_address)
            else:
                st.warning("Please enter a valid Gmail address")
        
        if st.session_state.gmail_connected:
            st.success("📧 Gmail Connected")
            if st.session_state.user_deadlines:
                st.write("**Upcoming Deadlines:**")
                for deadline in st.session_state.user_deadlines[:3]:
                    st.write(f"• {deadline['title']} - {deadline['date']}")
        
        # Quick tips
        st.header("💡 Quick Tips")
        st.markdown("""
        - Break tasks into 5-15 minute chunks
        - Use timers for focus sessions
        - Take breaks when you need them
        - Celebrate small wins!
        - Connect Gmail for personalized deadlines
        """)
    
    # Main content based on selected page
    if page == "Task Breakdown":
        task_breakdown_page()
    elif page == "Focus Sessions":
        focus_sessions_page()
    elif page == "Focus Techniques":
        focus_techniques_page()
    elif page == "Gmail Integration":
        gmail_integration_page()
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
                # Get Gmail address from sidebar if connected
                gmail_address = None
                if st.session_state.gmail_connected:
                    # In a real app, this would come from the sidebar input
                    gmail_address = "demo@example.com"  # Demo Gmail address
                
                breakdown = demo_task_breakdown(task, st.session_state.user_context, gmail_address)
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

def gmail_integration_page():
    """Gmail integration and deadline management"""
    st.header("📧 Gmail Integration & Deadline Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔗 Connect Your Gmail")
        st.markdown("""
        Connect your Gmail to get personalized task breakdowns based on your deadlines and schedule.
        
        **Benefits:**
        - Personalized time estimates based on urgency
        - Deadline-aware task prioritization
        - Calendar integration for better planning
        - Automatic deadline reminders
        """)
        
        gmail_address = st.text_input(
            "Enter your Gmail address:",
            placeholder="your.email@gmail.com",
            help="We'll analyze your emails for deadlines and important dates"
        )
        
        if st.button("🔗 Connect Gmail", type="primary"):
            if gmail_address and "@gmail.com" in gmail_address:
                st.session_state.gmail_connected = True
                st.session_state.user_deadlines = get_gmail_deadlines(gmail_address)
                st.success("✅ Gmail connected successfully!")
            else:
                st.warning("Please enter a valid Gmail address")
    
    with col2:
        st.subheader("📅 Your Deadlines")
        
        if st.session_state.gmail_connected and st.session_state.user_deadlines:
            st.success("📧 Gmail Connected")
            
            for deadline in st.session_state.user_deadlines:
                priority_color = "🔴" if deadline["priority"] == "high" else "🟡" if deadline["priority"] == "medium" else "🟢"
                st.markdown(f"""
                <div class="step-card">
                    <h4>{priority_color} {deadline['title']}</h4>
                    <p><strong>Date:</strong> {deadline['date']}</p>
                    <p><strong>Priority:</strong> {deadline['priority']}</p>
                    <p><strong>Source:</strong> {deadline['source']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Connect your Gmail to see your deadlines and get personalized task breakdowns")
    
    st.subheader("🎯 How Gmail Integration Helps")
    
    benefits = [
        {
            "title": "Personalized Time Estimates",
            "description": "Task breakdowns adjust based on your actual deadlines and urgency levels"
        },
        {
            "title": "Deadline Awareness",
            "description": "See relevant deadlines when breaking down tasks like quarterly reports"
        },
        {
            "title": "Priority Management",
            "description": "High-priority tasks get faster time estimates and urgent accommodations"
        },
        {
            "title": "Calendar Integration",
            "description": "Schedule focus sessions around your existing commitments"
        }
    ]
    
    for benefit in benefits:
        with st.expander(f"🎯 {benefit['title']}"):
            st.write(benefit['description'])
    
    st.subheader("🔒 Privacy & Security")
    st.markdown("""
    - **Demo Mode**: This demo uses sample data for demonstration
    - **Real Integration**: In the full version, we use secure OAuth2 authentication
    - **Data Privacy**: Your emails are never stored or shared
    - **Local Processing**: All analysis happens securely on your device
    """)

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

