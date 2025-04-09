# sentiment_analyzer.py
import logging
import re

logger = logging.getLogger(__name__)

# Simple lexicon-based sentiment analyzer
# In production, consider using VADER or TextBlob

POSITIVE_WORDS = [
    'bullish', 'moon', 'up', 'gain', 'profit', 'buy', 'good', 'great', 
    'amazing', 'excellent', 'excited', 'love', 'happy', 'win', 'winning',
    'surge', 'soar', 'rocket', 'growth', 'opportunity', 'potential'
]

NEGATIVE_WORDS = [
    'bearish', 'down', 'dip', 'crash', 'sell', 'bad', 'terrible', 'awful',
    'disappointed', 'hate', 'sad', 'lose', 'losing', 'drop', 'fall', 'plummet',
    'risk', 'danger', 'warning', 'avoid', 'trouble', 'problem'
]

def analyze_sentiment(text):
    """
    Perform basic sentiment analysis on text.
    Returns: 'positive', 'negative', or 'neutral'
    """
    text = text.lower()
    
    # Count positive and negative words
    positive_count = sum(1 for word in POSITIVE_WORDS if re.search(r'\b' + word + r'\b', text))
    negative_count = sum(1 for word in NEGATIVE_WORDS if re.search(r'\b' + word + r'\b', text))
    
    # Determine sentiment
    if positive_count > negative_count:
        sentiment = 'positive'
    elif negative_count > positive_count:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    logger.info(f"Sentiment analysis: {sentiment} (pos={positive_count}, neg={negative_count})")
    return sentiment
