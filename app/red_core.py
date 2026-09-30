from datetime import datetime, timezone
from app.tools import ToolRegistry
from app.attention import AttentionEngine
from app.memory import MemoryStore

class RedCore:
    def __init__(self):
        self.tools = ToolRegistry()
        self.attention = AttentionEngine()
        self.memory = MemoryStore()

    def handle(self, text: str):
        cleaned = text.strip()
        if not cleaned:
            return {"reply": "I'm listening.", "action": None}

        lower = cleaned.lower()
        if lower in {"status", "red status", "are you there"}:
            return {
                "reply": "Red is online.",
                "action": "status",
                "time": datetime.now(timezone.utc).isoformat(),
            }

        if lower.startswith("remember "):
            item = self.memory.remember(cleaned[9:])
            return {"reply": "Remembered.", "action": "remember", "memory": item}

        if lower in {"what do you remember", "recent memories"}:
            return {
                "reply": "Here are my recent memories.",
                "action": "memory",
                "memories": self.memory.recent(),
            }

        tool_result = self.tools.try_command(cleaned)
        if tool_result:
            return tool_result

        return {
            "reply": f"I heard: {cleaned}. My reasoning model will be connected next.",
            "action": "conversation",
        }
