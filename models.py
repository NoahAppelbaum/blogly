"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


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
    #FIXME: set default to default url variable in app.py => import it
    image_url = db.Column(
        db.String,
        default="https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg",
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
