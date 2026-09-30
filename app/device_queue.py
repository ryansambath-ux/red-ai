import json, os, uuid
from datetime import datetime, timezone
from pathlib import Path

class DeviceQueue:
    def __init__(self, path=None):
        self.path=Path(path or os.getenv("RED_DEVICE_QUEUE_FILE","data/device_queue.json"))
        self.path.parent.mkdir(parents=True,exist_ok=True)
        if not self.path.exists(): self.path.write_text('{"commands":[]}',encoding="utf-8")
    def _load(self):
        try:return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:return {"commands":[]}
    def _save(self,d):self.path.write_text(json.dumps(d,indent=2),encoding="utf-8")
    def enqueue(self,action,args=None):
        d=self._load(); item={"id":str(uuid.uuid4()),"action":action,"args":args or {},
        "status":"pending","created_at":datetime.now(timezone.utc).isoformat()}
        d["commands"].append(item);self._save(d);return item
    def next(self):
        d=self._load()
        for c in d["commands"]:
            if c["status"]=="pending": return c
        return None
    def complete(self,command_id,result):
        d=self._load()
        for c in d["commands"]:
            if c["id"]==command_id:
                c["status"]="complete";c["result"]=result;c["completed_at"]=datetime.now(timezone.utc).isoformat()
                self._save(d);return c
        return None
