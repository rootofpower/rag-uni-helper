import re

from crawl4ai import AsyncWebCrawler, BrowserConfig

from scraper import scrape_links
import asyncio


async def crawl(crawler: AsyncWebCrawler, start_urls: list, max_pages=50, lang_prefix=None, batch_size=5):
    visited_urls = set()
    visit_queue = list(start_urls)
    if lang_prefix is not None and not re.search("^/[a-z]{2}/$", lang_prefix):
        raise ValueError("Invalid lang_prefix")
    while visit_queue and len(visited_urls) < max_pages:
        batch = visit_queue[:batch_size]
        visit_queue = visit_queue[batch_size:]
        batch = [url for url in batch if url not in visited_urls]
        print(f"Batch size after filter: {len(batch)}")
        visited_urls.update(batch)
        results = await asyncio.gather(*[scrape_links(url=url, crawler=crawler) for url in batch])
        for url, links in zip(batch, results):
            print(f"Visiting: {url} ({len(visit_queue)}/{max_pages})")
            for link in (links if links is not None else []):
                link = link.split("#")[0]
                if (any(link.startswith(root) for root in start_urls)
                        and link not in visited_urls
                        and (lang_prefix is None
                             or lang_prefix in link)):
                    visit_queue.append(link)
    return visited_urls
