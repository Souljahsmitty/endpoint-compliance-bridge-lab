# Run And Test

These commands run the finished project locally.

## Step 1 - Open The Project Folder

```bash
cd "/Users/adamsmith/Documents/New project/endpoint-compliance-bridge-lab"
```

## Step 2 - Start The Server

```bash
python3 src/server.py
```

Expected output:

```text
Endpoint Compliance Bridge Lab running at http://127.0.0.1:8080
MOCK_MODE=true
```

Keep this terminal open while testing.

## Step 3 - Open The Dashboard

In another terminal:

```bash
open http://127.0.0.1:8080
```

Expected dashboard:

```text
Total devices: 3
Compliant: 2
Needs patch: 1
Mode: mock
```

## Step 4 - Test The API

```bash
curl http://127.0.0.1:8080/api/summary
```

Pretty-printed version:

```bash
curl http://127.0.0.1:8080/api/summary | python3 -m json.tool
```

Expected JSON shape:

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

## Step 5 - Stop The Server

Return to the server terminal and press:

```text
Control + C
```
