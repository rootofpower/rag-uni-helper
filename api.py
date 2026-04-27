from fastapi import FastAPI

from rag import get_answer_from_collection
from rag import add_source
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Simple RAG helper"}


@app.get("/ask")
def ask(query: str):
    return get_answer_from_collection(query)


@app.post("/add")
def add(source: str):
    return add_source(source)
