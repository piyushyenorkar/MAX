"""
tools/browser.py
Full browser & web automation — 60+ tools
WhatsApp, Email, Meetings, YouTube, Google Workspace, Browser Control, Social Media
Uses only: pyautogui, webbrowser, urllib.parse, subprocess, time, platform
"""

import time
import webbrowser
import urllib.parse
import pyautogui

pyautogui.PAUSE = 0.4  # Reliable key timing


# ══════════════════════════════════════════
#  WHATSAPP
# ══════════════════════════════════════════

def _focus_whatsapp_search():
    """Click on WhatsApp Web's search bar ('Search or start a new chat').
    Coordinates calibrated from user's actual WhatsApp Web screenshot (1920x1200).
    """
    screen_w, screen_h = pyautogui.size()

    # Step 1: Escape to dismiss any address bar focus
    pyautogui.press('escape')
    time.sleep(0.3)

    # Step 2: Click on the chat list area first (to give WhatsApp page focus)
    # This clicks on a chat entry in the left panel
    chat_x = int(screen_w * 0.25)
    chat_y = int(screen_h * 0.40)
    pyautogui.click(chat_x, chat_y)
    time.sleep(0.5)

    # Step 3: Click on the search bar "Search or start a new chat"
    # From screenshot: search bar is at ~22% from top, ~25% from left
    search_x = int(screen_w * 0.25)
    search_y = int(screen_h * 0.22)
    pyautogui.click(search_x, search_y)
    time.sleep(0.5)


def _paste_text(text: str):
    """Paste text using clipboard (more reliable than pyautogui.write)."""
    try:
        import pyperclip
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
    except ImportError:
        pyautogui.write(text, interval=0.03)


def send_whatsapp(phone: str, message: str, country_code: str = "91") -> str:
    """Send WhatsApp message via WhatsApp Web URL (by phone number)."""
    try:
        phone = phone.replace(" ", "").replace("-", "").replace("+", "")
        if len(phone) == 10:
            phone = country_code + phone

        # Validate: must be at least 10 digits (without country code)
        digits_only = ''.join(c for c in phone if c.isdigit())
        if len(digits_only) < 10:
            return f"Phone number too short: '{phone}'. Please say the full 10-digit number."

        if not message.strip():
            return "No message provided. Please say what message to send."

        encoded = urllib.parse.quote(message)
        webbrowser.open(f"https://web.whatsapp.com/send?phone={digits_only}&text={encoded}")
        time.sleep(10)  # WhatsApp Web needs time to load
        pyautogui.press('enter')
        time.sleep(1)
        return f"WhatsApp sent to {digits_only}"
    except Exception as e:
        return f"WhatsApp error: {e}"


def send_whatsapp_contact(contact_name: str, message: str) -> str:
    """Send WhatsApp message by searching contact name in WhatsApp Web."""
    try:
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(10)  # WhatsApp Web takes time to fully load

        # Focus WhatsApp's search (NOT Chrome's address bar)
        _focus_whatsapp_search()
        time.sleep(0.5)

        # Clear any previous search and type contact name
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        _paste_text(contact_name)
        time.sleep(2)  # Wait for search results to appear

        # Select the first search result
        pyautogui.press('down')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(1)

        # Now the chat is open — type the message in the message box
        _paste_text(message)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)

        return f"WhatsApp sent to {contact_name}"
    except Exception as e:
        return f"WhatsApp contact error: {e}"


def open_whatsapp_chat(contact_name: str) -> str:
    """Open a WhatsApp chat by contact name (don't send message)."""
    try:
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(10)

        _focus_whatsapp_search()
        time.sleep(0.5)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        _paste_text(contact_name)
        time.sleep(2)

        pyautogui.press('down')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(1)

        return f"Opened chat with {contact_name}"
    except Exception as e:
        return f"WhatsApp chat error: {e}"


def open_whatsapp() -> str:
    """Open WhatsApp Web."""
    webbrowser.open("https://web.whatsapp.com")
    return "Opened WhatsApp Web"


# ══════════════════════════════════════════
#  EMAIL (GMAIL)
# ══════════════════════════════════════════

