# reddit_scraper.py

import praw
import pandas as pd
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

def get_reddit_instance():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

def collect_posts(subreddit, query, limit=100):
    reddit = get_reddit_instance()
    subreddit_obj = reddit.subreddit(subreddit)
    posts = []
    for post in subreddit_obj.search(query, sort='new', limit=limit):
        posts.append({
            'post_id': post.id,
            'title': post.title,
            'content': post.selftext,
            'subreddit': subreddit,
            'score': getattr(post, 'score', 0),
            'num_comments': getattr(post, 'num_comments', 0),
            'timestamp': pd.to_datetime(post.created_utc, unit='s'),
            'author': str(post.author) if post.author else "N/A"
        })
    return pd.DataFrame(posts)

