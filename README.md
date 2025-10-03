ML Interview Pro - AI-Powered Interview Preparation Bot 🤖
<div align="center"> <img src="./assets/DEMO_ML.jpg" width="80%"> <br> <em>Interactive ML Interview Preparation Platform</em> </div><hr><div align="center">
https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
https://img.shields.io/badge/Groq-00FF00?style=for-the-badge&logo=groq&logoColor=black
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Machine%2520Learning-FF6B6B?style=for-the-badge&logo=ai&logoColor=white
https://img.shields.io/github/license/Sakshi983-cmd/ML_AI_Interview_Chatbot?style=for-the-badge

</div>
🎯 Purpose
ML Interview Pro is an intelligent chatbot designed specifically for machine learning freshers preparing for technical interviews. It provides personalized guidance through multiple AI personas and interactive learning sessions.

🚀 Quick Start
bash
# Clone repository
git clone https://github.com/Sakshi983-cmd/ML_AI_Interview_Chatbot.git
cd ML_AI_Interview_Chatbot

# Install dependencies
pip install -r requirements.txt

# Add API key to .env file
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run application
streamlit run app.py
🏗️ System Architecture
1. Main Application Flow
graph TD
    A[User Input] --> B[Persona Selection]
    B --> C[LLM Processing]
    C --> D[Context-Aware Response]
    D --> E[Interactive Learning]
    E --> F[Progress Tracking]
    
    B --> G[👨‍🏫 Mentor]
    B --> H[👨‍💻 Coder] 
    B --> I[📚 Teacher]
    B --> J[💼 Interviewer]
2. ML Process Flow
graph LR
    A[User Query] --> B[Input Processing]
    B --> C[LLM Engine]
    C --> D[Response Generation]
    D --> E[Learning Analytics]
    
    B --> F[Tokenization]
    B --> G[NLP Preprocessing]
    
    C --> H[Transformer Model]
    C --> I[Autoregressive Generation]
    
    E --> J[Concept Tracking]
    E --> K[Progress Monitoring]
🧠 ML Concepts Used
Stage	ML Concept	Implementation
Input Processing	Tokenization, NLP preprocessing	Handled internally by LLM
LLM Response	Transformer architecture, Autoregressive text generation	Groq API with LLaMA 3.1
Interactive Learning	Keyword tracking, Heuristic analysis	Progress statistics & concept counting
Future Enhancement	Vector embeddings, Similarity search	FAISS/Pinecone integration
🛠 Core Code Implementation
Main Application Setup
python
import streamlit as st
import groq
import os

# Secure environment configuration
def load_env_secure():
    try:
        with open('.env', 'r') as f:
            for line in f:
                if 'GROQ_API_KEY' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
                    return value.strip()
    except FileNotFoundError:
        return None

# LLM Client with Groq API
def get_llm_client():
    API_KEY = load_env_secure()
    if not API_KEY:
        st.error("API Key not found")
        return None
    
    client = groq.Client(api_key=API_KEY)
    return client
Multi-Persona Response System
python
def get_ai_response(user_input, persona, chat_history):
    persona_prompts = {
        "👨‍🏫 Mentor": "Explain concepts like talking to beginners with real examples...",
        "👨‍💻 Coder": "Provide Python code snippets and debugging tips...", 
        "📚 Teacher": "Step-by-step explanations with learning roadmaps...",
        "💼 Interviewer": "Mock interview questions with feedback..."
    }
    
    client = get_llm_client()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": persona_prompts[persona]},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content
Progress Tracking & Analytics
python
# Initialize session state
if "stats" not in st.session_state:
    st.session_state.stats = {
        "questions_asked": 0,
        "concepts_learned": 0, 
        "formulas_shown": 0
    }

# Track learning progress
def update_learning_stats(response):
    if any(keyword in response.lower() for keyword in ['formula', 'equation']):
        st.session_state.stats["formulas_shown"] += 1
    if any(keyword in response.lower() for keyword in ['concept', 'understand']):
        st.session_state.stats["concepts_learned"] += 1
📊 Features
🎭 4 AI Personas: Mentor, Coder, Teacher, Interviewer

📚 Fresher-Focused: Common problems database & ML formulas

📈 Progress Tracking: Real-time learning analytics

🎨 Modern UI: Glass morphism with animations

⚡ Fast Responses: Groq's LPU technology

📁 Project Structure
text
ML_AI_Interview_Chatbot/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── .env                  # API configuration
├── README.md            # Documentation
└── assets/
    ├── DEMO_ML.jpg      # App screenshot
    └── practical.jpg    # Implementation guide
🚀 Usage
Select Persona: Choose from 4 specialized guides

Ask Questions: Use chat or quick access buttons

Track Progress: Monitor learning in sidebar

Practice: Common ML problems & interview questions

📞 Contact
Author: Sakshi Tiwari
GitHub: Sakshi983-cmd

<div align="center"> <img src="./assets/practical.jpg" width="60%"> <br> <em>Practical Implementation Guide</em> </div>
