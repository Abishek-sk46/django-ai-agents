from langgraph.prebuilt import create_react_agent
from ai.tools import documents_tools, movie_discovery_tools
# from ai.llms  import get_gemini_model
from ai.llms import get_llm


def get_agent(model=None, checkpointer=None):
    llm_model = get_llm()


    agent = create_react_agent(
        model=llm_model,
        tools=documents_tools,
        prompt="You are a helpful assistant in managing a user's documents within this app",
        name="document_agent",  # ✅ unique name
        checkpointer=checkpointer
    )

    return agent


def get_movie_discovery_agent(model=None, checkpointer=None):
    llm_model = get_llm()


    agent = create_react_agent(
        model=llm_model,
        tools=movie_discovery_tools,
        prompt="You are a helpful assistant in finding and discovering information about movies",
        name="movie_agent",  # ✅ unique name
        checkpointer=checkpointer
    )

    return agent
