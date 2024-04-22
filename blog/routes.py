from flask import render_template, request, redirect, url_for, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm
import datetime

@app.route('/')
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).limit(4).all()
    return render_template('homepage.html', all_posts=all_posts)

@app.route('/post_all')
def post_all():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template('homepage.html', all_posts=all_posts)

@app.route('/new_post', methods=['GET','POST'])
def create_entry():
    return manage_entry(entry_id=None)

@app.route('/edit_post/<int:entry_id>', methods=["GET", "POST"])
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