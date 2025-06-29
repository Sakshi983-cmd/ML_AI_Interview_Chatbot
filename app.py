import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load CSV
df = pd.read_csv("ml_ai_interview_questions_100.csv")

# Page Title
st.title("🤖 ML/AI Interview Chatbot with Insights")

st.markdown("""
Welcome! This app helps you with ML/AI/Data Science interview preparation.  
You can ask questions and also explore data insights.  
---
""")

# ========= VISUALIZATIONS SECTION ==========

st.header("📊 Insights from ML/AI Question Dataset")

# 1. Topic-wise Bar Chart
st.subheader("📌 Number of Questions per Topic")
topic_counts = df['topic'].value_counts()

fig1, ax1 = plt.subplots()
topic_counts.plot(kind='bar', color='lightblue', ax=ax1)
ax1.set_ylabel("Number of Questions")
ax1.set_xlabel("Topic")
ax1.set_title("Questions per Topic")
st.pyplot(fig1)

# 2. Difficulty Level Pie Chart
st.subheader("🎯 Difficulty Level Distribution")
level_counts = df['level'].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', startangle=140)
ax2.axis('equal')
st.pyplot(fig2)

# 3. Word Cloud from Questions
st.subheader("☁️ Common Words in Questions")
text = ' '.join(df['question'].tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)

# 4. Heatmap of Topic vs Level
st.subheader("🔥 Heatmap: Topic vs Difficulty Level")
heatmap_data = pd.crosstab(df['topic'], df['level'])

fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', ax=ax4)
st.pyplot(fig4)

st.markdown("---")

# ========= CHATBOT SECTION ==========

st.header("💬 Ask the ML/AI Interview Chatbot")

user_question = st.text_input("🧠 Ask your question:")

if user_question:
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['question'].tolist() + [user_question])

    # Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_idx = cosine_sim.argmax()
    best_score = cosine_sim[0, best_match_idx]

    # Threshold for match
    threshold = 0.2

    if best_score < threshold:
        st.warning("⚠️ Sorry, I couldn’t find a relevant answer. Try rephrasing your question.")
    else:
        st.subheader("🔍 Best Match Found")
        st.markdown(f"**🗨 Question:** {df.loc[best_match_idx, 'question']}")
        st.markdown(f"**✅ Answer:**\n{df.loc[best_match_idx, 'answer']}")
        st.markdown(f"**📘 Level:** {df.loc[best_match_idx, 'level']}")
        st.markdown(f"**📌 Topic:** {df.loc[best_match_idx, 'topic']}")
