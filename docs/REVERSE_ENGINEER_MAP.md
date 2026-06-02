# Capability Map

This map connects the lab files to the endpoint-compliance workflow they model.

## Workflow Pieces

| Endpoint Workflow Need | Lab Project Piece |
| --- | --- |
| Read managed-device inventory | `JamfClient.fetch_devices()` |
| Read patch/compliance status | `BigFixClient.fetch_patch_summary()` |
| Combine device records | `build_summary()` in `src/server.py` |
| Display endpoint status | `static/index.html` |
| Expose machine-readable output | `/api/summary` |
| Keep credentials out of code | environment variables |
| Package the app repeatably | `Dockerfile` |
| Explain run/test behavior | `docs/RUN_AND_TEST.md` |
| Explain safe demo boundaries | `docs/SECURITY_AND_DEMO_NOTES.md` |

## Data Flow

```text
JAMF-style inventory
  + BigFix-style patch status
  -> normalized endpoint records
  -> summary counts
  -> local dashboard and JSON API
```

## Current Lab Behavior

The default mock data produces:

```text
3 total devices
2 compliant devices
1 device needing patch attention
```

## Next Project Upgrades

1. Add an Intune-style mock client for managed Windows devices.
2. Add CSV export for devices needing patch attention.
3. Add unit tests for record matching and summary counts.
4. Add configurable match keys beyond device name.
5. Add dashboard filtering by platform, MDM source, and patch status.
