from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Ambil variabel dari environment
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MENTION_CHUNK_SIZE = int(os.getenv("MENTION_CHUNK_SIZE", 5))
DELAY_BETWEEN_MESSAGES = int(os.getenv("DELAY_BETWEEN_MESSAGES", 2))

OWNER_USERNAME = "wlamora"  # Replace with your Telegram username without @
OWNER_ID = 6368336706  # Replace with your Telegram user ID
SUPPORT_GROUP = "thislamora"
DEVS = [6368336706]  # Ganti dengan ID kamu

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/lazzylam/tag")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = os.getenv("GIT_TOKEN")
