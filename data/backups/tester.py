import json
import os
import requests
import re

BASE_DIR = os.path.dirname(__file__)
files = [
    "fvdv.json"
    ]

all_secrets = []

# === Load all JSON files ===
for file in files:
    full_path = os.path.join(BASE_DIR, file)
    try:
        with open(full_path, 'r') as f:
            data = json.load(f)
            all_secrets.extend(data if isinstance(data, list) else [data])
    except Exception as e:
        print(f"Error loading {file}: {e}")

# === Testing Functions ===

def test_google_api_key(key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng=0,0&key={key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        error = data.get("error_message", "").lower()
        if "ip address" in error:
            return "invalid - IP restricted"
        elif "referer" in error:
            return "invalid - referer restricted"
        elif "not authorized" in error:
            return "invalid - API not enabled"
        elif "exceeded your daily request quota" in error:
            return "valid - quota exceeded"
        elif "invalid api key" in error or "not valid" in error:
            return "invalid - bad key"
        elif error:
            return f"invalid - {error}"
        else:
            return "valid"
    elif response.status_code == 403:
        return "invalid - permission denied (403)"
    elif response.status_code == 400:
        return "invalid - bad request (400)"
    else:
        return f"invalid - HTTP {response.status_code}"

def test_discord_token(token):
    headers = {"Authorization": f"Bot {token}"}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    return "valid" if response.status_code == 200 else "invalid"

def test_github_token(token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    return "valid" if response.status_code == 200 else "invalid"

def test_sendgrid_api_key(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get("https://api.sendgrid.com/v3/user/account", headers=headers)
    return "valid" if response.status_code == 200 else "invalid"

def test_mailgun_key(key):
    url = "https://api.mailgun.net/v3/domains"
    response = requests.get(url, auth=("api", key))
    return "valid" if response.status_code == 200 else "invalid"

def test_slack_token(token):
    response = requests.post("https://slack.com/api/auth.test", data={"token": token})
    return "valid" if response.json().get("ok") else "invalid"

def test_openai_api_key(key):
    url = "https://api.openai.com/v1/models"
    headers = {
        "Authorization": f"Bearer {key}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return "valid" if response.status_code == 200 else "invalid"
    except requests.exceptions.RequestException:
        return "invalid"


# === Tester Map ===
testers = {
    "Google API Key": test_google_api_key,
    "Discord Bot Token": test_discord_token,
    "GitHub Token": test_github_token,
    "SendGrid API Key": test_sendgrid_api_key,
    "Mailgun API Key": test_mailgun_key,
    "Slack Token": test_slack_token,
    "OpenAI API Key": test_openai_api_key,
}

# === Utility: sanitize filename (optional) ===
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

# === Run tests ===
tested = []
valid_by_type = {}

for secret in all_secrets:
    typ = secret["secret_type"]
    val = secret["secret_value"]
    test_func = testers.get(typ)

    if test_func:
        try:
            status = test_func(val.strip())
        except Exception as e:
            status = "error"
    else:
        status = "unsupported"

    secret["status"] = status
    tested.append(secret)

    print(f"[{status}] {typ} => {val[:10]}...")

    # ✅ Properly match all valid status variants
    if status.strip().lower().startswith("valid"):
        if typ not in valid_by_type:
            valid_by_type[typ] = []
        valid_by_type[typ].append(secret)

# === Save all tested results ===
with open("tested_results.json", "w") as f:
    json.dump(tested, f, indent=2)

# === Save valid results in grouped format with comment ===
commented_output = {
    "//": "This file contains VALID API keys categorized by type. Manually test further if needed.",
    **valid_by_type
}

with open("valid_apis.json", "w") as f:
    json.dump(commented_output, f, indent=2)

print("✅ Saved valid keys in valid_apis.json")
