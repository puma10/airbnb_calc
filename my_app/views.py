from flask import render_template, request, jsonify
from my_app import app
from my_app.models import *
from calculate import calculate_values
from database import session



@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        # created a function named calculate_values() that holds all calulation.  This will allow unittesting of the app.
        #run post data through calculate_values function
        calc_data = calculate_values()
        rent = calc_data['rent']

        # Get the form submission time direct from ajax
        date_time = request.form.get('submit_time')

        calc_data_post = Input(
                title = calc_data['title'],
                rent = calc_data['rent'],
                water = calc_data['water'],
                sewer = calc_data['sewer'],
                garbage = calc_data['garbage'],
                electric = calc_data['electric'],
                cable = calc_data['cable'],
                maid = calc_data['maid'],
                hotel_tax = calc_data['hotel_tax'],
                occupancy_percentage = calc_data['occupancy_percentage'],
                daily_price = calc_data['daily_price'],
                datetime = date_time
        )

        log.info("josh, datetime = " + calc_data_post.datetime)

        session.add(calc_data_post)
        try:
            sesssion.commit()
        except:
            log.info("couldn't commit")
            session.rollback()



        # return jsonified data to the frontend to be used in the html
        return jsonify(calc_data)

    #if POST doesn't render - render the below GET instead
    return render_template("calculator.html")


#SUMMARY OF DATA FLOW
# - With javascript HTML form posts but we stop it from interacting with the server with onsubmit="return false" in the form tag.
# - Then using main.js we grab the data in the fields.
# - Then using ajax we pass this data to our server in a post object.
# - We make our manupliations on the data in the home view
# - Any data we want to send back to the page we put into a dictionary and return to ajax.  We then tell ajax to insert the data into span tags we have identified.
