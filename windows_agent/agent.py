import os
import subprocess
import webbrowser
from pathlib import Path

# Red Windows Agent 0.1.
# Only explicit allow-listed actions are exposed.
ALLOWED_APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "file explorer": ["explorer.exe"],
    "chrome": ["cmd", "/c", "start", "chrome"],
}

def open_app(name: str):
    key = name.strip().lower()
    command = ALLOWED_APPS.get(key)
    if not command:
        return {"ok": False, "error": "Application is not allow-listed."}
    subprocess.Popen(command)
    return {"ok": True, "action": "open_app", "app": key}

def open_website(url: str):
    if not url.startswith(("https://", "http://")):
        return {"ok": False, "error": "Only HTTP/HTTPS URLs are allowed."}
    webbrowser.open(url)
    return {"ok": True, "action": "open_website"}

def find_file(filename: str, roots=None, limit=20):
    roots = roots or [Path.home() / "Documents", Path.home() / "Downloads"]
    target = filename.lower()
    matches = []
    for root in roots:
        if not root.exists():
            continue
        for base, _, files in os.walk(root):
            for file in files:
                if target in file.lower():
                    matches.append(str(Path(base) / file))
                    if len(matches) >= limit:
                        return matches
    return matches
