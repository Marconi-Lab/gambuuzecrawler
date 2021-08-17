from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, errors
from datetime import datetime as date
import os

env_path=os.path.join(os.getcwd(), ".env")

if os.path.exists(env_path):
    load_dotenv(env_path)

DATABASE_URL = os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)
try:
    client.gambuuze.lines.create_index([("name", ASCENDING)], unique=True)
    client.gambuuze.lines.insert({"text": "ben", "date": date.now()})
except errors.DuplicateKeyError:
    print("Text already exists")