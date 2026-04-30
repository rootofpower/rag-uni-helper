import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set")
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(query: str, context: str) -> str:
    prompt = f"""Answer the question based ONLY on the context below.
    Context: {context}
    Query: {query}
"""
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite-preview',
        contents=prompt,
    )
    return response.text
