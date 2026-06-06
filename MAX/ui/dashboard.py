"""
ui/dashboard.py
Beautiful Tkinter dashboard for MAX
No monkey-patching - uses state.last_tool for tool display
"""

import sys
import os
import threading
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    HAS_TK = True
except ImportError:
    HAS_TK = False


DARK_BG      = "#0d0d0f"
PANEL_BG     = "#131318"
CARD_BG      = "#1a1a24"
ACCENT       = "#00f5c4"
ACCENT2      = "#7c3aed"
ACCENT3      = "#f59e0b"
TEXT_PRIMARY = "#f0f0f5"
TEXT_DIM     = "#6b6b80"
SUCCESS      = "#22c55e"
ERROR        = "#ef4444"
WARNING      = "#f59e0b"
BORDER       = "#2a2a3a"

FONT_TITLE   = ("Courier New", 22, "bold")
FONT_HEADING = ("Courier New", 13, "bold")
FONT_BODY    = ("Courier New", 11)
FONT_SMALL   = ("Courier New", 9)
FONT_CODE    = ("Courier New", 10)


def launch_gui():
    if not HAS_TK:
        print("Tkinter not available. Running in terminal mode.")
        return False

    from max import state, process_command, run_voice_loop, check_api_key
    from config import ASSISTANT_NAME, WAKE_WORD, USER_NAME
    from core.logger import get_history

    root = tk.Tk()
    root.title(f"⚡ {ASSISTANT_NAME} — AI Desktop Assistant")
    root.geometry("1000x700")
    root.minsize(800, 600)
    root.configure(bg=DARK_BG)

    # ── Custom styling ──
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TFrame", background=DARK_BG)
    style.configure("Card.TFrame", background=CARD_BG)
    style.configure("TLabel", background=DARK_BG, foreground=TEXT_PRIMARY, font=FONT_BODY)
    style.configure("Heading.TLabel", background=DARK_BG, foreground=ACCENT, font=FONT_HEADING)
    style.configure("Dim.TLabel", background=DARK_BG, foreground=TEXT_DIM, font=FONT_SMALL)
    style.configure("Status.TLabel", background=CARD_BG, foreground=TEXT_PRIMARY, font=FONT_BODY)

    # ══════════════════════════════════════
    #  HEADER
    # ══════════════════════════════════════
    header = tk.Frame(root, bg=PANEL_BG, height=70)
    header.pack(fill="x", pady=(0, 1))
    header.pack_propagate(False)

    tk.Label(header, text="⚡ MAX", font=("Courier New", 20, "bold"),
             bg=PANEL_BG, fg=ACCENT).pack(side="left", padx=20, pady=15)

    tk.Label(header, text="AI Desktop Assistant",
             font=("Courier New", 10), bg=PANEL_BG, fg=TEXT_DIM).pack(side="left", padx=0, pady=20)

    # Live clock
    clock_var = tk.StringVar()
    clock_lbl = tk.Label(header, textvariable=clock_var, font=FONT_CODE,
                          bg=PANEL_BG, fg=ACCENT2)
    clock_lbl.pack(side="right", padx=20)

    def update_clock():
        while True:
            clock_var.set(datetime.now().strftime("  %H:%M:%S  |  %a %d %b %Y  "))
            time.sleep(1)
    threading.Thread(target=update_clock, daemon=True).start()

    # ══════════════════════════════════════
    #  MAIN LAYOUT
    # ══════════════════════════════════════
    main = tk.Frame(root, bg=DARK_BG)
    main.pack(fill="both", expand=True, padx=15, pady=10)

    # Left panel (chat + input)
    left = tk.Frame(main, bg=DARK_BG)
    left.pack(side="left", fill="both", expand=True, padx=(0, 8))

    # Right panel (status + history)
    right = tk.Frame(main, bg=DARK_BG, width=280)
    right.pack(side="right", fill="y")
    right.pack_propagate(False)

    # ── Chat Window ──
    chat_frame = tk.Frame(left, bg=CARD_BG, relief="flat")
    chat_frame.pack(fill="both", expand=True, pady=(0, 8))

    chat_header = tk.Frame(chat_frame, bg=CARD_BG)
    chat_header.pack(fill="x", padx=12, pady=(10, 0))
    tk.Label(chat_header, text="◈  CONVERSATION", font=FONT_HEADING,
             bg=CARD_BG, fg=ACCENT).pack(side="left")

    chat_clear_btn = tk.Button(chat_header, text="CLEAR", font=FONT_SMALL,
                                bg=CARD_BG, fg=TEXT_DIM, relief="flat",
                                cursor="hand2",
                                activebackground=CARD_BG, activeforeground=ACCENT,
                                command=lambda: chat_box.delete(1.0, "end"))
    chat_clear_btn.pack(side="right")

    chat_box = tk.Text(chat_frame, bg=DARK_BG, fg=TEXT_PRIMARY,
                       font=FONT_CODE, wrap="word", relief="flat",
                       insertbackground=ACCENT, state="disabled",
                       selectbackground=ACCENT2)
    chat_box.pack(fill="both", expand=True, padx=12, pady=10)

    # Configure tags
    chat_box.tag_configure("user", foreground=ACCENT3, font=("Courier New", 10, "bold"))
    chat_box.tag_configure("max", foreground=ACCENT, font=("Courier New", 10, "bold"))
    chat_box.tag_configure("tool", foreground=ACCENT2, font=("Courier New", 9))
    chat_box.tag_configure("error", foreground=ERROR, font=("Courier New", 9))
    chat_box.tag_configure("time", foreground=TEXT_DIM, font=("Courier New", 8))
    chat_box.tag_configure("body", foreground=TEXT_PRIMARY, font=FONT_CODE)

    def chat_append(role: str, text: str, tool: str = None):
        chat_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M")
        if role == "user":
            chat_box.insert("end", f"\n[{ts}] ", "time")
            chat_box.insert("end", f"{USER_NAME.upper()}  › ", "user")
        elif role == "max":
            chat_box.insert("end", f"\n[{ts}] ", "time")
            chat_box.insert("end", "MAX › ", "max")
        if tool and tool not in ("speak_only", "unknown"):
            chat_box.insert("end", f"[{tool}] ", "tool")
        chat_box.insert("end", text + "\n", "body")
        chat_box.config(state="disabled")
        chat_box.see("end")

    # ── Input Area ──
    input_frame = tk.Frame(left, bg=CARD_BG)
    input_frame.pack(fill="x", pady=(0, 4))

    input_inner = tk.Frame(input_frame, bg=CARD_BG)
    input_inner.pack(fill="x", padx=12, pady=10)

    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(input_inner, textvariable=cmd_var,
                          bg=DARK_BG, fg=TEXT_PRIMARY,
                          font=FONT_CODE, relief="flat",
                          insertbackground=ACCENT,
                          selectbackground=ACCENT2)
    cmd_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

    def send_command(event=None):
        text = cmd_var.get().strip()
        if not text:
            return
        cmd_var.set("")
        chat_append("user", text)

        def run():
            process_command(text)
            # Use state.last_tool directly — no monkey-patching needed
            tool = state.last_tool
            resp = state.last_response
            root.after(0, lambda: chat_append("max", resp, tool))

        threading.Thread(target=run, daemon=True).start()

    send_btn = tk.Button(input_inner, text="SEND ▶", font=FONT_SMALL,
                          bg=ACCENT, fg=DARK_BG, relief="flat",
                          activebackground="#00d4a8", activeforeground=DARK_BG,
                          cursor="hand2", padx=14, pady=5,
                          command=send_command)
    send_btn.pack(side="right")
    cmd_entry.bind("<Return>", send_command)

    # ══════════════════════════════════════
    #  RIGHT PANEL
    # ══════════════════════════════════════

    # Status card
    status_card = tk.Frame(right, bg=CARD_BG)
    status_card.pack(fill="x", pady=(0, 8))

    tk.Label(status_card, text="◈  STATUS", font=FONT_HEADING,
             bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=12, pady=(10, 6))

    status_dot = tk.Label(status_card, text="●", font=("Courier New", 20),
                           bg=CARD_BG, fg=TEXT_DIM)
    status_dot.pack(padx=12, pady=(0, 4))

    status_text = tk.Label(status_card, text="IDLE", font=FONT_HEADING,
                            bg=CARD_BG, fg=TEXT_DIM)
    status_text.pack(padx=12)

    status_sub = tk.Label(status_card, text="Ready for commands",
                           font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM)
    status_sub.pack(padx=12, pady=(0, 10))

    def update_status(s):
        colors = {
            "idle": (TEXT_DIM, "IDLE", f"Say '{WAKE_WORD}' or type below"),
            "listening": (SUCCESS, "LISTENING", "Speak now..."),
            "thinking": (ACCENT3, "THINKING", "Processing your command..."),
            "speaking": (ACCENT, "SPEAKING", "Max is responding..."),
        }
        mode = s.mode
        color, label, sub = colors.get(mode, (TEXT_DIM, mode.upper(), ""))
        status_dot.config(fg=color)
        status_text.config(text=label, fg=color)
        status_sub.config(text=sub)

    state.on_state_change = lambda s: root.after(0, lambda: update_status(s))

    # Stats card
    stats_card = tk.Frame(right, bg=CARD_BG)
    stats_card.pack(fill="x", pady=(0, 8))

    tk.Label(stats_card, text="◈  SESSION", font=FONT_HEADING,
             bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=12, pady=(10, 6))

    cmd_count_var = tk.StringVar(value="0")
    mode_var = tk.StringVar(value="Text + Voice")
    wake_var = tk.StringVar(value=f"Wake: '{WAKE_WORD}'")

    def make_stat(parent, label, var):
        f = tk.Frame(parent, bg=CARD_BG)
        f.pack(fill="x", padx=12, pady=2)
        tk.Label(f, text=label, font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM, width=14, anchor="w").pack(side="left")
        tk.Label(f, textvariable=var, font=FONT_SMALL, bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left")

    make_stat(stats_card, "Commands:", cmd_count_var)
    make_stat(stats_card, "Mode:", mode_var)
    make_stat(stats_card, "Wake word:", wake_var)
    tk.Frame(stats_card, height=8, bg=CARD_BG).pack()

    def update_stats():
        while True:
            cmd_count_var.set(str(state.command_count))
            time.sleep(1)
    threading.Thread(target=update_stats, daemon=True).start()

    # Quick commands card
    quick_card = tk.Frame(right, bg=CARD_BG)
    quick_card.pack(fill="x", pady=(0, 8))

    tk.Label(quick_card, text="◈  QUICK COMMANDS", font=FONT_HEADING,
             bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=12, pady=(10, 6))

    quick_commands = [
        ("🕐 Time", "what time is it"),
        ("📸 Screenshot", "take a screenshot"),
        ("🔊 Mute", "mute the volume"),
        ("🔍 Google", "open Google"),
        ("📁 Files", "list files on desktop"),
        ("🔋 Battery", "check battery"),
    ]

    def quick_action(cmd):
        cmd_var.set(cmd)
        send_command()

    btn_frame = tk.Frame(quick_card, bg=CARD_BG)
    btn_frame.pack(fill="x", padx=8, pady=(0, 10))

    for i, (label, cmd) in enumerate(quick_commands):
        btn = tk.Button(btn_frame, text=label, font=FONT_SMALL,
                         bg=DARK_BG, fg=TEXT_PRIMARY, relief="flat",
                         cursor="hand2", padx=6, pady=4,
                         activebackground=ACCENT2, activeforeground=TEXT_PRIMARY,
                         command=lambda c=cmd: quick_action(c))
        btn.grid(row=i//2, column=i%2, padx=3, pady=2, sticky="ew")
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    # Controls card
    ctrl_card = tk.Frame(right, bg=CARD_BG)
    ctrl_card.pack(fill="x")

    tk.Label(ctrl_card, text="◈  CONTROLS", font=FONT_HEADING,
             bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=12, pady=(10, 6))

    voice_active = tk.BooleanVar(value=False)
    voice_thread = [None]

    def toggle_voice():
        if not voice_active.get():
            voice_active.set(True)
            voice_btn.config(text="⏹  STOP VOICE", bg=ERROR, fg="white")
            state.running = True
            def run():
                run_voice_loop()
                voice_active.set(False)
                root.after(0, lambda: voice_btn.config(
                    text="🎤 START VOICE", bg=SUCCESS, fg=DARK_BG))
            voice_thread[0] = threading.Thread(target=run, daemon=True)
            voice_thread[0].start()
        else:
            state.running = False
            voice_active.set(False)
            voice_btn.config(text="🎤 START VOICE", bg=SUCCESS, fg=DARK_BG)

    voice_btn = tk.Button(ctrl_card, text="🎤 START VOICE", font=FONT_SMALL,
                           bg=SUCCESS, fg=DARK_BG, relief="flat",
                           cursor="hand2", padx=10, pady=6,
                           activebackground="#16a34a",
                           command=toggle_voice)
    voice_btn.pack(fill="x", padx=12, pady=(0, 4))

    wake_toggle = tk.BooleanVar(value=True)

    def toggle_wake():
        state.wake_mode = wake_toggle.get()

    wake_chk = tk.Checkbutton(ctrl_card, text=f"  Wake word required ('{WAKE_WORD}')",
                               variable=wake_toggle, font=FONT_SMALL,
                               bg=CARD_BG, fg=TEXT_DIM,
                               selectcolor=DARK_BG, activebackground=CARD_BG,
                               activeforeground=TEXT_PRIMARY,
                               command=toggle_wake)
    wake_chk.pack(anchor="w", padx=12, pady=(0, 10))

    # ══════════════════════════════════════
    #  FOOTER
    # ══════════════════════════════════════
    footer = tk.Frame(root, bg=PANEL_BG, height=28)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)

    tk.Label(footer, text="⚡ Powered by Groq + Llama 3.3  |  pyautogui  |  pyttsx3",
             font=FONT_SMALL, bg=PANEL_BG, fg=TEXT_DIM).pack(side="left", padx=12, pady=6)

    tk.Label(footer, text="Press Enter to send  |  Type 'help' for commands",
             font=FONT_SMALL, bg=PANEL_BG, fg=TEXT_DIM).pack(side="right", padx=12, pady=6)

    # ── Initial greeting in chat ──
    from max import _get_time_greeting
    greeting = _get_time_greeting()
    chat_append("max", greeting)
    chat_append("max", f"🎤 Voice mode is active — just say '{WAKE_WORD}' and talk to me!")

    # ── AUTO-START VOICE MODE (hands-free experience) ──
    def auto_start_voice():
        toggle_voice()
    root.after(1500, auto_start_voice)  # Start voice 1.5s after GUI loads

    cmd_entry.focus()
    root.mainloop()
    return True


if __name__ == "__main__":
    launch_gui()
