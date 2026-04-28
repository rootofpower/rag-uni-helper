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
async def add(source: str):
    return await add_source(source)


class CrawlRequest(BaseModel):
    start_urls: list[str]
    max_pages: int
    lang_prefix: str | None
    batch_size: int


@app.post("/crawl")
async def crawl(request: CrawlRequest):
    return await crawl_and_add(
        request.start_urls,
        request.max_pages,
        request.lang_prefix,
        request.batch_size
    )

# @app.post("/clear_source")
# async def clear_source(request: CrawlRequest):
