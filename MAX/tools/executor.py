"""
tools/executor.py
Maps AI brain decisions to actual computer tool calls — 80+ tools
"""

from tools.computer import (
    open_app, close_app, open_url, search_web,
    type_text, press_key, click, move_mouse, scroll,
    clipboard_copy, clipboard_paste,
    take_screenshot, create_file, create_folder,
    delete_file, list_files, move_file, copy_file,
    run_command, set_volume, mute_volume,
    get_time, get_battery, set_reminder,
    minimize_all, lock_screen, shutdown, restart,
    sleep_mode, speak_only
)

from tools.browser import (
    # WhatsApp
    send_whatsapp, send_whatsapp_contact, open_whatsapp_chat, open_whatsapp,
    # Email
    send_email, open_gmail, check_email, open_email_thread,
    # Meetings
    create_meeting, join_meeting, schedule_meeting,
    # YouTube
    open_youtube, search_youtube, play_youtube,
    youtube_pause_play, youtube_mute, youtube_fullscreen, youtube_skip,
    # Google Workspace
    open_google_docs, create_google_doc, open_google_drive, search_drive,
    open_google_sheets, create_google_sheet,
    # Browser control
    browser_new_tab, browser_close_tab, browser_switch_tab,
    browser_go_to, browser_search, browser_back, browser_forward,
    browser_refresh, browser_hard_refresh, browser_zoom,
    browser_bookmark, browser_fullscreen, browser_find,
    browser_new_incognito, browser_copy_url, browser_reopen_tab,
    browser_scroll_top, browser_scroll_bottom,
    # Social media
    open_linkedin, open_twitter, open_instagram, open_github,
    open_slack, open_notion, open_figma, open_zoom_web, open_teams_web,
    # Utilities
    open_maps, get_directions, open_translate, open_weather,
)


