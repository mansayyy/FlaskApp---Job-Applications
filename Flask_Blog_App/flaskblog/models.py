#!/usr/bin/env python3 
from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

friends = db.Table(
    'friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    applications = db.relationship('Applications',backref='author',lazy=True)
    friends = db.relationship(
        'User', 
        secondary=friends,
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.friend_id == id),
        backref=db.backref('friend_of', lazy='dynamic'),
        lazy='dynamic'
    )
    def __repr__(self):
        return f"User('{self.username}', '{self.email}' , '{self.image_file}')"

class Applications(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    companyname = db.Column(db.String(100), nullable=False)
    jobrole = db.Column(db.String(100), nullable=False)
    joblocation = db.Column(db.String(100))
    jobwebsite = db.Column(db.String(100))
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    jobdescription = db.Column(db.Text)
    def __repr__(self):
        return f"Job('{self.companyname}','{self.jobrole}', '{self.date_applied}')"

