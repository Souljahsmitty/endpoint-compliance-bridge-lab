# Replicate A Simple Version

This is the ADHD-friendly build path. Do one step at a time.

## Goal

Make a tiny web page that shows endpoint compliance data.

## Step 1 - Create A Folder

```bash
mkdir my-endpoint-lab
cd my-endpoint-lab
mkdir src static
```

## Step 2 - Create A Basic HTML File

Create `static/index.html`:

```html
<!doctype html>
<html>
  <body>
    <h1>Endpoint Lab</h1>
    <div id="output">Loading...</div>
    <script>
      fetch('/api/summary')
        .then(r => r.json())
        .then(data => {
          document.getElementById('output').textContent =
            JSON.stringify(data, null, 2);
        });
    </script>
  </body>
</html>
```

## Step 3 - Create A Tiny Python Server

Create `src/server.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/summary':
            data = {'devices': 3, 'needs_patch': 1}
            body = json.dumps(data).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        html = open('static/index.html', 'rb').read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html)

HTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
```

Run it:

```bash
python3 src/server.py
```

Open:

```text
http://localhost:8080
```

## Step 4 - Add Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY src ./src
COPY static ./static
EXPOSE 8080
CMD ["python", "src/server.py"]
```

Build:

```bash
docker build -t my-endpoint-lab .
```

Run:

```bash
docker run --rm -p 8080:8080 my-endpoint-lab
```

Open:

```text
http://localhost:8080
```

## Step 5 - Add JAMF/BigFix Vocabulary

Add fake data like:

```json
[
  {"name": "macbook-001", "mdm": "JAMF Pro", "patch_status": "Compliant"},
  {"name": "windows-009", "mdm": "Intune-style", "patch_status": "Needs Patch"}
]
```

Then explain:

"This is mock data shaped like endpoint inventory and patch status. In a real lab, the same structure would be populated by JAMF Pro and BigFix API calls."

## Truth Check

After doing this, you can say:

"I built a simple Dockerized HTML/Python dashboard that models endpoint compliance data and helped me understand the JAMF/BigFix integration pattern."

Do not say:

"I administered JAMF and BigFix for years."
