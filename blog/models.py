from . import db
import datetime

# Model reprezentujący wpis
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identyfikator wpisu
    title = db.Column(db.String(80), nullable=False)  # Tytuł wpisu
    body = db.Column(db.Text, nullable=False)  # Treść wpisu
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)  # Data publikacji
    is_published = db.Column(db.Boolean, default=False)  # Czy wpis jest opublikowany
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    comments = db.relationship('Comment', backref='entry', lazy=True)  # Relacja z komentarzami

# Model reprezentujący komentarz
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identyfikator komentarza
    text = db.Column(db.Text, nullable=False)  # Treść komentarza
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)  # Klucz obcy do powiązanego wpisu
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)  # Klucz obcy do powiązanego konta użytkownika

# Model reprezentujący konto użytkownika
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identyfikator konta
    name = db.Column(db.String(100), nullable=False) # Imie i Nazwisko
    username = db.Column(db.String(100), unique=True, nullable=False)  # Nazwa użytkownika
    password = db.Column(db.String(100), nullable=False)  # Hasło użytkownika
    email = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow) # Data dolaczenia
    comments = db.relationship('Comment', backref='account', lazy=True)  # Relacja jeden do wielu z komentarzami
    entries = db.relationship('Entry', backref='account', lazy=True)