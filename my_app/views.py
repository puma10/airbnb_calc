from flask import render_template, request, jsonify, redirect, url_for
from my_app import app
from my_app.models import *
from calculate import calculate_values
from database import session
from flask.ext.login import login_required
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash
from flask import flash


@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method=='POST':
        # created a function named calculate_values() that holds all calulation.  This will allow unittesting of the app.
        #run post data through calculate_values function
        calc_data = calculate_values()
        rent = calc_data['rent']

        # Get the form submission time direct from ajax

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
                daily_price = calc_data['daily_price']
        )

        session.add(calc_data_post)
        try:
            session.commit()
        except Exception as e:
            log.info("couldn't commit %s" % e)
            session.rollback()

        # return jsonified data to the frontend to be used in the html
        return jsonify(calc_data)

    #if POST doesn't render - render the below GET instead
    return render_template("calculator.html")


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect("/login")
    # return redirect(request.args.get('next') or url_for("posts"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "danger")
    return redirect("/login")


#SUMMARY OF DATA FLOW
# - With javascript HTML form posts but we stop it from interacting with the server with onsubmit="return false" in the form tag.
# - Then using main.js we grab the data in the fields.
# - Then using ajax we pass this data to our server in a post object.
# - We make our manupliations on the data in the home view
# - Any data we want to send back to the page we put into a dictionary and return to ajax.  We then tell ajax to insert the data into span tags we have identified.
