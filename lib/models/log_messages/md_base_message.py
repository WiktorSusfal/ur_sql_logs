from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base
import struct 
from typing import Any
from datetime import datetime

Base = declarative_base()

class MDBaseMessage(Base):

    __tablename__ = 'base_messages'

    message_id = Column(Integer, primary_key=True)
    robot_id = Column(String)
    msg_type = Column(String)
    timestamp = Column(String)
    date_time = Column(DateTime)
    source = Column(String)
    robot_message_type = Column(String)

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

        return [char_array, (offset + length)]


if __name__ == '__main__':
    m = MDBaseMessage()