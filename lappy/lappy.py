"""
lappy.py
Lappy — Pure Voice AI Agent
Talks to you like a person. No text, no GUI. Just speak and listen.
"""

import sys
import os
import time

# Add project root to path for proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import WAKE_WORD, ASSISTANT_NAME, GROQ_API_KEY, USER_NAME
from core.speech import speak, listen, listen_for_wake_word
from core.brain import think, clear_history
from core.logger import log, save_interaction
from tools.executor import execute


# ──────────────────────────────────────────
#  STATE
# ──────────────────────────────────────────

class LappyState:
    def __init__(self):
        self.running = False
        self.listening = False
        self.wake_mode = True
        self.mode = "idle"
        self.last_command = ""
        self.last_response = ""
        self.last_tool = ""
        self.command_count = 0
        self.on_state_change = None

state = LappyState()


# ──────────────────────────────────────────
#  PERSONALIZED GREETINGS
# ──────────────────────────────────────────

def _get_time_greeting() -> str:
    """Get a time-aware personalized greeting."""
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 12:
        time_greet = "Good morning"
    elif hour < 17:
        time_greet = "Good afternoon"
    else:
        time_greet = "Good evening"
    return f"{time_greet}, {USER_NAME}! I'm {ASSISTANT_NAME}. What can I do for you today?"


# ──────────────────────────────────────────
#  CORE PIPELINE
# ──────────────────────────────────────────

def process_command(user_input: str):
    """Full pipeline: input → brain → execute → speak."""
    if not user_input or not user_input.strip():
        return

    state.last_command = user_input
    state.mode = "thinking"
    _notify_state_change()

    log("info", f"Processing: {user_input}")

    # Handle built-in commands
    if any(word in user_input.lower() for word in ["exit", "quit", "goodbye", "bye lappy", "stop"]):
        speak(f"Goodbye, {USER_NAME}! See you next time.")
        state.running = False
        return

    if "clear history" in user_input.lower():
        clear_history()
        speak("Conversation history cleared.")
        return

    if "what can you do" in user_input.lower() or "help" == user_input.lower().strip():
        help_text = (
            f"Hey {USER_NAME}! I can open apps, search the web, take screenshots, "
            "manage files, type text, control volume, set reminders, and much more. "
            "Just tell me what you need!"
        )
        speak(help_text)
        state.last_response = help_text
        state.last_tool = "speak_only"
        _notify_state_change()
        return

    # Ask AI brain
    decision = think(user_input)

    # Execute the decision
    result = execute(decision)

    # Speak the response
    speak_text = result.get("speak_text", "Done.")
    state.last_response = speak_text
    state.last_tool = result.get("tool", "unknown")
    state.command_count += 1
    state.mode = "speaking"
    _notify_state_change()

    speak(speak_text)

    # Save to history
    save_interaction(
        user_input,
        result.get("tool", "unknown"),
        result.get("result", ""),
        speak_text
    )

    state.mode = "listening" if state.running else "idle"
    _notify_state_change()


def _notify_state_change():
    if state.on_state_change:
        state.on_state_change(state)


# ──────────────────────────────────────────
#  VOICE AGENT — ALWAYS LISTENING (NO WAKE WORD)
# ──────────────────────────────────────────

def run_voice_agent():
    """
    Pure voice agent — always listening, no wake word needed.
    Works like a real conversation: Lappy speaks, you speak, repeat.
    """
    state.running = True
    state.mode = "listening"
    log("info", "Lappy Voice Agent started")

    # Greet the user
    greeting = _get_time_greeting()
    speak(greeting)
    time.sleep(0.5)

    print("\n" + "="*50)
    print("  🎤 VOICE AGENT ACTIVE — Just speak naturally!")
    print("  Say 'goodbye' or 'stop' to exit.")
    print("="*50 + "\n")

    while state.running:
        try:
            state.mode = "listening"
            _notify_state_change()

            # Always listening — no wake word, just speak
            command = listen(timeout=8, phrase_limit=15)

            if command:
                # Skip empty/noise
                if len(command.strip()) < 2:
                    continue
                process_command(command)

                # Small pause between conversations
                time.sleep(0.3)
            else:
                # No speech detected, keep listening silently
                pass

        except KeyboardInterrupt:
            speak(f"Goodbye, {USER_NAME}!")
            break
        except Exception as e:
            log("error", f"Voice agent error: {e}")
            time.sleep(1)

    state.running = False
    state.mode = "idle"
    log("info", "Lappy Voice Agent stopped")


# ──────────────────────────────────────────
#  VOICE LOOP WITH WAKE WORD (for GUI use)
# ──────────────────────────────────────────

def run_voice_loop():
    """Voice loop with wake word — used by GUI."""
    state.running = True
    state.mode = "idle"
    log("info", "Lappy started in wake-word voice mode")

    greeting = _get_time_greeting()
    speak(greeting)
    time.sleep(1)

    while state.running:
        try:
            if state.wake_mode:
                state.mode = "idle"
                _notify_state_change()

                def on_wake():
                    speak(f"Yes, {USER_NAME}?")
                    state.mode = "listening"
                    _notify_state_change()
                    command = listen(timeout=7, phrase_limit=15)
                    if command:
                        process_command(command)

                listen_for_wake_word(WAKE_WORD, on_wake)
            else:
                state.mode = "listening"
                _notify_state_change()
                command = listen(timeout=5, phrase_limit=15)
                if command:
                    process_command(command)

        except KeyboardInterrupt:
            break
        except Exception as e:
            log("error", f"Loop error: {e}")
            time.sleep(1)

    state.running = False
    state.mode = "idle"
    log("info", "Lappy stopped")


def run_text_loop():
    """Text-based command loop (fallback)."""
    state.running = True
    log("info", "Lappy started in text mode")
    greeting = _get_time_greeting()
    speak(greeting)

    while state.running:
        try:
            user_input = input(f"\n💬 {USER_NAME}: ").strip()
            if user_input:
                process_command(user_input)
        except KeyboardInterrupt:
            break
        except EOFError:
            break

    state.running = False


# ──────────────────────────────────────────
#  CHECKS
# ──────────────────────────────────────────

def check_api_key() -> bool:
    """Verify API key is set."""
    if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
        print("\n❌ ERROR: Groq API key not set!")
        print("   Create a .env file with: GROQ_API_KEY=gsk_your_key_here")
        return False
    return True


def check_dependencies() -> list:
    """Check which dependencies are installed."""
    missing = []
    packages = {
        "groq": "groq",
        "speech_recognition": "SpeechRecognition",
        "pyautogui": "pyautogui",
        "pyttsx3": "pyttsx3",
        "psutil": "psutil",
        "pyperclip": "pyperclip",
        "dotenv": "python-dotenv",
        "pyaudio": "pyaudio",
    }
    for module, package in packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    return missing


# ──────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print(f"  🤖 {ASSISTANT_NAME} - Voice AI Agent")
    print("=" * 55)

    if not check_api_key():
        sys.exit(1)

    missing = check_dependencies()
    if missing:
        print(f"\n⚠️  Missing: {', '.join(missing)}")
        print(f"   Run: pip install {' '.join(missing)}")
        sys.exit(1)

    run_voice_agent()
