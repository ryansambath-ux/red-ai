import json
import os
import urllib.request
from datetime import datetime, timezone

class MonitorEngine:
    def __init__(self, attention):
        self.attention = attention

    def website(self, url: str):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RedAI/0.4"})
            with urllib.request.urlopen(req, timeout=15) as r:
                status = r.status
            ok = 200 <= status < 400
            return {"ok": ok, "kind": "website", "url": url, "status": status,
                    "attention": "remember" if ok else "notify",
                    "checked_at": datetime.now(timezone.utc).isoformat()}
        except Exception as exc:
            return {"ok": False, "kind": "website", "url": url, "error": str(exc),
                    "attention": "notify", "checked_at": datetime.now(timezone.utc).isoformat()}

    def configured_targets(self):
        raw = os.getenv("RED_WATCH_URLS", "")
        return [u.strip() for u in raw.split(",") if u.strip()]

    def run(self):
        return [self.website(url) for url in self.configured_targets()]
