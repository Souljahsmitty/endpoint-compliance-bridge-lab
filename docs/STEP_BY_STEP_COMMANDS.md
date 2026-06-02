# Step-By-Step Commands To Replicate This Lab

This guide shows how to rebuild a basic version of the endpoint-compliance lab from scratch.

It also shows how to run and test the finished repo.

## What You Are Building

A tiny web app with:

- one Python server
- one HTML page
- fake JAMF-style device inventory
- fake BigFix-style patch status
- one browser dashboard
- one API endpoint you can test with `curl`
- optional Docker packaging

## Part A - Run The Finished Repo

Use this if you already cloned or opened this repo.

### Step 1 - Go To The Project Folder

```bash
cd "/Users/adamsmith/Documents/New project/endpoint-compliance-bridge-lab"
```

What this does:

```text
Moves your terminal into the project folder.
```

### Step 2 - Start The Python Server

```bash
python3 src/server.py
```

What success looks like:

```text
Endpoint Compliance Bridge Lab running at http://127.0.0.1:8080
MOCK_MODE=true
```

Keep this terminal open. The server is running.

### Step 3 - Open The Dashboard

Open another terminal tab, or leave the server running and use this command:

```bash
open http://127.0.0.1:8080
```

What success looks like:

```text
The browser opens the dashboard.
It shows 3 total devices, 2 compliant, 1 needs patch.
```

### Step 4 - Test The API

In another terminal tab:

```bash
curl http://127.0.0.1:8080/api/summary
```

Cleaner version:

```bash
curl http://127.0.0.1:8080/api/summary | python3 -m json.tool
```

What success looks like:

```json
{
  "mode": "mock",
  "counts": {
    "devices": 3,
    "compliant": 2,
    "needs_patch": 1
  }
}
```

### Step 5 - Stop The Server

Go back to the terminal running the server and press:

```text
Control + C
```

That stops the local server.

## Part B - Build A Tiny Version From Scratch

Use this if you want to actually replicate the build manually.

### Step 1 - Create A New Project Folder

```bash
mkdir my-endpoint-lab
cd my-endpoint-lab
mkdir src static
```

What this creates:

```text
my-endpoint-lab/
├── src/
└── static/
```

### Step 2 - Create The HTML Dashboard

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

What this does:

```text
Creates a simple web page that calls /api/summary and displays device rows.
```

### Step 3 - Create The Python Server

```bash
cat > src/server.py <<'PY'
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

JAMF_DEVICES = [
    {
        "name": "macbook-finance-014",
        "platform": "macOS",
        "mdm": "JAMF Pro",
        "os_version": "14.6",
    },
    {
        "name": "macbook-field-022",
        "platform": "macOS",
        "mdm": "JAMF Pro",
        "os_version": "15.1",
    },
    {
        "name": "win-admin-009",
        "platform": "Windows",
        "mdm": "Other/Intune-style",
        "os_version": "11",
    },
]

BIGFIX_PATCH_STATUS = [
    {
        "name": "macbook-finance-014",
        "patch_status": "Compliant",
        "critical_missing": 0,
    },
    {
        "name": "macbook-field-022",
        "patch_status": "Needs Patch",
        "critical_missing": 2,
    },
    {
        "name": "win-admin-009",
        "patch_status": "Compliant",
        "critical_missing": 0,
    },
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

What this does:

```text
Creates fake JAMF device inventory.
Creates fake BigFix patch status.
Combines both by device name.
Serves the dashboard and API.
```

### Step 4 - Run The Tiny Version

```bash
python3 src/server.py
```

What success looks like:

```text
Endpoint lab running at http://127.0.0.1:8080
```

### Step 5 - Open The Tiny Dashboard

```bash
open http://127.0.0.1:8080
```

What success looks like:

```text
A browser page opens and shows 3 devices.
One device needs patch.
```

### Step 6 - Test The Tiny API

```bash
curl http://127.0.0.1:8080/api/summary | python3 -m json.tool
```

What success looks like:

```text
mode = mock
devices = 3
compliant = 2
needs_patch = 1
```

### Step 7 - Stop The Tiny Server

Press:

```text
Control + C
```

## Part C - Add Docker

Docker is optional. It packages the app so it can run in a container.

### Step 1 - Create A Dockerfile

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

### Step 2 - Build The Docker Image

```bash
docker build -t my-endpoint-lab .
```

What success looks like:

```text
Successfully built ...
Successfully tagged my-endpoint-lab:latest
```

If this fails with Docker daemon errors, start Docker Desktop first.

### Step 3 - Run The Docker Container

```bash
docker run --rm -p 8080:8080 my-endpoint-lab
```

### Step 4 - Open The Docker Version

```bash
open http://127.0.0.1:8080
```

### Step 5 - Test The Docker API

```bash
curl http://127.0.0.1:8080/api/summary | python3 -m json.tool
```

## Part D - GitHub Commands

Use these only after you are inside your project folder.

### Step 1 - Initialize Git

```bash
git init
```

### Step 2 - Add Files

```bash
git add .
```

### Step 3 - Commit Files

```bash
git commit -m "Create endpoint compliance lab"
```

### Step 4 - Create A GitHub Repo With GitHub CLI

```bash
gh repo create my-endpoint-lab --public --source=. --remote=origin --push
```

What success looks like:

```text
A public GitHub repo is created and your code is pushed.
```

## Part E - Truthful Resume Line

After building this, you can truthfully say:

```text
Built a local endpoint-compliance dashboard that models JAMF-style device inventory and BigFix-style patch status, using Python, HTML, mock data, API testing, Git, GitHub, and optional Docker packaging.
```

Do not say:

```text
I administered JAMF Pro and BigFix in production for years.
```
