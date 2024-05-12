import os
from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    # Sekretny klucz aplikacji
    SECRET_KEY = config('SECRET_KEY') or 'remember-to-add-key'

    # Token API TMDB
    API_TOKEN = config("TMDB_API_TOKEN")

    # Adres URI bazy danych SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
    )

    # Wyłączenie śledzenia modyfikacji w SQLAlchem
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    #ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')

    # Konfiguracja adresu e-mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD= config("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True