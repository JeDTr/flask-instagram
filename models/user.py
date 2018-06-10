from db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    fullname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    followers = db.Column(db.Text, default='')
    following =db.Column(db.Text, default='')

    def get_num_followers(self):
        return len([x for x in self.followers.split(',') if x])

    def get_num_following(self):
        return len([x for x in self.following.split(',') if x])
