# 🗝️ Key-Miners: Scrape, Mine & Test API Keys from GitHub

> **A Swiss Army Knife for API key mining, verification, and chaos.**

---

## 🚀 What is Key-Miners?

**Key-Miners** is a Python-powered toolkit to **scrape, mine, verify, and store API keys** from public GitHub repositories.  
It’s built to be messy — not restricted by pipelines or structure. You’re free to scrape, test, and use API keys in any way you like.

Whether you're a security researcher, bug bounty hunter, or someone building your own custom tooling — this is your base.

---

## ⚙️ Features

- 🔍 Scrape GitHub repos, gists, and files for API keys
- 🧠 Auto-detect key types (OpenAI, AWS, Slack, Gemini, etc.)
- 🧪 Verify/test API key validity using real endpoints
- 📦 Store and organize mined data in multiple layers:
  - Temporary raw data
  - Backup files
  - Verified key pools
- 🔄 Mix and match scripts as per your flow — no enforced logic
- 🛠️ Dashboard available (basic)

---

## 📁 Project Structure

```

📂 core/
├── github\_scraper.py       # Scrapes GitHub using API/keywords
├── matcher.py              # Detects and classifies API key types
├── storage.py              # Saves scraped/tested data
└── utils.py                # Helpers

📂 data/
├── results.json            # Scraped keys (raw)
├── valid\_apis.json         # Successfully verified keys
├── backups/                # Timestamped backups
└── sample.json             # Sample data for quick testing

📂 dashboard/
├── app.py                  # Basic dashboard (optional)
└── templates/index.html

🧪 testopenai.py               # Tests OpenAI keys
🧪 sandvox.py                  # Multi-key type test handler
🧪 tests.py                    # Additional key tests

🔧 config.py                   # Global config
🧾 requirements.txt            # Python dependencies
🚀 main.py                     # Entry point for scraping/testing

````

---

## 🔑 Supported Key Types

This repo currently supports detection and testing for:

- OpenAI
- Slack
- AWS
- Google Gemini
- Mailgun
- And more...

You can add your own matchers and testers easily inside the `core/` or root.

---

## ⚠️ Philosophy: No Structure by Design

This repo is **deliberately unstructured**. You won’t find:

- Any enforced testing pipeline  
- Strict file flows  
- Formal class-based systems  

You can:
- Run individual test scripts
- Scrap and store wherever you want
- Chain test + storage the way you like

It’s a **toolbox**, not a framework.

---

## 🧠 Usage (Basic)

```bash
# Clone the repo
git clone https://github.com/DevLord-Avijit/Key-miners.git
cd Key-miners

# Install dependencies
pip install -r requirements.txt

# Start scraping and testing
python main.py
````

For individual testing:

```bash
python testopenai.py
python sandvox.py
```

---

## 🤝 Contributing

We welcome chaos-lovers to build on this!

You can help by:

* ✨ Improving project structure
* ⚡ Adding new API key matchers
* 🧪 Writing more test scripts for services
* 📊 Improving dashboard or visual output
* 🧹 Cleaning up the mess (if you dare)

PRs are open. Fork and have fun.

---

## 💡 Ideas for Improvements

* Auto pipeline (scrape → detect → test → store)
* Live dashboard with refreshable valid key stats
* CLI utility
* GitHub action integration
* Secret scanning filter bypass improvements

---

## 📜 License

This repository is for **educational and ethical testing purposes only.**
Misuse is strictly discouraged. Use responsibly.

---

## 👤 Author

Made with ⚔️ by [Avijit Singh](https://github.com/DevLord-Avijit)

If you find it useful, consider giving it a ⭐ and sharing feedback!

---

## 📸 Output Preview

Check the following files for sample data:

* `data/results.json`
* `tested_results.json`
* `valid_apis.json`

Or run the dashboard:

```bash
cd dashboard
python app.py
```

---

> “Nothing is organized here. That’s the fun part.” 😈

## ⚠️ Disclaimer

This project is for **educational and security research** purposes only.

- All API keys were scraped from **publicly available** sources (e.g. GitHub public repos).
- No private repositories were accessed or targeted.
- This is intended to raise awareness about sensitive data exposure.
- If any API key owner wants their data removed, please open an issue or contact directly.
- All real-looking keys are assumed to be expired, revoked, or IP-bound.

