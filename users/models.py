import datetime

from flask.ext.login import UserMixin, AnonymousUser
from werkzeug import generate_password_hash, check_password_hash

from app import db

class Anonymous(AnonymousUser):
    name = u"Anonymous"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(200), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    date_registered = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name=None, email=None, password=None, active=True):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.active = active

    def check_password(self, passhash):
        return check_password_hash(self.password, passhash) 

	def is_active(self):
		return self.active

    def __repr__(self):
        return '<User %r>' % (self.name)