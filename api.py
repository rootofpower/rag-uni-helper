from fastapi import FastAPI
from pydantic import BaseModel
from rag import get_answer_from_collection, crawl_and_add
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

class CrawlRequest(BaseModel):
    start_urls: list[str]
    lang_prefix: str | None


@app.post("/crawl")
def crawl(request: CrawlRequest):
    return crawl_and_add(request.start_urls, request.lang_prefix)
