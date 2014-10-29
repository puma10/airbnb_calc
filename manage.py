import os

from flask.ext.script import Manager

from my_app import app

from getpass import getpass

from werkzeug.security import generate_password_hash

from my_app.models import User

from my_app.database import session

from flask.ext.migrate import Migrate, MigrateCommand

from my_app.database import Base

manager = Manager(app)



class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)



@manager.command
def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


@manager.command
def adduser():
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return

    password = raw_input("Password ")
    password_2 = raw_input("Password ")
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()

if __name__ == "__main__":
    manager.run()
