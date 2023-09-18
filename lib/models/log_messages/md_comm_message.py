from sqlalchemy import Column, String, Integer

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDCommMessage(MDBaseMessage):

    __tablename__ = COMM_MSG_TABLE_NAME

    code = Column(String)
    argument = Column(String)
    report_level = Column(String)
    report_level_name = Column(String)
    data_type = Column(String)
    data = Column(String)
    text_message = Column(String)

    def __init__(self):
        pass