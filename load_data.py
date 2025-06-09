from pymongo import MongoClient
import json
import os
from datetime import datetime
from IDPLig_app.ligands_logic.pdbe_ligands import get_ligand_site_data

def load_data_to_mongodb():
    """Load IDP data from JSON file into MongoDB"""
    # MongoDB connection
    mongo_host = "localhost"  # or your MongoDB host
    mongo_port = 27017
    mongo_username = "admin"
    mongo_password = "password"
    
    # Connect to MongoDB
    client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/")
    db = client["idp_database"]
    idp_collection = db["idp_data"]
    
    try:
        # Clear existing data
        idp_collection.delete_many({})
        print("Cleared existing data from collection")
        
        # Load new data
        with open('IDPLig_app/data/DisProt.json', 'r') as file:
            idp_data = json.load(file)
            if isinstance(idp_data, dict) and "data" in idp_data:
                simplified_data = []
                for item in idp_data["data"]:
                    if isinstance(item, dict):
                        uniprot_id = item.get('acc')
                        if uniprot_id:
                            simplified_doc = {
                                'uniprot_id': uniprot_id,
                                'name': item.get('name'),
                                'disprot_id': item.get('disprot_id'),
                                'ligands': get_ligand_site_data(uniprot_id)
                            }
                            simplified_data.append(simplified_doc)
                
                # Insert all data at once
                if simplified_data:
                    idp_collection.insert_many(simplified_data)
                    print(f"Loaded {len(simplified_data)} documents successfully!")
                    
                    # Save last update timestamp
                    with open('last_update.txt', 'w') as f:
                        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    
                print("IDP data loading completed!")
    except Exception as e:
        print(f"Error loading IDP data: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    load_data_to_mongodb() 