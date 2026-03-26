from langgraph.prebuilt import create_react_agent
from ai.tools import documents_tools
from ai.core.llm import get_llm


def get_document_agent(model=None, checkpointer=None):
    llm_model = get_llm()


    agent = create_react_agent(
        model=llm_model,
        tools=documents_tools,
        prompt="You are a helpful assistant in managing a user's documents within this app",
        name="document_agent",  # ✅ unique name
        checkpointer=checkpointer
    )

    return agent
