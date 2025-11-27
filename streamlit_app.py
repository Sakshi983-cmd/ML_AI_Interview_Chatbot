
import streamlit as st

# CRITICAL FIX: set_page_config FIRST – before ANY other st. command (line 3)
st.set_page_config(page_title="ML_AI_Interview_Chatbot", layout="centered")

# Now safe imports & warnings (after config)
import warnings
warnings.filterwarnings("ignore")  # Suppress any warnings

PDF_PARSE_AVAILABLE = False
GROQ_AVAILABLE = False

# Dummy PDF parser (no external deps)
def dummy_extract_text_from_pdf(file):
    return "Dummy resume: ML Fresher with Python, TensorFlow, 2 years experience in NLP projects."

# Dummy LLM response function
def dummy_llm_invoke(messages):
    last_user = messages[-1]["content"] if messages else ""
    responses = [
        "Demo Response: Excellent! L1 promotes sparsity (Lasso), L2 smooth weights (Ridge). Math: L1 = ||w||1, L2 = ||w||2^2. Score: 18/20. Next Q: Transfer learning in CNNs?",
        "Demo: Good! Transfer learning reuses pre-trained weights (e.g., ImageNet on custom data). Reduces overfitting. Score: 17/20. Q3: Explain backpropagation.",
        "Demo: Perfect! Backprop computes gradients via chain rule for neural nets. Score: 19/20. Q4: What is overfitting and how to fix?",
        "Demo: Solid! Overfitting = high train/low test accuracy. Fix: Dropout, regularization. Score: 16/20. Final Q: GANs vs VAEs.",
        "Demo: Nice! GANs adversarial training for generation, VAEs probabilistic latent space. Score: 15/20. Interview complete!"
    ]
    return responses[len(messages) % len(responses)]  # Cycle through responses

# Report generator (safe with reportlab)
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from datetime import datetime

    def generate_pdf(name, score, feedback):
        filename = f"{name}_ML_Interview_Report.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.setFillColorRGB(0.2, 0.2, 0.8)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 100, "ML/AI Interview Report")
        c.setFont("Helvetica", 14)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(50, height - 150, f"Candidate: {name}")
        c.drawString(50, height - 180, f"Date: {datetime.now().strftime('%B %d, %Y')}")
        c.drawString(50, height - 220, f"Score: {score}/100")
        c.drawString(50, height - 270, "Feedback:")
        text = c.beginText(70, height - 300)
        text.setFont("Helvetica", 12)
        for line in feedback.split('\n'):
            text.textLine(line)
        c.drawText(text)
        c.save()
        with open(filename, "rb") as f:
            return f.read(), filename
    PDF_GENERATOR_AVAILABLE = True
except ImportError:
    def generate_pdf(name, score, feedback):
        return f"Demo Report: {name} - {score}/100 - {feedback}".encode(), f"{name}_report.txt"
    PDF_GENERATOR_AVAILABLE = False
    st.warning("PDF fallback to text – check requirements.txt")

# Demo mode warning (after config)
st.warning("Demo Mode Active: Using dummy AI for quick deploy. Uncomment requirements for full Groq.")

st.title("🚀 ML_AI_Interview_Chatbot 2025")
st.markdown("**Resume Upload → Personalized ML/AI Interview → Auto Report** (Demo Mode)")

name = st.text_input("अपना नाम:", placeholder="Sakshi")
uploaded_file = st.file_uploader("Resume PDF अपलोड करें:", type="pdf")

if name and (uploaded_file or st.button("Demo Mode शुरू करें")):
    with st.spinner("Setup कर रहा हूँ..."):
        resume_text = dummy_extract_text_from_pdf(uploaded_file) if uploaded_file else "Dummy resume text."

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
                answer = dummy_llm_invoke(st.session_state.messages)
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Report button
    if len(st.session_state.messages) > 2 and st.button("🔚 Interview End & Report Generate"):
        with st.spinner("Report तैयार कर रहा हूँ..."):
            feedback = "Demo Feedback: Strong ML concepts (85/100). Improve on deployment. Hindi: अच्छा प्रयास, practice करें!"
            score = "85"
            try:
                pdf_bytes, filename = generate_pdf(name, score, feedback)
                st.balloons()
                st.success(f"🎉 {name}, Score: {score}/100")
                st.download_button("📄 Report Download", pdf_bytes, filename, "application/pdf" if PDF_GENERATOR_AVAILABLE else "text/plain")
            except Exception as e:
                st.error(f"Report Issue: {e}. Feedback: {feedback}")

else:
    st.info("👆 नाम डालें और PDF अपलोड करें (या Demo Mode दबाएँ)।")

# Footer for 2025 vibe
st.markdown("---")
st.markdown("*Built by Sakshi | 2025 Production Ready | Full Groq Mode Coming Soon*")
