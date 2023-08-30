"""Blogly application."""

import os

from flask import Flask, render_template, redirect, flash, request
from models import db, connect_db, User
# from flask_debugtoolbar import DebugToolbarExtension
# TODO: ask why flask debug tool bar won't let us run flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = 'aouiergjhalwekjghio23u'

# debug = DebugToolbarExtension(app)

connect_db(app)


@app.get("/")
def redirect_to_list():
    """ Redirects users to list of users """

    return redirect("/users")


@app.get("/users")
def list_users():
    """List users and show add form."""

    users = User.query.all()
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
    img_url = request.form["image-url"]

    user = User.create_user(first_name, last_name, img_url)
    db.session.add(user)
    db.session.commit()

    # TODO: check: do we want to redirect here? or send to "/" to redirect?
    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_profile(user_id):
    """Shows detailed profile for specified user by URL ID"""

    user = User.query.get_or_404(user_id)

    return render_template("userdetail.html",
                        user_id = user.id,
                        img_url=user.image_url,
                        name=user.get_full_name())

@app.get("/users/<int:user_id>/edit")
def show_user_edit(user_id):
    """Show the edit page for user"""

    user = User.query.get_or_404(user_id)

    return render_template("edituser.html",
                           user_id=user.id,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           img_url=user.image_url)