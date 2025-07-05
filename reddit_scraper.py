# Reddit data collection logic
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
            'score': post.score,
            'num_comments': post.num_comments,
            'timestamp': pd.to_datetime(post.created_utc, unit='s')
        })
    return pd.DataFrame(posts)
