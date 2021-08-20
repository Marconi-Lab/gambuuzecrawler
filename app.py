# Import libraries
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, errors
from datetime import datetime as date
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import requests
import re

# Import utils
from utils import crawl

# Load environment variables
env_path=os.path.join(os.getcwd(), ".env")

if os.path.exists(env_path):
    load_dotenv(env_path)

# Initialize DB
DATABASE_URL = os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)

def remove_unrecognizable_chars(text):
    text = text.replace("\n", " ")
    text = text.replace("‘", "'")
    text = text.replace("”", "")
    text = text.replace("’", "'")
    text = text.replace("“", "")
    text = text.replace("–", "-")
    text = text.replace("  ", " ")
    return text

def extract_text(array):
    """" Extracts text for every element in the array"""
    new_set = set()
    new_set_long = set()
    # Special character regex
    regex = re.compile('[_#$^*=<>©@\|}{~]�')
    for i in array:
        for j in i.find_all():
            j.decompose()
        text = i.get_text()
        text = remove_unrecognizable_chars(text)
        # Check if string consists Special character
        if regex.search(text) == None:
            if len(text.split(" ")) > 14:
                text = text.split(".")
                for txt in text:
                    if len(txt.split(" ")) > 14:
                        new_set_long.add(txt)
                    else:
                        new_set.add(txt)
            else:
                new_set.add(text)
        else:
            continue
        
    return new_set, new_set_long

# Crawl site
def run(url):
    try:
        all_urls = crawl(url)
        # Create index key (text)
        client.gambuuze.lines.create_index([("text", ASCENDING)], unique=True)
        client.gambuuze.linesLong.create_index([("text", ASCENDING)], unique=True)

        for link in all_urls:
            session = requests.Session()
            retry  = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            res = session.get(link)
            page = BeautifulSoup(res.text, 'lxml')
        
            # Select all headings
            headings = page.select("h1")
            headings, headings_long = extract_text(headings)
            # Select all Paragraphs
            paragraphs = page.select("p")
            paragraphs, paragraphs_long = extract_text(paragraphs)
            # Select all anchor tags
            anchor_tags = page.select("a")
            anchor_tags, anchor_tags_long = extract_text(anchor_tags)

            page_data = headings.union(paragraphs,anchor_tags)
            page_data_long = headings_long.union(paragraphs_long, anchor_tags_long)
            for text in page_data:
                if len(text.split(" ")) < 4:
                    continue
                else:
                    try:
                        print(f"Writing {str(text)}")
                        client.gambuuze.lines.insert({"text": str(text), "date": date.now()})
                    except errors.DuplicateKeyError:
                        print("Text already exists")
            for text in page_data_long:
                if len(text.split(" ")) < 4:
                    continue
                else:
                    try:
                        print(f"Writing {str(text)}")
                        client.gambuuze.linesLong.insert({"text": str(text), "date": date.now()})
                    except errors.DuplicateKeyError:
                        print("Text already exists")
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    TARGET_URL = os.getenv('TARGET_URL')
    run(TARGET_URL)