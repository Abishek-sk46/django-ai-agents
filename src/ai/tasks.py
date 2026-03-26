from types import SimpleNamespace
from celery import shared_task

from ai.agents.github_agent import run_github_agent
from ai.core.logger import log_event


def serialize_result(result):
    """
    Convert AgentResultContract → JSON-safe dict
    """
    return {
        "status": result.status,
        "agent": result.agent,
        "output": str(result.output),  # convert complex objects → string
        "error": str(result.error) if result.error else None,
        "meta": result.meta,
    }


@shared_task(bind=True)
def execute_github_issue_task(self, request_data: dict):
    try:
        log_event(
            event="task_started",
            layer="celery",
            request_id=request_data.get("request_id"),
            payload=request_data,
        )

        # Convert dict → object (so agent can use .message etc.)
        request_obj = SimpleNamespace(**request_data)

        # Run your existing agent logic
        result = run_github_agent(request_obj)

        log_event(
            event="task_completed",
            layer="celery",
            request_id=request_data.get("request_id"),
        )

        # Return JSON-safe result
        return serialize_result(result)

    except Exception as e:
        log_event(
            event="task_failed",
            layer="celery",
            request_id=request_data.get("request_id"),
            error=str(e),
        )
        raise e