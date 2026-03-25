from langgraph_supervisor import create_supervisor

from ai.agents import get_document_agent, get_movie_discovery_agent
from ai.core.contracts import SupervisorResultContract
from ai.core.error_utils import map_exception_to_error_contract
from ai.core.llm import get_llm
from ai.core.logger import log_event
from ai.agents.github_agent import get_github_agent


def get_supervisor(model=None, checkpointer=None):
    llm_model = model or get_llm()

    return create_supervisor(
        agents=[
            get_document_agent(),
            get_movie_discovery_agent(),
            get_github_agent(),
        ],
        model=llm_model,
        prompt=(
            "You manage a document management assistant (`document_agent`) "
            "and a movie discovery assistant (`movie_agent`).\n\n"

            "Routing rules:\n"
            "- If the request is about documents, send it to `document_agent`.\n"
            "- If the request is about movies, send it to `movie_agent`.\n\n"

            "Response rules:\n"
            "- Never just acknowledge.\n"
            "- After receiving a tool or agent's result, summarize it in plain language for the user.\n"
            "- If the tool returns a list (e.g., document titles), format it as a readable numbered list.\n"
            "- If nothing is found, politely tell the user there are no results."
        )
    ).compile(checkpointer=checkpointer)


def _extract_final_message(response):
    if not isinstance(response, dict):
        return str(response)

    messages = response.get("messages", [])
    if not messages:
        return ""

    last_message = messages[-1]

    if hasattr(last_message, "content"):
        return last_message.content

    if isinstance(last_message, dict):
        return last_message.get("content", "")

    return str(last_message)


def _extract_selected_agent(response):
    if not isinstance(response, dict):
        return None

    if response.get("selected_agent"):
        return response["selected_agent"]

    messages = response.get("messages", [])
    for message in reversed(messages):
        name = getattr(message, "name", None)
        if name in {"document_agent", "movie_agent", "github_agent"}:
            return name

        if isinstance(message, dict) and message.get("name") in {"document_agent", "movie_agent", "github_agent"}:
            return message["name"]

    return None


def run_supervisor(request, model=None, checkpointer=None, request_id=None, trace=None):
    try:
        log_event(
            event="supervisor_started",
            layer="supervisor",
            request_id=request_id or "unknown",
            message=request.message,
            user_id=request.user_id,
        )
        if trace:
            trace.add_step(
                layer="supervisor",
                event="supervisor_started",
                message=request.message,
                user_id=request.user_id,
            )

        supervisor = get_supervisor(model=model, checkpointer=checkpointer)

        response = supervisor.invoke(
            {"messages": [("user", request.message)]},
            config={
                "configurable": {
                    "user_id": request.user_id,
                    "request_id": request_id,
                }
            },
        )

        final_message = _extract_final_message(response)
        selected_agent = _extract_selected_agent(response)

        log_event(
            event="agent_selected",
            layer="supervisor",
            request_id=request_id or "unknown",
            selected_agent=selected_agent,
        )
        if trace:
            trace.add_step(
                layer="supervisor",
                event="agent_selected",
                selected_agent=selected_agent,
            )

        log_event(
            event="supervisor_succeeded",
            layer="supervisor",
            request_id=request_id or "unknown",
            selected_agent=selected_agent,
        )
        if trace:
            trace.add_step(
                layer="supervisor",
                event="supervisor_succeeded",
                selected_agent=selected_agent,
            )

        return SupervisorResultContract(
            status="success",
            selected_agent=selected_agent,
            result={
                "message": final_message,
            },
            error=None,
            meta={},
        )

    except Exception as exc:
        error_contract = map_exception_to_error_contract(exc)

        log_event(
            event="supervisor_failed",
            layer="supervisor",
            request_id=request_id or "unknown",
            error_code=error_contract.code,
            error_message=error_contract.message,
        )
        if trace:
            trace.add_step(
                layer="supervisor",
                event="supervisor_failed",
                error_code=error_contract.code,
                error_message=error_contract.message,
            )

        return SupervisorResultContract(
            status="failure",
            selected_agent=None,
            result=None,
            error=error_contract,
            meta={},
        )