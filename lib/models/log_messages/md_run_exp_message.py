from sqlalchemy import Column, String, Integer
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDRunExpMessage(MDBaseMessage):

    __tablename__ = RUN_EXP_MSG_TABLE_NAME

    script_line_no = Column(Integer)
    script_column_no = Column(Integer)
    text_message = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        super(MDRunExpMessage, self).__init__(raw_msg, robot_id, capture_dt)