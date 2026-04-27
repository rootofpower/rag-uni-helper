import requests
from bs4 import BeautifulSoup


def scrape(url: str) -> str:
    r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
    soup = BeautifulSoup(r.text, 'html.parser')
    for tag in soup(["script", "style", "header", "nav", "footer"]):
        tag.decompose()
    content = soup.find("div", {"id": "mw-content-text"})
    if content is None:
        content = soup.find("main")
        if content is None:
            content = soup.find("body")
    if content is not None:
        return content.text
    else:
        return None

def scrape_links(url: str) -> set:
    r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find_all("a")
    links = set()
    for link in content:
        href = link.get("href")
        if isinstance(href, str):
            links.add(href)
    return links
