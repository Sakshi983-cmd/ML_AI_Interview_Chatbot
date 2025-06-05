import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load CSV
df = pd.read_csv("ml_ai_interview_questions_100.csv")

# Title
st.title("🤖 ML/AI Interview Chatbot")
st.markdown("Ask any question related to Machine Learning or AI (Beginner to Advanced)")

# User input
user_question = st.text_input("Ask a question:")

if user_question:
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['question'].values.tolist() + [user_question])
    
    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_idx = cosine_sim.argmax()
    
    # Display result
    st.subheader("🔍 Best Match")
    st.markdown(f"**Question:** {df.loc[best_match_idx, 'question']}")
    st.markdown(f"**Answer:** {df.loc[best_match_idx, 'answer']}")
    st.markdown(f"**Level:** {df.loc[best_match_idx, 'level']}")
    st.markdown(f"**Topic:** {df.loc[best_match_idx, 'topic']}")

        
