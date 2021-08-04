from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(1000))

    def __repr__(self):
        return f"<User: {self.username}>"

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    name = db.Column(db.String(1000))
    album = db.Column(db.String(128))
    lyrics = db.Column(db.String(100000000))

    def __repr__(self):
        return f"<Song: {self.title}"
