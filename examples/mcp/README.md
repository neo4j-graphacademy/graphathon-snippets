# MCP Examples

This is an example of an MCP server using a Neo4j database.

- `server/main.py` - A FastMCP server implementation including tools that use Neo4j.
- `client/main.py` - A simple MCP client that you can use to test MCP tools & resources.

## Installation

### Pre-requisites

```bash
pip install -r examples/mcp/requirements.txt
```

### Database

Create a Neo4j databases using the [recommendations dataset](https://github.com/neo4j-graph-examples/recommendations).

Import the movie plot embeddings and create the vector index:

```cypher
LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/rec-embed/movie-plot-embeddings-1k.csv'
AS row
MATCH (m:Movie {movieId: row.movieId})
CALL db.create.setNodeVectorProperty(m, 'plotEmbedding', apoc.convert.fromJsonList(row.embedding));

CREATE VECTOR INDEX moviePlots IF NOT EXISTS
FOR (m:Movie)
ON m.plotEmbedding
OPTIONS {indexConfig: {
 `vector.dimensions`: 1536,
 `vector.similarity_function`: 'cosine'
}};
```

### Environment variables

Create a `.env` file and updated with the environment variables from `.env.example`.

## Run

Run the server first:

```bash
python examples/mcp/server/main.py
```

In a new terminal, run the client:

```bash
python examples/mcp/client/main.py
```

Pick a tool or resource and enter any required values.

## VS Code Agent

To use the mcp tools with the VSCode Agent.

1. Start the server:

    ```bash
    python examples/mcp/server/main.py
    ```

2. Start the server in the `.vscode/mcp.json` configuration.

3. Open a new Agent by running command `Chat: Open Chat (Agent)`.