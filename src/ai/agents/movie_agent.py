from langgraph.prebuilt import create_react_agent

from ai.tools import movie_discovery_tools
from ai.core.llm import get_llm
from ai.core.contracts import AgentResultContract, ErrorContract


def get_movie_discovery_agent(model=None, checkpointer=None):
    llm_model = model or get_llm()

    agent = create_react_agent(
        model=llm_model,
        tools=movie_discovery_tools,
        prompt="You are a helpful assistant in finding and discovering information about movies",
        name="movie_agent",
        checkpointer=checkpointer,
    )

    return agent


def run_movie_discovery_agent(request, model=None, checkpointer=None):
    """
    Wrapper around the LangGraph movie agent that returns AgentResultContract.
    """

    try:
        agent = get_movie_discovery_agent(model=model, checkpointer=checkpointer)

        response = agent.invoke(
            {"messages": [("user", request.message)]},
            config={
                "configurable": {
                    "user_id": request.user_id,
                }
            },
        )

        return AgentResultContract(
            status="success",
            agent="movie_agent",
            output=response,
            error=None,
            meta={},
        )

    except Exception as exc:
        return AgentResultContract(
            status="failure",
            agent="movie_agent",
            output=None,
            error=ErrorContract(
                code="AGENT_EXECUTION_FAILED",
                message="Movie agent execution failed",
                details={"reason": str(exc)},
            ),
            meta={},
        )