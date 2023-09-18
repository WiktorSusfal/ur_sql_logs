from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MDBaseMessage(Base):

    __tablename__ = 'base_messages'

    message_id = Column(Integer, primary_key=True)
    robot_id = Column(String)
    type = Column(String)
    timestamp = Column(String)
    date_time = Column(DateTime)
    source = Column(String)
    robot_message_type = Column(String)

    def __init__(self):
        pass

if __name__ == '__main__':
    m = MDBaseMessage()