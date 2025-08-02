```python
import os
import sys
from dotenv import load_dotenv
import re

# -----------------------------------------------------------------------------
# sandvox.py
#
# This script searches for potentially sensitive information (like OpenAI API keys)
# within public GitHub repositories using the GitHub API.  It loads environment
# variables for configuration and logs its activities.
# -----------------------------------------------------------------------------

# ✅ Load .env variables first
# This line ensures that the script loads environment variables from a .env file
# (if it exists) before accessing them. This is good practice for keeping sensitive
# information like API keys out of the codebase.
load_dotenv()

# === GitHub Token ===
# The GitHub token is essential for authenticating API requests.
# It's retrieved from the environment variables.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    # If the token is missing, the script will print an error message and exit.
    print("❌ GitHub token not found in environment variables.")
    sys.exit(1)

# === Headers for GitHub API ===
# These headers are included in every API request to authenticate with GitHub
# and specify the type of response the script expects (JSON in this case).
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",  # Authentication with the GitHub token.
    "Accept": "application/vnd.github.v3+json"  # Requesting the JSON format of the GitHub API
}

# === Search Keywords ===
# A set of keywords that the script will use to search through repositories.
# These keywords are typically associated with sensitive information, such as
# OpenAI API keys.
SEARCH_KEYWORDS = {
    "openai api key",
    "chatgpt key",
    "openai secret",
    "sk-"
}

# === Regular Expression Patterns ===
#  This dictionary contains regular expression patterns to help identify
#  specific types of sensitive information. The keys are descriptions
#  of what the pattern matches, and the values are the compiled regular
#  expression objects.
REGEX_PATTERNS = {
    "OpenAI API Key": re.compile(r"sk-[A-Za-z0-9]{32,}"), # Matches OpenAI API keys.
}


# === GitHub Search Settings ===
# Configuration for controlling GitHub search behavior:

RESULTS_PER_PAGE = 30  # The number of results to fetch per page in the GitHub API.
MAX_PAGES = 4000       # The maximum number of pages to iterate through in search results.


# === Storage Paths ===
# Defines the file paths for storing search results and logs.
RESULTS_FILE = "data/results.json"  # File to store the search results in JSON format.
LOG_FILE = "logs/activity.log"      # File to log the script's activity and errors.
```