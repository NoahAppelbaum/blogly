"""Blogly application."""

import os

from flask import Flask, render_template, redirect, flash
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
    """Shows add form for users""""

    return render_template("userform.html")