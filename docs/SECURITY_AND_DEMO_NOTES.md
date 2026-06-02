# Security And Demo Notes

## Safe Demo Rule

This repo is safe to demo because it runs in mock mode by default.

Mock mode means:

- no real JAMF tenant is contacted
- no real BigFix server is contacted
- no real device inventory is pulled
- no real passwords are needed
- no real tokens are printed
- no remediation actions are performed

## What Not To Put In A Video

Do not record or publish:

- real JAMF tenant URLs
- real JAMF client IDs
- real JAMF client secrets
- real BigFix usernames
- real BigFix passwords
- real bearer tokens
- real agency/company device names
- screenshots from a live customer or employer tenant
- any `.env` file

## What Is Safe To Show

Safe video/demo content:

```bash
python3 src/server.py
open http://127.0.0.1:8080
curl http://127.0.0.1:8080/api/summary
```

Safe dashboard values:

```text
mode: mock
devices: 3
compliant: 2
needs_patch: 1
```

Safe fake device names:

```text
macbook-finance-014
macbook-field-022
win-admin-009
```

## How Secrets Would Work In A Real Lab

Use environment variables, not hard-coded values:

```bash
export MOCK_MODE=false
export JAMF_BASE_URL="https://example.jamfcloud.com"
export JAMF_CLIENT_ID="example-client-id"
export JAMF_CLIENT_SECRET="example-client-secret"
export BIGFIX_BASE_URL="https://example-bigfix-server:52311"
export BIGFIX_USERNAME="example-user"
export BIGFIX_PASSWORD="example-password"
```

The values above are placeholders. Do not use real values in a public repo or video.

## Why `.env` Is Ignored

`.gitignore` includes:

```text
.env
```

That helps prevent accidental commits of local secrets.

## Demo Scope

This project includes:

- mock mode
- API client structure
- environment-variable configuration
- endpoint inventory vocabulary
- patch/compliance reporting shape
- local testing
- Docker packaging structure
