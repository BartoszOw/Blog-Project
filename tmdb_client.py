import requests
import random
from config import Config
from dotenv import load_dotenv

load_dotenv()

# Funkcja wysyłająca zapytanie do API TMDB
def make_tmdb_request(endpoint):
    headers = {'Authorization': f'Bearer {Config.API_TOKEN}'}  # Ustawienie nagłówka autoryzacyjnego
    response = requests.get(endpoint, headers=headers)  # Wysłanie zapytania
    response.raise_for_status()  # Rzuca wyjątek, jeśli wystąpił błąd w odpowiedzi
    return response.json()  # Zwraca odpowiedź w formacie JSON

# Funkcja pobierająca listę filmów z API TMDB
def get_movies_list(list_type):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"  # Tworzenie adresu URL zgodnego z listą filmów
    return make_tmdb_request(endpoint)  # Wywołanie funkcji wysyłającej zapytanie i zwracającej wynik

# Funkcja tworząca adres URL do plakatu filmowego
def get_poster_url(poster_api_path, size='w342'):
    base_url = "https://image.tmdb.org/t/p/"  # Podstawowy adres URL dla plakatów
    return f"{base_url}{size}/{poster_api_path}"  # Zwraca pełny adres URL do plakatu o podanym rozmiarze

# Funkcja pobierająca listę losowych filmów
def get_movies(how_many, list_type='popular'):
    data = get_movies_list(list_type)  # Pobieranie listy filmów z podanego typu
    movies = random.sample(data['results'], k=how_many)  # Losowy wybór określonej liczby filmów
    return movies  # Zwraca listę wybranych filmów