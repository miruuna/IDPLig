# IDPLig

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

IDPLig is a atabase and web application that combines information about intrinsically disordered proteins (IDPs) with their associated ligands. The database integrates data from DISprot and PDBe. It is currently in its very early stages and the plan is to deploy it on a cloud platform.

## Features

- Integration with DISprot database for IDP information
- PDBe integration for ligand data
- MongoDB-based data storage
- Web interface for easy data access
- Docker support for easy deployment
- RESTful API endpoints

## Technology Stack

- **Backend**: Python 3.11, Flask
- **Database**: MongoDB
- **Containerization**: Docker
- **Web Server**: Gunicorn
- **Frontend**: HTML, CSS, JavaScript

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Git

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/miruuna/IDPLig.git
   cd IDPLig
   ```

2. Create and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Build and run with Docker:
   ```bash
   docker-compose up --build -d
   ```

4. Access the application at: http://localhost:5001

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/miruuna/IDPLig.git
   cd IDPLig
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   python IDPLig_app/app.py
   ```

## Usage

The web application provides several key features:

1. Browse IDP entries
2. Search for specific proteins
3. View ligand interactions
4. Access detailed protein information

## API Endpoints

- `/api/idps` - List all IDP entries
- `/api/idps/<id>` - Get specific IDP details
- `/api/ligands` - List all ligands
- `/api/ligands/<id>` - Get specific ligand details
