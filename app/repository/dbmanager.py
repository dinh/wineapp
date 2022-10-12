from pymongo import MongoClient
from app.project import info
if info['mongo']['auth']:
    db = MongoClient(f"mongodb://{info['mongo']['username']}:{info['mongo']['password']}@{info['mongo']['address']}:{info['mongo']['port']}")[f"{info['mongo']['dbname']}"]
else:
    db = MongoClient(f"mongodb://{info['mongo']['address']}:{info['mongo']['port']}")[f"{info['mongo']['dbname']}"]
