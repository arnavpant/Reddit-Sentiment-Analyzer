# sentiment_analyzer.py
# NLP sentiment analysis logic
from transformers import pipeline
import pandas as pd

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment_batch(texts):
    """
    Analyzes a batch of texts for sentiment.
    
    Args:
        texts (list of str): A list of texts to analyze.

    Returns:
        pd.DataFrame: A DataFrame with 'sentiment_score' and 'sentiment_label' for each text.
    """
    # Truncate texts to the model's max input size to prevent errors
    truncated_texts = [text[:512] for text in texts]
    
    # Run the pipeline on the entire batch of texts
    results = sentiment_pipeline(truncated_texts, truncation=True)
    
    scores = []
    labels = []
    
    # Process the results from the pipeline
    for result in results:
        label = result['label']
        # Convert score to be negative for 'NEGATIVE' label
        score = result['score'] if label == 'POSITIVE' else -result['score']
        
        # Determine the final sentiment label based on the score
        if score > 0.1:
            sentiment_label = 'Positive'
        elif score < -0.1:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'
            
        scores.append(score)
        labels.append(sentiment_label)
        
    return pd.DataFrame({'sentiment_score': scores, 'sentiment_label': labels})