import json
import os
from datetime import datetime, timezone
from pathlib import Path

class MemoryStore:
    """Simple local JSON memory for development. Cloud persistence comes next."""
    def __init__(self, path: str | None = None):
        self.path = Path(path or os.getenv("RED_MEMORY_FILE", "data/memory.json"))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"memories": []})

    def _read(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"memories": []}

    def _write(self, data):
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def remember(self, text: str, category: str = "general"):
        data = self._read()
        item = {
            "text": text.strip(),
            "category": category,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        data["memories"].append(item)
        self._write(data)
        return item

    def recent(self, limit: int = 10):
        return self._read()["memories"][-limit:]
