import struct
from dataclasses import dataclass
from typing import Generator
from datetime import datetime

from lib.helpers.constants.hp_message_attributes import *

@dataclass
class DsRobotMsgBuffer:
    buffer: bytes = None
    robot_id: str = None
    capture_dt: datetime = None

    def _get_buffer_part(self, offset: int, length: int) -> bytes:
        return self.buffer[offset : offset+length]

    def get_primary_client_messages(self) -> Generator[bytes, None, None]:
        offset = 0

        while offset < len(self.buffer):        
            
            b_part = self._get_buffer_part(offset+MAIN_PCKG_LEN_OFFSET, MAIN_PCKG_LEN_LEN)
            main_package_length = struct.unpack('!I', b_part)[0]

            b_part = self._get_buffer_part(offset+MAIN_MSG_TYPE_OFFSET, MAIN_MSG_TYPE_LEN)
            main_message_type = struct.unpack('!B', b_part)[0]

            if main_package_length == 0 or main_package_length > 4096:
                break
            
            if main_message_type == PRIMARY_CLIENT_MSG_CODE:
                b_part = self._get_buffer_part(offset, main_package_length)
                yield b_part
                
            offset += main_package_length