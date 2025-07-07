# pipeline.py

import os
from reddit_scraper import collect_posts_global
from data_processor import clean_text, save_to_db, setup_db
from sentiment_analyzer import analyze_sentiment
import pandas as pd

DB_PATH = 'data/reddit_posts.db'

def reset_database(db_path=DB_PATH):
    if os.path.exists(db_path):
        os.remove(db_path)

def run_pipeline(topic, limit=100):
    reset_database()       # Delete old DB before new search
    setup_db()
    df = collect_posts_global(topic, limit)
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
    expected_columns = ['topic', 'subreddit', 'title', 'content',
                        'sentiment_score', 'sentiment_label', 'post_score', 'timestamp', 'post_id', 'clean_content']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    save_to_db(df[expected_columns])
    return df
