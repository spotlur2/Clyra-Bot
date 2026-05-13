import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("discord_messages.json")
MAX_MESSAGES = 20

def save_discord_result(username, message, context, result):
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "message": message,
        "context": context,
        "decision": result.get("decision", {}),
        "fused_output": result.get("fused_output", {})
    }

    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding = "utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.insert(0, entry)
    data = data[:MAX_MESSAGES]

    with open(LOG_FILE, "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 4)