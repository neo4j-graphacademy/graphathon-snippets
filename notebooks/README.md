# Graphathon

Notebook walkthroughs for commonly used activities.

## Environment Setup

### Option 1: Docker Setup (Recommended)

The easiest way to get started is using Docker Compose to run Neo4j Enterprise with APOC and Graph Data Science plugins:

```bash
# Start Neo4j Enterprise with all plugins
docker-compose up -d

# Access Neo4j Browser at http://localhost:7474
# Default credentials: neo4j/neoneoneo
```

The Docker setup includes:
- Neo4j Enterprise Edition
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
- **neo4j_graphrag**: Neo4j GraphRAG, Retrievers and Knowledge Graph pipelines
- **google-cloud-bigquery**: For accessing BigQuery datasets
- **pandas**: Data manipulation and analysis
- **yfiles-jupyter-graphs-for-neo4j**: Advanced graph visualization in Jupyter
- **ipykernel**: Jupyter kernel support
- **mcp**: FastMCP server and tools

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

## Examples

## Troubleshooting

- **Neo4j Connection Error**: Verify your Neo4j instance is running and credentials in `.env` are correct
  - For Docker: Check with `docker-compose ps` and `docker-compose logs neo4j`
- **BigQuery Authentication Error**: Check your Google Cloud credentials and project settings
- **Missing Dependencies**: Run `uv sync` to ensure all packages are installed
- **Docker Issues**: Ensure Docker is running and you have enough memory allocated (at least 4GB recommended)
- **Plugin Issues**: APOC and GDS plugins are automatically installed in the Docker setup

