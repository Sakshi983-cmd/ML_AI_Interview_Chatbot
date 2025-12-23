"""
Production-ready ML/AI Interview Bot (Streamlit)
- Voice (via upload) + Text
- Resume-based question generation
- Auto scoring & feedback
- GenAI Chat
- No backend needed, all-in-one
"""

import streamlit as st
from groq import Groq
import PyPDF2
from io import BytesIO
import speech_recognition as sr
from dotenv import load_dotenv
import os
import tempfile

# Load .env for API key
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_KEY:
    st.error("❌ Please add your GROQ_API_KEY in .env file")
    st.stop()

client = Groq(api_key=GROQ_KEY)
recognizer = sr.Recognizer()

# Streamlit page config
st.set_page_config(page_title="ML/AI Interview Bot", layout="wide")

# ============================================================================
# Helper functions
# ============================================================================

def extract_resume(pdf_file):
    try:
        reader = PyPDF2.PdfReader(BytesIO(pdf_file))
        text = ""
        for page in reader.pages[:5]:
            text += page.extract_text() + "\n"
        return text.strip()
    except:
        return None

def extract_skills(resume_text):
    skills_list = ["Python","PyTorch","TensorFlow","NLP","LLM",
                   "AWS","Docker","Pandas","SQL","Git","Keras","Scikit-Learn"]
    found = [s for s in skills_list if s.lower() in resume_text.lower()]
    return found[:8]

def generate_question(role, q_num):
    try:
        prompt = f"Generate ONE unique ML/AI interview question #{q_num} for role '{role}'. Only question, no answer."
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def score_answer(question, answer, resume_text):
    try:
        if len(answer.strip()) < 20:
            return 5, "❌ Answer too short", "Minimum 20 characters required"
        score = 10
        depth_keywords = ["algorithm","complexity","optimize","pattern","design","approach"]
        depth = min(7, sum(1 for kw in depth_keywords if kw in answer.lower())*2)
        score += depth
        sentences = len([s for s in answer.split('.') if s.strip()])
        clarity = min(3, sentences//2)
        score += clarity
        overlap = len(set(resume_text.lower().split()) & set(answer.lower().split()))
        relevance = min(3, overlap//10)
        score += relevance
        final_score = min(20, score)
        if final_score >= 18: feedback="🌟 Excellent!"
        elif final_score >= 14: feedback="✅ Good"
        else: feedback="⚠️ Needs work"
        reasoning = f"Depth:{depth}/7 | Clarity:{clarity}/3 | Relevance:{relevance}/3"
        return final_score, feedback, reasoning
    except:
        return 0, "Error", "Scoring failed"

def transcribe_voice(audio_file_path):
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except Exception as e:
        return f"Error: {e}"

def chat_response(message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert ML/AI mentor."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ============================================================================
# UI
# ============================================================================

st.title("🚀 ML/AI Interview Bot")
st.markdown("**Voice (via Upload) + Text Interview | Resume-based Questions | Auto Scoring | GenAI Chat**")

# Sidebar
with st.sidebar:
    st.header("📊 Status")
    if "score_total" in st.session_state:
        st.metric("Current Score", st.session_state.score_total, "/100")
    if "q_answered" in st.session_state:
        st.metric("Questions", st.session_state.q_answered, "/5")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Setup", "🎤 Interview", "💬 Chat"])

# ============================================================================
# TAB 1: Setup
# ============================================================================

with tab1:
    st.markdown("### Upload Resume & Configure")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Name")
    with col2:
        role = st.selectbox("🎯 Role", ["ML Engineer", "Data Scientist", "AI Engineer", "NLP Specialist"])
    
    pdf_file = st.file_uploader("📄 Resume PDF", type=["pdf"])
    
    if pdf_file and st.button("✅ Load Resume"):
        resume_text = extract_resume(pdf_file.read())
        if resume_text:
            skills = extract_skills(resume_text)
            st.session_state.resume_text = resume_text
            st.session_state.name = name
            st.session_state.role = role
            st.session_state.skills = skills
            st.session_state.q_answered = 0
            st.session_state.score_total = 0
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.scores = []
            st.session_state.chat_history = []
            st.success(f"✅ Resume loaded. Detected skills: {', '.join(skills[:6])}")
        else:
            st.error("Failed to extract text from PDF")

# ============================================================================
# TAB 2: Interview
# ============================================================================

with tab2:
    if "name" not in st.session_state:
        st.info("👈 Upload resume first")
    else:
        st.markdown(f"### Interview - {st.session_state.name}")
        st.progress(st.session_state.q_answered / 5)
        st.write(f"**Progress: {st.session_state.q_answered}/5**")
        
        if st.session_state.q_answered < 5:
            # Generate question if needed
            if len(st.session_state.questions) <= st.session_state.q_answered:
                with st.spinner("🤖 Generating question..."):
                    q = generate_question(st.session_state.role, st.session_state.q_answered+1)
                    st.session_state.questions.append(q)
            current_q = st.session_state.questions[st.session_state.q_answered]
            st.markdown(f"### Q{st.session_state.q_answered+1}/5")
            st.write(current_q)
            
            # Answer input
            method = st.radio("Choose input method:", ["📝 Type", "🎤 Voice"], horizontal=True)
            answer = None
            if method=="📝 Type":
                answer = st.text_area("Your Answer:", height=200)
            else:
                st.info("Upload voice (.wav or .mp3)")
                audio_file = st.file_uploader("🎤 Record/Upload", type=["wav","mp3"], key="voice")
                if audio_file:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(audio_file.getvalue())
                        tmp_path = tmp.name
                    answer = transcribe_voice(tmp_path)
                    if answer:
                        st.success(f"✅ Heard: {answer[:100]}...")
            
            # Submit
            if st.button("✅ Submit Answer"):
                if not answer or len(answer.strip()) < 20:
                    st.error("Answer too short (min 20 chars)")
                else:
                    score, feedback, reasoning = score_answer(current_q, answer, st.session_state.resume_text)
                    st.session_state.answers.append(answer)
                    st.session_state.scores.append(score)
                    st.session_state.score_total += score
                    st.session_state.q_answered += 1
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"Score: {score}/20")
                    with col2:
                        st.info(f"Feedback: {feedback}")
                    
                    st.write(f"Reasoning: {reasoning}")
                    st.experimental_rerun()  # Safe rerun in latest Streamlit

# ============================================================================
# TAB 3: Chatbot
# ============================================================================

with tab3:
    st.markdown("### Free GenAI Chat")
    st.write("Ask anything about ML/AI, interviews, or career.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for role_name, message in st.session_state.chat_history:
        with st.chat_message(role_name):
            st.write(message)
    
    if prompt := st.chat_input("Your question..."):
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.spinner("🤖 Thinking..."):
            reply = chat_response(prompt)
        
        st.session_state.chat_history.append(("assistant", reply))
        with st.chat_message("assistant"):
            st.write(reply)

st.markdown("---")
st.markdown("**Production Ready | Voice + Text | Resume-Aware | GenAI**")






