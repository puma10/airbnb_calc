import os
class DevelopmentConfig(object):
    #os.environ.get trys to access the dictionary key heroku (DATABASE_URL) , fallsback to sqlite url if not
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','sqlite:///airbnb-development.db')
    # SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-development.db"
    DEBUG = True
    SECRET_KEY = "Not secret"
    MAIL_SERVER = 'smtp.mandrillapp.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'joshwardini@gmail.com'
    MAIL_PASSWORD = 'aeegUT85lKlYkkdJ-wu7wg'

    # SECRET_KEY = os.environ.get("MYAPP_SECRET_KEY", "")

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-testing.db"
    DEBUG = True
    SECRET_KEY = "Not secret"
    MAIL_SERVER = 'smtp.mandrillapp.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'joshwardini@gmail.com'
    MAIL_PASSWORD = 'aeegUT85lKlYkkdJ-wu7wg'


