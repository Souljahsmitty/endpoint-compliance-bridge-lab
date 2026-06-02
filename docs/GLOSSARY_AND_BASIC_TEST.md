# Glossary And Basic Test

This explains the phrase:

```text
JAMF Pro + BigFix endpoint-compliance integration without claiming production administration experience
```

## The Phrase, Broken Down

### JAMF Pro

JAMF Pro is a tool organizations use to manage Apple devices, especially Macs.

In plain English:

```text
JAMF answers: What Macs do we have, and are they managed?
```

In this lab:

```text
src/integrations/jamf.py
```

pretends to pull Mac inventory data.

### BigFix

BigFix is a tool organizations use to track endpoint state, patch status, and compliance.

In plain English:

```text
BigFix answers: Which devices are patched, and which need attention?
```

In this lab:

```text
src/integrations/bigfix.py
```

pretends to pull patch/compliance data.

### Endpoint

An endpoint is a user device or managed computer.

Examples:

- MacBook
- Windows laptop
- desktop workstation
- field laptop

In this lab, the endpoints are:

```text
macbook-finance-014
macbook-field-022
win-admin-009
```

### Compliance

Compliance means the device meets the rule.

For this lab, the rule is simple:

```text
Is the device patched, or does it need patches?
```

Example:

```text
Compliant = okay right now
Needs Patch = endpoint team should investigate or remediate
```

### Integration

Integration means two systems are connected into one workflow.

In this lab:

```text
JAMF-style inventory + BigFix-style patch status = one dashboard
```

The app combines two fake sources:

1. JAMF-style device inventory.
2. BigFix-style patch/compliance data.

Then it shows one table.

### Without Claiming Production Administration Experience

This is the truth boundary.

You can say:

```text
I built a lab project that models JAMF Pro and BigFix API integration patterns.
```

Do not say:

```text
I administered JAMF Pro and BigFix in production for years.
```

This project proves initiative, API literacy, Docker packaging, mock-data testing, and endpoint-compliance vocabulary.

It does not prove production admin tenure.

## What Working Looks Like

The dashboard should show:

```text
Total devices: 3
Compliant: 2
Needs patch: 1
Mode: mock
```

The device needing attention should be:

```text
macbook-field-022
```

because it has:

```text
patch_status: Needs Patch
critical_missing: 2
```

## Basic Test I Ran

From the repo folder:

```bash
cd "/Users/adamsmith/Documents/New project/endpoint-compliance-bridge-lab"
python3 src/server.py
```

In another terminal:

```bash
curl -fsS http://127.0.0.1:8080/api/summary | python3 -m json.tool
```

Expected output shape:

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

Then open:

```text
http://127.0.0.1:8080
```

Expected browser result:

- dashboard loads
- mode says `mock`
- table shows 3 devices
- one Mac says `Needs Patch`

## Build vs Run

These commands run the finished repo:

```bash
python3 src/server.py
curl -fsS http://127.0.0.1:8080/api/summary
```

These steps build a tiny version from scratch:

1. Create a folder.
2. Create `static/index.html`.
3. Create `src/server.py`.
4. Run `python3 src/server.py`.
5. Add a `Dockerfile`.
6. Add JAMF/BigFix-style mock data.

For the copy-by-hand build path, read:

```text
docs/REPLICATE_SIMPLE_PROJECT.md
```

## One-Sentence Explanation

This project is a safe mock endpoint dashboard that teaches how JAMF-style Mac inventory and BigFix-style patch status can be combined into one compliance view.
