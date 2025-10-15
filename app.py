import streamlit as st
import time
import groq
import requests
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# SECURE .env loading with better error handling
def load_env_secure():
    try:
        # Try to get from environment variables first
        api_key = os.getenv('GROQ_API_KEY')
        if api_key:
            print("✅ API Key loaded from environment variables")
            return api_key
            
        # Fallback to .env file
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() == 'GROQ_API_KEY':
                        print(f"✅ API Key loaded from .env file")
                        return value.strip()
        print("❌ GROQ_API_KEY not found")
        return None
    except FileNotFoundError:
        print("❌ .env file not found")
        return None
    except Exception as e:
        print(f"❌ Error loading environment: {e}")
        return None

# Load API key at startup
API_KEY = load_env_secure()

# LLM Client Setup - SIMPLIFIED
def get_llm_client():
    if not API_KEY:
        return None
    
    try:
        client = groq.Client(api_key=API_KEY)
        return client
    except Exception as e:
        st.sidebar.error(f"❌ API Error: {str(e)}")
        return None

# Page Configuration
st.set_page_config(
    page_title="ML Interview Pro - Fresher's Guide",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Animations (SAME AS BEFORE)
st.markdown("""
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 8s ease infinite;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
        font-size: 1.2rem;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        margin: 15px 0;
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 15px 0;
        animation: slideInRight 0.6s ease;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 15px 0;
        animation: slideInLeft 0.6s ease;
        max-width: 85%;
        border-left: 6px solid #4ECDC4;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        border: 1px solid rgba(0,0,0,0.1);
    }
    
    .formula-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #ffd700;
    }
    
    .problem-box {
        background: rgba(255,107,107,0.1);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #FF6B6B;
    }
    
    .quick-chip {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        padding: 12px 20px;
        margin: 8px;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.3);
        font-size: 0.9rem;
    }
    
    .quick-chip:hover {
        background: rgba(255,255,255,0.25);
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .typing-animation {
        display: inline-block;
    }
    
    .typing-animation::after {
        content: '▋';
        animation: typing 1s infinite;
        margin-left: 2px;
        color: #4ECDC4;
        font-weight: bold;
    }
    
    @keyframes typing {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .stats-box {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
    
    .api-status {
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
    }
    
    .api-connected {
        background: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        border: 2px solid #4CAF50;
    }
    
    .api-disconnected {
        background: rgba(244, 67, 54, 0.2);
        color: #F44336;
        border: 2px solid #F44336;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced LLM Response with Fresher Focus - SIMPLIFIED
def get_ai_response(user_input, persona, chat_history):
    client = get_llm_client()
    if not client:
        return "🚧 **API Connection Issue**\n\nPlease check your .env file and ensure:\n- GROQ_API_KEY is set in environment variables or .env file\n- Internet connection is working\n- API key is valid\n\nYou can get free API key from: https://console.groq.com"

    # Fresher-focused prompts
    persona_prompts = {
        "👨‍🏫 Mentor": "You are an experienced ML mentor guiding freshers. Explain concepts simply with real-world examples, common mistakes, and learning resources.",
        "👨‍💻 Coder": "You are a practical ML engineer. Provide Python code, explain libraries, debugging tips, and real project examples.",
        "📚 Teacher": "You are a patient teacher. Break down complex topics step-by-step with analogies and practice exercises.",
        "💼 Interviewer": "You are a tech interviewer. Ask relevant questions, evaluate answers, and provide interview tips."
    }
    
    # Build conversation context
    messages = [
        {"role": "system", "content": f"{persona_prompts[persona]}\n\nCurrent Date: {datetime.now().strftime('%Y-%m-%d')}\nYou're helping ML freshers with real problems."}
    ]
    
    # Add limited conversation history
    for msg in chat_history[-4:]:  # Reduced from 6 to 4
        messages.append({"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]})
    
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=800,  # Increased tokens
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"🚧 **Service Temporarily Unavailable**\n\nPlease try again in a few moments.\n\nError: {str(e)}"

# Initialize Session State - IMPROVED
def init_session():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []
        st.session_state.persona = "👨‍🏫 Mentor"
        st.session_state.stats = {"questions_asked": 0, "concepts_learned": 0, "formulas_shown": 0}

# Fresher Problems Database (SAME AS BEFORE)
FRESHER_PROBLEMS = {
    "🤔 Conceptual": [
        "What exactly is the difference between AI, ML, and DL?",
        "Why do we need both training and testing datasets?",
        "What is overfitting in simple terms?",
        "Explain bias-variance tradeoff with real example",
        "What are embeddings in NLP?"
    ],
    "💻 Implementation": [
        "How to handle missing values in a dataset?",
        "What's the difference between fit() and transform()?",
        "How to choose the right evaluation metric?",
        "Why do we need feature scaling?",
        "How to deal with imbalanced datasets?"
    ],
    "📊 Mathematics": [
        "Explain gradient descent with analogy",
        "What is backpropagation actually doing?",
        "Why do we use activation functions?",
        "Explain the math behind CNN filters",
        "What are loss functions and why do we need them?"
    ],
    "🚀 Career": [
        "What projects should I build as a fresher?",
        "How to prepare for ML interviews?",
        "What skills are companies looking for?",
        "Should I learn TensorFlow or PyTorch first?",
        "How to transition from academic to industry?"
    ]
}

def handle_problem_click(problem):
    """Handle problem button clicks without rerun issues"""
    st.session_state.messages.append({"role": "user", "content": problem})
    st.session_state.stats["questions_asked"] += 1

def main():
    init_session()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Interview Setup")
        
        # API Status
        if API_KEY:
            st.markdown('<div class="api-status api-connected">✅ API Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="api-status api-disconnected">❌ API Not Found</div>', unsafe_allow_html=True)
            st.info("Add GROQ_API_KEY to .env file or environment variables")
        
        # Persona Selection - FIXED
        st.markdown("#### 🎭 Choose Your Guide")
        personas = ["👨‍🏫 Mentor", "👨‍💻 Coder", "📚 Teacher", "💼 Interviewer"]
        
        selected_persona = st.radio(
            "Select your guide:",
            personas,
            index=personas.index(st.session_state.persona),
            label_visibility="collapsed"
        )
        
        if selected_persona != st.session_state.persona:
            st.session_state.persona = selected_persona
            st.rerun()
        
        st.divider()
        
        # Fresher Problems Quick Access - FIXED
        st.markdown("#### 🚨 Common Fresher Problems")
        for category, problems in FRESHER_PROBLEMS.items():
            with st.expander(category):
                for problem in problems:
                    if st.button(problem, key=f"prob_{problem[:20]}", use_container_width=True):
                        handle_problem_click(problem)
                        st.rerun()
        
        st.divider()
        
        # Learning Resources - FIXED
        st.markdown("#### 📚 Quick Resources")
        resource_options = {
            "🧮 ML Formulas": "Show me important ML formulas with examples",
            "📖 Book Suggestions": "Suggest books for ML beginners with details", 
            "🎯 Study Plan": "Create a 3-month study plan for ML freshers"
        }
        
        for resource, prompt in resource_options.items():
            if st.button(resource, key=f"res_{resource}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.stats["questions_asked"] += 1
                st.rerun()
        
        st.divider()
        
        # Stats
        st.markdown("#### 📊 Your Progress")
        st.markdown(f"**Questions Asked:** {st.session_state.stats['questions_asked']}")
        st.markdown(f"**Concepts Learned:** {st.session_state.stats['concepts_learned']}")
        st.markdown(f"**Formulas Mastered:** {st.session_state.stats['formulas_shown']}")
        
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.stats = {"questions_asked": 0, "concepts_learned": 0, "formulas_shown": 0}
            st.rerun()

    # Main Content Area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">ML Interview Pro</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">🤖 Your Personal AI Mentor for Machine Learning Interviews • Fresher-Focused</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="stats-box">'
                   f'<h3>🎯 {st.session_state.persona}</h3>'
                   f'<p>Active Guide</p>'
                   f'</div>', unsafe_allow_html=True)

    # Problem Categories - FIXED
    st.markdown("### 🚀 What's Troubling You?")
    
    cols = st.columns(4)
    problem_categories = [
        ("🤔 Conceptual", "Understand core concepts"),
        ("💻 Implementation", "Code and practical issues"), 
        ("📊 Mathematics", "Math behind algorithms"),
        ("🚀 Career", "Jobs and interviews")
    ]
    
    for i, (title, desc) in enumerate(problem_categories):
        with cols[i]:
            if st.button(f"**{title}**\n{desc}", key=f"cat_{i}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"I need help with {title.lower()} problems. Can you explain with examples?"
                })
                st.session_state.stats["questions_asked"] += 1
                st.rerun()

    # Interactive Tips Section
    st.markdown("### 💡 Pro Tips for Freshers")
    
    tip_cols = st.columns(3)
    tips = [
        ("🎯 Build Projects", "Start with small, end-to-end projects"),
        ("📚 Learn Fundamentals", "Don't skip math and statistics"),
        ("💼 Practice Interviews", "Regular mock interviews are key")
    ]
    
    for i, (tip, description) in enumerate(tips):
        with tip_cols[i]:
            st.markdown(f'<div class="tip-box">'
                       f'<h4>{tip}</h4>'
                       f'<p>{description}</p>'
                       f'</div>', unsafe_allow_html=True)

    # Chat Interface - FIXED
    st.markdown("### 💬 Interactive Learning Session")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">'
                       f'<strong>You:</strong><br>{message["content"]}'
                       f'</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">'
                       f'<strong>🤖 {st.session_state.persona}:</strong><br>{message["content"]}'
                       f'</div>', unsafe_allow_html=True)
    
    # Enhanced Chat Input
    if prompt := st.chat_input(f"Ask {st.session_state.persona} about ML concepts, problems, or career advice..."):
        # Update stats
        st.session_state.stats["questions_asked"] += 1
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        with st.spinner(f"🤖 {st.session_state.persona} is thinking..."):
            ai_response = get_ai_response(prompt, st.session_state.persona, st.session_state.messages)
        
        # Add AI response directly (removed typing animation for stability)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Update learning stats
        if any(keyword in ai_response.lower() for keyword in ['formula', 'equation', 'math']):
            st.session_state.stats["formulas_shown"] += 1
        if any(keyword in ai_response.lower() for keyword in ['concept', 'understand', 'explain']):
            st.session_state.stats["concepts_learned"] += 1
            
        st.rerun()

if __name__ == "__main__":
    main()
   
      
      
        
