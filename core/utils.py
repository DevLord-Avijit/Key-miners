import os
from datetime import datetime
from config import LOG_FILE

def log(message, level="INFO"):
    """
    Logs a message to the log file and prints it.

    Args:
        message (str): The message to log.
        level (str): The log level (default: "INFO").
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"

    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

    print(log_entry)
