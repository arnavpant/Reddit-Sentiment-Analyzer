# Main Streamlit app
import streamlit as st
from pipeline import run_pipeline  # if you put it in pipeline.py

from reddit_scraper import collect_posts
from data_processor import clean_text, save_to_db, setup_db
from sentiment_analyzer import analyze_sentiment

st.title("AI-Powered Sentiment Analysis for Social Movements")

topic = st.text_input("Enter topic/hashtag:")
subreddit = st.selectbox("Choose subreddit:", ["politics", "news", "worldnews"])
limit = st.slider("Number of posts:", 10, 500, 100)

if st.button("Analyze"):
    with st.spinner("Collecting and analyzing posts..."):
        df = run_pipeline(topic, subreddit, limit)
        st.success(f"Collected and analyzed {len(df)} posts.")
        st.write(df.head())
