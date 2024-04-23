from flask import render_template, request, redirect, url_for, flash, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import datetime
import functools

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args,**kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions

@app.route('/')
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).limit(4).all()
    return render_template('homepage.html', all_posts=all_posts)

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
    