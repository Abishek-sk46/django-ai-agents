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

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings

def get_gemini_model(model="gemini-1.5-flash", google_api_key=None):
    if google_api_key is None:
        # Try to get from environment variable first, then from Django settings
        google_api_key = os.getenv('GOOGLE_API_KEY') or getattr(settings, 'GOOGLE_API_KEY', None)
        
        if not google_api_key:
            raise ValueError("Google API key not found. Please set GOOGLE_API_KEY environment variable or in Django settings.")

    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        max_tokens=2048,
        google_api_key=google_api_key
    )