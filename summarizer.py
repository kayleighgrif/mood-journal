import os
import time
import requests
import json
from datetime import datetime, timedelta

# For simplicity, we'll store API key directly in the code
# In production, use environment variables or a secure vault
API_KEY = "your-anthropic-api-key-here"

# Simple rate limiting
last_request_time = None
MIN_REQUEST_INTERVAL = 1  # seconds between requests

def summarize_text(text, length='medium'):
    global last_request_time
    
    # Implement basic rate limiting
    if last_request_time is not None:
        elapsed = (datetime.now() - last_request_time).total_seconds()
        if elapsed < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - elapsed)
    
    # Claude API endpoint
    url = "https://api.anthropic.com/v1/messages"
    
    # Determine summary length prompt
    length_prompts = {
        'short': 'Provide a brief summary in 1-2 sentences.',
        'medium': 'Provide a concise summary in about 3-4 sentences.',
        'long': 'Provide a detailed summary in about 5-7 sentences.'
    }
    length_instruction = length_prompts.get(length, length_prompts['medium'])
    
    # Prepare the payload
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": f"Please summarize the following text. {length_instruction}\n\n{text}"
            }
        ]
    }
    
    # Set headers
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    try:
        # Record request time for rate limiting
        last_request_time = datetime.now()
        
        # Make the API call
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        # Extract the summary from the response
        result = response.json()
        summary = result["content"][0]["text"]
        
        return summary.strip()
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg += f" - {json.dumps(error_detail)}"
            except:
                error_msg += f" - Status code: {e.response.status_code}"
        raise Exception(error_msg)