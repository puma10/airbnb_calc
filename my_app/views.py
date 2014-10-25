from flask import render_template, request, jsonify

from my_app import app
from calculate import calculate_values


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        # created a function named calculate_values() that holds all calulation.  This will allow unittesting of the app.
        data = calculate_values()
        return jsonify(data)

    #if POST doesn't render - render the below GET instead
    return render_template("calculator.html")


#SUMMARY OF DATA FLOW
# - Grab HTML form posts but we stop it from interacting with the server with onsubmit="return false" in the form tag.
# - Then using main.js we grab the data in the fields.
# - Then using ajax we pass this data to our server in a post object.
# - We make our manupliations on the data in the home view
# - Any data we want to send back to the page we put into a dictionary and return to ajax.  We then tell ajax to insert the data into span tags we have identified.
