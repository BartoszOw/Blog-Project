from flask import render_template, request, redirect, url_for, flash, session
from blog import app
from blog.models import Entry, Comment, db
from blog.forms import EntryForm, LoginForm, ContactForm
import tmdb_client
import datetime
import functools

LIST_TYPES = [
    {'name': "Now Playing", 'type': "now_playing"},
    {'name': "Top Rated", 'type': "top_rated"},
    {'name': "Upcoming", 'type': "upcoming"},
    {'name': "Popular", 'type': "popular"}
]
CATEGORIES = [
    {'name': 'Sport', 'type' : 1},
    {'name': 'Food', 'type' : 2},
    {'name': 'Lifestyle', 'type' : 3},
    {'name': 'Games', 'type' : 4}
]

def get_list_types():
    return LIST_TYPES


@app.context_processor
def inject_list_types():
    return dict(list_types=get_list_types())

@app.context_processor
def utility_processor():

    def tmdb_image_url(path,size):
        return tmdb_client.get_poster_url(path,size)
    
    return {'tmdb_image_url': tmdb_image_url}



def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args,**kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.route('/movies')
def movies():
    selected_list = request.args.get('list_type', 'popular')

    valid_list_types = [lst['type'] for lst in LIST_TYPES]

    if selected_list not in valid_list_types:
        return redirect(url_for('movies', list_type='popular'))
    
    movies = tmdb_client.get_movies(16, list_type=selected_list)

    return render_template('movies.html', movies=movies, list=LIST_TYPES, selected_list=selected_list)


@app.route('/')
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).limit(4).all()

    comments_count = {entry.id: len(entry.comments) for entry in all_posts}
    return render_template('homepage.html', all_posts=all_posts, comments_count=comments_count)

@app.route('/post_all') 
def post_all():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template('homepage.html', all_posts=all_posts)

@app.route('/new_post', methods=['GET','POST'])
@login_required
def create_entry():
    return manage_entry(entry_id=None)

@app.route('/edit_post/<int:entry_id>', methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    return manage_entry(entry_id)

def manage_entry(entry_id):
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
    
    return render_template('entry_form.html', form=form, errors=errors)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == "POST":
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True
            flash("You are now logged in.", category="success")
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template('login_form.html', form=form, errors=errors)


@app.route('/logout/', methods=["GET","POST"])
def logout():
    if request.method == "POST":
        session.clear()
        flash('You are now logged out', category='danger')
    return redirect(url_for('index'))   

@app.route('/unpublished_list', methods=['GET'])
@login_required
def unpublished_list():
    un_list = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template('unpublished_list.html', un_list=un_list)


@app.route('/delete_entry', methods=['POST'])
@login_required
def delete_entry():
    entry_id = request.form.get('entry_id') 
    if entry_id:
        entry = Entry.query.get_or_404(entry_id)
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