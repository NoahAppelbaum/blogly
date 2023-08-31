"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

DEFAULT_IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"
)


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """model for user"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String,
        nullable=False
    )

    last_name = db.Column(
        db.String,
        nullable=False
    )

    image_url = db.Column(
        db.String,
        default=DEFAULT_IMAGE_URL,
        nullable=False
    )

    @classmethod
    def create_user(cls, first_name, last_name, image_url):
        """Creates a new User instance"""

        return User(
            first_name=first_name, last_name=last_name, image_url=image_url)

    def get_full_name(self):
        """Returns full name (first name and last name) as a string"""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """model for post"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(60),
        nullable=False
    )

    content = db.Column(
        db.String,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    @classmethod
    def create_blog_post(cls, title, content, user_id):
        """Creates a new Post instance"""

        return Post(
            title=title, content=content, user_id=user_id)

    user = db.relationship("User", backref="posts")
