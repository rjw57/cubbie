"""
Database models for cubbie.

"""
from cubbie.webapp import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    displayname = db.Column(db.Text, nullable=False, index=True)

