from dotenv import load_dotenv
from pymongo import MongoClient
import os

env_path=os.path.join(os.getcwd(), ".env")

if os.path.exists(env_path):
    load_dotenv(env_path)

DATABASE_URL = os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)