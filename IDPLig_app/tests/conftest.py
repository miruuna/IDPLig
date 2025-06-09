import pytest
from app import app as flask_app
from models import Database
import mongomock
import os

@pytest.fixture
def app():
    """Create a Flask app for testing"""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def mock_db():
    """Create a mock database for testing"""
    # Create a mock MongoDB client
    mock_client = mongomock.MongoClient()
    mock_db = mock_client.db
    
    # Create test data
    test_data = [
        {
            "uniprot_id": "P12345",
            "name": "Test Protein 1",
            "disprot_id": "DP12345",
            "ligands": [
                {"id": "L1", "name": "Ligand 1"},
                {"id": "L2", "name": "Ligand 2"}
            ]
        },
        {
            "uniprot_id": "P67890",
            "name": "Test Protein 2",
            "disprot_id": "DP67890",
            "ligands": [
                {"id": "L3", "name": "Ligand 3"}
            ]
        }
    ]
    
    # Insert test data
    mock_db.idp_data.insert_many(test_data)
    
    # Create a Database instance with the mock client
    db = Database()
    db.client = mock_client
    db.db = mock_db
    db.idp_collection = mock_db.idp_data
    
    return db 