import requests

from neurocore import settings

url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"


def get_headers():
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_API_KEY}"
    }

def search_movie(query: str, raw=False, page: int = 1):  # Added = before False
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query" : query,
        "page" : page,
        "include_adult": False,
        "language": "en-US",
    }

    headers = get_headers()

    response = requests.get(url , headers=headers , params=params)
    if raw:
        return response
    
    return response.json()


def movie_detail(movie_id: str, raw=False):  # Fixed parameter name and added =
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"  # Added f-string formatting
    
    params = {
        "include_adult": False,
        "language": "en-US",
    }
    
    headers = get_headers()
    response = requests.get(url , headers=headers)
    if raw:
        return response

    return response.json()


