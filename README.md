 🚀 Fully Functional ML/AI Interview Preparation Bot
A production-ready, voice-enabled and text-based AI interview chatbot designed for ML/AI aspirants and engineers. The system is resume-aware, auto-scores answers, and provides GenAI-powered chat guidance.

 LOOM DEMO VIDEO- https://www.loom.com/share/1a90ecb0958a48f6bd88c9362c3da381
Features

Resume-Aware Interview
Upload your resume (PDF), and the bot generates questions tailored to your profile and skills.

Voice + Text Interaction
Answer questions via typing or voice (WAV/MP3). Real-time transcription converts voice to text.

Auto Scoring System
Provides scores (0–20 per question) with feedback, reasoning, and detailed explanation.

GenAI Chatbot
Ask anything about ML, AI, career guidance, or interviews. Powered by LLM (Groq API).

Progress Tracking & Logging
Questions answered, total score, and feedback stored in session state for review.

System Design Showcase
Demonstrates end-to-end workflow design, logging, and real-time interaction suitable for production.

Tech Stack
Layer	Tools / Libraries
Frontend	Streamlit
Voice & Transcription	SpeechRecognition, PyAudio, Python
Resume Parsing	PyPDF2
GenAI / LLM	Groq API (LLaMA-based models)
Python Environment	3.11+
Deployment	Local / VS Code, Loom Video Demo
Screenshots / Demo

Loom Video Demo: Watch Here

Local Run Screenshot:

Installation & Setup

Clone the repo

git clone <your-github-repo-link>
cd ML_AI_Interview_Chatbot


Setup Python environment

python -m venv venv
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt


Add API Key
Create a .env file:

GROQ_API_KEY=your_groq_api_key_here


Run the app locally

streamlit run app.py


Open in browser: http://localhost:8501/

Optional
Record your answers with voice, type your answers, and get real-time scoring + feedback.

Usage

Go to Setup Tab

Enter Name, Role, and upload your resume.

Go to Interview Tab

Answer ML/AI interview questions via typing or voice.

Get score and detailed feedback for each question.

Track progress until 5 questions are answered.

Go to Chat Tab

Ask any AI/ML-related questions.

Get real-time GenAI responses.

Why This Project?

Practical Experience: Demonstrates ML/AI understanding, real-time LLM integration, voice processing, and resume-aware question generation.

Recruiter-Ready: Shows system design, logging, and AI workflow understanding.

Future-Ready (2025): Highlights LLM, RAG, and Generative AI capabilities relevant to current AI roles.

Notes

Ensure Python 3.11+ is installed.

.env file with Groq API Key is required for GenAI features.

Voice feature supports WAV/MP3.

Designed for local VS Code execution, but easily deployable to cloud.
