import struct 
from sqlalchemy import Column, String, DateTime, BigInteger, Sequence, ForeignKey
from typing import Any
from datetime import datetime

from lib.models.components.common import Base

from lib.helpers.constants.hp_backend_names import *

FK_COLUMN_REFERENCE = '.'.join([SCHEMA_NAME, ROBOT_INFO_TABLE_NAME, ROBOT_PK_COLUMN_NAME])

MESSAGE_SOURCES = {
 '-2': 'ROBOT_INTERFACE'
,'-3': 'RT_MACHINE'
,'-4': 'SIMULATED_ROBOT'
,'-5': 'GUI'
, '7': 'CONTROLLER'
, '8': 'RTDE'
}
DEFAULT_SOURCE = 'NOT KNOWN'

class MDBaseMessage(Base):

    __abstract__ = True

    msg_seq = Sequence(SEQUENCE_NAME, schema=SCHEMA_NAME)

    message_id = Column(BigInteger, msg_seq, primary_key=True)
    robot_id = Column(String, ForeignKey(FK_COLUMN_REFERENCE), nullable=False)
    msg_type = Column(String)
    timestamp = Column(String)
    date_time = Column(DateTime)
    source = Column(String)
    source_name = Column(String)
    robot_message_type = Column(String, nullable=False)

    def __init__(self, raw_msg: bytes, robot_id: str, capture_dt: datetime):
        self._offset = 0
        self._msg_size: int = None
        self._raw_msg = raw_msg

        self.robot_id = robot_id
        self.date_time = capture_dt

    def decode_message(self):
        raw_msg = self._raw_msg

        self._msg_size, self._offset = self._read_bytes(raw_msg, '!I', self._offset, 4)
        self.msg_type, self._offset = self._read_bytes(raw_msg, '!B', self._offset, 1)
        self.timestamp, self._offset = self._read_bytes(raw_msg, '!Q', self._offset, 8)
        
        self.source, self._offset = self._read_bytes(raw_msg, '!b', self._offset, 1)
        self.source_name = MESSAGE_SOURCES.get(str(self.source), DEFAULT_SOURCE)
        
        self.robot_message_type, self._offset = self._read_bytes(raw_msg, '!B', self._offset, 1)

    @staticmethod
    def _read_bytes(data_buffer: bytes, type: str, offset: int, length: int) -> tuple[Any, int]:
        end = offset + length
        buffer_part = data_buffer[offset : end]

        value = struct.unpack(type, buffer_part)[0]
        return (value, end)

    @staticmethod
    def _read_char_array_as_string(data_buffer: bytes, offset: int, length: int) -> tuple[str, int]:
        i = 0
        char_array = str()
        while i < length:
            start = offset + i
            end = start + 1
            
            char_array += str(struct.unpack('!c', data_buffer[start : end]))[3]
            i += 1

        return (char_array, (offset + length))
    
    def _get_custom_data_as_dict(self) -> dict[str, str]:
        raise NotImplementedError()
    
    def _get_custom_data_as_string(self) -> str:
        data_dict = self._get_custom_data_as_dict()
        return '{' + ', '.join([k + ': ' + v for k, v in data_dict.items()]) + ' }'
    
    def __repr__(self):
        return  f"{self.__class__.__name__} object.\nMessage size: {self._msg_size}.\nColumns:"\
                f"\n\t- robot_id: {self.robot_id}"\
                f"\n\t- msg_type:  {self.msg_type}"\
                f"\n\t- date_time: {self.date_time}"\
                f"\n\t- source: {self.source}"\
                f"\n\t- source_name: {self.source_name}"\
                f"\n\t- robot_message_type: {self.robot_message_type}"
    

if __name__ == '__main__':
    m = MDBaseMessage(bytes(), 'custom_robot_id', datetime(2023, 9, 30))
    print(m)