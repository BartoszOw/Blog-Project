import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    # Sekretny klucz aplikacji
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'remember-to-add-key'

    # Token API TMDB
    API_TOKEN = os.environ.get("TMDB_API_TOKEN", "")

    # Adres URI bazy danych SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
    )

    # Wyłączenie śledzenia modyfikacji w SQLAlchem
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    #ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    # Domyślny adres e-mail
    PRIMARY_MAIL = os.environ.get('PRIMARY_MAIL', 'owbartosz.pl@gmail.com')