from langgraph_supervisor import create_supervisor

from ai.agents import get_document_agent, get_movie_discovery_agent
from ai.core.llm import get_llm
from ai.core.contracts import SupervisorResultContract, ErrorContract


def get_supervisor(model=None, checkpointer=None):
    llm_model = model or get_llm()

    return create_supervisor(
        agents=[
            get_document_agent(),
            get_movie_discovery_agent(),
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


def run_supervisor(request, model=None, checkpointer=None):
    """
    Wrapper around the compiled supervisor that returns SupervisorResultContract.
    """

    try:
        supervisor = get_supervisor(model=model, checkpointer=checkpointer)

        response = supervisor.invoke(
            {"messages": [("user", request.message)]},
            config={
                "configurable": {
                    "user_id": request.user_id,
                }
            },
        )

        selected_agent = None
        if isinstance(response, dict):
            selected_agent = (
                response.get("selected_agent")
                or response.get("agent")
                or response.get("name")
            )

        return SupervisorResultContract(
            status="success",
            selected_agent=selected_agent,
            result=response,
            error=None,
            meta={},
        )

    except Exception as exc:
        return SupervisorResultContract(
            status="failure",
            selected_agent=None,
            result=None,
            error=ErrorContract(
                code="SUPERVISOR_EXECUTION_FAILED",
                message="Supervisor execution failed",
                details={"reason": str(exc)},
            ),
            meta={},
        )