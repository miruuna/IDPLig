import pytest
from models import Database

def test_get_all_idp_data(mock_db):
    """Test retrieving all IDP data"""
    data = mock_db.get_all_idp_data()
    assert len(data) == 2
    assert data[0]["uniprot_id"] == "P12345"
    assert data[1]["uniprot_id"] == "P67890"

def test_get_idp_by_id(mock_db):
    """Test retrieving a specific IDP by ID"""
    # Test existing IDP
    idp = mock_db.get_idp_by_id("P12345")
    assert idp is not None
    assert idp["name"] == "Test Protein 1"
    
    # Test non-existing IDP
    idp = mock_db.get_idp_by_id("NONEXISTENT")
    assert idp is None

def test_search_idp_data(mock_db):
    """Test searching IDP data"""
    # Test search by name
    results = mock_db.search_idp_data("Test Protein 1")
    assert len(results) == 1
    assert results[0]["uniprot_id"] == "P12345"
    
    # Test search by uniprot_id
    results = mock_db.search_idp_data("P67890")
    assert len(results) == 1
    assert results[0]["name"] == "Test Protein 2"
    
    # Test search with no results
    results = mock_db.search_idp_data("NONEXISTENT")
    assert len(results) == 0

def test_get_ligands(mock_db):
    """Test retrieving ligands for an IDP"""
    # Test existing IDP with ligands
    ligands = mock_db.get_ligands("P12345")
    assert len(ligands) == 2
    assert ligands[0]["id"] == "L1"
    assert ligands[1]["id"] == "L2"
    
    # Test non-existing IDP
    ligands = mock_db.get_ligands("NONEXISTENT")
    assert len(ligands) == 0

def test_get_idp_statistics(mock_db):
    """Test getting IDP statistics"""
    stats = mock_db.get_idp_statistics()
    assert stats["total_entries"] == 2
    assert stats["unique_proteins"] == 2
    assert stats["total_ligands"] == 3  # 2 ligands for first protein + 1 for second 