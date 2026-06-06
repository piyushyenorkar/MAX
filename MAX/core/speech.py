"""
core/speech.py
Handles all Speech-to-Text and Text-to-Speech operations
pyttsx3 is reinitialized per call to avoid event loop corruption
"""

import os
import time
from config import STT_ENGINE, TTS_ENGINE, WHISPER_MODEL, ASSISTANT_NAME

# ──────────────────────────────────────────
#  TEXT TO SPEECH
# ──────────────────────────────────────────

def speak(text: str, callback=None):
    """Speak the given text aloud. Creates a fresh TTS engine each time."""
    print(f"\n🤖 {ASSISTANT_NAME}: {text}")

    if TTS_ENGINE == "gtts":
        _speak_gtts(text)
    else:
        _speak_pyttsx3(text)

    if callback:
        callback()


def _speak_pyttsx3(text):
    """Speak using pyttsx3. Fresh engine each call to avoid lock-up."""
    try:
        import pyttsx3
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except Exception:
            pass
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # Prefer Zira (female, clearer) then David
        for voice in voices:
            if "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            for voice in voices:
                if "david" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS] Error: {e}")


def _speak_gtts(text):
    """Speak using Google TTS (online, better quality)."""
    try:
        from gtts import gTTS
        import pygame
        import tempfile
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            tmpfile = f.name
        pygame.mixer.init()
        pygame.mixer.music.load(tmpfile)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.unlink(tmpfile)
    except Exception as e:
        print(f"[TTS] gTTS error: {e}")
        _speak_pyttsx3(text)


# ──────────────────────────────────────────
#  SPEECH TO TEXT
# ──────────────────────────────────────────

def listen(timeout=5, phrase_limit=10) -> str | None:
    """Listen for a voice command and return text."""
    if STT_ENGINE == "whisper":
        return _listen_whisper(timeout)
    else:
        return _listen_google(timeout, phrase_limit)


def _listen_google(timeout=5, phrase_limit=10) -> str | None:
    """Use Google's free speech recognition."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.8

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                text = r.recognize_google(audio)
                print(f"👤 You: {text}")
                return text.lower().strip()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
    except Exception as e:
        print(f"[STT] Google error: {e}")
        return None


# ──────────────────────────────────────────
#  WHISPER (CACHED MODEL)
# ──────────────────────────────────────────

_whisper_model = None

def _get_whisper_model():
    """Load Whisper model once and cache it."""
    global _whisper_model
    if _whisper_model is None:
        import faster_whisper
        print(f"[STT] Loading Whisper model '{WHISPER_MODEL}'...")
        _whisper_model = faster_whisper.WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    return _whisper_model


def _listen_whisper(timeout=5) -> str | None:
    """Use OpenAI Whisper locally (offline)."""
    try:
        import speech_recognition as sr
        import tempfile
        import wave

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=15)
            except sr.WaitTimeoutError:
                return None

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(audio.sample_width)
                wf.setframerate(audio.sample_rate)
                wf.writeframes(audio.get_raw_data())
            tmpfile = f.name

        model = _get_whisper_model()
        segments, _ = model.transcribe(tmpfile, beam_size=5)
        text = " ".join([seg.text for seg in segments]).strip()
        os.unlink(tmpfile)

        if text:
            print(f"👤 You: {text}")
            return text.lower()
        return None

    except Exception as e:
        print(f"[STT] Whisper error: {e}")
        return None


# ──────────────────────────────────────────
#  WAKE WORD LISTENER
# ──────────────────────────────────────────

def listen_for_wake_word(wake_word: str, callback) -> bool:
    """Listen until wake word is detected."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.pause_threshold = 0.5

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=4)
                text = r.recognize_google(audio).lower()
                print(f"[WAKE DEBUG] Heard: '{text}'")
                if wake_word.lower() in text:
                    callback()
                    return True
            except Exception:
                pass
        return False
    except Exception as e:
        print(f"[WAKE] Error: {e}")
        return False
