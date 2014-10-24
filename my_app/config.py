import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-development.db"
    DEBUG = True
    SECRET_KEY = os.environ.get("MYAPP_SECRET_KEY", "")

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-testing.db"
    DEBUG = True
    SECRET_KEY = "Not secret"

