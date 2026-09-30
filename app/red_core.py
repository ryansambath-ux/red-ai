from datetime import datetime, timezone
from app.tools import ToolRegistry
from app.attention import AttentionEngine

class RedCore:
    def __init__(self):
        self.tools = ToolRegistry()
        self.attention = AttentionEngine()

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

        tool_result = self.tools.try_command(cleaned)
        if tool_result:
            return tool_result

        return {
            "reply": f"I heard: {cleaned}. My reasoning model will be connected in the next build step.",
            "action": "conversation",
        }
