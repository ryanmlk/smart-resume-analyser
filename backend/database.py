from pymongo import MongoClient
import logging
import os
from datetime import datetime

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "smart_resume_analyzer"
COLLECTION_NAME = "resumes"

class Database:
    def __init__(self, uri=MONGO_URI, db_name=DB_NAME):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[COLLECTION_NAME]
        logging.info(f"Connected to MongoDB: {db_name}")

    def insert_resume(self, resume_data: dict):
        """Inserts a parsed resume into the database."""
        resume_data["created_at"] = datetime.utcnow()
        result = self.collection.insert_one(resume_data)
        return str(result.inserted_id)

    def get_resume(self, resume_id: str):
        """Retrieves a resume by ID."""
        from bson.objectid import ObjectId
        return self.collection.find_one({"_id": ObjectId(resume_id)})

    def get_all_resumes(self):
        """Retrieves all resumes."""
        return list(self.collection.find({}, {"_id": 1, "name": 1, "email": 1, "score": 1, "created_at": 1}))

# Singleton instance
db = Database()
