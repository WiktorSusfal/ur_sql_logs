from sqlalchemy import Column, String, Index
from datetime import datetime

from lib.models.log_messages.md_base_message import MDBaseMessage

from lib.helpers.constants.hp_backend_names import *

SAFETY_MODE_TYPES_DICT = \
{1: 'NORMAL'
, 2: 'REDUCED'
, 3: 'PROTECTIVE_STOP'
, 4: 'RECOVERY'
, 5: 'SAFEGUARD_STOP'
, 6: 'SYSTEM_EMERGENCY_STOP'
, 7: 'ROBOT_EMERGENCY_STOP'
, 8: 'VIOLATION'
, 9: 'FAULT'
, 10: 'VALIDATE_JOINT_ID'
, 11: 'UNDEFINED'}


class MDSafetyMessage(MDBaseMessage):

    __tablename__ = SAFETY_MSG_TABLE_NAME
    __table_args__ =  ( Index('MDSafetyMessage_robot_info_fk', 'robot_id'), {'schema': SCHEMA_NAME} )

    code = Column(String)
    argument = Column(String)
    safety_mode_type = Column(String)
    safety_mode_name = Column(String)
    report_data_type = Column(String)
    report_data = Column(String)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
      super(MDSafetyMessage, self).__init__(raw_msg, robot_id, capture_dt)
  
    def decode_message(self):
        super().decode_message()

        rm = self._raw_msg
        o = self._offset

        self.code, o = self._read_bytes(rm, '!i', o, 4)
        self.argument, o = self._read_bytes(rm, '!i', o, 4)

        self.safety_mode_type, o = self._read_bytes(rm, '!B', o, 1)
        self.safety_mode_name = SAFETY_MODE_TYPES_DICT.get(self.safety_mode_type, None)

        self.report_data_type, o = self._read_bytes(rm, '!I', o, 4)
        self.report_data, o = self._read_bytes(rm, '!I', o, 4)

        self._offset = o

    def __repr__(self):
        return  super().__repr__() + \
                f"\n\t- code: {self.code}"\
                f"\n\t- argument: {self.argument}"\
                f"\n\t- safety_mode_type: {self.safety_mode_type}"\
                f"\n\t- safety_mode_name: {self.safety_mode_name}"\
                f"\n\t- report_data_type: {self.report_data_type}"\
                f"\n\t- report_data: {self.report_data}"