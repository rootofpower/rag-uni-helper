from fastapi import FastAPI

from rag import get_answer_from_collection

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Simple RAG helper"}


@app.get("/ask")
def ask(query: str):
    return get_answer_from_collection(query)
