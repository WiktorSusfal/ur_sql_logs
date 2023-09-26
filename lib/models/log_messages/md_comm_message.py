from sqlalchemy import Column, String
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *

REPORT_LEVELS_DICT = {
                        0: 'DEBUG'
                      , 1: 'INFO'
                      , 2: 'WARNING'
                      , 3: 'VIOLATION'
                      , 4: 'FAULT'
                      , 128: 'DEVL_DEBUG'
                      , 129: 'DEVL_INFO'
                      , 130: 'DEVL_WARNING'
                      , 131: 'DEVL_VIOLATION'
                      , 132: 'DEVL_FAULT'
                    }


class MDCommMessage(MDBaseMessage):

    __tablename__ = COMM_MSG_TABLE_NAME

    code = Column(String)
    argument = Column(String)
    report_level = Column(String)
    report_level_name = Column(String)
    data_type = Column(String)
    data = Column(String)
    text_message = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        super(MDCommMessage, self).__init__(raw_msg, robot_id, capture_dt)