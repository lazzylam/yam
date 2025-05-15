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

OWNER_USERNAME = os.getenv("OWNER_USERNAME")  # Contoh: wlamora
OWNER_ID = int(os.getenv("OWNER_ID", 0))  # Contoh: 6368336706
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP")  # Contoh: thislamora (tanpa @)

# DEVS bisa diisi dengan beberapa ID, dipisah spasi: "6368336706 1355077923"
DEVS = [int(i) for i in os.getenv("DEVS", "").split()]

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/lazzylam/tag")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = os.getenv("GIT_TOKEN")