
from django.db.models import Q
from documents.models import Document
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from tmdb import client as tmdb_client



@tool
def search_movies(query: str ,limit:int=5, config: RunnableConfig= {}):
    """
    Search the most recent 5 movies for the  movie database maximum of 25.

    arguments:
    query: string  or lookup search across title or content of movie
    limit: number of results to return
    """

    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    print('Searching for user:', user_id)

    response = tmdb_client.search_movie(query, raw=False)
    if not response.status_code not in range(200, 300):
        return []

    try:
        total_results = int(response.get("total_results"))
    except:
        total_results = -1

    if total_results == 0:
        return []

    if total_results > 25:
        limit = 25
    results = response.get("results")[:limit]

    return results
@tool
def movies_detail(movie_id: int , config: RunnableConfig= {}):
    """
    Movie detail from the Movie Database if it exists.

    arguments:
    movie_id: ID of the movie to retrieve details for
    """

    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    print('Searching for user:', user_id)

    response = tmdb_client.movie_detail(movie_id)

    if not response:
        return None

    return response

movie_discovery_tools = {
    search_movies,
    movies_detail,
}