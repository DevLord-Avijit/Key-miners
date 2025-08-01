import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from openai import AuthenticationError, RateLimitError
from typing import List, Set

def test_openai_key(api_key: str, index: int = None):
    client = OpenAI(api_key=api_key)
    try:
        response = client.models.list()
        print(f"[{index}] ✅ VALID")
        return "VALID"
    except AuthenticationError:
        print(f"[{index}] ❌ INVALID")
        return "INVALID"
    except RateLimitError:
        print(f"[{index}] ⚠️ RATE LIMITED (VALID)")
        return "RATE_LIMITED"
    except Exception as e:
        print(f"[{index}] ❗ ERROR: {e}")
        return "ERROR"

def load_unique_keys(filepath: str) -> List[str]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            keys = [entry["secret_value"] for entry in data if "secret_value" in entry]
            return list(set(keys))  # Remove duplicates
    except FileNotFoundError:
        print(f"❌ JSON file '{filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Invalid JSON format.")
        sys.exit(1)

def run_parallel_tests(api_keys: List[str], max_workers: int = 10):
    print(f"\n🚀 Running in parallel with {max_workers} threads...\n")
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(test_openai_key, key, idx + 1): key for idx, key in enumerate(api_keys)}
        for future in as_completed(futures):
            key = futures[future]
            result = future.result()
            results[key] = result
    return results

if __name__ == "__main__":
    json_path = "keys.json"  # 👈 Change this if needed
    api_keys = load_unique_keys(json_path)

    print(f"\n🔍 Loaded {len(api_keys)} unique API keys from JSON.")
    results = run_parallel_tests(api_keys, max_workers=20)  # Adjust threads if needed

    print("\n📊 Summary:")
    summary = {"VALID": 0, "INVALID": 0, "RATE_LIMITED": 0, "ERROR": 0}
    for res in results.values():
        summary[res] += 1

    for status, count in summary.items():
        print(f"{status:>12}: {count}")
