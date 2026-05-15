import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL_ID = "deepseek-v4-flash"
API_BASE = "https://api.deepseek.com/v1"
TEMPERATURE = 0.7
MAX_STEPS = 10
