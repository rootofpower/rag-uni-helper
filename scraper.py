import requests
from bs4 import BeautifulSoup


def scrape(url: str) -> str:
    r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
    soup = BeautifulSoup(r.text, 'html.parser')
    for tag in soup(["script", "style", "header", "nav", "footer"]):
        tag.decompose()
    content = soup.find("div", {"id": "mw-content-text"})
    if content is not None:
        return content.text
    else:
        return None
