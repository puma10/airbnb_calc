from __future__ import division
from flask import request, Response, jsonify
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


def calculate_values(data=None):
    # form.get is used to access the data from a form POST request
    # we create the below variables to grab the data from the ajax post.
    title = request.form.get('form_title')
    print request.form
    print "the title is {}".format(title)
    rent = float(str(request.form.get('form_rent')))
    print "rent variable is of type {}".format(type(rent))
    occupancy = request.form.get('occupancy_form')
    hotel_tax = request.form.get('hotel_tax_form')
    print "hotel_tax variable is of type {}".format(type(hotel_tax))
    hotel_tax = float(str(hotel_tax))
    hotel_tax_percentage = hotel_tax / 100
    # correct later for correct numbers of days in a month
    days_occupied = float(occupancy) / 100 * 30
    daily_rate = request.form.get('daily_price_form')

    # COSTS - UTILITIES ------------------
    water = request.form.get('water_form')
    sewer = request.form.get('sewer_form')
    garbage = request.form.get('garbage_form')
    electric = request.form.get('electric_form')
    cable = request.form.get('cable_form')

    # COSTS - SERVICES ------------------
    maid = request.form.get('maid_form')
    airbnb_service_charge = .03
    airbnb_service_charge_monthly = float(
        days_occupied) * float(daily_rate) * airbnb_service_charge
    # This assumes on average a person stays for 2 days.  Find a better way t0
    # establish this later.
    maid_costs_monthly = float(maid) * float(days_occupied) / 2
    hotel_tax_reserve_monthly = (
        float(daily_rate) * float(hotel_tax_percentage)) * days_occupied

    # COSTS - totals
    utility_costs_monthly = float(
        water) + float(sewer) + float(garbage) + float(electric) + float(cable)

    service_costs_monthly = maid_costs_monthly + \
        hotel_tax_reserve_monthly + airbnb_service_charge_monthly

    total_cost_monthly = float(
        utility_costs_monthly) + float(service_costs_monthly) + float(rent)

    # ------------------ OUTPUT ------------------
    # precautions - hotel tax reserve fund to save per booking

    breakeven = total_cost_monthly
    revenue = float(daily_rate) * float(days_occupied)
    profit = revenue - total_cost_monthly
    time_submitted = request.form.get('submit_time')

    # We add the data we want to pass back to a dictionary
    data = {
        "title": title,
        "rent": rent,
        "water": water,
        "sewer": sewer,
        "garbage": garbage,
        "electric": electric,
        "cable": cable,
        "maid": maid,
        "hotel_tax": hotel_tax,
        "occupancy_percentage": occupancy,
        "daily_price": daily_rate,
        "breakeven": breakeven,
        "time_submitted": time_submitted,
        "revenue": revenue,
        "profit": profit,
        "hotel_tax_percentage": hotel_tax_percentage,
        "days_occupied": days_occupied,
        "maid_costs_monthly": maid_costs_monthly,
        "hotel_tax_reserve_monthly": hotel_tax_reserve_monthly,
        "utility_costs_monthly": utility_costs_monthly,
        "service_costs_monthly": service_costs_monthly,
        "total_cost_monthly": total_cost_monthly,
        "airbnb_service_charge_monthly": airbnb_service_charge_monthly
    }

    # we return the data to ajax and in turn the html page after serilzing our
    # dictionary into json format.

    return data
