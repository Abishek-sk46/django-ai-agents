# from langchain_google-genai import ChatOpenAI
# from django.conf import settings
# def get_openai_model(model="gpt-4o-mini"):
   
    
#     return ChatOpenAI(
#     model=model,
#     temperature=0,
#     max_tokens=200,
#     max_retries=2,
#     api_key=settings.OPENAI_API_KEY,

# )

# from langchain_google_genai import ChatGoogleGenerativeAI
# from django.conf import settings

# def get_gemini_model(model="gemini-pro"):
#     return ChatGoogleGenerativeAI(
#         model=model,
#         temperature=0,
#         max_output_tokens=200,
#         max_retries=2,
#         google_api_key="AIzaSyAvmfl-1YRtQOJK8UJ-dBXPI-3hLrdJFkk" # Make sure this is set in your Django settings
#     )

from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings

def get_gemini_model(model="models/gemini-pro"):
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        max_tokens=2048,
        google_api_key="AIzaSyAvmfl-1YRtQOJK8UJ-dBXPI-3hLrdJFkk"
    )

