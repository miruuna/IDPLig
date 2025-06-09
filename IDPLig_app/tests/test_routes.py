import pytest
from flask import url_for

def test_home_page(client):
    """Test the home page route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'IDPLig' in response.data

def test_about_page(client):
    """Test the about page route"""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_data_page(client, mock_db):
    """Test the data page route"""
    # Test without search query
    response = client.get('/data')
    assert response.status_code == 200
    assert b'Test Protein 1' in response.data
    assert b'Test Protein 2' in response.data
    
    # Test with search query
    response = client.get('/data?search=Test Protein 1')
    assert response.status_code == 200
    assert b'Test Protein 1' in response.data
    assert b'Test Protein 2' not in response.data

def test_view_idp(client, mock_db):
    """Test viewing a specific IDP"""
    # Test existing IDP
    response = client.get('/idp/P12345')
    assert response.status_code == 200
    assert b'Test Protein 1' in response.data
    assert b'Ligand 1' in response.data
    assert b'Ligand 2' in response.data
    
    # Test non-existing IDP
    response = client.get('/idp/NONEXISTENT')
    assert response.status_code == 302  # Redirect status code

def test_check_data(client, mock_db):
    """Test the check data route"""
    # Test without uniprot_id
    response = client.get('/check_data')
    assert response.status_code == 302  # Redirect status code
    
    # Test with uniprot_id
    response = client.get('/check_data/P12345')
    assert response.status_code == 302  # Redirect status code 