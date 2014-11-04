from flask.ext.wtf import Form
from models import User
from database import session
from werkzeug.security import check_password_hash

from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from wtforms.validators import Required


class SignupForm(Form):
    firstname = TextField(
        "First name",  [validators.Required("Please enter your first name.")])
    lastname = TextField(
        "Last name",  [validators.Required("Please enter your last name.")])
    email = TextField("Email",  [validators.Required(
        "Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField(
        'Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    # Check to see if the person already exists as a user
    def validate(self):
        if not Form.validate(self):
            return False

        user = session.query(User).filter_by(email=self.email.data.lower()).first()
        if user:
            print "email taken"
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True
