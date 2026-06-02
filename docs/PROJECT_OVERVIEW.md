# Project Overview

Endpoint Compliance Bridge Lab is a small local dashboard that combines endpoint inventory and patch-status data into one view.

## Core Terms

### JAMF Pro

JAMF Pro is commonly used to manage Apple/macOS devices. In this project, the JAMF-style client provides mock Mac inventory data.

Project file:

```text
src/integrations/jamf.py
```

### BigFix

BigFix is commonly used for endpoint inventory, patch, and compliance reporting. In this project, the BigFix-style client provides mock patch status data.

Project file:

```text
src/integrations/bigfix.py
```

### Endpoint

An endpoint is a managed computer, such as a MacBook, Windows laptop, desktop, or field workstation.

### Compliance

Compliance is whether a device meets a required rule. This lab uses a simple patch-status rule:

```text
Compliant
Needs Patch
```

### Integration

Integration means combining data from more than one system into a single workflow. This project combines JAMF-style inventory and BigFix-style patch status, then shows the result in one dashboard.

## Local Demo Data

The project uses mock data by default:

```text
macbook-finance-014  macOS    JAMF Pro             Compliant
macbook-field-022    macOS    JAMF Pro             Needs Patch
win-admin-009        Windows  Other/Intune-style   Compliant
```

Expected summary:

```text
Total devices: 3
Compliant: 2
Needs patch: 1
```

## Architecture

```text
Browser
  -> static/index.html
  -> Python server at src/server.py
  -> JAMF-style client at src/integrations/jamf.py
  -> BigFix-style client at src/integrations/bigfix.py
  -> normalized JSON at /api/summary
```

## Production Considerations

To adapt this pattern for a real environment, the project would need:

- authorized JAMF Pro API access
- authorized BigFix API access
- secure secret storage
- authentication for the dashboard
- audit logging
- stronger device matching than device name alone
- error handling and retry behavior
- CSV export or ticket-system integration
