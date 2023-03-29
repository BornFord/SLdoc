from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    requests = db.relationship('Request', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))
    title = db.Column(db.String(128))
    comment = db.Column(db.String(256))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipients = db.relationship('Recipient', backref='request', lazy='dynamic')
    comments = db.relationship('Comment', backref='request', lazy='dynamic')

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
