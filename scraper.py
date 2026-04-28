# import requests
# from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

# def scrape(url: str) -> str:
#     r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
#     soup = BeautifulSoup(r.text, 'html.parser')
#     for tag in soup(["script", "style", "header", "nav", "footer"]):
#         tag.decompose()
#     content = soup.find("div", {"id": "mw-content-text"})
#     if content is None:
#         content = soup.find("main")
#         if content is None:
#             content = soup.find("body")
#     if content is not None:
#         return content.text
#     else:
#         return None


async def scrape(url: str, crawler: AsyncWebCrawler) -> str:
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        word_count_threshold=10
    )
    result = await crawler.arun(
        url=url,
        config=run_config
    )
    if result.success:
        return result.markdown
    else:
        print("Error while scraping")
        return None

# def scrape_links(url: str) -> set:
#     r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
#     soup = BeautifulSoup(r.text, 'html.parser')
#     content = soup.find_all("a")
#     links = set()
#     for link in content:
#         href = link.get("href")
#         if isinstance(href, str):
#             links.add(href)
#     return links


async def scrape_links(url: str, crawler: AsyncWebCrawler) -> set:
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        exclude_external_links=True
    )
    result = await crawler.arun(
        url=url,
        config=run_config
    )
    if result.success:
        links = set()
        for link in result.links["internal"]:
            links.add(link["href"])
        return links
    else:
        print("Error while scraping")
        return None
