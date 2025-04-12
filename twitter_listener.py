# twitter_listener.py using Twikit
import logging
import json
from datetime import datetime, timedelta
import os
from twikit import Client
from dotenv import load_dotenv
import time

os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

load_dotenv()

logger = logging.getLogger(__name__)
logger.info(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
logger.info(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")

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

async def get_latest_tweets():
    handles = load_twitter_handles()
    current_time = datetime.now()
    since_time = current_time - timedelta(minutes=2)  # Check tweets from last 2 minutes
    
    # Get Twitter credentials from environment variables
    username = os.environ.get('TWITTER_USERNAME')
    email = os.environ.get('TWITTER_EMAIL')
    password = os.environ.get('TWITTER_PASSWORD')
    
    if not username or not email or not password:
        logger.error("Twitter credentials not set. Set TWITTER_USERNAME, TWITTER_EMAIL, and TWITTER_PASSWORD env variables.")
        return []
    
    all_tweets = []
    
    try:
        # Initialize the client
        client = Client()
        
        # Load cookies if available to avoid repeated logins
        cookie_file = "twitter_cookies.json"
        if os.path.exists(cookie_file):
            try:
                client.load_cookies(cookie_file)
                logger.info("Loaded Twitter cookies from file")
            except Exception as e:
                logger.warning(f"Failed to load cookies: {e}")
                # Login if cookies failed
                client.login()
                client.save_cookies(cookie_file)
        else:
            # Login and save cookies for future use
            client.login(
                auth_info_1=username,
                auth_info_2=email,
                password=password,
            )
            client.save_cookies(cookie_file)
        
        for username in handles.keys():
            try:
                # Search for recent tweets from this user
                # Format: "from:username since:YYYY-MM-DD until:YYYY-MM-DD"
                search_query = f"from:{username} since:{since_time.strftime('%Y-%m-%d')}"
                
                # Get tweets (limit to 10 per user to avoid excessive processing)
                tweets = await client.search_tweet(query = search_query, product='Latest', count=2)
                
                for tweet in tweets:
                    # Convert tweet timestamp to datetime for comparison
                    tweet_time = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S %z %Y")
                    
                    # Check if tweet is recent enough (within last 2 minutes)
                    if tweet_time.replace(tzinfo=None) >= since_time:
                        tweet_data = {
                            "id": str(tweet.id),
                            "username": username,
                            "name": handles[username],
                            "text": tweet.text,
                            "timestamp": tweet_time.isoformat(),
                            "profile_image": tweet.user.profile_image_url if hasattr(tweet.user, 'profile_image_url') else ""
                        }
                        all_tweets.append(tweet_data)
                        
                # Be nice to Twitter - add a small delay between requests
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching tweets for {username}: {e}", exc_info=True)
        
    except Exception as e:
        logger.error(f"Error initializing Twitter client: {e}", exc_info=True)
    logger.info(f"Fetched {len(all_tweets)} new tweets")
    return all_tweets
