import requests
import random
from config import Config
from dotenv import load_dotenv

load_dotenv()

def make_tmdb_request(endpoint):
    headers = {'Authorization': f'Bearer {Config.API_TOKEN}'}
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

def get_movies_list(list_type):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    return make_tmdb_request(endpoint)

def get_poster_url(poster_api_path, size='w342'):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many, list_type='popular'):
    data = get_movies_list(list_type)
    movies = random.sample(data['results'], k=how_many)
    return movies
