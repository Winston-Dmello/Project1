from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from .Puzzles import Puzzle1

class Winners(db.Model):
    __tablename__ = 'winners'

    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True, nullable=False)  # Assuming usernames are unique
    Time_Taken = db.Column(db.String(8), nullable=False)  # Store the time taken in seconds


class Active_Users(db.Model, UserMixin):
    __tablename__ = 'active_users'
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True)
    Progress = db.Column(db.Integer, default=0)
    Lives = db.Column(db.Integer, default=5)
    Attempts = db.Column(db.Integer, default=5)
    Start_Time = db.Column(db.DateTime(timezone=True), default=func.now())
    