def send_email(to: str, subject: str = "", body: str = "") -> str:
    """Compose and send email via Gmail."""
    try:
        params = urllib.parse.urlencode({"view": "cm", "fs": "1", "to": to, "su": subject, "body": body})
        webbrowser.open(f"https://mail.google.com/mail/?{params}")
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'enter')  # Gmail send shortcut
        time.sleep(1)
        return f"Email sent to {to}"
    except Exception as e:
        return f"Email error: {e}"


def open_gmail() -> str:
    """Open Gmail."""
    webbrowser.open("https://mail.google.com")
    return "Opened Gmail"


def check_email() -> str:
    """Open Gmail inbox to check emails."""
    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    return "Opened Gmail inbox"


def open_email_thread(search_query: str) -> str:
    """Search for an email thread in Gmail."""
    try:
        encoded = urllib.parse.quote(search_query)
        webbrowser.open(f"https://mail.google.com/mail/u/0/#search/{encoded}")
        return f"Searching Gmail for: {search_query}"
    except Exception as e:
        return f"Email search error: {e}"


# ══════════════════════════════════════════
#  MEETINGS (GOOGLE MEET & CALENDAR)
# ══════════════════════════════════════════

def create_meeting() -> str:
    """Create new Google Meet and copy link."""
    try:
        webbrowser.open("https://meet.google.com/new")
        time.sleep(5)
        # Copy meeting link from address bar
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.3)
        pyautogui.press('escape')
        return "Meeting created. Link copied to clipboard."
    except Exception as e:
        return f"Meeting error: {e}"


def join_meeting(meet_link: str) -> str:
    """Join a meeting by link."""
    try:
        if not meet_link.startswith("http"):
            meet_link = "https://" + meet_link
        webbrowser.open(meet_link)
        time.sleep(3)
        return f"Joining meeting"
    except Exception as e:
        return f"Join error: {e}"


def schedule_meeting(title: str, date: str = "", meeting_time: str = "") -> str:
    """Open Google Calendar to schedule a meeting."""
    try:
        url = "https://calendar.google.com/calendar/u/0/r/eventedit"
        if title:
            url += f"?text={urllib.parse.quote(title)}"
        webbrowser.open(url)
        time.sleep(4)
        return f"Calendar opened to schedule: {title}"
    except Exception as e:
        return f"Schedule error: {e}"


# ══════════════════════════════════════════
#  YOUTUBE
# ══════════════════════════════════════════

def open_youtube(query: str = "") -> str:
    """Open YouTube, optionally search."""
    if query:
        encoded = urllib.parse.quote(query)
        webbrowser.open(f"https://www.youtube.com/results?search_query={encoded}")
        return f"Searching YouTube: {query}"
    webbrowser.open("https://www.youtube.com")
    return "Opened YouTube"


def search_youtube(query: str) -> str:
    """Search YouTube."""
    encoded = urllib.parse.quote(query)
    webbrowser.open(f"https://www.youtube.com/results?search_query={encoded}")
    return f"Searching YouTube: {query}"


def play_youtube(query: str) -> str:
    """Search YouTube and play the first result."""
    try:
        encoded = urllib.parse.quote(query)
        webbrowser.open(f"https://www.youtube.com/results?search_query={encoded}")
        time.sleep(4)
        # Tab to first video and press Enter
        pyautogui.press('tab', presses=6, interval=0.2)
        time.sleep(0.3)
        pyautogui.press('enter')
        return f"Playing: {query}"
    except Exception as e:
        return f"YouTube play error: {e}"


def youtube_pause_play() -> str:
    """Pause/play YouTube video (K shortcut)."""
    pyautogui.press('k')
    return "Toggled play/pause"


def youtube_mute() -> str:
    """Mute YouTube video (M shortcut)."""
    pyautogui.press('m')
    return "Toggled mute"


def youtube_fullscreen() -> str:
    """Toggle YouTube fullscreen (F shortcut)."""
    pyautogui.press('f')
    return "Toggled fullscreen"


