from flask import render_template, request,abort, redirect, url_for, flash, session
from flask_login import login_user
from blog import app
from blog.models import Entry, Comment, db, Account
from blog.forms import EntryForm, LoginForm, ContactForm, CommentForm
import tmdb_client
import datetime
import functools

# Lista typów filmów
LIST_TYPES = [
    {'name': "Now Playing", 'type': "now_playing"},
    {'name': "Top Rated", 'type': "top_rated"},
    {'name': "Upcoming", 'type': "upcoming"},
    {'name': "Popular", 'type': "popular"}
]

# Funkcja zwracająca listę typów filmów
def get_list_types():
    return LIST_TYPES

# Kontekst procesora w aplikacji
@app.context_processor
def inject_list_types():
    return dict(list_types=get_list_types())

# Procesor narzędziowy
@app.context_processor
def utility_processor():

    # Funkcja zwracająca adres URL obrazu TMDB
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    
    return {'tmdb_image_url': tmdb_image_url}

# Dekorator sprawdzający, czy użytkownik jest zalogowany
def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args,**kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login_page', next=request.path))
    return check_permissions

# Strona logowania
@app.route('/login', methods=['GET', 'POST'])
def login_page():

    # Logika logowania użytkownika
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            account = Account.query.filter_by(username=username).first()
            if account and account.password == password:
                session['logged_in'] = True
                session.permanent = True
                flash("You are now logged in.", category="success")
                return redirect(next_url or url_for('index'))
            else:
                errors = 'Invalid username or password'
    return render_template('login_form.html', form=form, errors=errors)


# Wylogowanie użytkownika
@app.route('/logout/', methods=["GET","POST"])
def logout():

    # Logika wylogowywania użytkownika
    if request.method == "POST":
        session.clear()
        flash('You are now logged out', category='danger')
    return redirect(url_for('index'))   

# Wyniki wyszukiwania
@app.route('/search_results', methods=['GET'])
def search():

    # Logika wyszukiwania
    query = request.args.get('search_bar', '')

    if query:
        search_result = Entry.query.filter(Entry.title.ilike(f'%{query}%') | Entry.body.ilike(f"%{query}%")).all()
    else:
        return redirect(url_for('index'))

    comments_count = {entry.id: len(entry.comments) for entry in search_result}
    return render_template('search.html', search_result=search_result, query=query, comments_count=comments_count)

@app.route('/<select_list>')
@login_required
def movies_page(select_list):
    
    valid_list_types = [lst['type'] for lst in LIST_TYPES]

    if select_list not in valid_list_types:
        return redirect(url_for('movies_page', select_list='popular'))
    
    movies = tmdb_client.get_movies(16, list_type=select_list)

    return render_template('movies.html', movies=movies, list=LIST_TYPES, selected_list=select_list)

def posts(limit=None):

    if limit is None:
        all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    else:
        all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).limit(limit).all()

    comments_count = {entry.id: len(entry.comments) for entry in all_posts}
    return render_template('homepage.html', all_posts=all_posts, comments_count=comments_count)

# Strona główna
@app.route('/')
def index():
    
    # Wyświetlenie wpisów na stronie głównej
    return posts(limit=4)

# Wyświetlenie wszystkich wpisów
@app.route('/post_all') 
def post_all():

    # Wyświetlenie wszystkich wpisów
    return posts()

# Szczegóły wpisu
@app.route('/post/<post_id>', methods=['GET', 'POST'])
def entry_details(post_id):

    # Logika wyświetlania i dodawania komentarzy
    entry = Entry.query.get(post_id)
    all_comments = Comment.query.filter_by(entry_id=post_id).order_by(Comment.id.desc()).all()
    
    if entry is None:
        abort(404)

    form = CommentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            text = form.text.data
            comment = Comment(text=text, entry_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', category='success')
            return redirect(request.url)
        else:
            flash('Error adding comment. Please check your input.', 'error')
    return render_template('entry_details.html', entry=entry, form=form, comments=all_comments)



# Dodanie nowego wpisu
@app.route('/new_post', methods=['GET','POST'])
@login_required
def create_entry():

    # Logika dodawania nowego wpisu
    return manage_entry(entry_id=None, action='Add a new Entry')

# Edycja istniejącego wpisu
@app.route('/edit_post/<int:entry_id>', methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    
    # Logika edycji wpisu
    return manage_entry(entry_id, action='Modify a Entry')

def manage_entry(entry_id, action):
    entry = None
    if entry_id:
        entry = Entry.query.get_or_404(entry_id)
    
    form = EntryForm(obj=entry)
    errors = None

    if form.validate_on_submit():
        if not entry:
            entry = Entry()
        form.populate_obj(entry)
        db.session.add(entry)
        db.session.commit()
        flash("Successfully Entry Added" if not entry_id else "Successfully Entry Modified", category="success")
        return redirect(url_for('index'))
    else:
        errors = form.errors
    
    return render_template('entry_form.html', form=form, errors=errors, action=action)

# Wyświetlenie listy nieopublikowanych wpisów
@app.route('/unpublished_list', methods=['GET'])
@login_required
def unpublished_list():

    # Logika wyświetlania nieopublikowanych wpisów
    un_list = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template('unpublished_list.html', un_list=un_list)


# Usunięcie wpisu
@app.route('/delete_entry', methods=['POST'])
@login_required
def delete_entry():

    # Logika usuwania wpisu
    entry_id = request.form.get('entry_id') 
    if entry_id:
        entry = Entry.query.get_or_404(entry_id)
        Comment.query.filter_by(entry_id=entry_id).delete()
        db.session.delete(entry)
        db.session.commit()
        flash("Entry has been deleted", category="success")
    else:
        flash("Entry ID is missing", category="danger")

    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('index'))
    

@app.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data

    
    return render_template('contact.html', form=form)