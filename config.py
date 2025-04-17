# config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://...")

# Admins who can use /togglelearn
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "123456789").split(",")))
