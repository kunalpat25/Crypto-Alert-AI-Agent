# telegram_bot.py
import logging
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import re

def escape_markdown(text, version=2):
    """
    Escapes special characters for Telegram Markdown.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

load_dotenv()

logger = logging.getLogger(__name__)

def send_telegram_alert(tweet, analysis, tokens):
    """
    Send alert to Telegram with tweet and analysis information.
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_USER_ID')
    
    if not bot_token or not chat_id:
        logger.error("Telegram credentials not set. Set TELEGRAM_BOT_TOKEN and TELEGRAM_USER_ID env variables.")
        return False
    
    # Format the message

    message = f"""
📣 Tweet by @{tweet['username']}
🧠 LLM: {analysis['action']} {analysis['token']}
📈 Confidence: {analysis['confidence']}%
🕒 Delay: 1 min
💬 "{tweet['text']}"

🔍 Reasoning: {analysis['reasoning']}
⚠️ Manipulation probability: {analysis['manipulation_probability']}%
"""
    escaped_message = escape_markdown(message, version=2)
    
    # Send the message
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": escaped_message,
        "parse_mode": "MarkdownV2"
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logger.info(f"Alert sent to Telegram successfully")
            return True
        else:
            logger.error(f"Failed to send Telegram alert: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {e}")
        return False
