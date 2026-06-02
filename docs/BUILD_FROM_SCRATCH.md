# Build From Scratch

This builds a small version of the lab manually.

## Step 1 - Create Folders

```bash
mkdir my-endpoint-lab
cd my-endpoint-lab
mkdir src static
```

## Step 2 - Create The HTML Page

```bash
cat > static/index.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Endpoint Lab</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 32px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background: #eef2f7; }
    .ok { color: green; font-weight: bold; }
    .warn { color: darkorange; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Endpoint Compliance Lab</h1>
  <p id="counts">Loading...</p>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Platform</th>
        <th>MDM</th>
        <th>Patch Status</th>
        <th>Critical Missing</th>
      </tr>
    </thead>
    <tbody id="rows"></tbody>
  </table>

  <script>
    fetch('/api/summary')
      .then(response => response.json())
      .then(data => {
        document.getElementById('counts').textContent =
          `${data.counts.devices} devices | ${data.counts.compliant} compliant | ${data.counts.needs_patch} needs patch`;

        const rows = document.getElementById('rows');
        for (const device of data.devices) {
          const statusClass = device.patch_status === 'Compliant' ? 'ok' : 'warn';
          rows.innerHTML += `<tr>
            <td>${device.name}</td>
            <td>${device.platform}</td>
            <td>${device.mdm}</td>
            <td class="${statusClass}">${device.patch_status}</td>
            <td>${device.critical_missing}</td>
          </tr>`;
        }
      });
  </script>
</body>
</html>
HTML
```

## Step 3 - Create The Python Server

```bash
cat > src/server.py <<'PY'
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

JAMF_DEVICES = [
    {"name": "macbook-finance-014", "platform": "macOS", "mdm": "JAMF Pro"},
    {"name": "macbook-field-022", "platform": "macOS", "mdm": "JAMF Pro"},
    {"name": "win-admin-009", "platform": "Windows", "mdm": "Other/Intune-style"},
]

BIGFIX_PATCH_STATUS = [
    {"name": "macbook-finance-014", "patch_status": "Compliant", "critical_missing": 0},
    {"name": "macbook-field-022", "patch_status": "Needs Patch", "critical_missing": 2},
    {"name": "win-admin-009", "patch_status": "Compliant", "critical_missing": 0},
]

def build_summary():
    by_name = {}
    for device in JAMF_DEVICES:
        by_name.setdefault(device["name"], {}).update(device)
    for device in BIGFIX_PATCH_STATUS:
        by_name.setdefault(device["name"], {}).update(device)

    devices = list(by_name.values())
    compliant = sum(1 for d in devices if d.get("patch_status") == "Compliant")
    needs_patch = sum(1 for d in devices if d.get("patch_status") == "Needs Patch")

    return {
        "mode": "mock",
        "counts": {
            "devices": len(devices),
            "compliant": compliant,
            "needs_patch": needs_patch,
        },
        "devices": devices,
    }

class Handler(BaseHTTPRequestHandler):
    def send_text(self, status, body, content_type):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/summary":
            self.send_text(200, json.dumps(build_summary(), indent=2), "application/json")
            return
        if self.path in ("/", "/index.html"):
            with open("static/index.html", "r", encoding="utf-8") as file:
                self.send_text(200, file.read(), "text/html")
            return
        self.send_text(404, "Not found", "text/plain")

print("Endpoint lab running at http://127.0.0.1:8080")
HTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
PY
```

## Step 4 - Run It

```bash
python3 src/server.py
```

## Step 5 - Open It

```bash
open http://127.0.0.1:8080
```

## Step 6 - Test The API

```bash
curl http://127.0.0.1:8080/api/summary | python3 -m json.tool
```

Expected result:

```text
mode: mock
devices: 3
compliant: 2
needs_patch: 1
```

## Step 7 - Add Docker

```bash
cat > Dockerfile <<'DOCKER'
FROM python:3.12-slim
WORKDIR /app
COPY src ./src
COPY static ./static
EXPOSE 8080
CMD ["python", "src/server.py"]
DOCKER
```

Build:

```bash
docker build -t my-endpoint-lab .
```

Run:

```bash
docker run --rm -p 8080:8080 my-endpoint-lab
```

Docker Desktop must be running for the Docker commands to work.
