from urllib.parse import urljoin

from scraper import scrape_links


def crawl(start_url, max_pages=50):
    visited_urls = set()
    visit_queue = [start_url]

    while visit_queue and len(visited_urls) < max_pages:
        url = visit_queue.pop(0)
        if url not in visited_urls:
            visited_urls.add(url)
            links = scrape_links(url=url)
            for link in links:
                link = urljoin(start_url, link)
                if link.startswith(start_url) and link not in visited_urls:
                    visit_queue.append(link)
    return visited_urls
