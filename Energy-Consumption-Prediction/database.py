from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient("mongodb://127.0.0.1:27017")

db = client["energy_dashboard"]

dataset_collection = db["dataset_records"]
stats_collection = db["dataset_stats"]
