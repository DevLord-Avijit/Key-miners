import requests

API_KEY = "key-328f4f3aecd8c8ac97ebb040c5cd145a"

response = requests.get("https://api.mailgun.net/v3/domains", auth=("api", API_KEY))

if response.status_code == 200:
    domains = response.json()
    print("✅ API key is valid. Domains linked to key:")
    for d in domains["items"]:
        print("-", d["name"])
else:
    print("❌ Invalid API key or no domains.")
    print(response.text)
