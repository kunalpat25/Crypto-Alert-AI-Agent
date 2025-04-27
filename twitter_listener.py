# twitter_listener.py using requests
import logging
import json
import requests
from datetime import datetime, timedelta
import time
import random
import os
from bs4 import BeautifulSoup

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
    
    # For development/testing, use a mock approach
    # In production, you'd replace this with actual scraping
    use_mock = False  # Set to False when you have a working scraper
    
    if use_mock:
        # Generate mock tweets for testing
        for username, display_name in handles.items():
            # 20% chance of generating a tweet for each user
            if random.random() < 0.2:
                mock_tweet = {
                    "id": f"mock_{int(time.time())}_{random.randint(1000, 9999)}",
                    "username": username,
                    "name": display_name,
                    "text": f"This is a mock tweet about {'#crypto' if random.random() < 0.5 else '$BTC'} from {display_name} at {current_time.strftime('%H:%M:%S')}",
                    "timestamp": current_time.isoformat(),
                    "profile_image": f"https://example.com/{username}.jpg"
                }
                all_tweets.append(mock_tweet)
                logger.info(f"Generated mock tweet for {username}")
    else:
        # Actual scraping implementation
        for username, display_name in handles.items():
            try:
                # Use requests to fetch the Twitter page
                user_agent = random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
                ])
                
                headers = {
                    "User-Agent": user_agent,
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
                }
                
                url = f"https://x.com/{username}"
                
                # Add random delay between requests
                time.sleep(random.uniform(2.0, 5.0))
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    # This is where you would parse the HTML to extract tweets
                    # For now, we'll just log that we got a successful response
                    logger.info(f"Successfully fetched page for {username}")
                    
                    # Parse the HTML here to extract tweets and filter by timestamp

                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Save the response page to a file for debugging purposes
                    debug_dir = "debug_pages"
                    os.makedirs(debug_dir, exist_ok=True)
                    debug_file_path = os.path.join(debug_dir, f"{username}_page.html")

                    with open(debug_file_path, "w", encoding="utf-8") as debug_file:
                        debug_file.write(response.text)

                    logger.info(f"Saved debug page for {username} to {debug_file_path}")
                    
                    # Example: Find tweet containers (this will depend on the actual HTML structure)
                    tweet_containers = soup.find_all('div', class_='tweet')
                    
                    for tweet in tweet_containers:
                        try:
                            tweet_text = tweet.find('p', class_='tweet-text').get_text(strip=True)
                            tweet_time = tweet.find('span', class_='tweet-timestamp')['data-time']
                            tweet_time = datetime.fromtimestamp(int(tweet_time))
                            
                            if tweet_time > since_time:
                                real_tweet = {
                                    "id": tweet['data-tweet-id'],
                                    "username": username,
                                    "name": display_name,
                                    "text": tweet_text,
                                    "timestamp": tweet_time.isoformat(),
                                    "profile_image": f"https://example.com/{username}.jpg"  # Replace with actual profile image URL if available
                                }
                                logger.info(f"Fetched tweet for {username}: {real_tweet}")
                                all_tweets.append(real_tweet)
                        except Exception as parse_error:
                            logger.warning(f"Error parsing tweet for {username}: {parse_error}")
                else:
                    logger.warning(f"Failed to fetch page for {username}: Status code {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error fetching tweets for {username}: {e}", exc_info=True)
    
    logger.info(f"Fetched {len(all_tweets)} new tweets")
    return all_tweets
