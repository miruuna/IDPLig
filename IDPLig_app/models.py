from pymongo import MongoClient
import os
import json

class Database:
    def __init__(self):
        mongo_host = os.environ.get("MONGO_HOST", "localhost")
        mongo_username = os.environ.get("MONGO_USERNAME", "admin")
        mongo_password = os.environ.get("MONGO_PASSWORD", "password")
        self.client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:27017/")
        self.db = self.client["idp_database"]
        self.idp_collection = self.db["idp_data"]
        
        # Load data automatically if collection is empty
        if self.idp_collection.count_documents({}) == 0:
            self._load_initial_data()

    def _load_initial_data(self):
        """Load IDP data from JSON file into MongoDB"""
        try:
            with open('data/DisProt.json', 'r') as file:
                idp_data = json.load(file)
                if isinstance(idp_data, list):
                    self.idp_collection.insert_many(idp_data)
                else:
                    self.idp_collection.insert_one(idp_data)
                print("IDP data loaded successfully!")
        except Exception as e:
            print(f"Error loading IDP data: {str(e)}")

    def get_all_idp_data(self):
        """Retrieve all IDP data from the database"""
        return list(self.idp_collection.find())

    def get_idp_by_id(self, idp_id):
        """Retrieve specific IDP data by ID"""
        return self.idp_collection.find_one({"id": idp_id})

    def search_idp_data(self, query):
        """Search IDP data based on various fields"""
        search_query = {}
        if query:
            search_query = {
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                    {"uniprot_id": {"$regex": query, "$options": "i"}}
                ]
            }
        return list(self.idp_collection.find(search_query))

    def get_idp_statistics(self):
        """Get basic statistics about the IDP data"""
        total = self.idp_collection.count_documents({})
        return {
            "total_entries": total,
            "unique_proteins": len(self.idp_collection.distinct("uniprot_id")),
            "disorder_regions": self.idp_collection.count_documents({"type": "disorder"})
        }

# Create a database instance
db = Database()
