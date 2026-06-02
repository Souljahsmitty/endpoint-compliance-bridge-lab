# Endpoint Compliance Bridge Lab

A small local dashboard that demonstrates a JAMF Pro + BigFix endpoint-compliance reporting pattern with mock data.

The app runs a local HTML dashboard. By default it uses mock data. If real lab credentials are provided, the same client structure can call JAMF Pro and BigFix REST APIs.

## What It Shows

- JAMF-style macOS inventory data
- BigFix-style patch/compliance data
- normalized endpoint summary data
- a local HTML dashboard
- a JSON API endpoint
- Docker packaging
- mock-mode security hygiene

## Quick Start

These commands run this finished repo. They are not the full from-scratch build path.

For the full command-by-command build path, read:

```text
docs/BUILD_FROM_SCRATCH.md
```

For the run and test commands, read:

```text
docs/RUN_AND_TEST.md
```

Run locally:

```bash
python3 src/server.py
```

Open:

```text
http://localhost:8080
```

Run with Docker:

```bash
docker build -t endpoint-compliance-bridge-lab .
docker run --rm -p 8080:8080 endpoint-compliance-bridge-lab
```

## Optional Real API Configuration

Mock mode is on by default.

```bash
export MOCK_MODE=false
export JAMF_BASE_URL="https://your-company.jamfcloud.com"
export JAMF_CLIENT_ID="your-client-id"
export JAMF_CLIENT_SECRET="your-client-secret"
export BIGFIX_BASE_URL="https://your-bigfix-server:52311"
export BIGFIX_USERNAME="your-username"
export BIGFIX_PASSWORD="your-password"
python3 src/server.py
```

Never commit real secrets. Use environment variables.

## Official Docs Used

- JAMF Pro API overview: https://developer.jamf.com/jamf-pro/
- JAMF client credentials: https://developer.jamf.com/jamf-pro/docs/client-credentials
- BigFix REST API: https://developer.bigfix.com/rest-api/
- BigFix query API: https://developer.bigfix.com/rest-api/api/query.html

## Project Structure

```text
endpoint-compliance-bridge-lab/
├── Dockerfile
├── README.md
├── docs/
│   ├── BUILD_FROM_SCRATCH.md
│   ├── PROJECT_OVERVIEW.md
│   ├── REAL_WORLD_USE_CASE.md
│   ├── REVERSE_ENGINEER_MAP.md
│   ├── RUN_AND_TEST.md
│   ├── SECURITY_AND_DEMO_NOTES.md
│   ├── SOURCES.md
│   └── working-dashboard.png
├── src/
│   ├── server.py
│   └── integrations/
│       ├── bigfix.py
│       └── jamf.py
└── static/
    └── index.html
```

## One-Sentence Architecture

Browser -> local Python server -> JAMF client + BigFix client -> normalized JSON -> HTML compliance dashboard.
