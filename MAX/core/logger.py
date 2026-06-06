"""
core/logger.py
Logs all interactions for history and debugging
"""

import os
import json
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
LOG_FILE = os.path.join(LOG_DIR, "max.log")
HISTORY_FILE = os.path.join(LOG_DIR, "history.json")


def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)


def log(level: str, message: str):
    ensure_dirs()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level.upper()}] {message}\n"
    print(line.strip())
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line)
    except Exception:
        pass


def save_interaction(user_input: str, tool: str, result: str, response: str):
    ensure_dirs()
    try:
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)

        history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "tool": tool,
            "result": result[:200],
            "response": response
        })

        # Keep last 100 interactions
        history = history[-100:]

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        log("error", f"Could not save history: {e}")


def get_history(limit: int = 20):
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
            return history[-limit:]
    except Exception:
        pass
    return []
