import requests

API_KEY = "key-328f4f3aecd8c8ac97ebb040c5cd145a"
DOMAIN = "sandboxb7de56698df443608af1bb4d7364d354.mailgun.org"
TO_EMAIL = "assistantmark1.0@gmail.com"

response = requests.post(
    f"https://api.mailgun.net/v3/{DOMAIN}/messages",
    auth=("api", API_KEY),
    data={
        "from": f"Demo User <mailgun@{DOMAIN}>",
        "to": TO_EMAIL,
        "subject": "Test Email from Public Mailgun Key",
        "text": "This is a safe test email using the Mailgun key from the demo repo."
    }
)

if response.status_code == 200:
    print("✅ Test email sent successfully.")
else:
    print("❌ Failed to send email.")
    print(response.status_code)
    print(response.text)
