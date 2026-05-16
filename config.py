import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration - OpenAI-compatible by default
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Agent settings
TEMPERATURE = 0.7
MAX_STEPS = 10
