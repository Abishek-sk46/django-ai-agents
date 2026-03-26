from langgraph.prebuilt import create_react_agent

from ai.tools.github_tool import github_tools
from ai.core.llm import get_llm
from ai.core.contracts import AgentResultContract, ErrorContract


def get_github_agent(model=None, checkpointer=None):
    llm_model = model or get_llm()

    agent = create_react_agent(
        model=llm_model,
        tools=github_tools,
        prompt=(
            "You are a GitHub assistant.\n\n"
            "Your job is to help users perform GitHub operations like creating issues.\n\n"
            "When creating an issue, extract:\n"
            "- repo (format: owner/repo)\n"
            "- title\n"
            "- body\n\n"
            "Use the provided tool to create the issue.\n"
            "Do not guess missing values.\n"
        ),
        name="github_agent",
        checkpointer=checkpointer,
    )

    return agent


def run_github_agent(request, model=None, checkpointer=None):
    """
    Wrapper around GitHub agent returning AgentResultContract
    """

    try:
        agent = get_github_agent(model=model, checkpointer=checkpointer)

        response = agent.invoke(
            {"messages": [("user", request.message)]},
            config={
                "configurable": {
                    "user_id": request.user_id,
                    "request_id": request.request_id,
                    "trace": request.trace,
                }
            },
        )

        return AgentResultContract(
            status="success",
            agent="github_agent",
            output=response,
            error=None,
            meta={},
        )

    except Exception as exc:
        return AgentResultContract(
            status="failure",
            agent="github_agent",
            output=None,
            error=ErrorContract(
                code="AGENT_EXECUTION_FAILED",
                message="GitHub agent execution failed",
                details={"reason": str(exc)},
            ),
            meta={},
        )