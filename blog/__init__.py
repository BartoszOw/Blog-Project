from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from blog import routes, models

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Entry': models.Entry,
        'Comment': models.Comment,
        'Account': models.Account,
        'session': session,
        'mail': mail
    }

