import datetime
from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime, Boolean

from flask.ext.login import UserMixin, current_user, current_app
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import pdb
import logging
from database import Base, engine
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

################################################################################
# set up logging - see: https://docs.python.org/2/howto/logging.html

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

###############################################################################

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128))
    password = Column(String(128))
    # active = Column(Boolean())
    #cascade delete when a parent item is delete with the below cascade parameter
    inputs = relationship("Input", backref="user", cascade="all, delete-orphan")

    def get_token(self, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'user': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return User.query.get(id)
        return None

    def is_authenticated(self):
        return True

    def __repr__(self):
        return "username {}: id{}".format(self.name, self.id)



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
    # lambda is an anonymous function, without a name it's like we do a get_current():return datetime.datetime.now()
    datetime = Column(DateTime, default=lambda: datetime.datetime.utcnow())

    outputs = relationship("Output", backref="input", cascade="all, delete-orphan")

    # used to convert our database data to json
    def as_dictionary(self):
        post = {
            "id": self.id,
            "title": self.title,
            "rent": self.rent,
            "water": self.water,
            "sewer": self.sewer,
            "garbage": self.garbage,
            "electric": self.electric,
            "cable": self.cable,
            "maid": self.maid,
            "hotel_tax": self.hotel_tax,
            "occupancy_percentage": self.occupancy_percentage,
            "daily_price": self.daily_price
            }

        return post

    def __repr__(self):
        return "'Input' object from model.py - input_title = {}: input id = {}".format(self.title, self.id)



class Output(Base):
    __tablename__ = "outputs"
    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey('inputs.id'))

    break_even = Column(Integer)
    monthly_profit = Column(Integer)

    def __repr__(self):
        return "'Output' object from model.py - output id = {}".format(self.id)

Base.metadata.create_all(engine)
