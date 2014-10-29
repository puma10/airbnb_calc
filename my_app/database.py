from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from my_app import app

# this tells sqlalchemey which database to use
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

# this is an extension on sqlalchemey called declartive - it's the most up to date way to handle connect persiting models with sqlalchemy
Base = declarative_base()

#session is a sqlalchemy feature that holds the objects you've created in memory so they can be used in an ongoing transaction of changes to a database (update, insert, delete)
#also used to query the database

#Sessionmaker is a factory function used to create a standard for how sessions are created.  This is put at the global level to other objects can create sessions
Session = sessionmaker(bind=engine)

session = Session()


# session.add(a) - the session is in the transient state (dies with the session when commited - no insert without commit)

# session.flush() - the session in in a modified state (dies with the session when not commited - no changes persited without commit) - no variable neede

# afer session.add or session.flush but before commit we are in pending state

# session.commit() - the date is persistant



