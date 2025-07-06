# app.py

import streamlit as st
from pipeline import run_pipeline
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="AI-Powered Sentiment Analysis", layout="wide")

st.title("🧠 AI-Powered Sentiment Analysis for Social Movements")
st.markdown(
    """
    Analyze public sentiment on any topic or hashtag across Reddit in real time.<br>
    <small>Track trends, visualize opinions, and discover the most positive and negative posts!</small>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Controls")
    topic = st.text_input("Enter topic or hashtag:", value="climate change")
    subreddit = st.selectbox("Choose subreddit:", ["politics", "news", "worldnews"])
    limit = st.slider("Number of posts to analyze:", 10, 500, 100)
    analyze_btn = st.button("🔍 Analyze")

if analyze_btn:
    with st.spinner("Collecting and analyzing posts..."):
        df = run_pipeline(topic, subreddit, limit)
        st.success(f"Collected and analyzed {len(df)} posts.")

        # --- Summary Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Posts", len(df))
        with col2:
            avg_sent = df['sentiment_score'].mean()
            st.metric("Avg. Sentiment Score", f"{avg_sent:.2f}")
        with col3:
            st.metric("Subreddit", subreddit)

        # --- Visualizations ---
        st.subheader("Sentiment Dashboard")
        col_a, col_b = st.columns([1, 1])

        # Pie Chart: Sentiment Distribution
        with col_a:
            sentiment_counts = df['sentiment_label'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment_label', 'count']
            fig_pie = px.pie(
                sentiment_counts,
                names='sentiment_label',
                values='count',
                color='sentiment_label',
                color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'},
                title='Sentiment Distribution'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Line Chart: Sentiment Trend Over Time
        with col_b:
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            trend = df.groupby('date')['sentiment_score'].mean().reset_index()
            fig_line = px.line(
                trend,
                x='date',
                y='sentiment_score',
                markers=True,
                title='Sentiment Trend Over Time'
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # --- Word Cloud ---
        st.subheader("Word Cloud of Most Common Words")
        text = ' '.join(df['clean_content'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig_wc, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig_wc)

        # --- Top Posts ---
        st.subheader("Top Posts by Sentiment")
        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.markdown("#### Top 10 Most Positive Posts")
            top_positive = df.sort_values('sentiment_score', ascending=False).head(10)[['title', 'sentiment_score']]
            st.table(top_positive.rename(columns={'title': 'Title', 'sentiment_score': 'Score'}))
        with col_neg:
            st.markdown("#### Top 10 Most Negative Posts")
            top_negative = df.sort_values('sentiment_score', ascending=True).head(10)[['title', 'sentiment_score']]
            st.table(top_negative.rename(columns={'title': 'Title', 'sentiment_score': 'Score'}))

        # --- Data Table (Expandable) ---
        with st.expander("See All Analyzed Posts"):
            st.dataframe(df[['title', 'sentiment_label', 'sentiment_score', 'subreddit', 'timestamp']])

else:
    st.info("Enter a topic and click **Analyze** to get started!")

