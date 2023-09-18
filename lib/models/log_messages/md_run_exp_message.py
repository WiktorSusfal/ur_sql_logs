from sqlalchemy import Column, String, Integer

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDRunExpMessage(MDBaseMessage):

    __tablename__ = RUN_EXP_MSG_TABLE_NAME

    script_line_no = Column(Integer)
    script_column_no = Column(Integer)
    text_message = Column(String)

    def __init__(self):
        pass