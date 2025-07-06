import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pipeline import run_pipeline

st.set_page_config(page_title="AI-Powered Sentiment Analysis", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        "<h2 style='font-weight:700; margin-bottom:0.5em;'>AI-Powered<br>Sentiment Analysis<br>for Social Movements</h2>",
        unsafe_allow_html=True
    )
    topic = st.text_input("Topic/Hashtag", value="")
    subreddit = st.selectbox("Subreddit", ["All", "politics", "news", "worldnews"])
    limit = st.slider("Number of posts", 10, 500, 100)
    analyze_btn = st.button("Analyze", use_container_width=True)

# --- MAIN CONTENT ---
st.markdown("<h1 style='font-weight:700;'>Sentiment Analysis</h1>", unsafe_allow_html=True)

if analyze_btn:
    if not topic.strip():
        st.error("Please enter a topic or hashtag to analyze.")
    else:
        with st.spinner("Collecting and analyzing posts..."):
            # Use 'all' subreddit for global search if "All" selected
            subreddit_to_use = subreddit if subreddit != "All" else "all"
            df = run_pipeline(topic, subreddit_to_use, limit)
            if df.empty:
                st.warning("No posts found for the given topic and subreddit.")
            else:
                st.success(f"Collected and analyzed {len(df)} posts.")

                # --- METRICS ---
                total_posts = len(df)
                avg_sentiment = df['sentiment_score'].mean()
                col1, col2, col3 = st.columns([1, 1, 1])
                col1.metric("Total Posts", f"{total_posts:,}")
                col2.metric("Average Sentiment", f"{avg_sentiment:+.2f}")
                col3.empty()  # For symmetry

                # --- SENTIMENT DISTRIBUTION PIE CHART ---
                sentiment_counts = df['sentiment_label'].value_counts().reset_index()
                sentiment_counts.columns = ['sentiment_label', 'count']
                fig_pie = px.pie(
                    sentiment_counts,
                    names='sentiment_label',
                    values='count',
                    color='sentiment_label',
                    color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gold'},
                    title='Sentiment Distribution',
                    hole=0.4
                )
                fig_pie.update_traces(
                    textinfo='none',  # Hide percentages on chart
                    hovertemplate='%{label}: %{percent}',  # Show percentage on hover
                )
                fig_pie.update_layout(showlegend=True, legend_title_text='')

                # --- SENTIMENT TREND LINE CHART (Smooth) ---
                df['date'] = pd.to_datetime(df['timestamp']).dt.date
                trend = df.groupby('date')['sentiment_score'].mean().reset_index()
                if len(trend) > 2:
                    trend['smoothed'] = trend['sentiment_score'].rolling(window=3, min_periods=1, center=True).mean()
                else:
                    trend['smoothed'] = trend['sentiment_score']
                fig_line = px.line(
                    trend,
                    x='date',
                    y='smoothed',
                    title='Sentiment Trend Over Time',
                    markers=False
                )
                fig_line.update_traces(line_shape='spline')  # Smooth line

                # --- WORD CLOUD ---
                text = ' '.join(df['clean_content'].dropna())
                wordcloud = WordCloud(width=600, height=300, background_color='white', colormap='Blues').generate(text)
                fig_wc, ax = plt.subplots(figsize=(6, 3))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                plt.tight_layout(pad=0)

                # --- TOP 5 POSITIVE/NEGATIVE POSTS (Clickable) ---
                def make_clickable(title, post_id):
                    url = f"https://www.reddit.com/comments/{post_id}"
                    return f"<a href='{url}' target='_blank'>{title}</a>"

                top_positive = df.sort_values('sentiment_score', ascending=False).head(5)
                top_positive['Clickable Title'] = top_positive.apply(lambda row: make_clickable(row['title'], row['post_id']), axis=1)
                top_positive_display = top_positive[['Clickable Title', 'sentiment_score']].rename(columns={'Clickable Title': 'Title', 'sentiment_score': 'Score'})

                top_negative = df.sort_values('sentiment_score', ascending=True).head(5)
                top_negative['Clickable Title'] = top_negative.apply(lambda row: make_clickable(row['title'], row['post_id']), axis=1)
                top_negative_display = top_negative[['Clickable Title', 'sentiment_score']].rename(columns={'Clickable Title': 'Title', 'sentiment_score': 'Score'})

                # --- DASHBOARD LAYOUT ---
                upper = st.columns([1, 1, 1])
                with upper[0]:
                    st.plotly_chart(fig_line, use_container_width=True)
                with upper[1]:
                    st.plotly_chart(fig_pie, use_container_width=True)
                with upper[2]:
                    st.markdown("#### Word Cloud")
                    st.pyplot(fig_wc, use_container_width=True)

                lower = st.columns(2)
                with lower[0]:
                    st.markdown("#### Top Positive Posts")
                    st.write(
                        top_positive_display.to_html(escape=False, index=False),
                        unsafe_allow_html=True
                    )
                with lower[1]:
                    st.markdown("#### Top Negative Posts")
                    st.write(
                        top_negative_display.to_html(escape=False, index=False),
                        unsafe_allow_html=True
                    )

else:
    st.info("Enter a topic and click **Analyze** to get started!")
