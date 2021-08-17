from urllib.request import urlopen, urlparse, urljoin
from bs4 import BeautifulSoup
import re

def is_valid(url):
    """
        checks whether 'url' is a valid URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)