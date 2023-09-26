from sqlalchemy import Column, String, Integer
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDKeyMessage(MDBaseMessage):

    __tablename__ = KEY_MSG_TABLE_NAME

    code = Column(String)
    argument = Column(String)
    title = Column(String)
    text_message = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        super(MDKeyMessage, self).__init__(raw_msg, robot_id, capture_dt)