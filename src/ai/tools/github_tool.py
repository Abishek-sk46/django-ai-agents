from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import os

from ai.core.contracts import ToolResultContract, ErrorContract
from ai.core.logger import log_event

from ai.tools.clients.github_client import GitHubClient


@tool
def create_github_issue(
    repo: str,
    title: str,
    body: str,
    config: RunnableConfig = {},
):
    """
    Create a GitHub issue.

    arguments:
    repo: repository in format "owner/repo"
    title: issue title
    body: issue description
    """

    configurable = config.get("configurable") or config.get("metadata") or {}
    user_id = configurable.get("user_id")
    request_id = configurable.get("request_id")
    trace = configurable.get("trace")

    try:
        # 🔹 log start
        log_event(
            event="tool_started",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="create_github_issue",
            user_id=user_id,
            repo=repo,
            title=title,
        )

        if trace:
            trace.add_step(
                layer="tool",
                event="tool_started",
                tool_name="create_github_issue",
                user_id=user_id,
                repo=repo,
                title=title,
            )

        # 🔹 get token
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return ToolResultContract(
                status="failure",
                data=None,
                error=ErrorContract(
                    code="CONFIG_ERROR",
                    message="Missing GITHUB_TOKEN",
                    details={},
                ),
                meta={},
            )

        client = GitHubClient(token)

        # 🔹 call GitHub API
        response = client.create_issue(repo, title, body)

        status_code = response.get("status_code")
        data = response.get("data", {})

        # ✅ SUCCESS
        if status_code == 201:
            result = ToolResultContract(
                status="success",
                data={
                    "issue_url": data.get("html_url"),
                    "issue_number": data.get("number"),
                    "title": data.get("title"),
                },
                error=None,
                meta={"repo": repo},
            )

            log_event(
                event="tool_succeeded",
                layer="tool",
                request_id=request_id or "unknown",
                tool_name="create_github_issue",
                repo=repo,
                issue_number=data.get("number"),
            )

            if trace:
                trace.add_step(
                    layer="tool",
                    event="tool_succeeded",
                    tool_name="create_github_issue",
                    repo=repo,
                    issue_number=data.get("number"),
                )

            return result

        # ❌ FAILURE — structured mapping
        if status_code == 401:
            error_code = "GITHUB_AUTH_ERROR"
            message = "Invalid or missing GitHub token"

        elif status_code == 403:
            error_code = "GITHUB_PERMISSION_DENIED"
            message = "Permission denied to access repository"

        elif status_code == 404:
            error_code = "GITHUB_NOT_FOUND"
            message = "Repository not found"

        elif status_code == 422:
            error_code = "GITHUB_VALIDATION_ERROR"
            message = "Invalid issue data"

        elif status_code == 429:
            error_code = "GITHUB_RATE_LIMIT"
            message = "GitHub rate limit exceeded"

        elif status_code >= 500:
            error_code = "GITHUB_SERVER_ERROR"
            message = "GitHub server error"

        else:
            error_code = "GITHUB_UNKNOWN_ERROR"
            message = "Unexpected GitHub API error"

        # 🔹 log failure
        log_event(
            event="tool_failed",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="create_github_issue",
            error_code=error_code,
            repo=repo,
            response=data,
        )

        if trace:
            trace.add_step(
                layer="tool",
                event="tool_failed",
                tool_name="create_github_issue",
                error_code=error_code,
                repo=repo,
            )

        return ToolResultContract(
            status="failure",
            data=None,
            error=ErrorContract(
                code=error_code,
                message=message,
                details=data,
            ),
            meta={"repo": repo},
        )

    except Exception as exc:
        # ❌ unexpected failure (network, timeout, etc.)
        log_event(
            event="tool_failed",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="create_github_issue",
            error_code="TOOL_FAILURE",
            error_message=str(exc),
        )

        if trace:
            trace.add_step(
                layer="tool",
                event="tool_failed",
                tool_name="create_github_issue",
                error_code="TOOL_FAILURE",
                error_message=str(exc),
            )

        return ToolResultContract(
            status="failure",
            data=None,
            error=ErrorContract(
                code="TOOL_FAILURE",
                message="GitHub issue creation failed",
                details={"reason": str(exc), "repo": repo},
            ),
            meta={},
        )


# export
github_tools = [
    create_github_issue,
]