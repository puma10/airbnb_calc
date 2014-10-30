import os
class DevelopmentConfig(object):
    #os.environ.get trys to access the dictionary key heroku (DATABASE_URL) , fallsback to sqlite url if not
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','sqlite:///airbnb-development.db')
    # SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-development.db"
    DEBUG = True
    SECRET_KEY = "Not secret"
    # SECRET_KEY = os.environ.get("MYAPP_SECRET_KEY", "")

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-testing.db"
    DEBUG = True
    SECRET_KEY = "Not secret"

