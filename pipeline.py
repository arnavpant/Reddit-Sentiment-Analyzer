# pipeline.py
from reddit_scraper import collect_posts
from data_processor import clean_text, save_to_db, setup_db, get_existing_post_ids
from sentiment_analyzer import analyze_sentiment_batch  # <-- Import the new batch function
import pandas as pd


def run_pipeline(topic, subreddit, limit=100):
    setup_db()
    df = collect_posts(subreddit, topic, limit)
    
    # Return an empty DataFrame if no posts are collected
    if df.empty:
        return df

    df['clean_content'] = df['title'].fillna('') + ' ' + df['content'].fillna('')
    df['clean_content'] = df['clean_content'].apply(clean_text)

    # --- OPTIMIZED SENTIMENT ANALYSIS ---
    # Analyze the entire batch of content at once instead of one by one
    sentiment_results = analyze_sentiment_batch(df['clean_content'].tolist())
    df['sentiment_score'] = sentiment_results['sentiment_score']
    df['sentiment_label'] = sentiment_results['sentiment_label']
    
    df['topic'] = topic
    if 'score' not in df.columns:
        df['score'] = 0
    df = df.rename(columns={'score': 'post_score'})

    expected_columns = ['topic', 'subreddit', 'title', 'content',
                    'sentiment_score', 'sentiment_label', 'post_score', 'timestamp', 'post_id']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None  # or 0, or appropriate default

    
    existing_ids = get_existing_post_ids()
    df = df[~df['post_id'].isin(existing_ids)]
    
    # Ensure the dataframe is not empty after filtering before saving
    if not df.empty:
        save_to_db(df[expected_columns])
        
    return df