from crawler import crawl

links = crawl("https://fei.tuke.sk/")

for link in links:
    print(link)