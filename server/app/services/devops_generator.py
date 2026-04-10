from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import Config

def get_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=Config.GEMINI_API_KEY,
        temperature=0.3,
    )
    return llm