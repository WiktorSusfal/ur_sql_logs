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

    def _get_custom_data_as_dict(self) -> dict[str, str]:
        return {
                'project_name': str(self.project_name)
                ,'major_version': str(self.major_version)
                ,'minor_version': str(self.minor_version)
                ,'bugfix_version': str(self.bugfix_version)
                ,'build_number': str(self.build_number)
                ,'build_date': str(self.build_date)
              }
    
    def __repr__(self):
        return  super().__repr__() + \
                f"\n\t- project_name: {self.project_name}"\
                f"\n\t- major_version: {self.major_version}"\
                f"\n\t- minor_version: {self.minor_version}"\
                f"\n\t- bugfix_version: {self.bugfix_version}"\
                f"\n\t- build_number: {self.build_number}"\
                f"\n\t- build_date: {self.build_date}"