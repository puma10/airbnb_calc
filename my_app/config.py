import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgres://talzrazzwolyoi:roDY1kg7PgN1tX9LyWP6Nlex7U@ec2-54-243-42-236.compute-1.amazonaws.com:5432/d61lneaff8ggt2"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-development.db"
    DEBUG = True
    SECRET_KEY = "Not secret"
    # SECRET_KEY = os.environ.get("MYAPP_SECRET_KEY", "")

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///airbnb-testing.db"
    DEBUG = True
    SECRET_KEY = "Not secret"

