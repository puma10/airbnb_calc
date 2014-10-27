import unittest
import os
import json
from my_app.calculate import calculate_values

# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "my_app.config.TestingConfig"

from my_app import app
from my_app.views import home
from my_app.models import *
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
        # This setup configuration comes from the following tutorial
        # http://flask.pocoo.org/docs/0.10/testing/

        # These are variables, functions, databases and other depnedices we want to be available to all or tests

        self.client = app.test_client()


    def tearDown(self):
        """ Test teardown """
        pass


    def testCalculations(self):
        # Getting my_app from an empty database
        response = self.client.post("/",
        data={
            'form_title': "Dave's Condo",
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
            # 'submit_time': datetime.date(2013, 3, 25)
        })


        # The test_request_context() makes the request below work for some reason
        with app.test_request_context():

# ------------------IMPORTANT----------------------------------------------
            # your data should be returned in json - figure out to get these values
            # look at how to load your jsonified data - see chords
            # then you can test yor values
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["days_occupied"], 21)
            self.assertEqual(data["hotel_tax_percentage"], 0.12)
            self.assertEqual(data["maid_costs_monthly"], 525)
            self.assertEqual(data["hotel_tax_reserve_monthly"], 252)
            self.assertEqual(data["airbnb_service_charge_monthly"], 63)
            self.assertEqual(data["utility_costs_monthly"], 250)
            self.assertEqual(data["service_costs_monthly"], 840)
            self.assertEqual(data["total_cost_monthly"], 2090)
            self.assertEqual(data["revenue"], 2100)
            self.assertEqual(data["profit"], 10)


if __name__ == "__main__":
    unittest.main()
