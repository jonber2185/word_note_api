import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

connect_info = {
    "id": os.getenv("Mongo_ID"),
    "pw": os.getenv("Mongo_PASSWORD"),
}

uri = f"mongodb+srv://{connect_info['id']}:{connect_info['pw']}@wordnote.qsphxkm.mongodb.net/?appName=wordNote"

def db_connection():
    client = MongoClient(uri)
    db = client["wordNote"]
    table = db["wordList"]
    return table
