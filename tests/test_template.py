import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure our app to use the testing database
os.environ["CONFIG_PATH"] = "my_app.config.TestingConfig"

from my_app import app
from my_app import models
from my_app.database import Base, engine, session



class TestViews(unittest.TestCase):

    def setUp(self):
        """ Test setup """
        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        Base.metadata.drop_all(engine)
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
