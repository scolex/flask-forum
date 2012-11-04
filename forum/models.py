import datetime
from app import db

class Category(db.Model):
    id_category = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(200), unique=True)
    posititon = db.Column(db.Integer)
    id_creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    topics = db.relationship('Topic', backref='category',
                                lazy='dynamic')

    def __init__(self, title=None, posititon=10, id_creator=None):
        self.title = title
        self.posititon = posititon
        self.id_creator = id_creator

    def __repr__(self):
        return '<Category %r>' % (self.title)

class Topic(db.Model):
    id_topic = db.Column(db.Integer, primary_key=True)
    id_creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_category = db.Column(db.Integer, db.ForeignKey('category.id_category'))
    admin = db.Column(db.Integer, db.ForeignKey('user.id'))  
    title = db.Column(db.Text(200))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    locked = db.Column(db.Boolean, default=False)
    important = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='topic', lazy='dynamic')

    def __init__(self, title=None, id_category=None, id_creator=None, important=False, locked=False):
        self.title = title
        self.id_creator = id_creator
        self.id_category = id_category
        self.admin = id_creator
        self.important = important
        self.locked = locked

    def __repr__(self):
        return '<Topic %r>' % (self.title)


class Post(db.Model):
    id_post = db.Column(db.Integer, primary_key=True)
    id_sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_topic = db.Column(db.Integer, db.ForeignKey('topic.id_topic'))   
    content = db.Column(db.Text(5000))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", uselist=False, backref="post")

    def __init__(self, id_topic=None, id_sender=None, content=None):
        self.id_topic = id_topic
        self.id_sender = id_sender
        self.content = content

    def __repr__(self):
        return '<Post %r>' % (self.content)


moderators = db.Table('moderators',
    db.Column('id_user', db.Integer, db.ForeignKey('user.id')),
    db.Column('id_topic', db.Integer, db.ForeignKey('topic.id_topic'))
)


user_topic_visits = db.Table('topic_visit',
    db.Column('id_user', db.Integer, db.ForeignKey('user.id')),
    db.Column('id_topic', db.Integer, db.ForeignKey('topic.id_topic'))
)
