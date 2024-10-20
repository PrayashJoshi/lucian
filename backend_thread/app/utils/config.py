from dotenv import main
import os

# Load environment variables from .env
main.load_dotenv()

# Access API keys and URLs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
WEAVIATE_ADMIN_KEY = os.getenv("WEAVIATE_ADMIN_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
# app/utils/config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    WEAVIATE_ADMIN_KEY = os.getenv("WEAVIATE_ADMIN_KEY")
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
    AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")