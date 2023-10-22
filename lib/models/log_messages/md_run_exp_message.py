from sqlalchemy import Column, String, Integer, Index
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *


class MDRunExpMessage(MDBaseMessage):

    __tablename__ = RUN_EXP_MSG_TABLE_NAME
    __table_args__ =  ( Index('MDRunExpMessage_robot_info_fk', 'robot_id')
                       , {'schema': SCHEMA_NAME} )

    script_line_no = Column(Integer)
    script_column_no = Column(Integer)
    text_message = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        super(MDRunExpMessage, self).__init__(raw_msg, robot_id, capture_dt)

    def decode_message(self):
        super().decode_message()

        rm = self._raw_msg
        o = self._offset

        self.script_line_no, o = self._read_bytes(rm, '!i', o, 4)
        self.script_column_no, o = self._read_bytes(rm, '!i', o, 4)
        
        len_remain =  self._msg_size - o
        self.text_message, o = self._read_char_array_as_string(rm, o, len_remain)

        self._offset = o

    def _get_custom_data_as_dict(self) -> dict[str, str]:
        return {
                'line_no': str(self.script_line_no)
                ,'column_no': str(self.script_column_no)
                ,'text_message': str(self.text_message)
              }
    
    def __repr__(self):
        return  super().__repr__() + \
                f"\n\t- script_line_no: {self.script_line_no}"\
                f"\n\t- script_column_no: {self.script_column_no}"\
                f"\n\t- text_message: {self.text_message}"