"""
Web UI: python app.py  ->  open http://localhost:8000
Requires LM Studio running its local server (default http://localhost:1234).
"""
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from datetime import datetime

from agents import DISCLAIMER, JURISDICTIONS, Case, build_report, run_case

HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")
CONFIG = {"lm_url": "http://localhost:1234", "model": None}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = HTML.replace("__JURIS__", json.dumps(list(JURISDICTIONS))) \
                       .replace("__DISCLAIMER__", DISCLAIMER).encode()
            self._send(200, "text/html; charset=utf-8", body)
        else:
            self._send(404, "text/plain", b"not found")

    def do_POST(self):
        if self.path != "/analyse":
            return self._send(404, "text/plain", b"not found")
        data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if not data.get("charges", "").strip():
            return self._send(400, "text/plain", b"charges required")
        case = Case(**{k: str(data.get(k, "")) for k in
                       ("charges", "jurisdiction", "location", "facts", "age", "priors")})

        # Stream newline-delimited JSON, one line per finished agent.
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.end_headers()

        def emit(obj):
            self.wfile.write((json.dumps(obj) + "\n").encode())
            self.wfile.flush()

        try:
            result = run_case(case, CONFIG["lm_url"], CONFIG["model"],
                              on_step=lambda n, t: emit({"agent": n, "output": t}))
            report = build_report(case, result)
            path = Path(__file__).parent / "reports" / f"defence_report_{datetime.now():%Y%m%d_%H%M%S}.md"
            path.parent.mkdir(exist_ok=True)
            path.write_text(report, encoding="utf-8")
            emit({"done": True, "model": result["model"], "report": report, "saved": str(path)})
        except Exception as e:
            emit({"error": f"Could not reach LM Studio at {CONFIG['lm_url']}: {e}"})

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--lm-studio-url", default="http://localhost:1234")
    p.add_argument("--model", default=None, help="LM Studio model id (auto-detected)")
    a = p.parse_args()
    CONFIG.update(lm_url=a.lm_studio_url, model=a.model)
    print(f"Open http://localhost:{a.port}  (LM Studio: {a.lm_studio_url})")
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()
