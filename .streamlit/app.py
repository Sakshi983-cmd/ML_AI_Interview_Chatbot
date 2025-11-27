import streamlit as st
from utils.resume_parser import extract_text_from_pdf
from utils.report_generator import generate_pdf
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Groq API (तू बाद में अपना key डाल देना, अभी demo के लिए ये चलेगा)
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY", "gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")  # तू अपना key डालना
)

st.set_page_config(page_title="ML_AI_Interview_Chatbot", layout="centered")
st.title("ML_AI_Interview_Chatbot 2025")
st.markdown("### Resume डालो → Voice/Text Interview → Instant Report")

name = st.text_input("अपना नाम डालो")
uploaded_file = st.file_uploader("Resume PDF डालो", type="pdf")

if uploaded_file and name:
    with st.spinner("Resume पढ़ रहा हूँ..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    
    st.success("Resume पढ़ लिया! अब Interview शुरू करते हैं")
    
    prompt = f"""
    You are an expert ML Engineer interviewing {name}.
    Resume: {resume_text[:3000]}
    
    Ask 5 tough but fair ML/AI questions one by one.
    Rate each answer out of 20 and give feedback.
    At the end give total score and improvement tips.
    """
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "नमस्ते! Interview शुरू करते हैं। पहला सवाल: Explain the difference between L1 and L2 regularization with mathematical intuition."}]
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if user_input := st.chat_input("अपना जवाब दो..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            with st.spinner("सोच रहा हूँ..."):
                response = llm.invoke(st.session_state.messages)
                answer = response.content
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    
    if st.button("Interview खत्म करो & Report दो"):
        final_prompt = "Give final score out of 100 and detailed feedback in Hindi + English."
        with st.spinner("Report बना रहा हूँ..."):
            final = llm.invoke(st.session_state.messages + [{"role": "user", "content": final_prompt}])
            feedback = final.content
            score = "85"  # बाद में auto calculate करेंगे
            pdf_bytes, filename = generate_pdf(name, score, feedback)
            st.balloons()
            st.success(f"{name} का Score: {score}/100")
            st.download_button("PDF Report डाउनलोड करो", pdf_bytes, filename, "application/pdf")
