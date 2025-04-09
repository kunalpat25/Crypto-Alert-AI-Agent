# Crypto Alert Bot

A simple bot that monitors influential Twitter accounts for cryptocurrency mentions and sends alerts via Telegram when potential market-moving tweets are detected.

## Features

- Monitors top crypto influencers on Twitter
- Detects cryptocurrency token mentions
- Analyzes sentiment and context
- Fetches related news headlines
- Uses LLM to determine trading signals
- Sends alerts via Telegram

## Setup

### Prerequisites

- Python 3.8+
- Telegram bot token (create one via @BotFather)
- Your Telegram user ID

### Installation

1. Clone this repository:

[git clone https://github.com/yourusername/crypto-alert-bot.git](https://github.com/kunalpat25/Crypto-Alert-AI-Agent.git)
cd crypto-alert-bot


2. Install dependencies:
pip install -r requirements.txt


3. Set up environment variables:
export TELEGRAM_BOT_TOKEN=your_bot_token
export TELEGRAM_USER_ID=your_user_id
export OPENAI_API_KEY=your_openai_key # Optional for production