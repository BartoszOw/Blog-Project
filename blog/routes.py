from flask import render_template
from blog import app
from blog.models import Entry

@app.route('/')
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).limit(4).all()
    return render_template('homepage.html', all_posts=all_posts)

@app.route('/post_all')
def post_all():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template('homepage.html', all_posts=all_posts)