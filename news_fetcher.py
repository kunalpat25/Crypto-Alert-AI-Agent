# news_fetcher.py
import logging
import random

logger = logging.getLogger(__name__)

def fetch_related_news(tokens):
    """
    Fetch news headlines related to the detected tokens.
    In production, this would use a news API or web scraping.
    """
    # Mock news headlines for demo purposes
    news_database = {
        "BTC": [
            "Bitcoin breaks $60K resistance level",
            "Institutional investors pile into Bitcoin ETFs",
            "Bitcoin mining difficulty reaches all-time high"
        ],
        "ETH": [
            "Ethereum 2.0 upgrade scheduled for next month",
            "ETH gas fees drop to 6-month low",
            "DeFi projects on Ethereum see surge in TVL"
        ],
        "DOGE": [
            "Dogecoin rallies after Elon Musk tweet",
            "Dogecoin Foundation announces new roadmap",
            "DOGE becomes payment option on major platform"
        ],
        "PEPE": [
            "PEPE meme coin gains 300% in a week",
            "Whales accumulating PEPE, on-chain data shows",
            "PEPE listed on major exchange"
        ]
    }
    
    # Collect headlines for all detected tokens
    headlines = []
    for token in tokens:
        if token in news_database:
            # Get up to 2 random headlines per token
            token_headlines = random.sample(
                news_database[token], 
                min(2, len(news_database[token]))
            )
            headlines.extend(token_headlines)
    
    # Limit to top 3 headlines total
    headlines = headlines[:3]
    
    logger.info(f"Fetched {len(headlines)} news headlines")
    return headlines
