# twitter_listener.py using twitter-scraper-selenium
import logging
import json
from datetime import datetime, timedelta
from twitter_scraper_selenium import scrape_profile

logger = logging.getLogger(__name__)

def load_twitter_handles():
    try:
        with open('config/twitter_handles.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Twitter handles config not found, using default list")
        return {
            "elonmusk": "Elon Musk",
            "cz_binance": "CZ Binance",
            "VitalikButerin": "Vitalik Buterin"
        }

def get_latest_tweets():
    handles = load_twitter_handles()
    current_time = datetime.now()
    since_time = current_time - timedelta(minutes=2)  # Check tweets from last 2 minutes
    
    all_tweets = []
    
    for username, display_name in handles.items():
        try:
            # Fetch the 5 most recent tweets for each user
            # TODO: test the working and use alternative library if needed
            tweets = scrape_profile(twitter_username=username, tweets_count=5, browser="chrome", headless=True)
            
            for tweet in tweets:
                # Parse the tweet timestamp
                tweet_time = datetime.strptime(tweet['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
                
                # Check if tweet is recent enough (within last 2 minutes)
                if tweet_time >= since_time:
                    tweet_data = {
                        "id": str(tweet['tweet_id']),
                        "username": username,
                        "name": display_name,
                        "text": tweet['text'],
                        "timestamp": tweet['timestamp'],
                        "profile_image": tweet.get('profile_picture', "")
                    }
                    all_tweets.append(tweet_data)
        
        except Exception as e:
            logger.error(f"Error fetching tweets for {username}: {e}")
    
    logger.info(f"Fetched {len(all_tweets)} new tweets")
    return all_tweets
