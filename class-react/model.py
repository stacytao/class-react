from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.Unicode(80), unique=True, nullable=False)
    password = db.Column(db.Unicode(80), nullable=False)
    user_name = db.Column(db.Unicode(80), nullable=False)
    active_reaction_id = db.Column(db.Integer, db.ForeignKey("history.message_id"))
    active_reaction = db.relationship("History", uselist=False, backref=db.backref("user"))


class History(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, unique=True)
    message = db.Column(db.Unicode(140), nullable=False)
    author_name = db.Column(db.Unicode(80), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
