#models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(10), default='', nullable=True)
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(20), default='Unknown')
    pincode = db.Column(db.String(6))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    records = db.relationship('Record')