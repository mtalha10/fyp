from . import db  # Importing the db instance from __init__.py
from flask_login import UserMixin  # Importing UserMixin for user model
from sqlalchemy.sql import func  # Importing func for SQL functions

class Note(db.Model):  # Defining the Note model
    id = db.Column(db.Integer, primary_key=True)  # Note ID column
    data = db.Column(db.String(10000))  # Data column for the note content
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Date column for note creation
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key column referencing the User model

class User(db.Model, UserMixin):  # Defining the User model
    id = db.Column(db.Integer, primary_key=True)  # User ID column
    email = db.Column(db.String(150), unique=True)  # Email column with uniqueness constraint
    password = db.Column(db.String(150))  # Password column
    first_name = db.Column(db.String(150))  # First name column
    notes = db.relationship('Note')  # Relationship to the Note model
