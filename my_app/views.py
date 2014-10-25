from flask import render_template, jsonify, request, Response

from my_app import app

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)



@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        # form.get is used to access the data from a form POST request
        # we create the below variables to grab the data from the ajax post.
        title = request.form.get('form_title')
        rent = float(request.form.get('form_rent'))
        occupancy = float(request.form.get('occupancy_form'))
        hotel_tax_percentage = (float(request.form.get('hotel_tax_form'))) / 100
        #correct later for correct numbers of days in a month
        days_occupied = float((occupancy/100)) * 30
        daily_rate = float(request.form.get('daily_price_form'))

        # COSTS - UTILITIES ------------------
        water = float(request.form.get('water_form'))
        sewer = float(request.form.get('sewer_form'))
        garbage = float(request.form.get('garbage_form'))
        electric = float(request.form.get('electric_form'))
        cable = float(request.form.get('cable_form'))

        # COSTS - SERVICES ------------------
        maid = float(request.form.get('form_rent'))
        # This assumes on average a person stays for 2 days.  Find a better way t0 establish this later.
        maid_costs_monthly = ((maid * days_occupied) / 2)
        hotel_tax_reserve_monthly = (daily_rate * hotel_tax_percentage) * days_occupied

        # COSTS - totals
        utility_costs_monthly = water + sewer + garbage + electric + cable
        service_costs_monthly = maid_costs_monthly + hotel_tax_reserve_monthly
        total_cost_monthly = utility_costs_monthly + service_costs_monthly


        # ------------------ OUTPUT ------------------
        #precautions - hotel tax reserve fund to save per booking

        breakeven = total_cost_monthly
        revenue = daily_rate * days_occupied
        profit = revenue - total_cost_monthly
        time_submitted = request.form.get('submit_time')


        # We add the data we want to pass back to a dictionary
        data = {"breakeven": str(breakeven),
            "time_submitted": time_submitted,
            "revenue": revenue,
            "profit": profit
            }

        #we return the data to ajax and in turn the html page after serilzing our dictionary into json format.
        log.info(title)
        return jsonify(data)

    #if POST doesn't render - render the below GET instead
    return render_template("calculator.html")


#SUMMARY OF DATA FLOW
# - Grab HTML form posts but we stop it from interacting with the server with onsubmit="return false" in the form tag.
# - Then using main.js we grab the data in the fields.
# - Then using ajax we pass this data to our server in a post object.
# - We make our manupliations on the data in the home view
# - Any data we want to send back to the page we put into a dictionary and return to ajax.  We then tell ajax to insert the data into span tags we have identified.
