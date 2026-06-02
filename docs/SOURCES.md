# Sources

These are the official vendor docs used to shape the lab.

## JAMF Pro

- JAMF Pro API overview: https://developer.jamf.com/jamf-pro/
- JAMF client credentials guide: https://developer.jamf.com/jamf-pro/docs/client-credentials

Project takeaway:

- JAMF Pro APIs are accessed through a Jamf Pro instance under `/api`.
- Client Credentials authorization uses an API Client and API Role.
- A client ID and client secret are exchanged for a short-lived access token.
- The access token is sent as a bearer token for other API calls.

## BigFix

- BigFix REST API overview: https://developer.bigfix.com/rest-api/
- BigFix query API: https://developer.bigfix.com/rest-api/api/query.html

Project takeaway:

- BigFix exposes a REST API.
- Query workflows often use BigFix Relevance to ask questions about managed endpoints.
- A reporting project can query endpoint data, normalize it, and show compliance state.

## Truth Boundary

This lab is based on public documentation and mock data unless real tenant credentials are supplied. It is valid as a learning/portfolio project, not proof of production administration years.
