from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class MDBaseMessage(Base):

    __tablename__ = 'base_messages'

    robot_id = Column(String)
    type = Column(String)
    timestamp = Column(String)
    date_time = Column(DateTime)
    source = Column(String)
    robot_message_type = Column(String)

    def __init__(self):
        pass