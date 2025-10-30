import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

# from neo4j import AsyncGraphDatabase, AsyncDriver
from neo4j import GraphDatabase, Driver
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever, Text2CypherRetriever

from mcp.server.fastmcp import FastMCP, Context



# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

@dataclass
class AppContext:
    """Application context with Neo4j driver."""
    driver: Driver
    database: str

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage Neo4j driver lifecycle."""

    # Read connection details from environment
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE")

    # Initialize driver on startup
    driver = GraphDatabase.driver(uri, auth=(username, password))

    try:
        # Yield context with driver
        yield AppContext(driver=driver, database=database)
    finally:
        # Close driver on shutdown
        driver.close()

# Create server with lifespan
mcp = FastMCP("Movies GraphRAG Server", lifespan=app_lifespan)

@mcp.tool()
async def graph_statistics(ctx: Context) -> dict[str, int]:
    """Count the number of nodes and relationships in the graph."""

    # Access the driver from lifespan context
    driver = ctx.request_context.lifespan_context.driver
    database = ctx.request_context.lifespan_context.database

    # Use the driver to query Neo4j with the correct database
    records, summary, keys = driver.execute_query(
        r"RETURN COUNT {()} AS nodes, COUNT {()-[]-()} AS relationships",
        database_=database
    )

    # Process the results
    if records:
        return dict(records[0])
    return {"nodes": 0, "relationships": 0}

@mcp.tool()
async def search_movies_by_title(title: str, ctx: Context = None) -> list[dict]:
    """
    Search for movies by a title.

    Args:
        title: The title of the movie 
        ctx: Context object (injected automatically)

    Returns:
        List of movies with tmdbId, title, plot and release date.
    """
    await ctx.info(f"Searching for a movie by title : {title}")

    driver = ctx.request_context.lifespan_context.driver
    database = ctx.request_context.lifespan_context.database

    try:
        records, _, _ = driver.execute_query(
            """
            MATCH (m:Movie)
            WHERE toLower(m.title) CONTAINS toLower($title)
            RETURN 
                m.tmdbId AS tmdbId,
                m.title AS title,
                m.plot AS plot,
                m.released AS released
            """,
            title=title,
            database_=database
        )

        if not records:
            await ctx.warning(f"No movies found with a title containing '{title}'")
            return f"No movies found with a title containing '{title}'"
        
        return [record.data() for record in records]
    
    except Exception as e:
        await ctx.error(f"Failed to find movie by title: {str(e)}")
        raise


@mcp.tool()
async def search_movies_by_plot(plot: str, top_k: int = 6, ctx: Context = None) -> list[str]:
    """
    Search for movies similar to the given plot description.

    Args:
        plot: The plot of the movie use in the semantic search 
        top_k: The number of similar movies to return
        ctx: Context object (injected automatically)

    Returns:
        List of movies with title, tmdbId and plot ordered by similarity score.
    """
    await ctx.info(f"Searching for a movie by plot : {plot}")

    driver = ctx.request_context.lifespan_context.driver
    database = ctx.request_context.lifespan_context.database

    try:
        embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
        
        # Create retriever
        retriever = VectorRetriever(
            driver,
            neo4j_database=database,
            index_name="moviePlots",
            embedder=embedder,
            return_properties=["title", "tmdbId", "plot"],
        )

        result = retriever.search(query_text=plot, top_k=top_k)
        movies = []
        for item in result.items:
            movies.append(item.content)
        
        return movies
    
    except Exception as e:
        await ctx.error(f"Failed to find movie by plot: {str(e)}")
        raise

@mcp.tool()
async def get_movie_information_by_tmdbId(tmdbId: str, ctx: Context) -> str:
    """
    Get details information about a specific movie.

    Args:
        tmdbId: The TMDB ID of the movie (e.g., "603" for The Matrix)

    Returns:
        Formatted string with movie details including title, plot, cast, and genres
    """
    await ctx.info(f"Fetching movie details for TMDB ID: {tmdbId}")

    driver = ctx.request_context.lifespan_context.driver
    database = ctx.request_context.lifespan_context.database

    try:
        records, _, _ = driver.execute_query(
            """
            MATCH (m:Movie {tmdbId: $tmdbId})
            RETURN m.title AS title,
               m.released AS released,
               m.tagline AS tagline,
               m.runtime AS runtime,
               m.plot AS plot,
               [ (m)-[:IN_GENRE]->(g:Genre) | g.name ] AS genres,
               [ (p)-[r:ACTED_IN]->(m) | {name: p.name, role: r.role} ] AS actors,
               [ (d)-[:DIRECTED]->(m) | d.name ] AS directors
            """,
            tmdbId=tmdbId,
            database_=database
        )

        if not records:
            await ctx.warning(f"Movie with TMDB ID {tmdbId} not found")
            return f"Movie with TMDB ID {tmdbId} not found in database"

        movie = records[0].data()

        # Format the output
        output = []
        output.append(f"# {movie['title']} ({movie['released']})")
        output.append("")

        if movie['tagline']:
            output.append(f"_{movie['tagline']}_")
            output.append("")

        output.append(f"**Runtime:** {movie['runtime']} minutes")
        output.append(f"**Genres:** {', '.join(movie['genres'])}")

        if movie['directors']:
            output.append(f"**Director(s):** {', '.join(movie['directors'])}")

        output.append("")
        output.append("## Plot")
        output.append(movie['plot'])

        if movie['actors']:
            output.append("")
            output.append("## Cast")
            for actor in movie['actors']:
                if actor['role']:
                    output.append(f"- {actor['name']} as {actor['role']}")
                else:
                    output.append(f"- {actor['name']}")

        result = "\n".join(output)

        await ctx.info(f"Successfully fetched details for '{movie['title']}'")

        return result

    except Exception as e:
        await ctx.error(f"Failed to fetch movie: {str(e)}")
        raise

@mcp.tool()
async def catch_all_query_movie_database(query: str, ctx: Context) -> dict:
    """
    Query the database with a natural language question.

    Args:
        query: The natural language question about the movie database

    Returns:
        List of results
    """
    pass

    driver = ctx.request_context.lifespan_context.driver
    database = ctx.request_context.lifespan_context.database

    # Create Cypher LLM 
    t2c_llm = OpenAILLM(
        model_name="gpt-4o", 
        model_params={"temperature": 0}
    )

    # Specify your own Neo4j schema
    neo4j_schema = """
    Node properties:
    Person {name: STRING, born: INTEGER}
    Movie {tagline: STRING, title: STRING, released: INTEGER}
    Genre {name: STRING}
    User {name: STRING}

    Relationship properties:
    ACTED_IN {role: STRING}
    RATED {rating: INTEGER}

    The relationships:
    (:Person)-[:ACTED_IN]->(:Movie)
    (:Person)-[:DIRECTED]->(:Movie)
    (:User)-[:RATED]->(:Movie)
    (:Movie)-[:IN_GENRE]->(:Genre)
    """
    
    # Cypher examples as input/query pairs
    examples = [
        "USER INPUT: 'Get user ratings for a movie?' QUERY: MATCH (u:User)-[r:RATED]->(m:Movie) WHERE m.title = 'Movie Title' RETURN r.rating"
        "USER INPUT: 'Get details for this case sensitive name property' QUERY: MATCH (n) WHERE toLower(n.name) CONTAINS toLower(name) RETURN n"
    ]

    # Build the retriever
    retriever = Text2CypherRetriever(
        driver=driver,
        neo4j_database=database,
        llm=t2c_llm,
        neo4j_schema=neo4j_schema,
        examples=examples,
    )

    result = retriever.search(query_text=query)

    results = {
        "cypher": result.metadata["cypher"],
        "records": [item.content for item in result.items]
    }
    # for item in result.items:
    #     results["records"].append(item.content)
    
    return results


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
