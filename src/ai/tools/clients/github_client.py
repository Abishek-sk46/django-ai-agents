import asyncio
from typing import Dict, Any

import httpx


class GitHubClient:
    BASE_URL = "https://api.github.com"

    # ✅ shared async client (connection pooling)
    _client = httpx.AsyncClient(timeout=5)

    def __init__(self, token: str, timeout: int = 5):
        self.token = token
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    # ✅ async implementation (non-blocking I/O)
    async def _create_issue_async(
        self, repo: str, title: str, body: str
    ) -> Dict[str, Any]:

        url = f"{self.BASE_URL}/repos/{repo}/issues"

        payload = {
            "title": title,
            "body": body
        }

        try:
            response = await self._client.post(
                url,
                json=payload,
                headers=self._headers(),
                timeout=self.timeout
            )

            try:
                data = response.json() if response.content else None
            except Exception:
                data = None

            return {
                "status_code": response.status_code,
                "data": data
            }

        # ✅ timeout
        except httpx.TimeoutException:
            return {
                "status_code": 408,
                "data": {"error": "GitHub API timeout"}
            }

        # ✅ network error
        except httpx.RequestError as e:
            return {
                "status_code": 503,
                "data": {"error": f"Network error: {str(e)}"}
            }

        # ✅ fallback error
        except Exception as e:
            return {
                "status_code": 500,
                "data": {"error": f"Unexpected error: {str(e)}"}
            }

    # ✅ IMPROVED sync wrapper (Task 5 fix)
    def create_issue(self, repo: str, title: str, body: str) -> Dict[str, Any]:
        """
        Safe execution of async function without excessive event loop creation
        """

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # No event loop exists → create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # ✅ If loop already running (future-safe)
        if loop.is_running():
            # fallback (rare case, but safe)
            return asyncio.run(
                self._create_issue_async(repo, title, body)
            )
        else:
            return loop.run_until_complete(
                self._create_issue_async(repo, title, body)
            )