TOOL_MAP = {
    # ── Desktop & Apps ──
    "open_app":        lambda p: open_app(p.get("app", "")),
    "close_app":       lambda p: close_app(p.get("app_title", "")),
    "open_url":        lambda p: open_url(p.get("url", ""), p.get("browser", "default")),
    "search_web":      lambda p: search_web(p.get("query", "")),

    # ── Keyboard & Mouse ──
    "type_text":       lambda p: type_text(p.get("text", "")),
    "press_key":       lambda p: press_key(p.get("key", ""), p.get("times", 1)),
    "click":           lambda p: click(p.get("x", 0), p.get("y", 0), p.get("button", "left")),
    "move_mouse":      lambda p: move_mouse(p.get("x", 0), p.get("y", 0)),
    "scroll":          lambda p: scroll(p.get("direction", "down"), p.get("amount", 3)),

    # ── Clipboard ──
    "clipboard_copy":  lambda p: clipboard_copy(p.get("text", "")),
    "clipboard_paste": lambda p: clipboard_paste(),

    # ── Screenshot & Files ──
    "take_screenshot": lambda p: take_screenshot(p.get("filename", None)),
    "create_file":     lambda p: create_file(p.get("path", ""), p.get("content", "")),
    "create_folder":   lambda p: create_folder(p.get("path", "")),
    "delete_file":     lambda p: delete_file(p.get("path", "")),
    "list_files":      lambda p: list_files(p.get("path", None)),
    "move_file":       lambda p: move_file(p.get("src", ""), p.get("dest", "")),
    "copy_file":       lambda p: copy_file(p.get("src", ""), p.get("dest", "")),

    # ── System ──
    "run_command":     lambda p: run_command(p.get("command", "")),
    "set_volume":      lambda p: set_volume(p.get("level", 50)),
    "mute_volume":     lambda p: mute_volume(),
    "get_time":        lambda p: get_time(),
    "get_battery":     lambda p: get_battery(),
    "set_reminder":    lambda p: set_reminder(p.get("message", ""), p.get("seconds", 60)),
    "minimize_all":    lambda p: minimize_all(),
    "lock_screen":     lambda p: lock_screen(),
    "shutdown":        lambda p: shutdown(p.get("delay", 0)),
    "restart":         lambda p: restart(p.get("delay", 0)),
    "sleep_mode":      lambda p: sleep_mode(),

    # ── WhatsApp ──
    "send_whatsapp":         lambda p: send_whatsapp(p.get("phone", ""), p.get("message", ""), p.get("country_code", "91")),
    "send_whatsapp_contact": lambda p: send_whatsapp_contact(p.get("contact_name", ""), p.get("message", "")),
    "open_whatsapp_chat":    lambda p: open_whatsapp_chat(p.get("contact_name", "")),
    "open_whatsapp":         lambda p: open_whatsapp(),

    # ── Email (Gmail) ──
    "send_email":        lambda p: send_email(p.get("to", ""), p.get("subject", ""), p.get("body", "")),
    "open_gmail":        lambda p: open_gmail(),
    "check_email":       lambda p: check_email(),
    "open_email_thread": lambda p: open_email_thread(p.get("search_query", "")),

    # ── Meetings ──
    "create_meeting":    lambda p: create_meeting(),
    "join_meeting":      lambda p: join_meeting(p.get("meet_link", p.get("link", ""))),
    "schedule_meeting":  lambda p: schedule_meeting(p.get("title", ""), p.get("date", ""), p.get("time", "")),

    # ── YouTube ──
    "open_youtube":      lambda p: open_youtube(p.get("query", "")),
    "search_youtube":    lambda p: search_youtube(p.get("query", "")),
    "play_youtube":      lambda p: play_youtube(p.get("query", "")),
    "youtube_pause_play":lambda p: youtube_pause_play(),
    "youtube_mute":      lambda p: youtube_mute(),
    "youtube_fullscreen":lambda p: youtube_fullscreen(),
    "youtube_skip":      lambda p: youtube_skip(p.get("seconds", 10)),

    # ── Google Workspace ──
    "open_google_docs":    lambda p: open_google_docs(),
    "create_google_doc":   lambda p: create_google_doc(p.get("title", "")),
    "open_google_drive":   lambda p: open_google_drive(),
    "search_drive":        lambda p: search_drive(p.get("query", "")),
    "open_google_sheets":  lambda p: open_google_sheets(),
    "create_google_sheet": lambda p: create_google_sheet(p.get("title", "")),

    # ── Browser Control ──
    "browser_new_tab":       lambda p: browser_new_tab(p.get("url", "")),
    "browser_close_tab":     lambda p: browser_close_tab(),
    "browser_switch_tab":    lambda p: browser_switch_tab(p.get("direction", "next")),
    "browser_go_to":         lambda p: browser_go_to(p.get("url", "")),
    "browser_search":        lambda p: browser_search(p.get("query", "")),
    "browser_back":          lambda p: browser_back(),
    "browser_forward":       lambda p: browser_forward(),
    "browser_refresh":       lambda p: browser_refresh(),
    "browser_hard_refresh":  lambda p: browser_hard_refresh(),
    "browser_zoom":          lambda p: browser_zoom(p.get("direction", "in"), p.get("amount", 1)),
    "browser_bookmark":      lambda p: browser_bookmark(),
    "browser_fullscreen":    lambda p: browser_fullscreen(),
    "browser_find":          lambda p: browser_find(p.get("text", "")),
    "browser_new_incognito": lambda p: browser_new_incognito(),
    "browser_copy_url":      lambda p: browser_copy_url(),
    "browser_reopen_tab":    lambda p: browser_reopen_tab(),
    "browser_scroll_top":    lambda p: browser_scroll_top(),
    "browser_scroll_bottom": lambda p: browser_scroll_bottom(),

    # ── Social Media ──
    "open_linkedin":    lambda p: open_linkedin(),
    "open_twitter":     lambda p: open_twitter(),
    "open_instagram":   lambda p: open_instagram(),
    "open_github":      lambda p: open_github(p.get("repo", "")),
    "open_slack":       lambda p: open_slack(),
    "open_notion":      lambda p: open_notion(),
    "open_figma":       lambda p: open_figma(),
    "open_zoom_web":    lambda p: open_zoom_web(),
    "open_teams_web":   lambda p: open_teams_web(),

    # ── Maps, Translate, Weather ──
    "open_maps":        lambda p: open_maps(p.get("location", "")),
    "get_directions":   lambda p: get_directions(p.get("origin", ""), p.get("destination", "")),
    "open_translate":   lambda p: open_translate(p.get("text", ""), p.get("from_lang", "en"), p.get("to_lang", "hi")),
    "open_weather":     lambda p: open_weather(p.get("city", "")),

    # ── Conversational ──
    "speak_only":       lambda p: speak_only(),
}


def execute(decision: dict) -> dict:
    """Take a brain decision dict and execute it."""
    tool_name = decision.get("tool", "speak_only")
    params = decision.get("params", {})
    speak_text = decision.get("speak", "Done.")

    print(f"\n⚡ [{tool_name}] {params}")

    tool_fn = TOOL_MAP.get(tool_name)
    if tool_fn:
        try:
            result = tool_fn(params)
            print(f"✅ {result}")
            return {
                "tool": tool_name,
                "result": result,
                "speak_text": speak_text,
                "success": True
            }
        except Exception as e:
            print(f"❌ {tool_name}: {e}")
            return {
                "tool": tool_name,
                "result": str(e),
                "speak_text": f"Something went wrong.",
                "success": False
            }
    else:
        return {
            "tool": "unknown",
            "result": f"Unknown tool: {tool_name}",
            "speak_text": speak_text,
            "success": False
        }
