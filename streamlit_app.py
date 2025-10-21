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
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --info-color: #3b82f6;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-radius: 12px;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Main header with modern gradient */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Modern card design */
    .step-card {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: var(--border-radius);
        border-left: 6px solid var(--primary-color);
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .step-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
    
    .step-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .step-card h4 {
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    
    .step-card p {
        color: var(--text-secondary);
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    
    /* Status cards with better colors */
    .break-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border-left: 6px solid var(--warning-color);
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    .encouragement-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border-left: 6px solid var(--success-color);
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    .sensory-tip {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        border-left: 4px solid var(--info-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .focus-session {
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border-left: 6px solid var(--secondary-color);
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    .demo-notice {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border-left: 6px solid var(--warning-color);
        margin: 1rem 0;
        box-shadow: var(--shadow);
    }
    
    /* Modern button styles */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Progress indicators */
    .progress-step {
        display: flex;
        align-items: center;
        margin: 1rem 0;
        padding: 1rem;
        background: var(--light-bg);
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
    }
    
    .progress-step .step-number {
        background: var(--primary-color);
        color: white;
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-right: 1rem;
    }
    
    /* Accessibility improvements */
    .high-contrast {
        background: #000;
        color: #fff;
    }
    
    .large-text {
        font-size: 1.2rem;
        line-height: 1.8;
    }
    
    /* Focus indicators */
    .focus-indicator {
        outline: 3px solid var(--primary-color);
        outline-offset: 2px;
    }
    
    /* Sensory-friendly animations */
    .smooth-transition {
        transition: all 0.3s ease;
    }
    
    /* Reduced motion for sensitive users */
    @media (prefers-reduced-motion: reduce) {
        .step-card:hover,
        .stButton > button:hover {
            transform: none;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        :root {
            --light-bg: #1f2937;
            --card-bg: #374151;
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
        }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .step-card {
            padding: 1.5rem;
        }
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
        },
        "prepare for job interview": {
            "steps": [
                {"description": "Research the company and role thoroughly", "estimated_time": "30", "tips": "Check their website, LinkedIn, recent news, and job description"},
                {"description": "Prepare your elevator pitch (30 seconds)", "estimated_time": "15", "tips": "Practice introducing yourself and your key strengths"},
                {"description": "Prepare answers to common questions", "estimated_time": "45", "tips": "Use STAR method: Situation, Task, Action, Result"},
                {"description": "Prepare 3-5 thoughtful questions to ask them", "estimated_time": "15", "tips": "Show genuine interest in the role and company"},
                {"description": "Plan your outfit and test it", "estimated_time": "10", "tips": "Choose something comfortable and professional"},
                {"description": "Prepare your portfolio/resume materials", "estimated_time": "20", "tips": "Print copies, organize digital files, prepare examples"},
                {"description": "Practice with a friend or in front of a mirror", "estimated_time": "30", "tips": "Practice your answers out loud - it helps with confidence"},
                {"description": "Plan your route and timing", "estimated_time": "10", "tips": "Check traffic, parking, and arrive 10 minutes early"},
                {"description": "Prepare for virtual interview (if applicable)", "estimated_time": "15", "tips": "Test your camera, microphone, and internet connection"},
                {"description": "Get a good night's sleep", "estimated_time": "0", "tips": "Rest is crucial for clear thinking and confidence"}
            ],
            "focus_techniques": ["Time blocking for each preparation area", "Practice with a friend", "Record yourself answering questions"],
            "accommodations": ["Prepare in a quiet space", "Use notes as backup", "Practice relaxation techniques", "Have water nearby"],
            "sensory_tips": ["Wear comfortable clothes", "Test your setup beforehand", "Have backup plans", "Take deep breaths before starting"],
            "encouragement": "You've got this! Your unique perspective and skills are valuable. Be yourself and show your passion!"
        },
        "conduct performance review": {
            "steps": [
                {"description": "Review employee's job description and goals", "estimated_time": "15", "tips": "Understand their role and what was expected"},
                {"description": "Gather performance data and examples", "estimated_time": "20", "tips": "Collect specific examples of achievements and areas for improvement"},
                {"description": "Prepare the review document", "estimated_time": "30", "tips": "Use a structured format with clear sections"},
                {"description": "Schedule the meeting with advance notice", "estimated_time": "5", "tips": "Give them time to prepare their own thoughts"},
                {"description": "Prepare your talking points", "estimated_time": "20", "tips": "Focus on specific examples and constructive feedback"},
                {"description": "Set up a comfortable meeting space", "estimated_time": "5", "tips": "Choose a private, comfortable location"},
                {"description": "Start with positive feedback", "estimated_time": "10", "tips": "Begin with what they're doing well"},
                {"description": "Discuss areas for improvement constructively", "estimated_time": "15", "tips": "Be specific and offer support"},
                {"description": "Set goals for the next period", "estimated_time": "15", "tips": "Make goals SMART: Specific, Measurable, Achievable, Relevant, Time-bound"},
                {"description": "Document the discussion", "estimated_time": "10", "tips": "Write down key points and agreed-upon actions"}
            ],
            "focus_techniques": ["Time blocking for preparation", "Practice with a colleague", "Use a structured approach"],
            "accommodations": ["Prepare in advance", "Use templates and checklists", "Have backup materials", "Take breaks if needed"],
            "sensory_tips": ["Choose a comfortable meeting space", "Have water available", "Use natural lighting", "Take notes to stay focused"],
            "encouragement": "Performance reviews are about growth and development. You're helping your team member succeed!"
        },
        "manage project deadline": {
            "steps": [
                {"description": "Break down the project into smaller tasks", "estimated_time": "20", "tips": "List every task, no matter how small"},
                {"description": "Estimate time for each task", "estimated_time": "15", "tips": "Be realistic - add buffer time for unexpected issues"},
                {"description": "Prioritize tasks by importance and urgency", "estimated_time": "10", "tips": "Use the Eisenhower Matrix: urgent/important, not urgent/important, etc."},
                {"description": "Create a project timeline", "estimated_time": "15", "tips": "Use a calendar or project management tool"},
                {"description": "Identify potential roadblocks", "estimated_time": "10", "tips": "Think about what could go wrong and plan alternatives"},
                {"description": "Set up regular check-ins", "estimated_time": "5", "tips": "Schedule daily or weekly progress reviews"},
                {"description": "Start with the most critical tasks", "estimated_time": "30", "tips": "Tackle the hardest or most important work first"},
                {"description": "Track progress daily", "estimated_time": "10", "tips": "Update your task list and adjust timeline as needed"},
                {"description": "Communicate with stakeholders", "estimated_time": "15", "tips": "Keep everyone informed of progress and any issues"},
                {"description": "Prepare for the final push", "estimated_time": "20", "tips": "Review everything, do final quality checks, and prepare for delivery"}
            ],
            "focus_techniques": ["Time blocking for each task", "Pomodoro technique for focused work", "Regular breaks to maintain energy"],
            "accommodations": ["Use project management tools", "Set up reminders and alerts", "Ask for help when needed", "Break work into smaller chunks"],
            "sensory_tips": ["Create a comfortable workspace", "Use noise-cancelling headphones if needed", "Take movement breaks", "Stay hydrated"],
            "encouragement": "You can meet this deadline! Break it down into manageable pieces and tackle one task at a time."
        },
        "handle difficult conversation": {
            "steps": [
                {"description": "Clarify the issue and your goals", "estimated_time": "10", "tips": "What exactly needs to be discussed? What outcome do you want?"},
                {"description": "Prepare your key points", "estimated_time": "15", "tips": "Write down the main points you want to make"},
                {"description": "Practice what you want to say", "estimated_time": "20", "tips": "Practice out loud - it helps you feel more confident"},
                {"description": "Choose the right time and place", "estimated_time": "5", "tips": "Pick a private, comfortable setting when both parties are calm"},
                {"description": "Start with a positive or neutral opening", "estimated_time": "5", "tips": "Begin with something like 'I'd like to discuss...' or 'I've noticed...'"},
                {"description": "Use 'I' statements", "estimated_time": "10", "tips": "Say 'I feel...' instead of 'You always...' to avoid blame"},
                {"description": "Listen actively to their response", "estimated_time": "15", "tips": "Really listen to understand their perspective"},
                {"description": "Stay calm and focused", "estimated_time": "10", "tips": "Take deep breaths if you feel emotional"},
                {"description": "Work toward a solution together", "estimated_time": "15", "tips": "Focus on finding a resolution that works for both parties"},
                {"description": "Follow up on any agreements", "estimated_time": "5", "tips": "Check in later to ensure the solution is working"}
            ],
            "focus_techniques": ["Practice with a trusted friend", "Use breathing exercises", "Prepare talking points in advance"],
            "accommodations": ["Prepare in advance", "Have notes as backup", "Take breaks if needed", "Ask for support from a colleague"],
            "sensory_tips": ["Choose a comfortable setting", "Have water available", "Use calming techniques", "Take deep breaths"],
            "encouragement": "Difficult conversations are part of professional growth. You're being brave by addressing issues directly and constructively."
        },
        "prepare for team meeting": {
            "steps": [
                {"description": "Define the meeting purpose and agenda", "estimated_time": "10", "tips": "What needs to be accomplished? What topics will be covered?"},
                {"description": "Prepare necessary materials", "estimated_time": "15", "tips": "Gather reports, data, presentations, or other documents needed"},
                {"description": "Send agenda to participants in advance", "estimated_time": "5", "tips": "Give everyone time to prepare and contribute"},
                {"description": "Set up the meeting space or technology", "estimated_time": "10", "tips": "Test equipment, reserve room, or set up virtual meeting"},
                {"description": "Prepare your talking points", "estimated_time": "15", "tips": "Outline what you want to say and key questions to ask"},
                {"description": "Anticipate questions and prepare answers", "estimated_time": "10", "tips": "Think about what others might ask and how you'll respond"},
                {"description": "Prepare for different scenarios", "estimated_time": "10", "tips": "What if someone disagrees? What if the discussion goes off-topic?"},
                {"description": "Set time limits for each agenda item", "estimated_time": "5", "tips": "Keep the meeting focused and on schedule"},
                {"description": "Prepare follow-up actions", "estimated_time": "10", "tips": "Think about what needs to happen after the meeting"},
                {"description": "Arrive early to set up", "estimated_time": "5", "tips": "Give yourself time to get comfortable and organized"}
            ],
            "focus_techniques": ["Time blocking for preparation", "Practice your opening", "Use a structured approach"],
            "accommodations": ["Prepare in advance", "Use templates and checklists", "Have backup materials", "Take breaks if needed"],
            "sensory_tips": ["Choose a comfortable meeting space", "Have water available", "Use natural lighting", "Take notes to stay focused"],
            "encouragement": "You're facilitating important discussions that help your team succeed. Your preparation shows your commitment to the team!"
        },
        "create project proposal": {
            "steps": [
                {"description": "Define the problem or opportunity", "estimated_time": "15", "tips": "Clearly articulate what you're trying to solve or achieve"},
                {"description": "Research the background and context", "estimated_time": "30", "tips": "Gather relevant data, market research, and stakeholder information"},
                {"description": "Define your proposed solution", "estimated_time": "25", "tips": "Be specific about what you're proposing and how it addresses the problem"},
                {"description": "Create a project timeline", "estimated_time": "15", "tips": "Break down the work into phases with realistic timeframes"},
                {"description": "Estimate costs and resources needed", "estimated_time": "20", "tips": "Be thorough but realistic about budget and resource requirements"},
                {"description": "Identify risks and mitigation strategies", "estimated_time": "15", "tips": "Think about what could go wrong and how you'll address it"},
                {"description": "Define success metrics", "estimated_time": "10", "tips": "How will you measure if the project is successful?"},
                {"description": "Write the executive summary", "estimated_time": "20", "tips": "Summarize the key points in 1-2 pages"},
                {"description": "Create supporting materials", "estimated_time": "25", "tips": "Charts, graphs, detailed timelines, and other visual aids"},
                {"description": "Review and refine the proposal", "estimated_time": "20", "tips": "Check for clarity, completeness, and persuasiveness"}
            ],
            "focus_techniques": ["Time blocking for each section", "Research in focused sessions", "Use templates and examples"],
            "accommodations": ["Break work into smaller chunks", "Use project management tools", "Ask for feedback from colleagues", "Take breaks between sections"],
            "sensory_tips": ["Create a comfortable workspace", "Use natural lighting", "Have water and snacks nearby", "Take movement breaks"],
            "encouragement": "Your proposal could lead to exciting new opportunities! Take it one section at a time and don't worry about perfection on the first draft."
        },
        "handle customer complaint": {
            "steps": [
                {"description": "Listen actively to the customer", "estimated_time": "10", "tips": "Let them fully explain their issue without interrupting"},
                {"description": "Acknowledge their concern", "estimated_time": "5", "tips": "Show empathy and understanding for their situation"},
                {"description": "Ask clarifying questions", "estimated_time": "10", "tips": "Get specific details about what went wrong and when"},
                {"description": "Take detailed notes", "estimated_time": "5", "tips": "Document everything for follow-up and resolution"},
                {"description": "Apologize sincerely", "estimated_time": "5", "tips": "Take responsibility for any mistakes on your part"},
                {"description": "Explain what happened (if you know)", "estimated_time": "10", "tips": "Be honest about what went wrong without making excuses"},
                {"description": "Propose a solution", "estimated_time": "15", "tips": "Offer specific steps to resolve the issue"},
                {"description": "Get their agreement on the solution", "estimated_time": "10", "tips": "Make sure they're satisfied with your proposed resolution"},
                {"description": "Follow up on the resolution", "estimated_time": "10", "tips": "Check back to ensure the issue is fully resolved"},
                {"description": "Document the incident", "estimated_time": "10", "tips": "Record what happened and how it was resolved for future reference"}
            ],
            "focus_techniques": ["Stay calm and focused", "Use active listening", "Take notes to stay organized"],
            "accommodations": ["Prepare standard responses", "Use templates for documentation", "Ask for help from a supervisor if needed"],
            "sensory_tips": ["Choose a quiet space for the conversation", "Have water available", "Take deep breaths if needed"],
            "encouragement": "Handling complaints well can turn unhappy customers into loyal ones. You're doing important work for the business!"
        }
    }
    
    # Try to find a matching breakdown with improved matching
    task_lower = task.lower()
    breakdown = None
    
    # Check for exact matches first
    for key, bd in demo_breakdowns.items():
        if key in task_lower:
            breakdown = bd
            break
    
    # If no exact match, try keyword matching
    if not breakdown:
        if any(keyword in task_lower for keyword in ["quarterly", "report", "10-q", "sec"]):
            if any(keyword in task_lower for keyword in ["quarterly", "report"]):
                breakdown = demo_breakdowns["prepare quarterly report"]
        elif any(keyword in task_lower for keyword in ["clean", "room", "organize"]):
            breakdown = demo_breakdowns["clean my room"]
        elif any(keyword in task_lower for keyword in ["study", "exam", "test", "learn"]):
            breakdown = demo_breakdowns["study for exam"]
        elif any(keyword in task_lower for keyword in ["write", "blog", "article", "post"]):
            breakdown = demo_breakdowns["write a blog post"]
        elif any(keyword in task_lower for keyword in ["presentation", "present", "speech", "talk"]):
            breakdown = demo_breakdowns["plan a presentation"]
        elif any(keyword in task_lower for keyword in ["interview", "job", "career", "hiring"]):
            breakdown = demo_breakdowns["prepare for job interview"]
        elif any(keyword in task_lower for keyword in ["performance", "review", "evaluation", "feedback"]):
            breakdown = demo_breakdowns["conduct performance review"]
        elif any(keyword in task_lower for keyword in ["project", "deadline", "timeline", "deliverable"]):
            breakdown = demo_breakdowns["manage project deadline"]
        elif any(keyword in task_lower for keyword in ["difficult", "conversation", "conflict", "confrontation"]):
            breakdown = demo_breakdowns["handle difficult conversation"]
        elif any(keyword in task_lower for keyword in ["meeting", "team", "agenda", "facilitate"]):
            breakdown = demo_breakdowns["prepare for team meeting"]
        elif any(keyword in task_lower for keyword in ["proposal", "project", "business", "pitch"]):
            breakdown = demo_breakdowns["create project proposal"]
        elif any(keyword in task_lower for keyword in ["complaint", "customer", "service", "issue"]):
            breakdown = demo_breakdowns["handle customer complaint"]
    
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
        # Accessibility options
        st.markdown("### ♿ Accessibility Options")
        col1, col2 = st.columns(2)
        with col1:
            high_contrast = st.checkbox("High Contrast", help="Increase contrast for better visibility")
        with col2:
            large_text = st.checkbox("Large Text", help="Increase text size for easier reading")
        
        # Navigation
        st.markdown("### 🎯 Navigation")
        page = st.selectbox("Choose a page:", [
            "Task Breakdown",
            "Focus Sessions", 
            "Focus Techniques",
            "Gmail Integration",
            "About FocusCoach"
        ], help="Select what you'd like to work on")
        
        # User preferences
        st.markdown("### ⚙️ Your Preferences")
        st.session_state.user_context = st.text_area(
            "Tell me about your needs:",
            value=st.session_state.user_context,
            help="Share any specific challenges, preferences, or accommodations you need",
            height=100
        )
        
        # Focus session preferences
        st.markdown("### 🎯 Focus Preferences")
        focus_duration = st.slider("Preferred focus time (minutes)", 5, 60, 25, help="How long do you like to focus at once?")
        break_duration = st.slider("Preferred break time (minutes)", 2, 30, 5, help="How long do you like your breaks?")
        
        # Gmail Integration
        st.markdown("### 📧 Gmail Integration")
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
        
        # Quick tips with better formatting
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;">
        <p style="margin: 0.5rem 0;"><strong>🎯 Focus:</strong> Break tasks into 5-15 minute chunks</p>
        <p style="margin: 0.5rem 0;"><strong>⏰ Timing:</strong> Use timers for focus sessions</p>
        <p style="margin: 0.5rem 0;"><strong>🧘 Breaks:</strong> Take breaks when you need them</p>
        <p style="margin: 0.5rem 0;"><strong>🎉 Celebrate:</strong> Small wins matter!</p>
        <p style="margin: 0.5rem 0;"><strong>📧 Connect:</strong> Gmail for personalized deadlines</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Emergency help
        st.markdown("### 🆘 Need Help?")
        if st.button("🆘 I'm Overwhelmed", help="Get immediate support and calming techniques"):
            st.info("""
            **You're not alone! Here's what you can do:**
            
            1. **Take a deep breath** - Count to 4, hold for 4, exhale for 4
            2. **Step away** - Take a 5-minute break
            3. **Break it down** - What's the smallest next step?
            4. **Ask for help** - Reach out to someone you trust
            5. **Be kind to yourself** - You're doing your best
            """)
        
        # Progress tracking
        if 'completed_tasks' not in st.session_state:
            st.session_state.completed_tasks = 0
        
        st.markdown("### 📊 Your Progress")
        st.metric("Tasks Completed", st.session_state.completed_tasks)
        if st.session_state.completed_tasks > 0:
            st.balloons()
    
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
    # Modern header with better spacing
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #1f2937; font-size: 2.5rem; margin-bottom: 0.5rem;">📋 Task Breakdown</h1>
        <p style="color: #6b7280; font-size: 1.2rem; margin-bottom: 0;">Describe a task you'd like help with, and I'll break it down into manageable steps!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show examples of tasks that work well with better design
    with st.expander("💡 Examples of tasks that work well", expanded=False):
        st.markdown("""
        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; border-left: 6px solid #6366f1;">
        <h3 style="color: #1f2937; margin-top: 0;">Try these specific tasks for detailed breakdowns:</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #6366f1; margin-top: 0;">📊 Work & Business</h4>
                <ul style="margin: 0; padding-left: 1rem;">
                    <li><strong>Quarterly Report</strong> - 15 detailed SEC-compliant steps</li>
                    <li><strong>Job Interview</strong> - 10 preparation steps</li>
                    <li><strong>Performance Review</strong> - 10 review management steps</li>
                    <li><strong>Project Deadline</strong> - 10 deadline management steps</li>
                    <li><strong>Difficult Conversation</strong> - 10 conversation handling steps</li>
                    <li><strong>Team Meeting</strong> - 10 meeting preparation steps</li>
                    <li><strong>Project Proposal</strong> - 10 proposal creation steps</li>
                    <li><strong>Customer Complaint</strong> - 10 complaint handling steps</li>
                </ul>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #10b981; margin-top: 0;">🏠 Personal & Academic</h4>
                <ul style="margin: 0; padding-left: 1rem;">
                    <li><strong>Clean My Room</strong> - 8 organization steps</li>
                    <li><strong>Study for Exam</strong> - 10 study techniques</li>
                    <li><strong>Write a Blog Post</strong> - 10 writing steps</li>
                    <li><strong>Plan a Presentation</strong> - 10 presentation steps</li>
                </ul>
            </div>
        </div>
        
        <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <h4 style="color: #92400e; margin-top: 0;">🔍 Keywords that trigger detailed breakdowns:</h4>
            <p style="margin: 0.5rem 0;"><strong>Work:</strong> "quarterly", "report", "interview", "job", "performance", "review", "project", "deadline", "meeting", "proposal", "complaint"</p>
            <p style="margin: 0.5rem 0;"><strong>Personal:</strong> "clean", "room", "study", "exam", "write", "blog", "presentation"</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick test buttons with better design
    st.markdown("""
    <div style="background: #f8fafc; padding: 2rem; border-radius: 12px; margin: 2rem 0;">
        <h2 style="color: #1f2937; text-align: center; margin-bottom: 1.5rem;">🚀 Quick Test Buttons</h2>
        <p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Click any button to get instant detailed breakdowns!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # First row - Personal tasks
    st.markdown("### 🏠 Personal Tasks")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🧹 Clean Room", help="Get 8 organization steps", key="clean_room"):
            task = "clean my room"
    with col2:
        if st.button("📚 Study Exam", help="Get 10 study techniques", key="study_exam"):
            task = "study for exam"
    with col3:
        if st.button("✍️ Blog Post", help="Get 10 writing steps", key="blog_post"):
            task = "write a blog post"
    with col4:
        if st.button("🎤 Presentation", help="Get 10 presentation steps", key="presentation"):
            task = "plan a presentation"
    with col5:
        if st.button("💼 Job Interview", help="Get 10 interview prep steps", key="job_interview"):
            task = "prepare for job interview"
    
    # Second row - Work tasks
    st.markdown("### 💼 Work Tasks")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📊 Quarterly Report", help="Get 15 detailed SEC-compliant steps", key="quarterly_report"):
            task = "prepare quarterly report"
    with col2:
        if st.button("👥 Performance Review", help="Get 10 review steps", key="performance_review"):
            task = "conduct performance review"
    with col3:
        if st.button("⏰ Project Deadline", help="Get 10 deadline management steps", key="project_deadline"):
            task = "manage project deadline"
    with col4:
        if st.button("💬 Difficult Conversation", help="Get 10 conversation steps", key="difficult_conversation"):
            task = "handle difficult conversation"
    with col5:
        if st.button("🤝 Team Meeting", help="Get 10 meeting prep steps", key="team_meeting"):
            task = "prepare for team meeting"
    
    # Third row - Business tasks
    st.markdown("### 🏢 Business Tasks")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📋 Project Proposal", help="Get 10 proposal steps", key="project_proposal"):
            task = "create project proposal"
    with col2:
        if st.button("😤 Customer Complaint", help="Get 10 complaint handling steps", key="customer_complaint"):
            task = "handle customer complaint"
    with col3:
        if st.button("📈 Business Plan", help="Get detailed business planning steps", key="business_plan"):
            task = "create business plan"
    with col4:
        if st.button("💰 Budget Planning", help="Get detailed budget steps", key="budget_planning"):
            task = "create budget"
    with col5:
        if st.button("📊 Data Analysis", help="Get detailed analysis steps", key="data_analysis"):
            task = "analyze data"
    
    # Task input with better design
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin: 2rem 0;">
        <h3 style="color: #1f2937; margin-top: 0;">Or describe your own task:</h3>
    </div>
    """, unsafe_allow_html=True)
    
    task_input = st.text_area(
        "Describe your task:",
        placeholder="e.g., Prepare quarterly report, Clean my room, Study for exam...",
        height=120,
        help="Use specific keywords like 'quarterly report' or 'clean room' for detailed breakdowns",
        key="task_input"
    )
    
    # Use quick test task if available, otherwise use input
    if 'task' not in locals():
        task = task_input
    
    # Break down button with better design
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Break Down This Task", type="primary", use_container_width=True):
            if task.strip():
                with st.spinner("Creating a neurodivergent-friendly plan..."):
                    # Get Gmail address from sidebar if connected
                    gmail_address = None
                    if st.session_state.gmail_connected:
                        # In a real app, this would come from the sidebar input
                        gmail_address = "demo@example.com"  # Demo Gmail address
                    
                    breakdown = demo_task_breakdown(task, st.session_state.user_context, gmail_address)
                    st.session_state.task_breakdown = breakdown
                
                # Track progress
                if 'completed_tasks' not in st.session_state:
                    st.session_state.completed_tasks = 0
                st.session_state.completed_tasks += 1
                
                display_task_breakdown(breakdown)
            else:
                st.warning("Please enter a task to break down!")
    
    # Show progress if tasks have been completed
    if st.session_state.get('completed_tasks', 0) > 0:
        st.markdown("""
        <div style="background: #d1fae5; padding: 1rem; border-radius: 8px; border-left: 4px solid #10b981; margin: 1rem 0;">
            <p style="margin: 0; color: #065f46;"><strong>🎉 Great job!</strong> You've completed {completed_tasks} task breakdowns!</p>
        </div>
        """.format(completed_tasks=st.session_state.completed_tasks), unsafe_allow_html=True)

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
