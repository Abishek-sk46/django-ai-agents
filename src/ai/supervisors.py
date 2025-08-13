from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_google_genai import ChatGoogleGenerativeAI

from ai.llms import get_gemini_model
from ai import agents


def get_supervisor(model=None, checkpointer=None):
    llm_model = get_gemini_model(model=model)

    return create_supervisor(
        agents=[
            agents.get_agent(),
            agents.get_movie_discovery_agent(),
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
