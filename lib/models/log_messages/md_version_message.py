from sqlalchemy import Column, String, Index
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDVersionMessage(MDBaseMessage):

    __tablename__ = VERSION_MSG_TABLE_NAME
    __table_args__ =  ( Index('MDVersionMessage_robot_info_fk', 'robot_id')
                       , {'schema': SCHEMA_NAME} )

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
        rm = self._raw_msg
        o = self._offset

        project_name_size, o = self._read_bytes(rm, '!b', o, 1)
        self.project_name, o = self._read_char_array_as_string(rm, o, project_name_size)
        self.major_version, o = self._read_bytes(rm, '!B', o, 1)
        self.minor_version, o = self._read_bytes(rm, '!B', o, 1)
        self.bugfix_version, o = self._read_bytes(rm, '!i', o, 4)
        self.build_number, o = self._read_bytes(rm, '!i', o, 4)
        
        len_remain =  self._msg_size - o
        self.build_date, o = self._read_char_array_as_string(rm, o, len_remain)

        self._offset = o


