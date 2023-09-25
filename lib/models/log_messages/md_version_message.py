from sqlalchemy import Column, String, Integer
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDVersionMessage(MDBaseMessage):

    __tablename__ = VERSION_MSG_TABLE_NAME

    project_name = Column(String)
    major_version = Column(String)
    minor_version = Column(String)
    bugfix_version = Column(String)
    build_number = Column(String)
    build_date = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        super(MDVersionMessage, self).__init__(raw_msg, robot_id, capture_dt)

    def decode_message(self):
        super().decode_message()
        ...