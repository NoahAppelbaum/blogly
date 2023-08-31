from models import User, DEFAULT_IMAGE_URL, Post
from app import app, db
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Testing the users list page"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_user_page(self):
        """Testing page for individual user details"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            test_user = User.query.get(self.user_id)
            self.assertIn(f"{test_user.first_name}", html)
            # testing to see if our default image is attached
            self.assertIn(DEFAULT_IMAGE_URL, html)

    def test_user_form(self):
        """Testing the user form page"""
        with self.client as c:
            resp = c.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create User', html)

    def test_making_user(self):
        """Testing creating a user"""
        with self.client as c:
            resp = c.post("/users/new",
                          data={
                              'first-name': 'Noah',
                              'last-name': 'Appelbaum',
                              'image-url': ''
                          })
            users_table = User.query.all()
            first_names = [user.first_name for user in users_table]

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")
            self.assertIn('Noah', first_names)

    def test_edit_user_form(self):
        """Testing showing page for user"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            user = User.query.get(self.user_id)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(user.first_name, html)
            self.assertIn(user.last_name, html)


class PostViewTestCase(TestCase):
    """Test views for blog posts."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Post.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title="test_title",
            content="test_content",
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_user_page(self):
        """Testing page for listed blog post"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            test_post = Post.query.get(self.post_id)
            self.assertIn(f"{test_post.title}", html)

    # TODO: more...
    # def test_user_form(self):
    #     """Testing the user form page"""
    #     with self.client as c:
    #         resp = c.get("/users/new")
    #         html = resp.get_data(as_text=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<h1>Create User', html)

    # def test_making_user(self):
    #     """Testing creating a user"""
    #     with self.client as c:
    #         resp = c.post("/users/new",
    #                       data={
    #                           'first-name': 'Noah',
    #                           'last-name': 'Appelbaum',
    #                           'image-url': ''
    #                       })
    #         users_table = User.query.all()
    #         first_names = [user.first_name for user in users_table]

    #         self.assertEqual(resp.status_code, 302)
    #         self.assertEqual(resp.location, "/users")
    #         self.assertIn('Noah', first_names)

    # def test_edit_user_form(self):
    #     """Testing showing page for user"""
    #     with self.client as c:
    #         resp = c.get(f"/users/{self.user_id}/edit")
    #         html = resp.get_data(as_text=True)
    #         user = User.query.get(self.user_id)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn(user.first_name, html)
    #         self.assertIn(user.last_name, html)
