import requests
import json
from config import GROQ_API_KEY, GROQ_MODEL

def call_groq(messages, max_tokens=2000):
    """Simple Groq API call"""
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY not found")
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": max_tokens
    }
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Groq API error: {response.status_code}")
    
    return response.json()["choices"][0]["message"]["content"]

def parse_json_response(content):
    """Parse JSON from AI response with fallback"""
    try:
        # Try to find JSON in the response
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start != -1 and end > start:
            json_str = content[start:end]
            parsed = json.loads(json_str)
            
            # Validate that it has the required fields
            if ("trending_angles" in parsed and 
                "hashtags" in parsed and 
                "post_blueprints" in parsed):
                return parsed
    except Exception as e:
        print(f"JSON parsing error: {e}")
    
    # Return None if parsing failed (don't return fallback for modifications)
    return None