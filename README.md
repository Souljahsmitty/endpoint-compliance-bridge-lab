# Endpoint Compliance Bridge Lab

A small, truthful portfolio project that demonstrates the structure of a JAMF Pro + BigFix endpoint-compliance integration without claiming production administration experience.

The app runs a local HTML dashboard. By default it uses mock data. If real lab credentials are provided, the same client structure can call JAMF Pro and BigFix REST APIs.

## What This Proves

- I understand the basic job of JAMF Pro: Apple/macOS device inventory and management data.
- I understand the basic job of BigFix: endpoint inventory, patch, and compliance data.
- I can structure API clients, environment variables, mock mode, Docker, and a simple HTML dashboard.
- I can document the difference between "built a lab integration" and "administered JAMF/BigFix in production."

## What This Does Not Prove

- It does not prove years of JAMF Pro administration.
- It does not prove years of BigFix administration.
- It does not prove access to an enterprise tenant.
- It does not prove production patch authority.

Truthful resume phrasing:

> Built a Dockerized endpoint-compliance lab that models JAMF Pro and BigFix API integration patterns, normalizes mock device/patch data, and presents a simple HTML compliance dashboard.

Truthful interview phrasing:

> I have not been a dedicated JAMF or BigFix administrator yet. I built a lab project to understand the API shape, authentication flow, device inventory concepts, patch-compliance reporting pattern, Docker packaging, and the kind of documentation an endpoint team would expect.

## Quick Start

These commands run this finished repo. They are not the full from-scratch build path.

For the from-scratch build path, read:

```text
docs/REPLICATE_SIMPLE_PROJECT.md
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
│   ├── ADHD_JOB_APPLICATION_BRIEF.md
│   ├── FEYNMAN_EXPLANATION.md
│   ├── FLASHCARDS.md
│   ├── GLOSSARY_AND_BASIC_TEST.md
│   ├── REAL_WORLD_USE_CASE.md
│   ├── REPLICATE_SIMPLE_PROJECT.md
│   ├── REVERSE_ENGINEER_MAP.md
│   ├── SOURCES.md
│   └── TRUTHFUL_TALKING_POINTS.md
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
