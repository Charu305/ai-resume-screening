from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv() 

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")  # ← keep this
    )

def get_llm_flash():
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")  # ← keep this
    )