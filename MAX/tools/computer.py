"""
tools/computer.py
All computer control functions - the hands of MAX
Includes input sanitization for shell commands
"""

import os
import sys
import subprocess
import platform
import shutil
import threading
import time
import webbrowser

OS = platform.system()  # Windows, Darwin, Linux


# ──────────────────────────────────────────
#  APP LAUNCHER
# ──────────────────────────────────────────

APP_MAP_WINDOWS = {
    "chrome": ["chrome", "google chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
    "firefox": ["firefox"],
    "notepad": ["notepad"],
    "calculator": ["calc"],
    "explorer": ["explorer"],
    "terminal": ["cmd", "wt"],  # tries Windows Terminal first
    "spotify": ["spotify"],
    "vscode": ["code"],
    "word": ["winword", r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"],
    "excel": ["excel", r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"],
    "powerpoint": ["powerpnt"],
    "settings": ["ms-settings:"],
    "paint": ["mspaint"],
    "photos": ["ms-photos:"],
    "camera": ["microsoft.windows.camera:"],
    "task_manager": ["taskmgr"],
    "control_panel": ["control"],
    "vlc": ["vlc"],
    "zoom": ["zoom"],
    "teams": ["teams"],
    "discord": ["discord"],
    "whatsapp": ["whatsapp"],
    "steam": ["steam"],
}

APP_MAP_MAC = {
    "chrome": ["open -a 'Google Chrome'"],
    "firefox": ["open -a Firefox"],
    "terminal": ["open -a Terminal"],
    "safari": ["open -a Safari"],
    "notes": ["open -a Notes"],
    "spotify": ["open -a Spotify"],
    "vscode": ["open -a 'Visual Studio Code'"],
    "finder": ["open -a Finder"],
    "calculator": ["open -a Calculator"],
    "settings": ["open -a 'System Preferences'"],
    "photos": ["open -a Photos"],
    "music": ["open -a Music"],
}

APP_MAP_LINUX = {
    "chrome": ["google-chrome", "chromium-browser", "chromium"],
    "firefox": ["firefox"],
    "terminal": ["gnome-terminal", "xterm", "konsole"],
    "files": ["nautilus", "dolphin", "thunar"],
    "vscode": ["code"],
    "spotify": ["spotify"],
    "calculator": ["gnome-calculator", "kcalc"],
    "settings": ["gnome-control-center"],
    "vlc": ["vlc"],
}


def open_app(app: str) -> str:
    """Open an application by name."""
    app = app.lower().strip()

    try:
        if OS == "Windows":
            candidates = APP_MAP_WINDOWS.get(app, [app])
            for cmd in candidates:
                try:
                    if cmd.startswith("ms-") or cmd.startswith("microsoft."):
                        os.startfile(cmd)
                    else:
                        subprocess.Popen(cmd, shell=True,
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                    return f"Opened {app}"
                except Exception:
                    continue

        elif OS == "Darwin":
            candidates = APP_MAP_MAC.get(app, [f"open -a {app}"])
            for cmd in candidates:
                try:
                    subprocess.Popen(cmd, shell=True)
                    return f"Opened {app}"
                except Exception:
                    continue

        elif OS == "Linux":
            candidates = APP_MAP_LINUX.get(app, [app])
            for cmd in candidates:
                try:
                    subprocess.Popen(cmd, shell=True)
                    return f"Opened {app}"
                except Exception:
                    continue

        # Generic fallback
        subprocess.Popen(app, shell=True)
        return f"Attempted to open {app}"
    except Exception as e:
        return f"Could not open {app}: {e}"


def close_app(app_title: str) -> str:
    """Close a window by its title."""
    try:
        import pygetwindow as gw
        windows = gw.getWindowsWithTitle(app_title)
        if windows:
            for w in windows:
                w.close()
            return f"Closed {app_title}"
        return f"No window found with title: {app_title}"
    except Exception as e:
        return f"Error closing {app_title}: {e}"


# ──────────────────────────────────────────
#  WEB & BROWSER
# ──────────────────────────────────────────

def open_url(url: str, browser: str = "default") -> str:
    """Open a URL in the browser."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened {url}"


def search_web(query: str) -> str:
    """Search Google."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searched Google for: {query}"


# ──────────────────────────────────────────
#  KEYBOARD & MOUSE
# ──────────────────────────────────────────

def type_text(text: str) -> str:
    """Type text using keyboard (supports Unicode)."""
    try:
        import pyautogui
        pyautogui.PAUSE = 0.05
        # Use write() instead of typewrite() for Unicode support
        pyautogui.write(text)
        return f"Typed: {text[:50]}..."
    except Exception as e:
        return f"Error typing: {e}"


def press_key(key: str, times: int = 1) -> str:
    """Press a keyboard shortcut or key."""
    try:
        import pyautogui
        key = key.lower()
        for _ in range(times):
            if "+" in key:
                keys = key.split("+")
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(key)
        return f"Pressed {key} x{times}"
    except Exception as e:
        return f"Error pressing key: {e}"


def click(x: int, y: int, button: str = "left") -> str:
    """Click at coordinates."""
    try:
        import pyautogui
        pyautogui.click(x, y, button=button)
        return f"Clicked at ({x}, {y})"
    except Exception as e:
        return f"Click error: {e}"


def move_mouse(x: int, y: int) -> str:
    """Move mouse to coordinates."""
    try:
        import pyautogui
        pyautogui.moveTo(x, y, duration=0.3)
        return f"Moved mouse to ({x}, {y})"
    except Exception as e:
        return f"Move error: {e}"


def scroll(direction: str = "down", amount: int = 3) -> str:
    """Scroll up or down."""
    try:
        import pyautogui
        clicks = -amount if direction == "down" else amount
        pyautogui.scroll(clicks)
        return f"Scrolled {direction}"
    except Exception as e:
        return f"Scroll error: {e}"


# ──────────────────────────────────────────
#  CLIPBOARD
# ──────────────────────────────────────────

def clipboard_copy(text: str) -> str:
    """Copy text to clipboard."""
    try:
        import pyperclip
        pyperclip.copy(text)
        return f"Copied to clipboard"
    except Exception as e:
        # Fallback
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            return "Copied selection to clipboard"
        except:
            return f"Clipboard error: {e}"


def clipboard_paste() -> str:
    """Paste from clipboard."""
    try:
        import pyautogui
        pyautogui.hotkey('ctrl', 'v')
        return "Pasted from clipboard"
    except Exception as e:
        return f"Paste error: {e}"


# ──────────────────────────────────────────
#  SCREENSHOT
# ──────────────────────────────────────────

def take_screenshot(filename: str = None) -> str:
    """Take a screenshot."""
    try:
        import pyautogui
        from datetime import datetime
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        # Save to Desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(desktop, exist_ok=True)
        path = os.path.join(desktop, filename)

        img = pyautogui.screenshot()
        img.save(path)
        return f"Screenshot saved to Desktop as {filename}"
    except Exception as e:
        return f"Screenshot error: {e}"


# ──────────────────────────────────────────
#  FILE SYSTEM
# ──────────────────────────────────────────

def create_file(path: str, content: str = "") -> str:
    """Create a file with content."""
    try:
        # Expand ~ to home directory
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Created file: {path}"
    except Exception as e:
        return f"File creation error: {e}"


def create_folder(path: str) -> str:
    """Create a directory."""
    try:
        path = os.path.expanduser(path)
        os.makedirs(path, exist_ok=True)
        return f"Created folder: {path}"
    except Exception as e:
        return f"Folder creation error: {e}"


def delete_file(path: str) -> str:
    """Delete a file or folder."""
    try:
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return f"Deleted: {path}"
    except Exception as e:
        return f"Delete error: {e}"


def list_files(path: str = None) -> str:
    """List files in a directory."""
    try:
        if not path:
            path = os.path.expanduser("~/Desktop")
        path = os.path.expanduser(path)
        items = os.listdir(path)
        files = [f for f in items if os.path.isfile(os.path.join(path, f))]
        folders = [f for f in items if os.path.isdir(os.path.join(path, f))]
        result = f"📁 {path}\n"
        result += f"Folders: {', '.join(folders[:10]) if folders else 'none'}\n"
        result += f"Files: {', '.join(files[:15]) if files else 'none'}"
        return result
    except Exception as e:
        return f"List error: {e}"


def move_file(src: str, dest: str) -> str:
    """Move a file."""
    try:
        shutil.move(os.path.expanduser(src), os.path.expanduser(dest))
        return f"Moved {src} → {dest}"
    except Exception as e:
        return f"Move error: {e}"


def copy_file(src: str, dest: str) -> str:
    """Copy a file."""
    try:
        shutil.copy2(os.path.expanduser(src), os.path.expanduser(dest))
        return f"Copied {src} → {dest}"
    except Exception as e:
        return f"Copy error: {e}"


# ──────────────────────────────────────────
#  SYSTEM — WITH INPUT SANITIZATION
# ──────────────────────────────────────────

# Dangerous patterns that should never be run from AI commands
BLOCKED_COMMANDS = [
    "rm -rf /", "rm -rf ~", "rm -rf *",
    "format c:", "format d:",
    "del /f /s /q c:", "del /f /s /q d:",
    "rd /s /q c:", "rd /s /q d:",
    ":(){:|:&};:",            # fork bomb
    "mkfs.", "dd if=",        # disk wipe
    "shutdown /s", "shutdown /r",  # handled via dedicated tools
    ":(){ :|:& };:",         # bash fork bomb
    "> /dev/sda",
]


def _is_command_safe(command: str) -> bool:
    """Check if a shell command is safe to execute."""
    cmd_lower = command.lower().strip()
    for blocked in BLOCKED_COMMANDS:
        if blocked.lower() in cmd_lower:
            return False
    return True


def run_command(command: str) -> str:
    """Run a shell command (with safety checks)."""
    if not _is_command_safe(command):
        return f"⚠️ Blocked dangerous command: {command[:60]}..."
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        output = result.stdout or result.stderr
        return output.strip()[:500] if output else "Command executed"
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Command error: {e}"


def set_volume(level: int) -> str:
    """Set system volume (0-100)."""
    try:
        level = max(0, min(100, level))
        if OS == "Windows":
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
        elif OS == "Linux":
            run_command(f"amixer sset Master {level}%")
        elif OS == "Darwin":
            run_command(f"osascript -e 'set volume output volume {level}'")
        return f"Volume set to {level}%"
    except Exception as e:
        # Fallback using nircmd
        try:
            run_command(f"nircmd.exe setsysvolume {int(level * 655.35)}")
        except:
            pass
        return f"Volume set to {level}% (approximate)"


def mute_volume() -> str:
    """Mute or unmute system volume."""
    try:
        if OS == "Windows":
            import pyautogui
            pyautogui.press('volumemute')
        elif OS == "Darwin":
            run_command("osascript -e 'set volume with output muted'")
        elif OS == "Linux":
            run_command("amixer set Master toggle")
        return "Volume muted/unmuted"
    except Exception as e:
        return f"Mute error: {e}"


def get_time() -> str:
    """Get current time and date."""
    from datetime import datetime
    now = datetime.now()
    return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}"


def get_battery() -> str:
    """Get battery status."""
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            status = "charging" if battery.power_plugged else "not charging"
            return f"Battery is at {battery.percent:.0f}%, {status}"
        return "No battery found (likely a desktop)"
    except Exception as e:
        return f"Battery info unavailable: {e}"


def set_reminder(message: str, seconds: int = 60) -> str:
    """Set a timed reminder."""
    def _remind():
        time.sleep(seconds)
        from core.speech import speak
        speak(f"Reminder: {message}")
        # Also show notification
        try:
            if OS == "Windows":
                run_command(f'msg * "MAX REMINDER: {message}"')
            elif OS == "Darwin":
                run_command(f'osascript -e \'display notification "{message}" with title "MAX Reminder"\'')
        except:
            pass

    t = threading.Thread(target=_remind, daemon=True)
    t.start()
    mins = seconds // 60
    secs = seconds % 60
    time_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
    return f"Reminder set for {time_str}: {message}"


def minimize_all() -> str:
    """Minimize all windows."""
    try:
        import pyautogui
        if OS == "Windows":
            pyautogui.hotkey('win', 'd')
        elif OS == "Darwin":
            pyautogui.hotkey('command', 'option', 'm')
        return "Minimized all windows"
    except Exception as e:
        return f"Error: {e}"


def lock_screen() -> str:
    """Lock the screen."""
    if OS == "Windows":
        run_command("rundll32.exe user32.dll,LockWorkStation")
    elif OS == "Darwin":
        run_command("pmset displaysleepnow")
    elif OS == "Linux":
        run_command("gnome-screensaver-command -l")
    return "Screen locked"


def shutdown(delay: int = 0) -> str:
    """Shutdown the computer."""
    if OS == "Windows":
        subprocess.run(f"shutdown /s /t {delay}", shell=True)
    elif OS in ["Darwin", "Linux"]:
        subprocess.run(f"sudo shutdown -h +{delay//60}" if delay > 0 else "sudo shutdown -h now", shell=True)
    return f"Shutting down in {delay} seconds"


def restart(delay: int = 0) -> str:
    """Restart the computer."""
    if OS == "Windows":
        subprocess.run(f"shutdown /r /t {delay}", shell=True)
    elif OS in ["Darwin", "Linux"]:
        subprocess.run("sudo reboot", shell=True)
    return f"Restarting in {delay} seconds"


def sleep_mode() -> str:
    """Put computer to sleep."""
    if OS == "Windows":
        subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
    elif OS == "Darwin":
        subprocess.run("pmset sleepnow", shell=True)
    elif OS == "Linux":
        subprocess.run("systemctl suspend", shell=True)
    return "Sleeping..."


def speak_only() -> str:
    """No-op tool for conversational responses."""
    return "OK"
