from sqlalchemy import Column, String, Integer

from lib.models.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_indicators import *


class MDKeyMessage(MDBaseMessage):

    __tablename__ = KEY_MSG_TABLE_NAME

    code = Column(String)
    argument = Column(String)
    title = Column(String)
    text_message = Column(String)

    def __init__(self):
        pass