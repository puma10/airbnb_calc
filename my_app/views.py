from flask import render_template, request, jsonify, redirect, url_for
from my_app import app
from my_app.models import *
from calculate import calculate_values
from database import session
from flask.ext.login import login_required
from flask.ext.login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash
from forms import SignupForm, ResetPassword
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired

def serialize_expiring_token(data, expiration=3600):
    return Serializer(app.config['SECRET_KEY'], expires_in=expiration).dumps(data)

def deserialize_expiring_token(data, expiration=3600):
    try:
        return Serializer(app.config['SECRET_KEY'], expires_in=expiration).loads(data)
    except SignatureExpired:
        return {}

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)



@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # created a function named calculate_values() that holds all calulation.  This will allow unittesting of the app.
        # run post data through calculate_values function
        calc_data = calculate_values()
        rent = calc_data['rent']

        # Get the form submission time direct from ajax
        print "the current user is", current_user.get_id()
        calc_data_post_input = Input(
            user_id=current_user.get_id(),
            title=calc_data['title'],
            rent=calc_data['rent'],
            water=calc_data['water'],
            sewer=calc_data['sewer'],
            garbage=calc_data['garbage'],
            electric=calc_data['electric'],
            cable=calc_data['cable'],
            maid=calc_data['maid'],
            hotel_tax=calc_data['hotel_tax'],
            occupancy_percentage=calc_data['occupancy_percentage'],
            daily_price=calc_data['daily_price']
        )

        calc_data_post_output = Output(
            input_id=calc_data_post_input.id,
            break_even=calc_data['breakeven'],
            monthly_profit=calc_data['profit']
        )

        session.add_all([calc_data_post_input, calc_data_post_output])

        try:
            session.commit()
        except Exception as e:
            log.info("couldn't commit %s" % e)
            session.rollback()

        # return jsonified data to the frontend to be used in the html
        return jsonify(calc_data)

    print "the current user is", current_user.get_id()
    # if POST doesn't render - render the below GET instead
    return render_template("calculator.html")


@app.route("/data_rows")
# @app.route("/page/<int:page>")
def data_rows(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1
    count = session.query(Input).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    data_rows = session.query(Input).filter(
        Input.user_id == current_user.get_id())
    data_rows = data_rows.order_by(Input.datetime.desc())
    data_rows = data_rows[start:end]

    return render_template("data_rows.html",
                           data_rows=data_rows,
                           has_next=has_next,
                           has_prev=has_prev,
                           page=page,
                           total_pages=total_pages
                           )


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
    return redirect(url_for('home'))
    # return redirect(request.args.get('next') or url_for("posts"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    print "the current user id is {}".format(current_user.get_id())
    flash("You have been logged out", "danger")
    return redirect("/login")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(
                name="{} {}".format(form.firstname.data, form.lastname.data),
                email=form.email.data,
                password=generate_password_hash(form.password.data)
                )
            session.add(newuser)
            session.commit()
            login_user(newuser)
            return redirect(url_for('home'))


    elif request.method == 'GET':
        return render_template('signup.html', form=form)



@app.route('/reset_pass', methods=['GET', 'POST'])
def reset_pass():
    form = ResetPassword()

    if form.validate_on_submit():
        print "the current user is {}".format(current_user)
        email = form.email.data
        # Add password reset logic here
        serial = serialize_expiring_token(email, expiration=3600)
        user = session.query(User).filter(User.email==email).first()

        print "the serial is {}".format(serial)
        print "the url we are going to pass is {}".format(url_root + url_for('confirm', token=serial))
        # if user:
        #     subject = "Change Password Request"
        #     sender = "hello@airbnbcalc.com"
        #     recipients = user.email
        #     text_body ="Please follow the following link to reset your password.\
        #     \n {}".format(url_for(confirm(serial)))
        #     html_body = None

        #     m = send_email(subject, sender, recipients, text_body, html_body)

        #     print m.html_body

        #     flash("Please check your email to reset your password.")
        #     return redirect(url_for('home'))

        # elif not user:
        #     flash("This email is not in our database.")
        #     return render_template('password_reset.html', form=form)

        print form.errors
        return render_template('password_reset.html', form=form)

    elif request.method == 'GET':
        return render_template('password_reset.html', form=form)


@app.route('/confirm/<token>/')
def confirm(token):
    pass
    # data = deserialize_expiring_token(token, 3600*3600)
    # if data.get('email'):
    #     u = session.query(User).filter_by(User.email==data['email']).first()
    #     u.confirmed = True
    #     session.add(u)
    #     session.commit()
    #     flash("Your account was confirmed and your trial was extended to 30 days.")
    #     return redirect(url_for('login'))
    # return redirect(url_for('index'))



# @app.route('/reset_password/<url>/', methods=['GET', 'POST'])
# def reset_password(url):
#     if current_user.is_authenticated():
#         flash("You are logged in. You can't reset the password.")
#         return redirect(url_for('user', nickname=current_user.nickname))
#     data = deserialize_expiring_token(url, 3600*24)
#     if data.get('reset'):
#         u = User.query.filter(User.email==data['reset']).first()
#         if u:
#             form = PasswordResetForm()
#             if form.validate_on_submit():
#                 u.password = generate_password_hash(form.password.data)
#                 session.add(u)
#                 session.commit()
#                 m = send_email(u.email, 'You password was successfully changed!', 'auth/email/password_changed', user=u)
#                 flash("Your password was changed.")
#                 return redirect(url_for('user', nickname=u.nickname))
#             return render_template('reset_password.html', form=form)
#     flash("Wrong url or expired password reset token. Please try again.")
#     return redirect(url_for('index'))



# SUMMARY OF DATA FLOW
# - With javascript HTML form posts but we stop it from interacting with the server with onsubmit="return false" in the form tag.
# - Then using main.js we grab the data in the fields.
# - Then using ajax we pass this data to our server in a post object.
# - We make our manupliations on the data in the home view
# - Any data we want to send back to the page we put into a dictionary and return to ajax.  We then tell ajax to insert the data into span tags we have identified.
