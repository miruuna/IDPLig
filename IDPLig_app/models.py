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
        """Load IDP data from JSON file into MongoDB, extracting only acc and name"""
        try:
            with open('data/DisProt.json', 'r') as file:
                idp_data = json.load(file)
                if isinstance(idp_data, dict) and "data" in idp_data:
                    # Extract only acc and name from each document
                    simplified_data = []
                    for item in idp_data["data"]:
                        if isinstance(item, dict):
                            simplified_doc = {
                                'acc': item.get('acc'),
                                'name': item.get('name'),
                                'disprot_id': item.get('disprot_id')
                            }
                            if simplified_doc['acc'] and simplified_doc['name'] and simplified_doc['disprot_id']:  
                                simplified_data.append(simplified_doc)
                    
                    # Insert all data at once
                    if simplified_data:
                        self.idp_collection.insert_many(simplified_data)
                        print(f"Loaded {len(simplified_data)} documents successfully!")
                print("IDP data loading completed!")
        except Exception as e:
            print(f"Error loading IDP data: {str(e)}")

    def get_all_idp_data(self):
        """Retrieve all IDP data from the database"""
        return list(self.idp_collection.find())

    def get_idp_by_id(self, idp_id):
        """Retrieve specific IDP data by ID"""
        return self.idp_collection.find_one({"acc": idp_id})

    def search_idp_data(self, query):
        """Search IDP data based on various fields"""
        search_query = {}
        if query:
            search_query = {
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"acc": {"$regex": query, "$options": "i"}}
                ]
            }
        return list(self.idp_collection.find(search_query))

    def get_idp_statistics(self):
        """Get basic statistics about the IDP data"""
        total = self.idp_collection.count_documents({})
        return {
            "total_entries": total,
            "unique_proteins": len(self.idp_collection.distinct("acc"))
        }

# Create a database instance
db = Database()
