from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask.ext.login import login_required
from flask.ext.sqlalchemy import Pagination

from app import db
from flask.ext.login import current_user

from forum.models import Category, Topic, Post
from forum.forms import CreateCategoryForm, CreateTopicForm, SendPostForm

blueprint = Blueprint('forum', __name__, url_prefix='/forum', template_folder='templates')

PER_PAGE = 10

@blueprint.route("/category/create", methods=['GET', 'POST'])
@login_required
def create_category():
    form = CreateCategoryForm()
    if form.validate_on_submit():
        category = Category(form.title.data, 10, int(current_user.id))
        db.session.add(category)
        db.session.commit()
        flash('New category created')
        return redirect(url_for('index'))
    return render_template("forum/create_category.html", form=form)


@blueprint.route("/category/<int:id_category>/detele")
@login_required
def delete_category(id_category):
    category = Category.query.filter_by(id_category=id_category).first()
    db.session.delete(category)
    db.session.commit()
    flash("Category %s has been deleted" % category.title)
    return redirect(url_for("index"))


@blueprint.route("/category/<int:id_category>/create/topic", methods=['GET', 'POST'])
@login_required
def create_topic(id_category):
    form = CreateTopicForm()
    if form.validate_on_submit():
        topic = Topic(form.title.data, id_category, int(current_user.id), \
            form.important.data, form.locked.data)
        db.session.add(topic)
        db.session.commit()
        flash('New topic created')
        return redirect(url_for('index'))
    return render_template("forum/create_topic.html", form=form, id_category=id_category)


@blueprint.route("/category/<int:id_category>/move/<direction>")
@login_required
def move_category(id_category):
    return redirect(url_for("index"))    


@blueprint.route("/topic/<int:id_topic>/view", defaults={'page': 1})
@blueprint.route("/topic/<int:id_topic>/view/page/<int:page>")
@login_required
def view_topic(id_topic, page):
    form = SendPostForm()
    topic = Topic.query.filter_by(id_topic=id_topic).first()
    return render_template("/forum/view_topic.html", topic=topic,form=form, page=page, per_page=PER_PAGE)


@blueprint.route("/topic/<int:id_topic>/delete")
@login_required
def delete_topic(id_topic):
    topic = Topic.query.filter_by(id_topic=id_topic).first()
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for("index"))


@blueprint.route("/topic/<int:id_topic>/delete/post/<int:id_post>", defaults={'page': 1})
@blueprint.route("/topic/<int:id_topic>/delete/page/<int:page>/post/<int:id_post>")
@login_required
def delete_post(id_topic, id_post, page):
    post = Post.query.filter_by(id_post=id_post).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("forum.view_topic", id_topic=id_topic, page=page))


@blueprint.route("/topic/<int:id_topic>/send/post/", methods=['GET', 'POST'])
@login_required
def send_post(id_topic):
    form = SendPostForm()
    if form.validate_on_submit():
        post = Post(id_topic, int(current_user.id), form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Post sended')
    
    return redirect(url_for('forum.view_topic', id_topic=id_topic))