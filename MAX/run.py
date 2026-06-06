"""
run.py
Max launcher — Voice-first AI agent.
Default: Pure voice agent (always listening, no GUI).
Use --gui for dashboard, --text for text mode.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    print("\n" + "="*55)
    print("   ⚡  MAX — Voice AI Agent")
    print("="*55)

    from max import check_api_key, check_dependencies, run_voice_agent, run_text_loop
    from config import ASSISTANT_NAME

    if not check_api_key():
        print("\n📝 Create a .env file with your Groq API key.")
        print("   Get a free key at: https://console.groq.com")
        input("\nPress Enter to exit...")
        return

    # Check deps
    missing = check_dependencies()
    if missing:
        print(f"\n📦 Missing packages: {', '.join(missing)}")
        print(f"   Installing automatically...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing,
                       capture_output=False)
        print("\n✅ Packages installed.\n")

    # --gui  → GUI dashboard with voice toggle
    if "--gui" in sys.argv:
        try:
            import tkinter
            from ui.dashboard import launch_gui
            print("🖥️  Launching GUI dashboard...")
            launch_gui()
        except ImportError:
            print("⚠️  Tkinter not available. Starting voice agent...")
            run_voice_agent()
        except Exception as e:
            print(f"⚠️  GUI failed ({e}). Starting voice agent...")
            run_voice_agent()

    # --text → text mode
    elif "--text" in sys.argv:
        print("💬 Starting in text mode...")
        run_text_loop()

    # DEFAULT → Pure voice agent (always listening)
    else:
        print("🎤 Starting voice agent...")
        run_voice_agent()


if __name__ == "__main__":
    main()
