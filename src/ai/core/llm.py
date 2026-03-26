
from langchain_openai import ChatOpenAI
from django.conf import settings

def get_llm(model="gpt-4o-mini"):
    return ChatOpenAI(
        model=model,
        temperature=0,
        api_key=settings.OPENAI_API_KEY
    )

