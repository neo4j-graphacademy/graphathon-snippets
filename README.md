# Graphathon Code Snippets

A set of code snippets to help you get started with Neo4j at the Graphathon. This repository provides practical examples of how to:

1. Connect to and work with Neo4j databases
2. Load data from external sources like BigQuery
3. Create graph structures with nodes and relationships
4. Visualize graph data using modern tools

## Repository Structure

- `notebooks/` - Jupyter notebooks with interactive examples
- `pyproject.toml` - Project dependencies and configuration

## Purpose

These examples are designed to be generic starting points that you can adapt for your Graphathon projects. The specific implementation details are less important than understanding the patterns and techniques demonstrated.

## Prerequisites

- Python 3.13+
- Neo4j database (local, cloud, or Docker)
- Google Cloud access (for BigQuery examples)
- Docker and Docker Compose (for local Neo4j setup)

## Environment Setup

### Option 1: Docker Setup (Recommended)

The easiest way to get started is using Docker Compose to run Neo4j Enterprise with APOC and Graph Data Science plugins:

```bash
# Start Neo4j Enterprise with all plugins
docker-compose up -d

# Access Neo4j Browser at http://localhost:7474
# Default credentials: neo4j/password123
```

The Docker setup includes:
- Neo4j 5.15 Enterprise Edition
- APOC plugin for extended procedures
- Graph Data Science (GDS) plugin
- Persistent data volumes

### Option 2: Manual Setup

Create a `.env` file in the root directory with the following variables:

```env
# Neo4j Database Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123

# For Neo4j AuraDB (cloud), use the connection string provided
# NEO4J_URI=neo4j+s://xxxxxx.databases.neo4j.io
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your_aura_password

# Google Cloud BigQuery (optional - for BigQuery examples)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
# Or use: gcloud auth application-default login

# BigQuery Project Settings (optional)
GOOGLE_CLOUD_PROJECT=your-project-id
```

## Installation

```bash
# Install dependencies using uv (recommended)
uv sync

# Or using pip
pip install google-cloud-bigquery>=3.36.0 ipykernel>=6.30.1 neo4j>=5.28.2 pandas>=2.3.2 yfiles-jupyter-graphs-for-neo4j>=1.7.0
```

## Usage

Start Jupyter Lab and explore the example notebooks:

```bash
# Start Jupyter Lab
jupyter lab

# Open notebooks in the notebooks/ folder
```

## Key Dependencies

This project includes several powerful tools for working with Neo4j:

- **neo4j**: Official Neo4j Python driver for database connections
- **google-cloud-bigquery**: For accessing BigQuery datasets
- **pandas**: Data manipulation and analysis
- **yfiles-jupyter-graphs-for-neo4j**: Advanced graph visualization in Jupyter
- **ipykernel**: Jupyter kernel support

## Getting Started

### Quick Start with Docker

1. Start Neo4j with Docker: `docker-compose up -d`
2. Install Python dependencies: `uv sync`
3. Start Jupyter Lab: `jupyter lab`
4. Open and run the example notebooks
5. Adapt the patterns for your Graphathon project

### Manual Setup

1. Set up your `.env` file with the required credentials
2. Install dependencies with `uv sync`
3. Start your Neo4j instance
4. Start Jupyter Lab with `jupyter lab`
5. Open and run the example notebooks
6. Adapt the patterns for your Graphathon project

## Troubleshooting

- **Neo4j Connection Error**: Verify your Neo4j instance is running and credentials in `.env` are correct
  - For Docker: Check with `docker-compose ps` and `docker-compose logs neo4j`
- **BigQuery Authentication Error**: Check your Google Cloud credentials and project settings
- **Missing Dependencies**: Run `uv sync` to ensure all packages are installed
- **Docker Issues**: Ensure Docker is running and you have enough memory allocated (at least 4GB recommended)
- **Plugin Issues**: APOC and GDS plugins are automatically installed in the Docker setup

## For Graphathon Participants

These code snippets provide foundational patterns for:
- Connecting to Neo4j databases
- Loading data from various sources
- Creating graph structures
- Visualizing results

Use these examples as starting points and modify them for your specific Graphathon use case. The goal is to help you get up and running quickly with Neo4j!

