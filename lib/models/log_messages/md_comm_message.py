from sqlalchemy import Column, String, Index
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
    __table_args__ =  ( Index('MDCommMessage_robot_info_fk', 'robot_id')
                       , {'schema': SCHEMA_NAME} )

    code = Column(String)
    argument = Column(String)
    report_level = Column(String)
    report_level_name = Column(String)
    data_type = Column(String)
    data = Column(String)
    text_message = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        super(MDCommMessage, self).__init__(raw_msg, robot_id, capture_dt)

    def decode_message(self):
      super().decode_message()

      rm = self._raw_msg
      o = self._offset

      self.code, o = self._read_bytes(rm, '!i', o, 4)
      self.argument, o = self._read_bytes(rm, '!i', o, 4)

      self.report_level, o = self._read_bytes(rm, '!i', o, 4)
      self.report_level_name = REPORT_LEVELS_DICT.get(self.report_level, None)

      self.data_type, o = self._read_bytes(rm, '!I', o, 4)
      self.data, o = self._read_bytes(rm, '!I', o, 4)

      len_remain =  self._msg_size - o
      self.text_message, o = self._read_char_array_as_string(rm, o, len_remain)

      self._offset = o

    def __repr__(self):
        return  super().__repr__() + \
                f"\n\t- code: {self.code}"\
                f"\n\t- argument: {self.argument}"\
                f"\n\t- report_level: {self.report_level}"\
                f"\n\t- report_level_name: {self.report_level_name}"\
                f"\n\t- data_type: {self.data_type}"\
                f"\n\t- data: {self.data}"\
                f"\n\t- text_message: {self.text_message}"