from sqlalchemy import Column, String, Index
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDKeyMessage(MDBaseMessage):

    __tablename__ = KEY_MSG_TABLE_NAME
    __table_args__ =  ( Index('MDKeyMessage_robot_info_fk', 'robot_id')
                       , {'schema': SCHEMA_NAME} )

    code = Column(String)
    argument = Column(String)
    title = Column(String)
    text_message = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        super(MDKeyMessage, self).__init__(raw_msg, robot_id, capture_dt)

    def decode_message(self):
        super().decode_message()
        
        rm = self._raw_msg
        o = self._offset

        self.code, o = self._read_bytes(rm, '!i', o, 4)
        self.argument, o = self._read_bytes(rm, '!i', o, 4)
        
        title_size, o = self._read_bytes(rm, '!B', o, 1)
        self.title, o = self._read_char_array_as_string(rm, o, title_size)
        
        len_remain =  self._msg_size - o
        self.text_message, o = self._read_char_array_as_string(rm, o, len_remain)

        self._offset = o

    def _get_custom_data_as_dict(self) -> dict[str, str]:
        return {
                'line_no': str(self.code)
                ,'column_no': str(self.argument)
                ,'title': str(self.title)
                ,'text_message': str(self.text_message)
              }

    def __repr__(self):
        return  super().__repr__() + \
                f"\n\t- code: {self.code}"\
                f"\n\t- argument: {self.argument}"\
                f"\n\t- title: {self.title}"\
                f"\n\t- text_message: {self.text_message}"