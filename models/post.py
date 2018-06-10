from db import db

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    post_image = db.Column(db.String(255))
    post_caption = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    posted_by = db.Column(db.String(15))
    people_liked = db.Column(db.Text)
