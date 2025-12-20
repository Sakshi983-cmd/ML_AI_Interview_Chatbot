"""
ML/AI Interview Bot - Advanced UI/UX + Free Chatbot
Production Ready | Beautiful Animations | All Features
"""

import streamlit as st
from groq import Groq
import logging
import time
from datetime import datetime

from utils.resume_parser import ResumeParser
from utils.scoring_engine import ScoringEngine
from utils.pdf_generator import PDFReportGenerator
from utils.cache_manager import CacheManager
from utils.metrics import MetricsCollector
from utils.rate_limiter import RateLimiter

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
st.set_page_config(
    page_title="ML/AI Interview Bot 2025",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ADVANCED CSS - ANIMATIONS & BEAUTIFUL UI
# ============================================================================

st.markdown("""
<style>
    :root {
        --primary: #6366f1;
        --dark-bg: #0f172a;
        --secondary-bg: #1e293b;
        --text: #e2e8f0;
        --accent: #10b981;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 100%);
    }
    
    .main-title {
        background: linear-gradient(45deg, #6366f1, #10b981, #6366f1);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease infinite;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 20px;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #10b981;
        font-size: 1.2rem;
        animation: fadeInUp 1s ease;
        margin-bottom: 30px;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .feature-card {
        background: rgba(99, 102, 241, 0.1);
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease;
    }
    
    .feature-card:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.8);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #10b981 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        animation: buttonBounce 0.6s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
    }
    
    @keyframes buttonBounce {
        0% { transform: scale(0.9); opacity: 0; }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .metric-card {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .question-card {
        background: rgba(99, 102, 241, 0.12);
        border: 2px solid rgba(99, 102, 241, 0.4);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        animation: questionAppear 0.5s ease;
    }
    
    @keyframes questionAppear {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .chat-message {
        padding: 12px 15px;
        border-radius: 10px;
        margin: 8px 0;
        animation: chatSlideIn 0.3s ease;
    }
    
    @keyframes chatSlideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .bot-message {
        background: rgba(99, 102, 241, 0.15);
        border-left: 4px solid #6366f1;
    }
    
    .user-message {
        background: rgba(16, 185, 129, 0.15);
        border-left: 4px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# VOICE RECORDING HTML
# ============================================================================

VOICE_HTML = """
<div style="padding: 20px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(99, 102, 241, 0.1)); border-radius: 15px; border: 2px solid rgba(99, 102, 241, 0.3); text-align: center;">
    <h3 style="color: #10b981; margin-bottom: 15px;">🎤 Voice Recording</h3>
    <button id="recordBtn" onclick="startRec()" style="padding: 12px 30px; background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);">🎤 Start Recording</button>
    <button id="stopBtn" onclick="stopRec()" style="display:none; padding: 12px 30px; background: linear-gradient(135deg, #ef4444, #dc2626); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);">⏹️ Stop</button>
    <div id="status" style="margin-top: 15px; font-weight: bold; color: #10b981; min-height: 30px;">Ready</div>
</div>

<script>
let mediaRecorder; let chunks = [];
async function startRec() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({audio: true});
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = e => chunks.push(e.data);
        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, {type: 'audio/webm'});
            const reader = new FileReader();
            reader.onload = () => {
                window.parent.postMessage({type: 'AUDIO_DATA', data: reader.result.split(',')[1]}, '*');
            };
            reader.readAsDataURL(blob);
        };
        mediaRecorder.start();
        document.getElementById('recordBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'inline-block';
        document.getElementById('status').innerHTML = '🔴 Recording...';
    } catch(e) {
        document.getElementById('status').innerHTML = '❌ ' + e.message;
    }
}
function stopRec() {
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(t => t.stop());
    document.getElementById('recordBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').style.display = 'none';
    document.getElementById('status').innerHTML = '✅ Processing...';
}
</script>
"""

# ============================================================================
# INITIALIZATION
# ============================================================================

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    st.error("❌ GROQ API Key missing")
    st.stop()

if 'client' not in st.session_state:
    st.session_state.client = Groq(api_key=GROQ_API_KEY)
    st.session_state.cache = CacheManager()
    st.session_state.metrics = MetricsCollector()
    st.session_state.rate_limiter = RateLimiter()
    st.session_state.chat_history = []
    logger.info("✅ Components initialized")

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-title">🚀 ML/AI Interview Bot 2025</div>
<div class="subtitle">Advanced UI • Free Chatbot • All Features</div>
""", unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["🎯 Interview", "💬 Free Chatbot", "📊 Dashboard"])

# ============================================================================
# TAB 1: INTERVIEW
# ============================================================================

with tab1:
    st.markdown("### 📋 Start Your Interview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        name = st.text_input("👤 Your Name", placeholder="Sakshi Kumar")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        role = st.selectbox("🎯 Role", 
            ["ML Engineer", "Data Scientist", "AI Engineer", "NLP Specialist"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        resume_file = st.file_uploader("📄 Resume (PDF)", type="pdf")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if name and resume_file and role:
        with st.spinner("🔄 Analyzing resume..."):
            resume_text = ResumeParser.extract_pdf(resume_file)
            if not resume_text:
                st.error("❌ Could not parse PDF")
                st.stop()
            skills = ResumeParser.extract_skills(resume_text)
