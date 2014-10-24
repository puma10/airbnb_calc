import unittest
import os
import json
from urlparse import urlparse

# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "my_app.config.TestingConfig"

from my_app import app
from my_app import models
from my_app.models import Input, User
from my_app.database import Base, engine, session
from my_app import api


#setup logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)



class TestAPI(unittest.TestCase):
    """ Tests for the my_app API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

    def testGetEmptyInputData(self):
        # Getting my_app from an empty database
        response = self.client.get("/api", headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(data, [])


    def testGetInputData(self):
        my_condo = Input(
                user_id = 1,
                title = "First Condo",
                rent = 900,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 250,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )

        phil_condo = Input(
                user_id = 1,
                title = "Second Condo",
                rent = 600,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 150,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )


        dave_condo = Input(
                user_id = 2,
                title = "Second Condo",
                rent = 600,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 150,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )

        session.add_all([my_condo, phil_condo, dave_condo])
        session.commit()

        response = self.client.get("/api", headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        my_condo = data[0]
        self.assertEqual(my_condo["title"], "First Condo")

    def testGetSingleInput(self):
        """ Getting a single post from a populated database """
        my_condo = Input(
                user_id = 1,
                title = "First Condo",
                rent = 900,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 250,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )

        phil_condo = Input(
                user_id = 1,
                title = "Second Condo",
                rent = 600,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 150,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )


        dave_condo = Input(
                user_id = 2,
                title = "Second Condo",
                rent = 600,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 150,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )

        session.add_all([my_condo, phil_condo, dave_condo])
        session.commit()

        # Get my_condo.id from the json response through the view
        response = self.client.get("/api/posts/{}".format(my_condo.id), headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        post = json.loads(response.data)
        self.assertEqual(post["title"], "First Condo")

    def testGetNonExistantPost(self):
        """ Getting a single post which doesn't exist """
        response = self.client.get("/api/posts/1", headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(data["message"], "Could not find post with id 1")

    def testUnsupportedAcceptHeader(self):
        response = self.client.get("/api",
            headers=[("Accept", "application/xml")]
        )

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(data["message"],
                         "Request must accept application/json data")

    def testInputPost(self):
        """ Posting a new post """
        data = {
            "title": "Example Post",
            "rent": 700
        }

        response = self.client.post("/api/posts",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(urlparse(response.headers.get("Location")).path,
                         "/api/posts/1")

        data = json.loads(response.data)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], "Example Post")
        self.assertEqual(data["rent"], 700)

        posts = session.query(Input).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, "Example Post")
        self.assertEqual(post.rent, 700)


    def testUnsupportedMimetype(self):
        data = "<xml></xml>"
        response = self.client.post("/api/posts",
            data=json.dumps(data),
            content_type="application/xml",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(data["message"],
                         "Request must contain application/json data")


    def testInvalidData(self):
        """ Posting a post with an invalid body """
        data = {
            "title": 32,
            "rent": 700
        }

        response = self.client.post("/api/posts",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 422)

        data = json.loads(response.data)

        log.info(data)
        self.assertEqual(data["message"], "32 is not of type 'string'")

    def testMissingData(self):
        """ Posting a post with a missing body """
        data = {
            "title": "Example Post",
        }

        response = self.client.post("/api/posts",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "'rent' is a required property")





if __name__ == "__main__":
    unittest.main()
