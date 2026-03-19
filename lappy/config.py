# ============================================================
#   LAPPY - Config File
#   API key loaded from .env file (create one if missing)
# ============================================================

import os
import platform
from pathlib import Path

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenv not installed, fall back to env vars

# --- AI Brain (Get free key at console.groq.com) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# --- User Name (for personalized greetings) ---
USER_NAME = "Piyush"

# --- Speech (Whisper runs locally - no key needed) ---
# Options: "google" (needs internet) | "whisper" (offline, recommended)
STT_ENGINE = "google"

# --- Text to Speech ---
# Options: "pyttsx3" (offline) | "gtts" (online, better quality)
TTS_ENGINE = "pyttsx3"

# --- AI Model ---
AI_MODEL = "llama-3.3-70b-versatile"   # Smart enough for tool routing

# --- Whisper Model (if using whisper STT) ---
# Options: "tiny", "base", "small", "medium"
WHISPER_MODEL = "base"

# --- Wake Word (say this to activate) ---
WAKE_WORD = "lappy"

# --- Assistant Name & Personality ---
ASSISTANT_NAME = "Lappy"
ASSISTANT_PERSONALITY = """You are Lappy, a powerful AI assistant that controls a computer.
You are concise, efficient, and proactive. When given a task, you figure out 
the best way to execute it using available tools. Always confirm actions taken.
Keep responses short and clear. You can open apps, manage files, search the web,
take screenshots, type text, and much more. Be direct and action-oriented."""

# --- OS Detection (auto-detected, but can override) ---
OS = platform.system()  # "Windows", "Darwin" (macOS), "Linux"

# --- Logging ---
LOG_FILE = "data/lappy.log"
SAVE_HISTORY = True
MAX_HISTORY = 50
