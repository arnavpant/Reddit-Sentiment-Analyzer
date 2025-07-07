# sentiment_analyzer.py

from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    if not text.strip():
        return 0.0, "Neutral"
    result = sentiment_pipeline(text[:512])[0]
    label = result['label']
    score = result['score'] if label == 'POSITIVE' else -result['score']
    # Map to three-class system
    if score > 0.1:
        sentiment = 'Positive'
    elif score < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return score, sentiment

