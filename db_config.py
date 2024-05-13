from faker import Faker
from blog.models import Entry, db, Comment, Account
from blog import app,db
import random


# Generowanie wpisów
def generate_entries():
    fake = Faker()
    accounts = Account.query.all()

    # Tworzenie określonej liczby wpisów
    selected_accounts = random.choice(accounts)
    for i in range(random.randint(1, 10)):
        post = Entry(
            title=fake.sentence(),  # Losowy tytuł
            body='\n'.join(fake.paragraphs(15)),  # Losowa treść składająca się z 15 akapitów
            is_published=True,  # Wpis jest opublikowany
            account_id=selected_accounts.id
        )
        db.session.add(post)
        selected_accounts = random.choice(accounts)
    db.session.commit()

# Generowanie komentarzy
def generate_comments():
    fake = Faker()
    entries = Entry.query.all()  # Pobranie wszystkich wpisów
    accounts = Account.query.all()  # Pobranie wszystkich kont
    

    # Dla każdego wpisu generowane są komentarze
    for entry in entries:
        # Wybierz losowego użytkownika dla każdego wpisu
        selected_accounts = random.choice(accounts)
        for entry in entries:
            for i in range(random.randint(1, 3)):
                comment = Comment(
                    text=fake.paragraph(),  # Losowy tekst komentarza
                    entry_id=entry.id,  # Identyfikator wpisu, do którego należy komentarz
                    account_id=selected_accounts.id  # Identyfikator konta użytkownika, który utworzył komentarz
                )
                db.session.add(comment)
                selected_accounts = random.choice(accounts)
    db.session.commit()

# Generowanie kont użytkowników
def generate_accounts():
    fake = Faker()

    # Tworzenie określonej liczby kont
    for i in range(random.randint(1, 15)):
        account = Account(
            name=fake.name(),
            username=fake.user_name(),  # Losowa nazwa użytkownika
            password=fake.password(),  # Losowe hasło
            email=fake.email()
        )
        db.session.add(account)
    db.session.commit()


with app.app_context():
#    generate_accounts()
#    generate_entries()
    generate_comments()


