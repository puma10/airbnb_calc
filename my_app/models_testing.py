
import datetime
from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime

from flask.ext.login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import pdb
import logging

#turned on for testing
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


#turned off for testing
#from database import Base, engine

################################################################################
# set up logging - see: https://docs.python.org/2/howto/logging.html

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


################################################################################

#turned on for testing
Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128))
    password = Column(String(128))
    #cascade delete when a parent item is delete with the below cascade parameter
    inputs = relationship("Input", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return "username {}: id{}".format(self.name, self.id)

    def is_authenticated(self):
        return True

class Input(Base):
    __tablename__ = "inputs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))


    title = Column(String(1024))
    rent = Column(Integer)
    water = Column(Integer)
    sewer = Column(Integer)
    garbage = Column(Integer)
    electric = Column(Integer)
    cable = Column(Integer)
    maid = Column(Integer)
    hotel_tax = Column(Integer)
    occupancy_percentage = Column(Integer)
    daily_price = Column(Integer)
    datetime = Column(DateTime, default=datetime.datetime.now)

    outputs = relationship("Output", backref="input", cascade="all, delete-orphan")

    def __repr__(self):
        return "input set title {}: input id {}".format(self.title, self.id)



class Output(Base):
    __tablename__ = "outputs"
    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey('inputs.id'))

    break_even = Column(Integer)
    monthly_profit = Column(Integer)

    def __repr__(self):
        return "output id = {}".format(self.id)


###############################################################################

def init_db(engine):
    "initialize our database, drops and creates our tables"
    log.info("init_db() engine: {}".format(engine) )

    log.info("base class generated: {}".format(Base) )

    # drop all tables and recreate
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    log.info("  - tables dropped and created")

if __name__ == "__main__":
    log.info("main executing:")

    # create an engine
    engine = create_engine('sqlite:///:memory:')
    log.info("created engine: {}".format(engine) )

    # if we asked to init the db from the command line, do so
    if True:
        init_db(engine)

    # call the sessionmaker factory to make a Session class
    Session = sessionmaker(bind=engine)

    # get a local session for the this script
    db_session = Session()
    log.info("Session created: {}".format(db_session) )

    # count our starting number of users, inputs and outputs
    num_users = db_session.query(User).count()
    num_inputs = db_session.query(Input).count()
    num_outputs = db_session.query(Output).count()
    log.info("starting with {} users, {} inputs and {} outputs ".format(num_users, num_inputs, num_outputs))


############################## Create User ####################################

    log.info("Creating Users (Transient)")
    josh = User(
                name="Josh",
                email = "joshwardini@gmail.com",
                password = "password"
                )

    dave = User(
                name="Dave",
                email = "joshwardini@gmail.com",
                password = "password"
                )

    db_session.add_all([josh, dave])
    db_session.commit()

    log.info("user {} was created with an id of {}".format(josh.name, josh.id))

############################# Create Input Set ################################


    log.info("Creating Input Set (Transient)")
    my_condo = Input(
                user_id = 1,
                title = "First Condo",
                rent = 900,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 250,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )

    log.info("Creating Input Set (Transient)")
    phil_condo = Input(
                user_id = 1,
                title = "Second Condo",
                rent = 600,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 150,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )

    dave_condo = Input(
                user_id = 2,
                title = "Second Condo",
                rent = 600,
                water = 50,
                sewer = 55,
                garbage = 45,
                electric = 90,
                cable = 85,
                maid = 150,
                hotel_tax = 12,
                occupancy_percentage = 70,
                daily_price = 125
                )

    db_session.add_all([my_condo, phil_condo, dave_condo])
    db_session.commit()


    log.info("Input set number {} was created with a title of {} at {}.".format(my_condo.id, my_condo.title, my_condo.datetime))

############################# Create Output   ################################

    log.info("Creating Output")
    my_output = Output(
                input_id = 1,
                break_even = 1600,
                monthly_profit = 500
                )

    his_output = Output(
                input_id = 2,
                break_even = 1600,
                monthly_profit = 500
                )

    db_session.add_all([my_output, his_output])
    db_session.commit()

    log.info("output #{} was created with a breakeven of {}".format(my_output.id, my_output.break_even))


########################## Testing Relationships ##############################

#All Josh's output
    #title
    #Occupancy
    #Price
    #Monthly Proift


    # This is a join
    # The domain class passed first as an argument to query is what we want to get back
    # We then join, usually in the order of the key relationships to different classes.
    # We can add as many filter clauses as we want after the joins
    # We can't filter on a class until we've joined it
    user_inputs = db_session.query(Input).join(User)\
                .filter(User.name=="Josh").all()

    josh = db_session.query(User).filter(User.name=="Josh").first().name

    josh_object = db_session.query(User).filter(User.name=="Josh").first()

    log.info(josh)

    print josh, "owns", user_inputs.count


    for user in user_inputs:
        print user.title
        print user.occupancy_percentage
        print user.daily_price

        # query the loop adding each user to get the output values
        monthly_profit = db_session.query(Output).get(user.id).monthly_profit
        print "The monthly profit = ", monthly_profit


    #Update Josh
    josh_object.name = "John"
    db_session.commit()
    assert josh_object.name == "John"



    db_session.delete(josh_object)

    # Assert Josh has been deleted
    assert db_session.query(User).filter(User.name=="Josh").first() == None

    #Assert Josh's dependies have been cascade delete with delete-orphan
    assert db_session.query(Input).join(User)\
                .filter(User.name=="Josh").first() == None














#Turned off for testing
# # This line must be below your classes or the new classes you create will not create tables.
# Base.metadata.create_all(engine)
