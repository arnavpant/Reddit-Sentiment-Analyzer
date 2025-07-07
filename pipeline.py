# pipeline.py

from reddit_scraper import collect_posts
from data_processor import clean_text, save_to_db, setup_db, get_existing_post_ids
from sentiment_analyzer import analyze_sentiment
import pandas as pd
from datetime import datetime, timedelta

def run_pipeline(topic, limit=100):
    setup_db()
    df = collect_posts(topic, limit)
    if df.empty:
        return df

    df['clean_content'] = df['title'].fillna('') + ' ' + df['content'].fillna('')
    df['clean_content'] = df['clean_content'].apply(clean_text)
    df[['sentiment_score', 'sentiment_label']] = df['clean_content'].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )
    df['topic'] = topic
    if 'score' not in df.columns:
        df['score'] = 0
    df = df.rename(columns={'score': 'post_score'})

    # Filter for posts from the last 30 days
    now = datetime.now()
    thirty_days_ago = now - timedelta(days=30)
    df = df[df['timestamp'] >= thirty_days_ago]

    expected_columns = [
        'topic', 'subreddit', 'title', 'content',
        'sentiment_score', 'sentiment_label', 'post_score', 'timestamp',
        'post_id', 'clean_content', 'author'
    ]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    existing_ids = get_existing_post_ids()
    df = df[~df['post_id'].isin(existing_ids)]

    save_to_db(df[expected_columns])
    return df

