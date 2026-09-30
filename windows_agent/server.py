import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from app.device_auth import verify
from windows_agent.agent import open_app, open_website, find_file

HOST = "127.0.0.1"
PORT = 8765

class Handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            return self._json(200, {"ok": True, "agent": "red-windows"})
        self._json(404, {"ok": False})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        timestamp = self.headers.get("X-Red-Timestamp", "")
        signature = self.headers.get("X-Red-Signature", "")
        if not verify(timestamp, body, signature):
            return self._json(401, {"ok": False, "error": "Invalid device signature."})
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return self._json(400, {"ok": False, "error": "Invalid JSON."})

        if self.path == "/action/open-app":
            return self._json(200, open_app(payload.get("name", "")))
        if self.path == "/action/open-website":
            return self._json(200, open_website(payload.get("url", "")))
        if self.path == "/action/find-file":
            return self._json(200, {"ok": True, "matches": find_file(payload.get("name", ""))})
        return self._json(404, {"ok": False, "error": "Unknown action."})

if __name__ == "__main__":
    print(f"Red Windows Agent listening locally on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
