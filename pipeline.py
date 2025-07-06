from reddit_scraper import collect_posts
from data_processor import clean_text, save_to_db, setup_db
from sentiment_analyzer import analyze_sentiment
import pandas as pd


def run_pipeline(topic, subreddit, limit=100):
    setup_db()
    df = collect_posts(subreddit, topic, limit)
    df['clean_content'] = df['title'].fillna('') + ' ' + df['content'].fillna('')
    df['clean_content'] = df['clean_content'].apply(clean_text)
    df[['sentiment_score', 'sentiment_label']] = df['clean_content'].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )
    df['topic'] = topic
    df = df.rename(columns={'score': 'post_score'})

    save_to_db(df[['topic', 'subreddit', 'title', 'content', 'sentiment_score', 'sentiment_label', 'score', 'timestamp', 'post_id']])
    return df
