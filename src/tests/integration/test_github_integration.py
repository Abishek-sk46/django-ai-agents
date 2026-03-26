from django.test import TestCase
from unittest.mock import patch

from ai.supervisor.main import run_supervisor
from ai.core.contracts import RequestContract


class GitHubIntegrationTests(TestCase):

    @patch("ai.tools.github_tool.GitHubClient.create_issue")
    def test_create_issue_success(self, mock_create_issue):
        # 🔹 mock GitHub response
        mock_create_issue.return_value = {
            "status_code": 201,
            "data": {
                "html_url": "https://github.com/test/repo/issues/1",
                "number": 1,
                "title": "TestIssue"
            }
        }

        request = RequestContract(
            message="create github issue repo=test/repo title=TestIssue body=Hello",
            user_id=None
        )

        result = run_supervisor(request)

        self.assertEqual(result.status, "success")
        self.assertEqual(result.selected_agent, "github_agent")
        self.assertIn("message", result.result)

    @patch("ai.tools.github_tool.GitHubClient.create_issue")
    def test_create_issue_auth_failure(self, mock_create_issue):
        mock_create_issue.return_value = {
            "status_code": 401,
            "data": {"message": "Bad credentials"}
        }

        request = RequestContract(
            message="create github issue repo=test/repo title=TestIssue",
            user_id=None
        )

        result = run_supervisor(request)

        self.assertEqual(result.status, "success")  # supervisor succeeded
        message = result.result["message"].lower()

        self.assertTrue(
            "github" in message and ("token" in message or "auth" in message)
        )


    def test_missing_repo(self):
        request = RequestContract(
            message="create github issue title=TestIssue",
            user_id=None
        )

        result = run_supervisor(request)

        self.assertEqual(result.status, "success")
        self.assertIn("repo", result.result["message"].lower())

    