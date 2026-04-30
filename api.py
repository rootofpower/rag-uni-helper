from fastapi import FastAPI
from pydantic import BaseModel

from db import (create_collection,
                clear_collection,
                delete_collection,
                list_collection,
                documents_count)
from rag import (get_answer_from_collection,
                 crawl_and_add,
                 add_source_from_url)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Simple RAG helper"}


@app.get("/ask")
async def ask(collection_name: str, query: str):
    return get_answer_from_collection(collection_name, query)


class CrawlRequest(BaseModel):
    start_urls: list[str]
    collection_name: str
    max_pages: int
    lang_prefix: str | None
    batch_size: int


@app.post("/crawl_and_add")
async def crawl(request: CrawlRequest):
    return await crawl_and_add(
        request.start_urls,
        request.collection_name,
        request.max_pages,
        request.lang_prefix,
        request.batch_size
    )


@app.post("/collection/create")
async def create_coll(collection_name: str):
    return create_collection(collection_name)


@app.post("/collection/add_source")
async def add_source(source: str, collection_name: str):
    return await add_source_from_url(
        url=source,
        collection_name=collection_name
    )


@app.post("/collection/clear")
async def clear_coll(collection_name: str):
    return clear_collection(collection_name)


@app.delete("/collection/delete")
async def delete_coll(collection_name: str):
    return delete_collection(collection_name)


@app.get("/collection/list")
async def list_coll():
    return list_collection()


@app.get("/collection/docs_count")
async def docs_count(collection_name: str):
    return documents_count(collection_name)
