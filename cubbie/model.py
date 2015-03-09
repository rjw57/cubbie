"""
Database models for cubbie.

"""
from cubbie.webapp import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    displayname = db.Column(db.Text, nullable=False)

    def __init__(self, displayname):
        self.displayname = displayname

    def __repr__(self):
        return '<User %s>' % self.displayname

