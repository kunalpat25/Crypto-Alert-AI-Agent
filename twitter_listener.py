# twitter_listener.py
import json
import logging
import os
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Load Twitter handles from config
def load_twitter_handles():
    try:
        with open('config/twitter_handles.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Twitter handles config not found, using default list")
        return {
            "elonmusk": "Elon Musk",
            "cz_binance": "CZ Binance",
            "SBF_FTX": "Sam Bankman-Fried",
            "VitalikButerin": "Vitalik Buterin"
        }

# Mock function to simulate getting tweets (replace with actual API call later)
def get_latest_tweets():
    handles = load_twitter_handles()
    
    # TODO : Implement actual Twitter API call to fetch tweets from these handles
    # For now, we will simulate the behavior with a mock function
    # For demo purposes, randomly return a tweet from one of our monitored accounts
    # In production, this would call Twitter API or use scraping
    
    # Mock tweets for testing
    mock_tweets = [
        {
            "id": "123456789",
            "username": "elonmusk",
            "name": "Elon Musk",
            "text": "Dogecoin to the moon! $DOGE",
            "timestamp": datetime.now().isoformat(),
            "profile_image": "https://example.com/elonmusk.jpg"
        },
        {
            "id": "987654321",
            "username": "cz_binance",
            "name": "CZ Binance",
            "text": "Just bought more $BTC. Long-term bullish!",
            "timestamp": datetime.now().isoformat(),
            "profile_image": "https://example.com/cz.jpg"
        },
        {
            "id": "543216789",
            "username": "VitalikButerin",
            "name": "Vitalik Buterin",
            "text": "Excited about the latest $ETH developments. Scaling solutions coming soon.",
            "timestamp": datetime.now().isoformat(),
            "profile_image": "https://example.com/vitalik.jpg"
        }
    ]
    
    # TODO: Implement logic to check if we've already processed these tweets
    # In the real implementation, we would:
    # 1. Check if we've already processed these tweets (using a simple DB or file)
    # 2. Only return tweets newer than our last check
    
    # For demo, randomly decide whether to return tweets or empty list
    if random.random() < 0.3:  # 30% chance to get a tweet
        return [random.choice(mock_tweets)]
    
    return []  # Most poll cycles will return nothing
