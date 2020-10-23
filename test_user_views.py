"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """ Tests for views of API."""

    
    def setUp(self):
        """Make demo data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    def test_logged_in_user(self):
        with app.test_client() as client:

        # u = User(
        #     email="test@test.com",
        #     username="testuser",
        #     password="HASHED_PASSWORD"
        # )
        # db.session.add(u)
        # db.session.commit()
            u = User.signup("testuser", "email@email.com", "password","https://www.google.com/")
            db.session.commit()
            us = {"email": "test@test.com", "username":"testuser", "password":"password"}
            resp = client.post("/login", data=us, follow_redirects=True)
            html = resp.get_data(as_text=True)
            print("RESPONSEEEEEE", resp.status_code)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("success", html)







    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    
