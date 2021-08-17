from urllib.request import urlopen, urlparse
from bs4 import BeautifulSoup
import requests

def is_valid(url):
    """s
        checks whether 'url' is a valid URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

all_urls = set()
def get_all_website_links(url):
    """
    Returns all URLs that are found on the website
    
    """
    print(f"Crawling {url}.")
    urls = set()
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if not "https://gambuuze" in href:
            continue
        if not is_valid(href):
            continue
        if href in urls:
            continue
        urls.add(href)
        all_urls.add(href)
    return urls

def crawl(url):
    global all_urls
    links = get_all_website_links(url)
    for link in links:
        get_all_website_links(link)
    return all_urls