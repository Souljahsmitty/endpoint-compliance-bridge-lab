from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import sys

from integrations.bigfix import BigFixClient
from integrations.jamf import JamfClient


ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "static"


def build_summary():
    jamf = JamfClient.from_env()
    bigfix = BigFixClient.from_env()

    jamf_devices = jamf.fetch_devices()
    bigfix_devices = bigfix.fetch_patch_summary()

    by_name = {}
    for device in jamf_devices:
        by_name.setdefault(device["name"], {}).update(device)
    for device in bigfix_devices:
        by_name.setdefault(device["name"], {}).update(device)

    devices = list(by_name.values())
    compliant = sum(1 for d in devices if d.get("patch_status") == "Compliant")
    needs_patch = sum(1 for d in devices if d.get("patch_status") == "Needs Patch")

    return {
        "mode": "mock" if jamf.mock_mode or bigfix.mock_mode else "live",
        "counts": {
            "devices": len(devices),
            "compliant": compliant,
            "needs_patch": needs_patch,
        },
        "devices": devices,
        "notes": [
            "Mock mode is safe for portfolio demos.",
            "Live mode requires real JAMF Pro and BigFix credentials.",
            "This project demonstrates integration structure, not production admin tenure.",
        ],
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type="application/json"):
        encoded = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/api/summary":
            try:
                self._send(200, json.dumps(build_summary(), indent=2))
            except Exception as exc:
                payload = {"error": str(exc), "hint": "Use MOCK_MODE=true unless real lab credentials are configured."}
                self._send(500, json.dumps(payload, indent=2))
            return

        target = STATIC_DIR / "index.html"
        if self.path not in ("/", "/index.html"):
            self._send(404, "Not found", "text/plain")
            return
        self._send(200, target.read_bytes(), "text/html; charset=utf-8")

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Endpoint Compliance Bridge Lab running at http://{host}:{port}")
    print(f"MOCK_MODE={os.getenv('MOCK_MODE', 'true')}")
    server.serve_forever()


if __name__ == "__main__":
    main()
