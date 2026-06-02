import json
import os
import urllib.parse
import urllib.request


class JamfClient:
    def __init__(self, base_url, client_id, client_secret, mock_mode=True):
        self.base_url = (base_url or "").rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.mock_mode = mock_mode

    @classmethod
    def from_env(cls):
        return cls(
            base_url=os.getenv("JAMF_BASE_URL"),
            client_id=os.getenv("JAMF_CLIENT_ID"),
            client_secret=os.getenv("JAMF_CLIENT_SECRET"),
            mock_mode=os.getenv("MOCK_MODE", "true").lower() != "false",
        )

    def fetch_devices(self):
        if self.mock_mode:
            return [
                {"name": "macbook-finance-014", "platform": "macOS", "mdm": "JAMF Pro", "os_version": "14.6"},
                {"name": "macbook-field-022", "platform": "macOS", "mdm": "JAMF Pro", "os_version": "15.1"},
                {"name": "win-admin-009", "platform": "Windows", "mdm": "Other/Intune-style", "os_version": "11"},
            ]

        if not all([self.base_url, self.client_id, self.client_secret]):
            raise RuntimeError("Missing JAMF_BASE_URL, JAMF_CLIENT_ID, or JAMF_CLIENT_SECRET")

        token = self._token()
        endpoint = os.getenv(
            "JAMF_DEVICES_ENDPOINT",
            "/api/v1/computers-inventory?section=GENERAL&page=0&page-size=25",
        )
        data = self._get_json(endpoint, token)
        return self._normalize_inventory(data)

    def _token(self):
        body = urllib.parse.urlencode(
            {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/api/oauth/token",
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))["access_token"]

    def _get_json(self, endpoint, token):
        request = urllib.request.Request(
            f"{self.base_url}{endpoint}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def _normalize_inventory(self, payload):
        results = payload.get("results", [])
        devices = []
        for item in results:
            general = item.get("general", {})
            hardware = item.get("hardware", {})
            operating_system = item.get("operatingSystem", {})
            devices.append(
                {
                    "name": general.get("name") or item.get("name") or "unknown-jamf-device",
                    "platform": "macOS",
                    "mdm": "JAMF Pro",
                    "os_version": operating_system.get("version") or hardware.get("osVersion") or "unknown",
                }
            )
        return devices
