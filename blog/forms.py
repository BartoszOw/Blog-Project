from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from blog.models import Account
from config import Config
from werkzeug.routing import ValidationError


# Formularz reprezentujący wpis
class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  # Pole do wprowadzania tytułu, wymagane
    body = TextAreaField('Content', validators=[DataRequired()])  # Pole do wprowadzania treści, wymagane
    is_published = BooleanField('Is Published?')  # Pole wyboru, czy wpis jest opublikowany

# Formularz reprezentujący komentarz
class CommentForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])  # Pole do wprowadzania tekstu komentarza, wymagane

# Formularz reprezentujący logowanie
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Pole do wprowadzania nazwy użytkownika, wymagane
    password = PasswordField('Password', validators=[DataRequired()])  # Pole do wprowadzania hasła, wymagane

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=3, max=100)])
    name = StringField('Name',  validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

# Formularz reprezentujący kontakt
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])  # Pole do wprowadzania imienia, wymagane
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])  # Pole do wprowadzania tytułu, wymagane
    message = TextAreaField('Message', validators=[DataRequired()])  # Pole do wprowadzania wiadomości, wymagane