# NLP sentiment analysis logic
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    result = sentiment_pipeline(text[:512])[0]  # Truncate to 512 tokens
    label = result['label'] 
    score = result['score'] if label == 'POSITIVE' else -result['score']
    # Map to your three-class system
    if score > 0.1:
        sentiment = 'Positive'
    elif score < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return score, sentiment
