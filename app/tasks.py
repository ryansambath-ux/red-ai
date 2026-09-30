import json
from datetime import datetime, timezone
from pathlib import Path
import os
import uuid

class TaskStore:
    def __init__(self, path=None):
        self.path = Path(path or os.getenv("RED_TASK_FILE", "data/tasks.json"))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text('{"tasks":[]}', encoding="utf-8")

    def _load(self):
        try: return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception: return {"tasks":[]}

    def _save(self, data):
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(self, text, due=None):
        data=self._load()
        item={"id":str(uuid.uuid4()),"text":text,"due":due,"done":False,
              "created_at":datetime.now(timezone.utc).isoformat()}
        data["tasks"].append(item); self._save(data); return item

    def list(self):
        return self._load()["tasks"]
