"""Blogly application."""

import os

from flask import Flask, render_template, redirect, flash, request
from models import db, connect_db, User
# from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = 'aouiergjhalwekjghio23u'

# debug = DebugToolbarExtension(app)

connect_db(app)

DEFAULT_IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"
)


@app.get("/")
def redirect_to_list():
    """ Redirects users to list of users """

    return redirect("/users")


@app.get("/users")
def list_users():
    """List users and show add form."""

    users = User.query.order_by('last_name', 'first_name').all()
    return render_template("list.html", users=users)


@app.get("/users/new")
def add_user_form():
    """Shows add form for users"""

    return render_template("userform.html")


@app.post("/users/new")
def add_user():
    """Process new user form and add to database"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"] or None

    user = User.create_user(first_name, last_name, image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_profile(user_id):
    """Shows detailed profile for specified user by URL ID"""

    user = User.query.get_or_404(user_id)

    return render_template("userdetail.html",
                           user_id=user.id,
                           image_url=user.image_url,
                           name=user.get_full_name())


@app.get("/users/<int:user_id>/edit")
def show_user_edit(user_id):
    """Show the edit page for user"""

    user = User.query.get_or_404(user_id)

    return render_template("edituser.html",
                           user_id=user.id,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           image_url=user.image_url)


@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """processes user profile edit"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"] or DEFAULT_IMAGE_URL

    user = User.query.get(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """deletes user from users db table"""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
