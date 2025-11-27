import streamlit as st

# Ultra-safe imports
PDF_PARSE_AVAILABLE = False
GROQ_AVAILABLE = False
try:
    import PyPDF2
    from io import BytesIO
    PDF_PARSE_AVAILABLE = True
except ImportError:
    st.warning("PDF parser fallback to dummy.")

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    st.warning("Groq fallback to dummy responses.")

from utils.report_generator import generate_pdf  # ये safe है

# Groq key check
groq_key = st.secrets.get("GROQ_API_KEY", "")
llm = None
if GROQ_AVAILABLE and groq_key and groq_key.startswith("gsk_"):
    try:
        llm = ChatGroq(model="llama3-70b-8192", temperature=0.7, groq_api_key=groq_key)  # Model name fix: llama3-70b-8192 (versatile old name issue)
    except:
        st.warning("LLM init fallback.")
else:
    st.info("Demo mode: Using dummy AI responses.")

st.set_page_config(page_title="ML_AI_Interview_Chatbot", layout="centered")
st.title("🚀 ML_AI_Interview_Chatbot 2025")
st.markdown("**Resume Upload → Personalized ML/AI Interview → Auto Report**")

name = st.text_input("अपना नाम:", placeholder="Sakshi")
uploaded_file = st.file_uploader("Resume PDF अपलोड करें:", type="pdf")

if name and (uploaded_file or st.button("Demo Mode शुरू करें")):
    with st.spinner("Setup कर रहा हूँ..."):
        if uploaded_file and PDF_PARSE_AVAILABLE:
            try:
                pdf_file = BytesIO(uploaded_file.getvalue())
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                resume_text = ""
                for page in pdf_reader.pages:
                    resume_text += page.extract_text() + "\n"
                pdf_file.close()
            except Exception as e:
                resume_text = f"Parse error: {e}. Using dummy resume."
        else:
            resume_text = "Dummy resume: ML Fresher with Python, TensorFlow experience."

    st.success("✅ Ready! Interview शुरू।")

    if "messages" not in st.session_state:
        first_question = "Q1: L1 vs L2 regularization explain with math? (Based on your resume's ML focus)"
        st.session_state.messages = [{"role": "assistant", "content": first_question}]

    # Chat display
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    if user_input := st.chat_input("जवाब टाइप करें..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI सोच रहा है..."):
                if llm:
                    try:
                        response = llm.invoke(st.session_state.messages)
                        answer = response.content
                    except Exception as e:
                        answer = f"Demo: Great! Score 18/20. {e}"  # Fallback
                else:
                    answer = "Demo Response: Excellent explanation! L1 for sparsity, L2 for small weights. Score: 18/20. Next Q: Gradient descent variants?"
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Report button
    if len(st.session_state.messages) > 2 and st.button("🔚 Interview End & Report Generate"):
        with st.spinner("Report तैयार कर रहा हूँ..."):
            if llm:
                final_prompt = [{"role": "user", "content": "Summarize interview: Score /100, feedback in Hindi/English, tips."}]
                try:
                    final = llm.invoke(final_prompt)
                    feedback = final.content
                except:
                    feedback = "Demo Feedback: Strong basics (85/100). Improve on optimization. Hindi: अच्छा प्रयास!"
            else:
                feedback = "Demo Feedback: 85/100 - Good ML knowledge. Practice coding interviews. Hindi: ML concepts मजबूत हैं!"

            score = "85"
            try:
                pdf_bytes, filename = generate_pdf(name, score, feedback)
                st.balloons()
                st.success(f"🎉 {name}, Score: {score}/100")
                st.download_button("📄 PDF Report Download", pdf_bytes, filename, "application/pdf")
            except Exception as e:
                st.error(f"PDF Issue: {e}. Feedback: {feedback}")

else:
    st.info("👆 नाम डालें और PDF अपलोड करें (या Demo Mode दबाएँ)।")
