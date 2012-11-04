from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from flask.ext.login import (LoginManager, login_required,
                            login_user, logout_user)

from app import app
from app import db
from users.forms import RegisterForm, LoginForm
from users.models import Anonymous, User

login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.login_view = "users.login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == int(id)).first()

blueprint = Blueprint('users', __name__, template_folder='templates')

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("users.home"))
    return render_template("login.html", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Thanks for registering')
        return redirect(url_for('users.home'))
    return render_template("register.html", form=form)


@blueprint.route('/home')
@login_required
def home():
    return render_template("users/home.html")
