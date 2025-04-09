# llm_analyzer.py update with Groq API
import logging
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def analyze_with_llm(tweet, tokens, news):
    """
    Analyze tweet with Groq LLM API to determine trading action.
    """
    groq_api_key = os.environ.get('GROQ_API_KEY')
    
    if not groq_api_key:
        logger.error("GROQ_API_KEY environment variable not set")
        return {
            "action": "IGNORE",
            "token": tokens[0] if tokens else "",
            "confidence": 0,
            "manipulation_probability": 50,
            "reasoning": "Error: LLM API key not configured"
        }
    
    # Format news headlines as a string
    news_text = "\n".join([f"- {headline}" for headline in news]) if news else "None"
    
    # Construct the prompt
    prompt = f"""You are a financial analyst bot trained to analyze market-manipulative tweets.

Tweet: "{tweet['text']}" by @{tweet['username']} ({tweet['name']})
Mentioned tokens: {', '.join(tokens) if tokens else 'None'}
Recent news: 
{news_text}

Analyze if this tweet hints at a market move. Consider:
1. Is this likely to influence crypto prices?
2. Does it contain direct or indirect signals about buying or selling?
3. Is there evidence of potential market manipulation?

Respond in JSON format:
{{
  "action": "BUY" or "SELL" or "IGNORE",
  "token": "The token symbol to trade",
  "confidence": A number from 0-100 representing confidence in this signal,
  "manipulation_probability": A number from 0-100 representing likelihood this is market manipulation,
  "reasoning": "Brief explanation of your analysis"
}}
"""

    # Call Groq API (using Mixtral model)
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result['choices'][0]['message']['content']
            
            # Extract JSON from response
            try:
                # Find JSON object in the response
                json_start = llm_response.find('{')
                json_end = llm_response.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = llm_response[json_start:json_end]
                    analysis = json.loads(json_str)
                    
                    # Ensure all required fields are present
                    required_fields = ["action", "token", "confidence", "manipulation_probability", "reasoning"]
                    for field in required_fields:
                        if field not in analysis:
                            analysis[field] = "" if field in ["token", "reasoning"] else 0
                    
                    logger.info(f"LLM Analysis: {json.dumps(analysis)}")
                    return analysis
                else:
                    raise ValueError("No JSON object found in LLM response")
                    
            except Exception as e:
                logger.error(f"Error parsing LLM response: {e}")
                logger.error(f"Raw response: {llm_response}")
                
                # Fallback response
                return {
                    "action": "IGNORE",
                    "token": tokens[0] if tokens else "",
                    "confidence": 30,
                    "manipulation_probability": 50,
                    "reasoning": f"Error parsing LLM response: {str(e)[:100]}"
                }
        else:
            logger.error(f"LLM API error: {response.status_code} - {response.text}")
            return {
                "action": "IGNORE",
                "token": tokens[0] if tokens else "",
                "confidence": 0,
                "manipulation_probability": 50,
                "reasoning": f"LLM API error: {response.status_code}"
            }
            
    except Exception as e:
        logger.error(f"Error calling LLM API: {e}")
        return {
            "action": "IGNORE",
            "token": tokens[0] if tokens else "",
            "confidence": 0,
            "manipulation_probability": 50,
            "reasoning": f"Error: {str(e)[:100]}"
        }
