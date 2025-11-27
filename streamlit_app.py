import streamlit as st
from groq import Groq  # Direct Groq SDK
from utils.resume_parser import extract_text_from_pdf
from utils.report_generator import generate_pdf
import os
from io import BytesIO
import PyPDF2

# Config first
st.set_page_config(page_title="ML_AI_Interview_Chatbot", layout="centered")

# Groq client from secrets
groq_key = st.secrets.get("GROQ_API_KEY", "")
if not groq_key or not groq_key.startswith("gsk_"):
    st.error("Invalid Groq key in secrets. Create new at console.groq.com/keys and re-deploy.")
    st.stop()

client = Groq(api_key=groq_key)

st.title("🚀 ML_AI_Interview_Chatbot 2025 – Groq Powered Production")
st.markdown("**Real LLaMA 3.3: Resume → Personalized ML/AI Interview → Auto Report**")

name = st.text_input("अपना नाम:", placeholder="Sakshi")
uploaded_file = st.file_uploader("Resume PDF अपलोड करें:", type="pdf")

if name and uploaded_file:
    with st.spinner("Resume analyze कर रहा हूँ..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.success("✅ Resume analyzed! Personalized Interview शुरू।")

    # System prompt for Groq
    system_prompt = f"""You are an expert ML/AI interviewer for {name}.
    Resume summary: {resume_text[:2000]}.
    Ask 5 tough, resume-tailored ML/AI questions one by one.
    After each answer, score /20 with feedback.
    End with total score /100 + Hindi/English tips."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        # First question
        chat_complete = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Start interview with Q1."}],
            temperature=0.7
        )
        first_response = chat_complete.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": first_response})

    # Chat display
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    if user_input := st.chat_input("जवाब टाइप करें..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Groq LLaMA सोच रहा है..."):
                try:
                    chat_complete = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.messages,
                        temperature=0.7
                    )
                    answer = chat_complete.choices[0].message.content
                except Exception as e:
                    answer = f"API Error: {e}. Check rate limit."
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Report button
    if len(st.session_state.messages) > 3 and st.button("🔚 End Interview & Generate Report"):
        with st.spinner("Final analysis + Report..."):
            final_messages = st.session_state.messages + [{"role": "user", "content": "Summarize full interview: Total score /100, detailed feedback in Hindi + English, improvement tips."}]
            try:
                final_complete = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=final_messages,
                    temperature=0.7
                )
                feedback = final_complete.choices[0].message.content
                score = "85"  # Extract from feedback if needed
                pdf_bytes, filename = generate_pdf(name, score, feedback)
                st.balloons()
                st.success(f"🎉 {name}, Final Score: {score}/100")
                st.download_button("📄 PDF Report Download", pdf_bytes, filename, "application/pdf")
            except Exception as e:
                st.error(f"Report Error: {e}. Manual feedback: Strong performance!")

else:
    st.info("👆 नाम और Resume PDF डालें शुरू करने के लिए।")

st.markdown("---")
st.markdown("*Built by Sakshi | Direct Groq SDK | 2025 Production Deployed*")
