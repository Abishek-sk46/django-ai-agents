from langgraph.prebuilt import create_react_agent
from ai.tools import documents_tools
from ai.llms  import get_gemini_model

def get_agent(model=None,checkpointer = None):
    llm_model = get_gemini_model(model = model)

    agent = create_react_agent(
        model=llm_model,
        tools=documents_tools,
        prompt="You are a helpful assistant in managing a user's documents within this app",
        checkpointer=checkpointer
    )

    return agent

