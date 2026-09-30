import json, os, uuid
from datetime import datetime, timezone
from pathlib import Path

class EventStore:
    def __init__(self,path=None):
        self.path=Path(path or os.getenv("RED_EVENT_FILE","data/events.json"));self.path.parent.mkdir(parents=True,exist_ok=True)
        if not self.path.exists():self.path.write_text('{"events":[]}',encoding="utf-8")
    def _load(self):
        try:return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:return {"events":[]}
    def _save(self,d):self.path.write_text(json.dumps(d,indent=2),encoding="utf-8")
    def add(self,kind,message,level="remember",data=None):
        d=self._load();e={"id":str(uuid.uuid4()),"kind":kind,"message":message,"level":level,"data":data or {},
        "read":False,"created_at":datetime.now(timezone.utc).isoformat()};d["events"].append(e);self._save(d);return e
    def unread(self):
        return [e for e in self._load()["events"] if not e["read"]]
    def mark_read(self,event_id):
        d=self._load()
        for e in d["events"]:
            if e["id"]==event_id:e["read"]=True;self._save(d);return e
