import json
import os
from config import RESULTS_FILE

def save_results(new_results):
    """
    Appends new results to the results JSON file safely.

    Args:
        new_results (list): List of dicts containing matched key info.
    """
    existing_results = []

    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                existing_results = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_results = []

    combined_results = existing_results + new_results

    # Optional: remove duplicates based on 'match' field if present
    seen = set()
    unique_results = []
    for res in combined_results:
        key = res.get("match") or json.dumps(res)
        if key not in seen:
            seen.add(key)
            unique_results.append(res)

    with open(RESULTS_FILE, "w") as f:
        json.dump(unique_results, f, indent=2)
