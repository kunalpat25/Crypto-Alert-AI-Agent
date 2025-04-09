# main.py
import time
import logging
from twitter_listener import get_latest_tweets
from token_detector import detect_tokens
from sentiment_analyzer import analyze_sentiment
from news_fetcher import fetch_related_news
from llm_analyzer import analyze_with_llm
from telegram_bot import send_telegram_alert
from profile_change_detector import detect_profile_changes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
polling_interval = 10  # seconds

def main():
    logger.info("Starting Crypto Alert Bot")
    
    while True:
        try:
            # 1. Get latest tweets from monitored accounts
            tweets = get_latest_tweets()
            
            # Inside the main loop:
            for tweet in tweets:
                # Check for profile changes
                profile_changes = detect_profile_changes(
                    tweet['username'], 
                    tweet['name'], 
                    tweet['profile_image']
                )
                
                # Detect mentioned tokens
                tokens = detect_tokens(tweet['text'])
                
                # If profile changed but no tokens detected in tweet, check if name contains tokens
                if profile_changes and not tokens:
                    if 'name_change' in profile_changes:
                        new_name = profile_changes['name_change']['new']
                        name_tokens = detect_tokens(new_name)
                        if name_tokens:
                            tokens = name_tokens
                            logger.info(f"Detected tokens in profile name change: {tokens}")
                
                if tokens or profile_changes:
                    # Analyze sentiment
                    sentiment = analyze_sentiment(tweet['text'])
                    
                    # Fetch related news
                    news = fetch_related_news(tokens)
                    
                    # Analyze with LLM (include profile changes in analysis)
                    analysis = analyze_with_llm(tweet, tokens, news, profile_changes)
                    
                    # Send alert if action recommended
                    if analysis['action'] != 'IGNORE':
                        send_telegram_alert(tweet, analysis, tokens, profile_changes)
            
            # Wait for next polling interval 
            logger.info("Waiting for next polling cycle...")
            time.sleep(polling_interval)
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(polling_interval)  # Continue despite errors

if __name__ == "__main__":
    main()
