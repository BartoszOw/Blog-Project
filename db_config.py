from faker import Faker
from blog.models import Entry, db, Comment, Account
from blog import app,db


# Generowanie wpisów
def generate_entries(how_many=10):
    fake = Faker()

    # Tworzenie określonej liczby wpisów
    for i in range(how_many):
        post = Entry(
            title=fake.sentence(),  # Losowy tytuł
            body='\n'.join(fake.paragraphs(15)),  # Losowa treść składająca się z 15 akapitów
            is_published=True  # Wpis jest opublikowany
        )
        db.session.add(post)
    db.session.commit()

# Generowanie komentarzy
def generate_comments(how_many=5):
    fake = Faker()
    entries = Entry.query.all()  # Pobranie wszystkich wpisów

    # Dla każdego wpisu generowane są komentarze
    for entry in entries:
        for i in range(how_many):
            comment = Comment(
                text=fake.paragraph(),  # Losowy tekst komentarza
                entry_id=entry.id  # Identyfikator wpisu, do którego należy komentarz
            )
            db.session.add(comment)
    db.session.commit()

# Generowanie kont użytkowników
def generate_accounts(how_many=5):
    fake = Faker()

    # Tworzenie określonej liczby kont
    for i in range(how_many):
        account = Account(
            username=fake.user_name(),  # Losowa nazwa użytkownika
            password=fake.password()  # Losowe hasło
        )
        db.session.add(account)
    db.session.commit()


#with app.app_context():
#    generate_accounts()
#    generate_entries()
#    generate_comments()


