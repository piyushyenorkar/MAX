# ⚡ MAX — AI Desktop Assistant
> Your personal voice-controlled AI that sees your screen and controls your entire computer.

---

## 📁 Project Structure

```
jarvis/
├── run.py              ← START HERE (main launcher)
├── max.py            ← Core agent orchestrator
├── config.py           ← Configuration (reads .env for API key)
├── .env                ← ⭐ YOUR API KEY GOES HERE
├── requirements.txt    ← Python dependencies
├── start_max.vbs     ← Auto-start on Windows login
│
├── core/
│   ├── brain.py        ← Groq LLM integration (singleton + retry)
│   ├── speech.py       ← Voice input/output (cached Whisper)
│   └── logger.py       ← Logging & history
│
├── tools/
│   ├── computer.py     ← All PC control functions (30+ tools)
│   └── executor.py     ← Maps AI decisions to actions
│
├── ui/
│   └── dashboard.py    ← Beautiful Tkinter GUI
│
└── data/
    ├── max.log       ← Activity log (auto-created)
    └── history.json    ← Command history (auto-created)
```

---

## 🚀 Setup (5 minutes)

### Step 1 — Get Your Free Groq API Key
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Click "API Keys" → "Create API Key"
4. Copy the key (starts with `gsk_...`)

### Step 2 — Add Your Key
The API key is stored securely in a `.env` file. Open `.env` and set:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3 — Install Python Dependencies
Make sure you have Python 3.9+ installed, then:
```bash
pip install -r requirements.txt
```

If you get errors with `pyaudio` on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

On Mac:
```bash
brew install portaudio
pip install pyaudio
```

### Step 4 — Run MAX!
```bash
python run.py
```

---

## 🎮 How to Use

### Voice Mode
1. Click **"START VOICE"** in the dashboard
2. Say **"MAX"** to wake it up
3. Give your command
4. Uncheck "Wake word required" for always-on listening

### Text Mode
- Just type in the input box at the bottom and press Enter

---

## 🔁 Auto-Start on Windows Login

To make MAX launch automatically when you open your laptop:

1. Press `Win + R`, type `shell:startup`, hit Enter
2. Copy `start_max.vbs` into the Startup folder
3. Restart your PC — MAX will greet you by name!

---

## 💬 Example Commands

### Apps
- "Open Chrome"
- "Open Notepad and type Hello World"
- "Open Spotify"
- "Close Calculator"
- "Open VS Code"

### Web
- "Search Google for Python tutorials"
- "Open YouTube"
- "Go to github.com"

### Files
- "Take a screenshot"
- "Create a folder called MyProject on Desktop"
- "List files in my Downloads"
- "Create a text file called notes with the content buy groceries"

### System
- "What time is it?"
- "Check my battery"
- "Set volume to 50"
- "Mute the volume"
- "Lock my screen"
- "Minimize all windows"
- "Remind me in 5 minutes to drink water"

### Keyboard
- "Press Enter"
- "Press Ctrl+C"
- "Type Hello, this is MAX!"

---

## ⚙️ Configuration (config.py)

| Setting | Options | Default |
|---|---|---|
| `STT_ENGINE` | `"google"` or `"whisper"` | `"google"` |
| `TTS_ENGINE` | `"pyttsx3"` or `"gtts"` | `"pyttsx3"` |
| `WAKE_WORD` | Any word | `"max"` |
| `AI_MODEL` | Any Groq model | `"llama-3.3-70b-versatile"` |
| `USER_NAME` | Your name | `"Piyush"` |

### Switching to Offline Whisper STT
1. Install: `pip install faster-whisper`
2. In config.py: `STT_ENGINE = "whisper"`
3. MAX will download the model on first run (~150MB for "base")

### Switching to Better TTS (gTTS)
1. Install: `pip install gTTS pygame`
2. In config.py: `TTS_ENGINE = "gtts"`

---

## 🔧 Troubleshooting

**Microphone not working?**
- Make sure your mic is set as default in system settings
- Try: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

**App won't open?**
- The app might be named differently on your system
- Use exact app name or try text mode: type the command manually

**GUI looks off?**
- Requires Python 3.9+ and Tkinter (included with most Python installs)
- Windows: should work out of the box
- Linux: `sudo apt-get install python3-tk`

**Voice recognition wrong language?**
- In `core/speech.py`, change `r.recognize_google(audio)` to
  `r.recognize_google(audio, language="hi-IN")` for Hindi, etc.

---

## 🔒 Privacy Notes
- Voice data sent to Google's STT (use Whisper mode for fully offline/private)
- Your commands are processed by Groq (they have a privacy policy at groq.com)
- All logs stored locally in `data/` folder
- API key stored in `.env` file, not in source code
- No data ever leaves your machine except for the API calls

---

## 🛣️ What's Next (Upgrade Ideas)
- Add screen vision: send screenshots to Gemini Vision for context
- Add custom wake word with `pvporcupine`
- Connect to Gmail/Calendar via API
- Build a mobile companion app with Flask
- Add memory/personality persistence
