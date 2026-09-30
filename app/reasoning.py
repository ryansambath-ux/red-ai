import os
import json
import urllib.request
import urllib.error

class ReasoningEngine:
    """Provider adapter for Red's reasoning model.

    No API key is stored in source. The initial adapter supports any
    OpenAI-compatible chat endpoint configured through environment variables.
    """

    def __init__(self):
        self.base_url = os.getenv("AI_BASE_URL", "").rstrip("/")
        self.api_key = os.getenv("AI_API_KEY", "")
        self.model = os.getenv("AI_MODEL", "")

    @property
    def configured(self):
        return bool(self.base_url and self.api_key and self.model)

    def respond(self, message: str, memories=None):
        if not self.configured:
            return {
                "reply": "My reasoning model is not configured yet.",
                "action": "reasoning_unconfigured",
            }

        memory_text = "\n".join(
            f"- {m.get('text', '')}" for m in (memories or [])[-10:]
        )
        system = (
            "You are Red, a practical personal AI assistant. Be concise and useful. "
            "Never claim an action succeeded unless a tool result confirms it. "
            "Ask for confirmation before consequential or critical actions."
        )
        if memory_text:
            system += "\nRelevant recent memory:\n" + memory_text

        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
        }).encode("utf-8")

        request = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=payload,
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode("utf-8"))
            return {
                "reply": data["choices"][0]["message"]["content"],
                "action": "reasoning",
            }
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
            return {"reply": "My reasoning service is unavailable.", "action": "reasoning_error", "error": str(exc)}
