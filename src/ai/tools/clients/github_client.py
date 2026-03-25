import requests
from typing import Dict, Any


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str, timeout: int = 5):
        self.token = token
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def create_issue(self, repo: str, title: str, body: str) -> Dict[str, Any]:
        """
        repo format: owner/repo
        """
        url = f"{self.BASE_URL}/repos/{repo}/issues"

        payload = {
            "title": title,
            "body": body
        }

        response = requests.post(
            url,
            json=payload,
            headers=self._headers(),
            timeout=self.timeout
        )

        # ✅ Safe JSON handling (IMPORTANT FIX)
        try:
            data = response.json() if response.content else None
        except Exception:
            data = None

        return {
            "status_code": response.status_code,
            "data": data
        }