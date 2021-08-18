from urllib.request import urlparse
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

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
    session = requests.Session()
    retry  = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    
    for a_tag in soup.findAll("a"):
        try:
            href = a_tag.attrs.get("href")
            if not "https://gambuuze" in href:
                continue
            if not is_valid(href):
                continue
            if href in urls:
                continue
            urls.add(href)
            all_urls.add(href)
        except Exception as e:
            print(e)
            continue
    return urls

def crawl(url):
    global all_urls
    links = get_all_website_links(url)
    for link in links:
        get_all_website_links(link)
        time.sleep(3)
    return all_urls