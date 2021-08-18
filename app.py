# Import libraries
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, errors
from datetime import datetime as date
from bs4 import BeautifulSoup
import os
import requests

# Import utils
from utils import crawl

# Load environment variables
env_path=os.path.join(os.getcwd(), ".env")

if os.path.exists(env_path):
    load_dotenv(env_path)

# Initialize DB
DATABASE_URL = os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)

def extract_text(array):
    """" Extracts text for every element in the array"""
    return [i.get_text() for i in array]

# Crawl site
TARGET_URL = os.getenv('TARGET_URL')
try:
    all_urls = crawl(TARGET_URL)
    client.gambuuze.lines.create_index([("text", ASCENDING)], unique=True)

    for link in all_urls:
        res = requests.get(link)
        page = BeautifulSoup(res.text, 'lxml')
    
        # Select all headings
        headings = page.select(".jeg_post_title")
        headings = extract_text(headings)
        # Select all list items
        list_items = page.select("li")
        list_items = extract_text(list_items)
        # Select all Paragraphs
        paragraphs = page.select("p")
        paragraphs = extract_text(paragraphs)
        # Select all anchor tags
        anchor_tags = page.select("a")
        anchor_tags = extract_text(anchor_tags)

        page_data = headings+list_items+paragraphs+anchor_tags
        for text in set(page_data):
            if len(text.split(" ")) < 4:
                continue
            else:
                try:
                    print(f"Writing {str(text)}")
                    client.gambuuze.lines.insert({"text": str(text), "date": date.now()})
                except errors.DuplicateKeyError:
                    print("Text already exists")
except Exception as e:
    print(e)