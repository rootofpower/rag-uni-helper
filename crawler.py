from urllib.parse import urljoin
import re
from scraper import scrape_links


def crawl(start_urls: list, max_pages=50, lang_prefix=None):
    visited_urls = set()
    visit_queue = list(start_urls)
    if lang_prefix is not None and not re.search("^/[a-z]{2}/$", lang_prefix):
        raise ValueError("Invalid lang_prefix")
    while visit_queue and len(visited_urls) < max_pages:
        url = visit_queue.pop(0)
        if url not in visited_urls:
            print(f"Visiting: {url} ({len(visit_queue)}/{max_pages})")
            visited_urls.add(url)
            links = scrape_links(url=url)
            for link in links:
                link = urljoin(url, link)
                link = link.split("#")[0]
                if any(link.startswith(root) for root in start_urls) and link not in visited_urls and (lang_prefix is None or lang_prefix in link):
                    visit_queue.append(link)
    return visited_urls
