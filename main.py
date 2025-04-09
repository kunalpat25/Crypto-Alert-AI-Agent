# main.py
import time
import logging
from twitter_listener import get_latest_tweets
from token_detector import detect_tokens
from sentiment_analyzer import analyze_sentiment
from news_fetcher import fetch_related_news
from llm_analyzer import analyze_with_llm
from telegram_bot import send_telegram_alert

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
            
            for tweet in tweets:
                # 2. Detect mentioned tokens
                tokens = detect_tokens(tweet['text'])
                
                if tokens:
                    # 3. Analyze sentiment
                    sentiment = analyze_sentiment(tweet['text'])
                    
                    # 4. Fetch related news
                    news = fetch_related_news(tokens)
                    
                    # 5. Analyze with LLM
                    analysis = analyze_with_llm(tweet, tokens, news)
                    
                    # 6. Send alert if action recommended
                    if analysis['action'] != 'IGNORE':
                        send_telegram_alert(tweet, analysis, tokens)
            
            # Wait for next polling interval 
            logger.info("Waiting for next polling cycle...")
            time.sleep(polling_interval)
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(polling_interval)  # Continue despite errors

if __name__ == "__main__":
    main()
