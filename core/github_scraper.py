import asyncio
import httpx
import logging
from config import HEADERS, SEARCH_KEYWORDS, RESULTS_PER_PAGE, MAX_PAGES, REGEX_PATTERNS
from core.matcher import compile_patterns, match_patterns

# Setup
compiled_patterns = compile_patterns(REGEX_PATTERNS)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

GITHUB_API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"


async def search_github_code(client, keyword, page):
    """Async search for code files on GitHub using keyword."""
    url = f"{GITHUB_API_BASE}/search/code"
    params = {
        "q": f"{keyword} in:file",
        "per_page": RESULTS_PER_PAGE,
        "page": page
    }
    try:
        response = await client.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        elif response.status_code == 403:
            logging.warning("Rate limit hit.")
        else:
            logging.error(f"[{response.status_code}] GitHub error: {response.text}")
    except httpx.RequestError as e:
        logging.error(f"Request error: {e}")
    return []


async def get_default_branch(client, repo_full_name):
    """Get repo's default branch."""
    try:
        url = f"{GITHUB_API_BASE}/repos/{repo_full_name}"
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("default_branch", "main")
    except Exception as e:
        logging.warning(f"Failed to get branch: {e}")
    return "main"


async def fetch_raw_file_content(client, repo, path, branch="main"):
    """Download raw file content from GitHub."""
    url = f"{RAW_BASE}/{repo}/{branch}/{path}"
    try:
        response = await client.get(url)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if "text" in content_type or "json" in content_type:
                return response.text
        else:
            logging.debug(f"Non-200: {url}")
    except httpx.RequestError as e:
        logging.error(f"Fetch error: {e}")
    return None


async def process_item(client, item):
    """Process a GitHub search result item."""
    repo = item.get("repository", {}).get("full_name", "")
    path = item.get("path", "")
    html_url = item.get("html_url", "")
    if not repo or not path:
        return []

    branch = await get_default_branch(client, repo)
    content = await fetch_raw_file_content(client, repo, path, branch)
    if not content:
        return []

    secrets = await match_patterns(content, compiled_patterns)
    return [{
        "file_url": html_url,
        "secret_type": sname,
        "secret_value": svalue
    } for sname, svalue in secrets]


async def run_full_scraper():
    """Run the async GitHub scraping job."""
    results = []
    logging.info("🧠 Starting GitHub async scraper...")

    async with httpx.AsyncClient(timeout=15) as client:
        for keyword in SEARCH_KEYWORDS:
            logging.info(f"🔍 Keyword: {keyword}")
            for page in range(1, MAX_PAGES + 1):
                logging.info(f"   ↳ Page {page}")
                items = await search_github_code(client, keyword, page)
                if not items:
                    break

                tasks = [process_item(client, item) for item in items]
                all_results = await asyncio.gather(*tasks)

                for res in all_results:
                    results.extend(res)

                await asyncio.sleep(1.5)  # Respect rate limits

    logging.info(f"✅ Scraping complete. {len(results)} secrets found.")
    return results
