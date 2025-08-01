import os
import sys
from dotenv import load_dotenv
import re

# ✅ Load .env variables first
load_dotenv()

# === GitHub Token ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ GitHub token not found in environment variables.")
    sys.exit(1)

# === Headers for GitHub API ===

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

SEARCH_KEYWORDS = {
    "openai api key",
    "chatgpt key",
    "openai secret",
    "sk-"
}

REGEX_PATTERNS = {
    "OpenAI API Key": re.compile(r"sk-[A-Za-z0-9]{32,}"),}


# === GitHub Search Settings ===
RESULTS_PER_PAGE = 30
MAX_PAGES = 4000

# === Storage Paths ===
RESULTS_FILE = "data/results.json"
LOG_FILE = "logs/activity.log"
