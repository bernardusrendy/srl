from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(1000), unique=True)
    gender = db.Column(db.String(100))
    usia = db.Column(db.Integer)
    asal = db.Column(db.String(100))
