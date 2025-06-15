import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load CSV
df = pd.read_csv("ml_ai_interview_questions_100.csv")

# Title
st.title("🤖 ML/AI Interview Chatbot")
st.markdown("""
Ask any question related to **Machine Learning**, **Artificial Intelligence**, or **Data Science** (Beginner to Advanced).  
You can also ask for **learning roadmaps** like:  
- *What is the roadmap to learn Machine Learning?*  
- *How can I learn AI from scratch?*  
- *What is the roadmap to become a Data Scientist?*
""")

# User Input
user_question = st.text_input("🧠 Ask your question:")

if user_question:
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['question'].tolist() + [user_question])
    
    # Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_idx = cosine_sim.argmax()
    best_score = cosine_sim[0, best_match_idx]

    # Match Threshold
    threshold = 0.2

    if best_score < threshold:
        st.warning("⚠️ Sorry, I couldn’t find a relevant answer. Try rephrasing your question.")
    else:
        # Show Result
        st.subheader("🔍 Best Match Found")
        st.markdown(f"**🗨 Question:** {df.loc[best_match_idx, 'question']}")
        st.markdown(f"**✅ Answer:**\n{df.loc[best_match_idx, 'answer']}")
        st.markdown(f"**📘 Level:** {df.loc[best_match_idx, 'level']}")
        st.markdown(f"**📌 Topic:** {df.loc[best_match_idx, 'topic']}")
