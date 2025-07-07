# app.py

import streamlit as st
from pipeline import run_pipeline
from utils import get_sentiment_feeling, get_sentiment_emoji
from visualizations import plot_sentiment_pie, plot_sentiment_trend, plot_wordcloud, render_top_posts

st.set_page_config(page_title="Social Movements Sentiment Analyzer", layout="wide")

st.title("AI-Powered Sentiment Analysis for Social Movements")

with st.sidebar:
    st.header("Configure Analysis")
    topic = st.text_input("Enter topic or hashtag", value="climate change")
    limit = st.slider("Number of Reddit posts to analyze", 10, 500, 100, step=10)
    analyze_btn = st.button("Analyze")

if analyze_btn:
    with st.spinner("Collecting and analyzing posts..."):
        df = run_pipeline(topic, limit)
        if df.empty:
            st.error("No posts found for your query. Try a different topic.")
        else:
            total_posts = len(df)
            avg_sentiment = df['sentiment_score'].mean()
            avg_sentiment_display = f"{avg_sentiment:+.2f}"
            avg_sentiment_emoji = get_sentiment_emoji(avg_sentiment)
            avg_sentiment_feeling = get_sentiment_feeling(avg_sentiment)
            unique_users = df['author'].nunique() if 'author' in df.columns else "N/A"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Posts", total_posts)
            with col2:
                st.metric("Average Sentiment", f"{avg_sentiment_display} {avg_sentiment_emoji}")
                st.caption(avg_sentiment_feeling)
            with col3:
                st.metric("Unique Users", unique_users)

            st.markdown("### Sentiment Distribution")
            pie_fig = plot_sentiment_pie(df)
            st.plotly_chart(pie_fig, use_container_width=True)

            st.markdown("### Sentiment Trend Over Time")
            trend_fig = plot_sentiment_trend(df)
            st.plotly_chart(trend_fig, use_container_width=True)

            col_wc, col_pos, col_neg = st.columns([2, 1.5, 1.5])
            with col_wc:
                st.markdown("### Word Cloud")
                wc_img = plot_wordcloud(df)
                st.image(wc_img, use_column_width=True)
            with col_pos:
                st.markdown("### Top 10 Positive Posts")
                render_top_posts(df, sentiment_label="Positive")
            with col_neg:
                st.markdown("### Top 10 Negative Posts")
                render_top_posts(df, sentiment_label="Negative")

            st.markdown("### All Posts")
            st.dataframe(df[["title", "subreddit", "sentiment_label", "sentiment_score", "timestamp"]], use_container_width=True)

            st.download_button(
                label="Download Results as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{topic}_reddit_sentiment.csv",
                mime="text/csv"
            )
else:
    st.info("Enter a topic and click Analyze to get started.")
