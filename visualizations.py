# visualizations.py

import plotly.graph_objs as go
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

def plot_sentiment_pie(df):
    counts = df['sentiment_label'].value_counts()
    labels = ['Positive', 'Neutral', 'Negative']
    values = [counts.get('Positive', 0), counts.get('Neutral', 0), counts.get('Negative', 0)]
    colors = ['#2ecc40', '#f1c40f', '#ff4136']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hoverinfo='label+percent',
        textinfo='label',
        showlegend=False
    )])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)
    return fig

def plot_sentiment_trend(df):
    df_sorted = df.sort_values("timestamp")
    # Group by date for smoothness
    df_sorted['date'] = pd.to_datetime(df_sorted['timestamp']).dt.date
    trend = df_sorted.groupby('date')['sentiment_score'].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend['date'],
        y=trend['sentiment_score'],
        mode='lines+markers',
        line_shape='spline',
        line=dict(color='#1a73e8', width=3),
        marker=dict(size=6)
    ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Average Sentiment Score",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320
    )
    return fig

def plot_wordcloud(df):
    text = " ".join(df['clean_content'].astype(str))
    stopwords = set(STOPWORDS)
    wc = WordCloud(
        width=600, height=300, background_color='white',
        stopwords=stopwords, collocations=False, colormap='tab20'
    ).generate(text)
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_top_posts(df, sentiment_label="Positive", top_n=10):
    posts = df[df['sentiment_label'] == sentiment_label].copy()
    if sentiment_label == "Positive":
        posts = posts.sort_values("sentiment_score", ascending=False).head(top_n)
    else:
        posts = posts.sort_values("sentiment_score", ascending=True).head(top_n)
    for _, row in posts.iterrows():
        post_url = f"https://reddit.com/{row['post_id']}"
        st.markdown(
            f'<div class="post-card"><a href="{post_url}" target="_blank">{row["title"]}</a> <span style="color:#888;font-size:0.9em;">[r/{row["subreddit"]}]</span></div>',
            unsafe_allow_html=True
        )


