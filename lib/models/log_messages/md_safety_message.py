from sqlalchemy import Column, String, Integer

from lib.models.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_indicators import *


class MDSafetyMessage(MDBaseMessage):

    __tablename__ = SAFETY_MSG_TABLE_NAME

    code = Column(String)
    argument = Column(String)
    safety_mode_type = Column(String)
    safety_mode_name = Column(String)
    report_data_type = Column(String)
    report_data = Column(String)

    def __init__(self):
        pass