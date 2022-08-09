import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

db_connect = MongoClient(os.environ.get("MONGODB_URI"))
db = db_connect.local
