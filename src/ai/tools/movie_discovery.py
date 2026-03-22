from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from tmdb import client as tmdb_client
from ai.core.contracts import ToolResultContract, ErrorContract
from ai.core.logger import log_event


@tool
def search_movies(query: str, limit: int = 5, config: RunnableConfig = {}):
    """
    Search movies from TMDB.

    arguments:
    query: search text for movie lookup
    limit: number of results to return
    """

    configurable = config.get("configurable") or config.get("metadata") or {}
    user_id = configurable.get("user_id")
    request_id = configurable.get("request_id")
    trace = configurable.get("trace")

    try:
        log_event(
            event="tool_started",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="search_movies",
            user_id=user_id,
            query=query,
            limit=limit,
        )
        if trace:
            trace.add_step(
                layer="tool",
                event="tool_started",
                tool_name="search_movies",
                user_id=user_id,
                query=query,
                limit=limit,
            )

        response = tmdb_client.search_movie(query, raw=False)

        try:
            total_results = int(response.get("total_results", 0))
        except (TypeError, ValueError):
            total_results = 0

        if total_results == 0:
            log_event(
                event="tool_failed",
                layer="tool",
                request_id=request_id or "unknown",
                tool_name="search_movies",
                error_code="NOT_FOUND",
                query=query,
            )
            if trace:
                trace.add_step(
                    layer="tool",
                    event="tool_failed",
                    tool_name="search_movies",
                    error_code="NOT_FOUND",
                    query=query,
                )

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

        log_event(
            event="tool_succeeded",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="search_movies",
            result_count=len(results),
        )
        if trace:
            trace.add_step(
                layer="tool",
                event="tool_succeeded",
                tool_name="search_movies",
                result_count=len(results),
            )

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
        log_event(
            event="tool_failed",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="search_movies",
            error_code="TOOL_FAILURE",
            error_message=str(exc),
        )
        if trace:
            trace.add_step(
                layer="tool",
                event="tool_failed",
                tool_name="search_movies",
                error_code="TOOL_FAILURE",
                error_message=str(exc),
            )

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

    configurable = config.get("configurable") or config.get("metadata") or {}
    user_id = configurable.get("user_id")
    request_id = configurable.get("request_id")
    trace = configurable.get("trace")

    try:
        log_event(
            event="tool_started",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="movies_detail",
            user_id=user_id,
            movie_id=movie_id,
        )
        if trace:
            trace.add_step(
                layer="tool",
                event="tool_started",
                tool_name="movies_detail",
                user_id=user_id,
                movie_id=movie_id,
            )

        response = tmdb_client.movie_detail(movie_id)

        if not response:
            log_event(
                event="tool_failed",
                layer="tool",
                request_id=request_id or "unknown",
                tool_name="movies_detail",
                error_code="NOT_FOUND",
                movie_id=movie_id,
            )
            if trace:
                trace.add_step(
                    layer="tool",
                    event="tool_failed",
                    tool_name="movies_detail",
                    error_code="NOT_FOUND",
                    movie_id=movie_id,
                )

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

        log_event(
            event="tool_succeeded",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="movies_detail",
            movie_id=movie_id,
        )
        if trace:
            trace.add_step(
                layer="tool",
                event="tool_succeeded",
                tool_name="movies_detail",
                movie_id=movie_id,
            )

        return ToolResultContract(
            status="success",
            data=response,
            error=None,
            meta={"movie_id": movie_id},
        )

    except Exception as exc:
        log_event(
            event="tool_failed",
            layer="tool",
            request_id=request_id or "unknown",
            tool_name="movies_detail",
            error_code="TOOL_FAILURE",
            error_message=str(exc),
        )
        if trace:
            trace.add_step(
                layer="tool",
                event="tool_failed",
                tool_name="movies_detail",
                error_code="TOOL_FAILURE",
                error_message=str(exc),
            )

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