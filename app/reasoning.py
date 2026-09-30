import os
import json
import urllib.request
import urllib.error

class ReasoningEngine:
    """Provider adapter for Red's reasoning model.

    Secrets are never returned by diagnostics. Environment values are read
    at request time so a Cloud Run revision always reflects its runtime config.
    """

    @staticmethod
    def _config():
        return {
            "base_url": os.getenv("AI_BASE_URL", "").strip().rstrip("/"),
            "api_key": os.getenv("AI_API_KEY", "").strip(),
            "model": os.getenv("AI_MODEL", "").strip(),
        }

    @property
    def configured(self):
        c = self._config()
        return bool(c["base_url"] and c["api_key"] and c["model"])

    def diagnostics(self):
        c = self._config()
        return {
            "configured": bool(c["base_url"] and c["api_key"] and c["model"]),
            "AI_BASE_URL": bool(c["base_url"]),
            "AI_MODEL": bool(c["model"]),
            "AI_API_KEY": bool(c["api_key"]),
            "model": c["model"] or None,
            "base_url": c["base_url"] or None,
        }

    def respond(self, message: str, memories=None):
        c = self._config()
        if not (c["base_url"] and c["api_key"] and c["model"]):
            missing = [
                name for name, value in (
                    ("AI_BASE_URL", c["base_url"]),
                    ("AI_MODEL", c["model"]),
                    ("AI_API_KEY", c["api_key"]),
                ) if not value
            ]
            return {
                "reply": "My reasoning model is not configured yet. Missing: " + ", ".join(missing),
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
            "model": c["model"],
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
        }).encode("utf-8")

        request = urllib.request.Request(
            c["base_url"] + "/chat/completions",
            data=payload,
            headers={
                "Authorization": "Bearer " + c["api_key"],
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
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:1000]
            return {
                "reply": "My reasoning service is configured but the AI provider rejected the request.",
                "action": "reasoning_error",
                "error": f"HTTP {exc.code}: {body}",
            }
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
            return {"reply": "My reasoning service is unavailable.", "action": "reasoning_error", "error": str(exc)}
