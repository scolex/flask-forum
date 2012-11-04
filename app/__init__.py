from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.debug = True

db = SQLAlchemy(app)
from forum.models import Category

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

@app.route("/")
def index():
    categories = Category.query.all()
    return render_template("index.html", categories=categories)

from users.views import blueprint as userBlueprint
app.register_blueprint(userBlueprint)

from forum.views import blueprint as forumBlueprint
app.register_blueprint(forumBlueprint)