def youtube_skip(seconds: int = 10) -> str:
    """Skip forward/backward in YouTube video."""
    if seconds > 0:
        # L = skip forward 10s, Right arrow = 5s
        presses = max(1, seconds // 10)
        pyautogui.press('l', presses=presses, interval=0.2)
        return f"Skipped forward {seconds}s"
    else:
        presses = max(1, abs(seconds) // 10)
        pyautogui.press('j', presses=presses, interval=0.2)
        return f"Skipped backward {abs(seconds)}s"


# ══════════════════════════════════════════
#  GOOGLE WORKSPACE
# ══════════════════════════════════════════

def open_google_docs() -> str:
    """Open Google Docs."""
    webbrowser.open("https://docs.google.com")
    return "Opened Google Docs"


def create_google_doc(title: str = "") -> str:
    """Create a new Google Doc."""
    webbrowser.open("https://docs.google.com/document/create")
    time.sleep(3)
    if title:
        # Click on "Untitled document" and type title
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.write(title, interval=0.03)
    return f"Created new Google Doc"


def open_google_drive() -> str:
    """Open Google Drive."""
    webbrowser.open("https://drive.google.com")
    return "Opened Google Drive"


def search_drive(query: str) -> str:
    """Search Google Drive."""
    encoded = urllib.parse.quote(query)
    webbrowser.open(f"https://drive.google.com/drive/search?q={encoded}")
    return f"Searching Drive: {query}"


def open_google_sheets() -> str:
    """Open Google Sheets."""
    webbrowser.open("https://sheets.google.com")
    return "Opened Google Sheets"


def create_google_sheet(title: str = "") -> str:
    """Create a new Google Sheet."""
    webbrowser.open("https://sheets.google.com/create")
    time.sleep(3)
    return "Created new Google Sheet"


# ══════════════════════════════════════════
#  BROWSER TAB & NAVIGATION CONTROL
# ══════════════════════════════════════════

def browser_new_tab(url: str = "") -> str:
    """Open new browser tab, optionally navigate to URL."""
    try:
        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.5)
        if url:
            if not url.startswith("http"):
                url = "https://" + url
            _type_in_address_bar(url)
        return "Opened new tab" + (f": {url}" if url else "")
    except Exception as e:
        return f"New tab error: {e}"


def browser_close_tab() -> str:
    """Close current browser tab."""
    pyautogui.hotkey('ctrl', 'w')
    return "Tab closed"


def browser_switch_tab(direction: str = "next") -> str:
    """Switch to next or previous tab."""
    if direction in ("previous", "prev", "left"):
        pyautogui.hotkey('ctrl', 'shift', 'tab')
    else:
        pyautogui.hotkey('ctrl', 'tab')
    return f"Switched {direction} tab"


def browser_go_to(url: str) -> str:
    """Navigate to URL in current tab."""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        _type_in_address_bar(url)
        return f"Going to {url}"
    except Exception as e:
        return f"Navigation error: {e}"


def browser_search(query: str) -> str:
    """Search in browser address bar."""
    try:
        _type_in_address_bar(query)
        return f"Searching: {query}"
    except Exception as e:
        return f"Search error: {e}"


def browser_back() -> str:
    """Go back."""
    pyautogui.hotkey('alt', 'left')
    return "Went back"


def browser_forward() -> str:
    """Go forward."""
    pyautogui.hotkey('alt', 'right')
    return "Went forward"


def browser_refresh() -> str:
    """Refresh page."""
    pyautogui.press('f5')
    return "Refreshed"


def browser_hard_refresh() -> str:
    """Hard refresh (bypass cache)."""
    pyautogui.hotkey('ctrl', 'shift', 'r')
    return "Hard refreshed"


def browser_zoom(direction: str = "in", amount: int = 1) -> str:
    """Zoom in, out, or reset."""
    for _ in range(amount):
        if direction == "in":
            pyautogui.hotkey('ctrl', '=')
        elif direction == "out":
            pyautogui.hotkey('ctrl', '-')
        elif direction == "reset":
            pyautogui.hotkey('ctrl', '0')
            break
    return f"Zoom {direction}"


def browser_bookmark() -> str:
    """Bookmark current page."""
    pyautogui.hotkey('ctrl', 'd')
    time.sleep(0.5)
    pyautogui.press('enter')
    return "Bookmarked"


def browser_fullscreen() -> str:
    """Toggle fullscreen."""
    pyautogui.press('f11')
    return "Toggled fullscreen"


def browser_find(text: str) -> str:
    """Find text on page."""
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.3)
    pyautogui.write(text, interval=0.03)
    pyautogui.press('enter')
    return f"Finding: {text}"


