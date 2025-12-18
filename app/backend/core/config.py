import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

# Platform configurations
PLATFORMS = {
    "linkedin": {
        "name": "LinkedIn",
        "description": "Professional networking and B2B content",
        "hashtag_count": "8-12 professional hashtags",
        "focus": "Career insights, industry trends, thought leadership"
    },
    "instagram": {
        "name": "Instagram", 
        "description": "Visual storytelling and lifestyle content",
        "hashtag_count": "15-25 discovery hashtags",
        "focus": "Visual content, tutorials, behind-the-scenes"
    },
    "twitter": {
        "name": "Twitter",
        "description": "Real-time engagement and discussions",
        "hashtag_count": "5-8 strategic hashtags", 
        "focus": "Threads, quick insights, discussions"
    }
}