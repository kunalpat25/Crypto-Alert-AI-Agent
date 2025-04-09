# news_fetcher.py update with Google News scraping
import logging
import requests
from bs4 import BeautifulSoup
import time
import random

logger = logging.getLogger(__name__)

def fetch_related_news(tokens):
    """
    Fetch news headlines related to the detected tokens using Google News.
    """
    if not tokens:
        return []
    
    all_headlines = []
    
    # Try to fetch news for each token
    for token in tokens:
        try:
            # Construct search query for crypto token
            query = f"{token} crypto"
            encoded_query = requests.utils.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}&tbm=nws&num=3"
            
            # Add random user agent to avoid blocking
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
            ]
            
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract news headlines
                news_elements = soup.select('div.mCBkyc')
                
                token_headlines = []
                for element in news_elements[:3]:  # Limit to top 3 per token
                    headline = element.text.strip()
                    if headline and len(headline) > 10:  # Filter out very short headlines
                        token_headlines.append(headline)
                
                all_headlines.extend(token_headlines)
                
                # Be nice to Google - add delay between requests
                time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error fetching news for {token}: {e}")
    
    # Limit to top 3 headlines total
    all_headlines = all_headlines[:3]
    
    logger.info(f"Fetched {len(all_headlines)} news headlines")
    return all_headlines
