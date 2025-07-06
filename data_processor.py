# Data cleaning, storage, and processing
import os
import re
import sqlite3
import pandas as pd

def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # Remove special chars
    text = text.lower().strip()
    return text

def save_to_db(df, db_path='data/reddit_posts.db'):
    conn = sqlite3.connect(db_path)
    df.to_sql('posts', conn, if_exists='append', index=False)
    conn.close()

def setup_db(db_path='data/reddit_posts.db'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        subreddit TEXT,
        title TEXT,
        content TEXT,
        sentiment_score REAL,
        sentiment_label TEXT,
        post_score INTEGER,
        timestamp DATETIME,
        post_id TEXT UNIQUE
    );
    """)
    conn.close()

def get_existing_post_ids(db_path='data/reddit_posts.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT post_id FROM posts")
    rows = cursor.fetchall()
    conn.close()
    return set(row[0] for row in rows)
