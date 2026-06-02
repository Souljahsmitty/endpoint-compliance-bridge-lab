import base64
import json
import os
import urllib.request


class BigFixClient:
    def __init__(self, base_url, username, password, mock_mode=True):
        self.base_url = (base_url or "").rstrip("/")
        self.username = username
        self.password = password
        self.mock_mode = mock_mode

    @classmethod
    def from_env(cls):
        return cls(
            base_url=os.getenv("BIGFIX_BASE_URL"),
            username=os.getenv("BIGFIX_USERNAME"),
            password=os.getenv("BIGFIX_PASSWORD"),
            mock_mode=os.getenv("MOCK_MODE", "true").lower() != "false",
        )

    def fetch_patch_summary(self):
        if self.mock_mode:
            return [
                {"name": "macbook-finance-014", "patch_status": "Compliant", "critical_missing": 0},
                {"name": "macbook-field-022", "patch_status": "Needs Patch", "critical_missing": 2},
                {"name": "win-admin-009", "patch_status": "Compliant", "critical_missing": 0},
            ]

        if not all([self.base_url, self.username, self.password]):
            raise RuntimeError("Missing BIGFIX_BASE_URL, BIGFIX_USERNAME, or BIGFIX_PASSWORD")

        relevance = os.getenv(
            "BIGFIX_RELEVANCE",
            '(name of it, id of it) of bes computers',
        )
        payload = self._query(relevance)
        return self._normalize_query(payload)

    def _query(self, relevance):
        auth = base64.b64encode(f"{self.username}:{self.password}".encode("utf-8")).decode("ascii")
        request = urllib.request.Request(
            f"{self.base_url}/api/query",
            data=relevance.encode("utf-8"),
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "text/plain",
                "Accept": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"raw": raw}

    def _normalize_query(self, payload):
        # BigFix deployments often customize Relevance output. This keeps live mode
        # intentionally conservative until a lab server shape is known.
        rows = payload.get("result", []) if isinstance(payload, dict) else []
        devices = []
        for row in rows:
            name = row[0] if isinstance(row, list) and row else str(row)
            devices.append({"name": name, "patch_status": "Unknown", "critical_missing": None})
        return devices
