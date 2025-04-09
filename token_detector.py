# token_detector.py
import json
import re
import logging

logger = logging.getLogger(__name__)

def load_coin_dictionary():
    try:
        with open('config/coin_dict.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Coin dictionary not found, using default list")
        return {
            "BTC": "Bitcoin",
            "ETH": "Ethereum",
            "DOGE": "Dogecoin",
            "XRP": "Ripple",
            "ADA": "Cardano",
            "SOL": "Solana",
            "PEPE": "Pepe",
            "SHIB": "Shiba Inu"
        }

def detect_tokens(text):
    """
    Detect cryptocurrency tokens mentioned in text.
    Returns a list of detected token symbols.
    """
    coins = load_coin_dictionary()
    
    # Pattern to match $SYMBOL format
    dollar_pattern = r'\$([A-Z]{2,10})'
    dollar_matches = re.findall(dollar_pattern, text)
    
    # Also look for coin names without $ symbol
    detected_tokens = []
    
    # Add tokens with $ prefix
    for match in dollar_matches:
        if match in coins:
            detected_tokens.append(match)
    
    # Look for coin names in text
    for symbol, name in coins.items():
        if name.lower() in text.lower() and symbol not in detected_tokens:
            detected_tokens.append(symbol)
    
    logger.info(f"Detected tokens: {detected_tokens}")
    return detected_tokens
