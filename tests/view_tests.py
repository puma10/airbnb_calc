import unittest
import os
import json
from urlparse import urlparse
from my_app.calculate import calculate_values

# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "my_app.config.TestingConfig"

from my_app import app
from my_app.views import home
from flask import request, Response


#setup logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


class TestFormCalculations(unittest.TestCase):
    """ Tests the calculations of the form """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        # Base.metadata.create_all(engine)

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        # Base.metadata.drop_all(engine)

    def testCalculations(self):
        # Getting my_app from an empty database
        response = self.client.post("/",
        data={
            'form_title': "Josh's Condo",
            'form_rent': 1000,
            'water_form': 50,
            'sewer_form': 50,
            'garbage_form': 50,
            'electric_form': 50,
            'cable_form': 50,
            'maid_form': 50,
            'hotel_tax_form': 12,
            'occupancy_form': 70,
            'daily_price_form': 100,
            'submit_time': "jan"
        })

        # The test_request_context() makes the request below work for some reason
        with app.test_request_context():
            calculate_values()

        self.assertEqual(days_occupied, 21)




        print title



        # self.assertEqual(home.days_occupied, 21)


if __name__ == "__main__":
    unittest.main()
