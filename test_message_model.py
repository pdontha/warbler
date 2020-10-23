"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_message_model(self):
        """Does basic model work?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        m = Message(
            text="warblewarble",
            user_id=u.id
        )
        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(u.messages), 1)
        self.assertEqual(m.text,"warblewarble")
    
    # def test_empty_message_model(self):
    #     u2 = User(
    #         email="test2@test.com",
    #         username="test2user",
    #         password="HASHED_PASSWORD"
    #     )
    #     db.session.add(u2)
    #     db.session.commit()
    #     m2 = Message(
    #             text=None,
    #             user_id=u2.id
    #         )
    #     with self.assertRaises(exc.IntegrityError):
    #         db.session.add(m2)
    #         db.session.commit()
    #     self.assertEqual(len(u2.messages), 0)

    def test_message_like_model(self):
        """Does basic model work?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        m = Message(
            text="warblewarble",
            user_id=u.id
        )
        db.session.add(m)
        db.session.commit()
        l = Likes(user_that_liked=u.id, message_liked=m.id)
        db.session.add(l)
        db.session.commit()
        self.assertEqual(len(u.likes), 1)


    def test_delete_messages_likes(self):
        """test if message got deleted by the user and it deletes from likes table"""
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

        m = Message(
            text="warblewarble",
            user_id=u.id
            )
        db.session.add(m)
        db.session.commit()
        l = Likes(user_that_liked=u2.id, message_liked=m.id)
        db.session.add(l)
        db.session.commit()
        self.assertEqual(len(u2.likes), 1)
        db.session.delete(m)
        db.session.commit()
        self.assertEqual(len(u2.likes), 0)
        self.assertEqual(len(u.messages), 0)
        
