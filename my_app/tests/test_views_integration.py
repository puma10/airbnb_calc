import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure our app to use the testing database
os.environ["CONFIG_PATH"] = "my_app.config.TestingConfig"

from my_app import app
from my_app import model
from my_app.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = model.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    def testAddPost(self):
        self.simulate_login()

        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        posts = session.query(model.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "<p>Test content</p>\n")
        self.assertEqual(post.author, self.user)

    def testDeletePost(self):
        self.simulate_login()

        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"
        })


if __name__ == "__main__":
    unittest.main()
