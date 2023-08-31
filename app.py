"""Blogly application."""

import os

from flask import Flask, render_template, redirect, flash, request
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'aouiergjhalwekjghio23u'

debug = DebugToolbarExtension(app)

connect_db(app)


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

    return render_template("userdetail.html", user=user)


@app.get("/users/<int:user_id>/edit")
def show_user_edit(user_id):
    """Show the edit page for user"""

    user = User.query.get_or_404(user_id)

    return render_template("edituser.html", user=user)


@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """processes user profile edit"""

    user = User.query.get(user_id)

    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"] or DEFAULT_IMAGE_URL

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """deletes user from users db table"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# Routes for blog posts


@app.get("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """displays new post form"""

    user = User.query.get_or_404(user_id)
    return render_template("postform.html", user=user)


@app.post("/users/<int:user_id>/posts/new")
def add_blog_post(user_id):
    """Process new post form and add to database"""
    post_title = request.form["post-title"]
    post_content = request.form["post-content"]

    blog_post = Post.create_blog_post(post_title, post_content, user_id)
    db.session.add(blog_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.get("/posts/<int:post_id>")
def show_blog_post(post_id):
    """Shows blog post html"""
    post = Post.query.get_or_404(post_id)

    return render_template("blogpost.html", post=post)


@app.get("/posts/<int:post_id>/edit")
def show_blog_post_edit(post_id):
    """Shows blog post editing html"""
    post = Post.query.get_or_404(post_id)

    return render_template("editblogpost.html", post=post)


@app.post("/posts/<int:post_id>/edit")
def edit_blog_post(post_id):
    """processes blog post edit"""

    post = Post.query.get(post_id)

    post.title = request.form["post-title"]
    post.content = request.form["post-content"]

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.post("/posts/<int:post_id>/delete")
def delete_blog_post(post_id):
    """deletes a blog post"""
    post = Post.query.get_or_404(post_id)
    # Need to capture author's id before deletion
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")
