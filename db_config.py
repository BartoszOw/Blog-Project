from faker import Faker
from blog.models import Entry, db, Comment, Account
from blog import app,db
def generate_entries(how_many=10):
    fake = Faker()

    for i in range(how_many):
        post = Entry(
            title = fake.sentence(),
            body='\n'.join(fake.paragraphs(15)),
            is_published = True
        )
        db.session.add(post)
    db.session.commit()



def generate_comments(how_many=5):
    fake = Faker()
    entries = Entry.query.all()

    for entry in entries:
        for i in range(how_many):
            comment = Comment(
                text = fake.paragraph(),
                entry_id = entry.id
            )
            db.session.add(comment)
    db.session.commit()

def generate_accounts(how_many=5):
    fake = Faker()

    for i in range(how_many):
        account = Account(
            username=fake.user_name(),
            password=fake.password()
        )
        db.session.add(account)
    db.session.commit()

#with app.app_context():
#    generate_accounts()
#    generate_entries()
#    generate_comments()


