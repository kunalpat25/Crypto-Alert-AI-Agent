# utils/helpers.py
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def save_processed_tweet_ids(tweet_id):
    """
    Save processed tweet IDs to avoid duplicate processing.
    """
    processed_file = "processed_tweets.json"
    
    try:
        if os.path.exists(processed_file):
            with open(processed_file, 'r') as f:
                processed_ids = json.load(f)
        else:
            processed_ids = []
        
        # Add new ID and keep only the last 1000
        processed_ids.append(tweet_id)
        processed_ids = processed_ids[-1000:]
        
        with open(processed_file, 'w') as f:
            json.dump(processed_ids, f)
            
        return True
    except Exception as e:
        logger.error(f"Error saving processed tweet ID: {e}")
        return False

def is_tweet_processed(tweet_id):
    """
    Check if a tweet has already been processed.
    """
    processed_file = "processed_tweets.json"
    
    try:
        if os.path.exists(processed_file):
            with open(processed_file, 'r') as f:
                processed_ids = json.load(f)
            return tweet_id in processed_ids
        return False
    except Exception as e:
        logger.error(f"Error checking processed tweet ID: {e}")
        return False
