#!/usr/bin/env python3
"""
Tricot R&D Platform — Desktop Launcher
Serves the app locally and opens it in your default browser as a full-screen window.
Works on Windows, macOS, and Linux with Python 3.6+
"""

import os
import sys
import time
import socket
import threading
import webbrowser
import subprocess
import http.server
import socketserver

APP_TITLE = "Tricot R&D Platform"
APP_FILE  = "TricotRD.html"

# ── Find a free port ──────────────────────────────────────
def free_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# ── Tiny static file server ───────────────────────────────
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass   # silence request logs

def serve(port, directory):
    os.chdir(directory)
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        httpd.serve_forever()

# ── Try to open a proper app window ──────────────────────
def open_window(url):
    """Try platform-specific windowed modes, fall back to default browser."""
    system = sys.platform

    # ── macOS: open as standalone app window via open -a ──
    if system == "darwin":
        # Try Chrome app mode
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
        for c in chrome_paths:
            if os.path.exists(c):
                subprocess.Popen([c, f"--app={url}", "--window-size=1400,900",
                                  f"--window-position=100,50",
                                  "--disable-extensions", "--no-first-run",
                                  f"--user-data-dir=/tmp/tricot_rd_chrome"])
                return
        # Try Safari / default
        subprocess.Popen(["open", url])
        return

    # ── Windows: Chrome/Edge app mode ─────────────────────
    if system == "win32":
        win_browsers = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        for b in win_browsers:
            if os.path.exists(b):
                subprocess.Popen([b, f"--app={url}", "--window-size=1440,900",
                                  "--disable-extensions", "--no-first-run",
                                  f"--user-data-dir={os.path.expanduser('~')}\\AppData\\Local\\TricotRD"])
                return
        os.startfile(url)
        return

    # ── Linux: Chrome/Chromium app mode ───────────────────
    for b in ["google-chrome", "chromium", "chromium-browser", "brave-browser"]:
        try:
            subprocess.Popen([b, f"--app={url}", "--window-size=1400,900",
                               "--disable-extensions", "--no-first-run",
                               "--user-data-dir=/tmp/tricot_rd_chrome"])
            return
        except FileNotFoundError:
            continue
    # Fallback
    webbrowser.open(url)

# ── Main ──────────────────────────────────────────────────
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, APP_FILE)

    if not os.path.exists(html_path):
        print(f"ERROR: {APP_FILE} not found in {base_dir}")
        input("Press Enter to exit...")
        sys.exit(1)

    port = free_port()
    url  = f"http://127.0.0.1:{port}/{APP_FILE}"

    print(f"{'='*50}")
    print(f"  {APP_TITLE}")
    print(f"{'='*50}")
    print(f"  Starting local server on port {port}...")

    # Start server in background thread
    t = threading.Thread(target=serve, args=(port, base_dir), daemon=True)
    t.start()
    time.sleep(0.6)   # brief pause for server to bind

    print(f"  Opening: {url}")
    print(f"  Keep this window open while using the app.")
    print(f"  Press Ctrl+C to quit.\n")

    open_window(url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTricot R&D Platform closed. Goodbye!")

if __name__ == "__main__":
    main()
