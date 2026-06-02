# Requirement Map

## Job Requirement

"Working experience with JAMF Pro, Intune, and BigFix."

## What The Employer Probably Needs

- Someone who can understand managed device inventory.
- Someone who can read endpoint compliance status.
- Someone who can help enforce patching and configuration standards.
- Someone who can troubleshoot why a device is not reporting correctly.
- Someone who can document the status clearly for audits or security reviews.

## What This Project Builds Toward

| Employer Need | Lab Project Piece |
| --- | --- |
| Device inventory | `JamfClient.fetch_devices()` |
| Patch/compliance status | `BigFixClient.fetch_patch_summary()` |
| Reporting dashboard | `static/index.html` |
| Safe credential handling | environment variables |
| Repeatable deployment | `Dockerfile` |
| Audit-style explanation | docs folder |
| Recruiter-safe truth | `TRUTHFUL_TALKING_POINTS.md` |

## Next Project Upgrade

Build one small add-on per missing tool:

1. JAMF: add a page explaining API Roles, API Clients, token flow, and computer inventory.
2. BigFix: add a page explaining Relevance query basics and patch status.
3. Intune: add a Microsoft Graph mock client for managed devices.
4. Compliance: add a CSV export for "devices needing patch."
5. Reporting: add a CSV export for "devices needing patch."
