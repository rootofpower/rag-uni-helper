import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig
from chunker import chunk_text
from crawler import crawl
from db import add_documents, get_documents, query_collection
from llm import generate_answer
from scraper import scrape


async def add_source(
        url: str,
        crawler: AsyncWebCrawler,
        collection_name: str
) -> dict:
    try:
        existing = get_documents(
            collection_name=collection_name,
            where={"source": url}
        )
    except Exception as e:
        print(f"ERROR IN add_source: {e}")
        return {"status": "error"}
    if existing["ids"]:
        print(f"Source {url} already exists")
        return {"status": "already_exists"}
    text = await scrape(url, crawler=crawler)
    if not text:
        return {"status": "skipped"}
    chunks = chunk_text(text)
    add_documents(collection_name=collection_name,
                  ids=[f"{url}_{i}" for i in range(len(chunks))],
                  documents=chunks,
                  metadatas=[{"source": url} for _ in range(len(chunks))
    ])
    return {"status": "success"}


async def crawl_and_add(start_urls: list,
                        collection_name: str,
                        max_pages=50,
                        lang_prefix=None,
                        batch_size=5,
) -> dict:
    browser_cfg = BrowserConfig(headless=True)
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        links = await crawl(
            start_urls=start_urls,
            crawler=crawler,
            max_pages=max_pages,
            lang_prefix=lang_prefix,
            batch_size=batch_size
        )
        errors = []
        results = await asyncio.gather(
            *[add_source(
                url=url,
                crawler=crawler,
                collection_name=collection_name
            )
                for url in links],
            return_exceptions=True
        )
        for link, result in zip(links, results):
            if isinstance(result, Exception):
                errors.append({"url": link, "result": str(result)})
    return {"status": "success", "added": len(links), "errors": errors}


def get_answer_from_collection(
        collection_name: str,
        query: str
) -> dict:
    (context, source) = query_collection(
        collection_name=collection_name,
        query=query
        )

    answer = generate_answer(
        query=query,
        context=context
    )
    return {"answer": answer, "source": source}


async def add_source_from_url(
        url:str,
        collection_name: str
) -> dict:
    browser_cfg = BrowserConfig(headless=True)
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        return await add_source(
            url=url,
            crawler=crawler,
            collection_name=collection_name
        )