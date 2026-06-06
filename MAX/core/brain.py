"""
core/brain.py
AI Brain - Uses Groq to understand commands and decide actions
Compact prompt to save tokens. Robust JSON parser.
"""

import json
import re
import time
from config import GROQ_API_KEY, AI_MODEL, ASSISTANT_PERSONALITY, MAX_HISTORY

_client = None

def _get_client():
    global _client
    if _client is None:
        from groq import Groq
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


conversation_history = []

SYSTEM_PROMPT = ASSISTANT_PERSONALITY + """

You control a computer. Respond with ONE JSON object only:
{"tool":"name","params":{},"speak":"short confirm"}

TOOLS (use exact names):
open_app(app) close_app(app_title) open_url(url) search_web(query)
send_whatsapp(phone,message,country_code) send_whatsapp_contact(contact_name,message) open_whatsapp_chat(contact_name) open_whatsapp()
send_email(to,subject,body) open_gmail() check_email() open_email_thread(search_query)
create_meeting() join_meeting(meet_link) schedule_meeting(title,date,time)
open_youtube(query) search_youtube(query) play_youtube(query) youtube_pause_play() youtube_mute() youtube_fullscreen() youtube_skip(seconds)
open_google_docs() create_google_doc(title) open_google_drive() search_drive(query) open_google_sheets() create_google_sheet(title)
browser_new_tab(url) browser_close_tab() browser_switch_tab(direction) browser_go_to(url) browser_search(query) browser_back() browser_forward() browser_refresh() browser_hard_refresh() browser_zoom(direction,amount) browser_bookmark() browser_fullscreen() browser_find(text) browser_new_incognito() browser_copy_url() browser_reopen_tab() browser_scroll_top() browser_scroll_bottom()
open_linkedin() open_twitter() open_instagram() open_github(repo) open_slack() open_notion() open_figma() open_zoom_web() open_teams_web()
open_maps(location) get_directions(origin,destination) open_translate(text,from_lang,to_lang) open_weather(city)
type_text(text) press_key(key,times) click(x,y) move_mouse(x,y) scroll(direction,amount) clipboard_copy(text) clipboard_paste()
take_screenshot(filename) create_file(path,content) create_folder(path) delete_file(path) list_files(path) move_file(src,dest) copy_file(src,dest)
run_command(command) set_volume(level) mute_volume() get_time() get_battery() set_reminder(message,seconds) minimize_all() lock_screen() shutdown(delay) restart(delay) sleep_mode()
speak_only() — for conversations/greetings

RULES:
1. Return EXACTLY ONE valid JSON object. Nothing else.
2. "speak" = 3-8 word confirmation. Never describe plans.
3. For multi-step requests, pick the MOST IMPORTANT tool. One tool per response.
4. WhatsApp: 10-digit phone → add "91" prefix. Use send_whatsapp_contact for names.
5. Never output multiple JSON objects. Pick ONE tool.

EXAMPLES:
User: "send whatsapp to mom saying i'll be late" → {"tool":"send_whatsapp_contact","params":{"contact_name":"mom","message":"I'll be late"},"speak":"Message sent to Mom."}
User: "open youtube and play lofi" → {"tool":"play_youtube","params":{"query":"lofi"},"speak":"Playing lofi."}
User: "what time is it" → {"tool":"get_time","params":{},"speak":""}
User: "how are you" → {"tool":"speak_only","params":{},"speak":"I'm great, thanks for asking!"}
"""


def think(user_input: str) -> dict:
    """Send user input to AI and get back a tool call decision."""
    MAX_RETRIES = 3

    conversation_history.append({"role": "user", "content": user_input})

    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

    for attempt in range(MAX_RETRIES):
        try:
            client = _get_client()
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *conversation_history
                ],
                temperature=0.2,
                max_tokens=200
            )

            reply = response.choices[0].message.content.strip()
            conversation_history.append({"role": "assistant", "content": reply})

            # Robust JSON extraction
            parsed = _extract_json(reply)
            if parsed:
                return parsed

            # Fallback: clean any code/JSON from speech
            clean = re.sub(r'\{[^}]*\}', '', reply).strip()
            clean = re.sub(r'["\[\]{}]', '', clean).strip()
            clean = re.sub(r',\s*speak:', '', clean).strip()
            if not clean or len(clean) < 2:
                clean = "Done."
            return {"tool": "speak_only", "params": {}, "speak": clean}

        except Exception as e:
            wait_time = (2 ** attempt) * 0.5
            print(f"[BRAIN] Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(wait_time)
            else:
                return {"tool": "speak_only", "params": {}, "speak": "Connection issue. Try again."}


def _extract_json(text: str) -> dict | None:
    """Try multiple strategies to extract valid JSON from AI response."""
    # Strategy 1: Direct parse
    try:
        return json.loads(text.strip())
    except (json.JSONDecodeError, ValueError):
        pass

    # Strategy 2: Remove markdown code fences
    clean = text.strip()
    if "```" in clean:
        for part in clean.split("```"):
            p = part.strip()
            if p.startswith("json"):
                p = p[4:].strip()
            try:
                return json.loads(p)
            except (json.JSONDecodeError, ValueError):
                continue

    # Strategy 3: Regex extract first JSON object
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', clean)
    if match:
        try:
            return json.loads(match.group())
        except (json.JSONDecodeError, ValueError):
            pass

    # Strategy 4: Find innermost {...} patterns
    for m in re.finditer(r'\{[^{}]+\}', clean):
        try:
            candidate = json.loads(m.group())
            if "tool" in candidate:
                return candidate
        except (json.JSONDecodeError, ValueError):
            continue

    return None


def clear_history():
    global conversation_history
    conversation_history = []


def get_history():
    return conversation_history.copy()
