"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from sqlalchemy.exc import ArgumentError, IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    
    def test_user_repr_method(self):
        """ test the repr method """
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()

        result_str = f"<User #{u.id}: {u.username}, {u.email}>"

        self.assertEqual(repr(u), result_str)

    def test_user_following_method(self):
        """test if user follow works"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        u2 = User(
            email="test@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()
        follow = Follows(
            user_being_followed_id=u.id,
            user_following_id=u2.id
        )
        db.session.add(follow)
        db.session.commit()
        self.assertEqual(len(u.followers), 1)
        self.assertEqual(len(u2.following), 1)
        self.assertEqual(len(u.following), 0)
        self.assertEqual(len(u2.followers), 0)

    def test_user_is_followed_by(self):
        """test if user followed by others"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        u2 = User(
            email="test@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()
        follow = Follows(
            user_being_followed_id=u.id,
            user_following_id=u2.id
        )
        db.session.add(follow)
        db.session.commit()
        self.assertTrue(u.is_followed_by(u2))
    

    def test_user_sign_up(self):
        """Does basic model work?"""
        u = User.signup("testuser", "email@email.com", "password","https://www.google.com/")
        db.session.commit()
        self.assertEqual(u.username, "testuser") 
        with self.assertRaises(IntegrityError):
            User.signup("testuser", "email2@email.com", "password","https://www.google.com/")
            db.session.commit()
    
    def test_user_authentication(self):

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u.authenticate("t","HASHED_PASSWORD"))
        with self.assertRaises(ValueError):
            u.authenticate("testuser","pwd")


    
