from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from tmdb import client as tmdb_client
from ai.core.contracts import ToolResultContract, ErrorContract


@tool
def search_movies(query: str, limit: int = 5, config: RunnableConfig = {}):
    """
    Search movies from TMDB.

    arguments:
    query: search text for movie lookup
    limit: number of results to return
    """

    try:
        configurable = config.get("configurable") or config.get("metadata") or {}
        user_id = configurable.get("user_id")
        print("Searching for user:", user_id)

        response = tmdb_client.search_movie(query, raw=False)

        try:
            total_results = int(response.get("total_results", 0))
        except (TypeError, ValueError):
            total_results = 0

        if total_results == 0:
            return ToolResultContract(
                status="failure",
                data=None,
                error=ErrorContract(
                    code="NOT_FOUND",
                    message="No movies found for the given query",
                    details={"query": query},
                ),
                meta={"count": 0},
            )

        if limit > 25:
            limit = 25

        results = response.get("results", [])[:limit]

        return ToolResultContract(
            status="success",
            data=results,
            error=None,
            meta={
                "count": len(results),
                "query": query,
                "limit": limit,
            },
        )

    except Exception as exc:
        return ToolResultContract(
            status="failure",
            data=None,
            error=ErrorContract(
                code="TOOL_FAILURE",
                message="Failed to search movies",
                details={"reason": str(exc), "query": query},
            ),
            meta={},
        )


@tool
def movies_detail(movie_id: int, config: RunnableConfig = {}):
    """
    Get movie details from TMDB.

    arguments:
    movie_id: ID of the movie to retrieve details for
    """

    try:
        configurable = config.get("configurable") or config.get("metadata") or {}
        user_id = configurable.get("user_id")
        print("Searching for user:", user_id)

        response = tmdb_client.movie_detail(movie_id)

        if not response:
            return ToolResultContract(
                status="failure",
                data=None,
                error=ErrorContract(
                    code="NOT_FOUND",
                    message="Movie details not found",
                    details={"movie_id": movie_id},
                ),
                meta={},
            )

        return ToolResultContract(
            status="success",
            data=response,
            error=None,
            meta={"movie_id": movie_id},
        )

    except Exception as exc:
        return ToolResultContract(
            status="failure",
            data=None,
            error=ErrorContract(
                code="TOOL_FAILURE",
                message="Failed to fetch movie details",
                details={"reason": str(exc), "movie_id": movie_id},
            ),
            meta={},
        )


movie_discovery_tools = [
    search_movies,
    movies_detail,
]