def browser_new_incognito() -> str:
    """Open new incognito window."""
    pyautogui.hotkey('ctrl', 'shift', 'n')
    return "Opened incognito"


def browser_copy_url() -> str:
    """Copy current page URL to clipboard."""
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    pyautogui.press('escape')
    return "URL copied"


def browser_reopen_tab() -> str:
    """Reopen last closed tab."""
    pyautogui.hotkey('ctrl', 'shift', 't')
    return "Reopened tab"


def browser_scroll_top() -> str:
    """Scroll to top of page."""
    pyautogui.press('home')
    return "Scrolled to top"


def browser_scroll_bottom() -> str:
    """Scroll to bottom of page."""
    pyautogui.press('end')
    return "Scrolled to bottom"


# ══════════════════════════════════════════
#  SOCIAL MEDIA & POPULAR SITES
# ══════════════════════════════════════════

def open_linkedin() -> str:
    webbrowser.open("https://www.linkedin.com")
    return "Opened LinkedIn"

def open_twitter() -> str:
    webbrowser.open("https://x.com")
    return "Opened Twitter/X"

def open_instagram() -> str:
    webbrowser.open("https://www.instagram.com")
    return "Opened Instagram"

def open_github(repo: str = "") -> str:
    if repo:
        webbrowser.open(f"https://github.com/{repo}")
        return f"Opened GitHub: {repo}"
    webbrowser.open("https://github.com")
    return "Opened GitHub"

def open_slack() -> str:
    webbrowser.open("https://app.slack.com")
    return "Opened Slack"

def open_notion() -> str:
    webbrowser.open("https://www.notion.so")
    return "Opened Notion"

def open_figma() -> str:
    webbrowser.open("https://www.figma.com")
    return "Opened Figma"

def open_zoom_web() -> str:
    webbrowser.open("https://zoom.us/start")
    return "Opened Zoom"

def open_teams_web() -> str:
    webbrowser.open("https://teams.microsoft.com")
    return "Opened Teams"


# ══════════════════════════════════════════
#  MAPS, TRANSLATE, WEATHER
# ══════════════════════════════════════════

def open_maps(location: str = "") -> str:
    """Open Google Maps, optionally search a location."""
    if location:
        encoded = urllib.parse.quote(location)
        webbrowser.open(f"https://www.google.com/maps/search/{encoded}")
        return f"Maps: {location}"
    webbrowser.open("https://www.google.com/maps")
    return "Opened Google Maps"


def get_directions(origin: str, destination: str) -> str:
    """Get directions on Google Maps."""
    o = urllib.parse.quote(origin)
    d = urllib.parse.quote(destination)
    webbrowser.open(f"https://www.google.com/maps/dir/{o}/{d}")
    return f"Directions: {origin} → {destination}"


def open_translate(text: str = "", from_lang: str = "en", to_lang: str = "hi") -> str:
    """Open Google Translate."""
    if text:
        encoded = urllib.parse.quote(text)
        webbrowser.open(f"https://translate.google.com/?sl={from_lang}&tl={to_lang}&text={encoded}")
        return f"Translating: {text}"
    webbrowser.open("https://translate.google.com")
    return "Opened Google Translate"


def open_weather(city: str = "") -> str:
    """Check weather on Google."""
    if city:
        encoded = urllib.parse.quote(f"weather {city}")
        webbrowser.open(f"https://www.google.com/search?q={encoded}")
        return f"Weather for {city}"
    webbrowser.open("https://www.google.com/search?q=weather")
    return "Opened weather"


# ══════════════════════════════════════════
#  HELPER
# ══════════════════════════════════════════

def _type_in_address_bar(text: str):
    """Focus address bar, clear it, type text, press Enter."""
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    try:
        import pyperclip
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
    except ImportError:
        pyautogui.write(text, interval=0.02)
    time.sleep(0.2)
    pyautogui.press('enter')
