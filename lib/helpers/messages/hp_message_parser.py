from threading import Lock
from queue import Queue
from datetime import datetime
import struct

from lib.models.data_structures.ds_robot_msg_buffer import DsRobotMsgBuffer

from lib.helpers.messages.hp_message_decoder import HpMessageDecoder
from lib.helpers.utils.looped_tasks.hp_looped_task_manager import HpLoopedTaskManager
from lib.helpers.constants.hp_message_attributes import *

PARSING_INTERVAL = 0.1

class HpMessageParser:

    _data_lock: Lock = Lock()
    _input_buffers: Queue[DsRobotMsgBuffer] = Queue(1000)

    _ltm: HpLoopedTaskManager = None

    @classmethod
    def put_in_queue(cls, buffer: bytes, id: str, capture_dt: datetime):
        if not cls._ltm:
            cls._ltm = cls._get_task_manager()
            cls._ltm.start_process()

        with cls._data_lock:
            cls._input_buffers.put_nowait(DsRobotMsgBuffer(buffer, id, capture_dt))

    @classmethod
    def _parse_messages(cls) -> bool:
        msg_buffer = cls._get_next_robot_msg_buffer()
        if msg_buffer is None:
            return False
        
        raw_message_data = set()
        for raw_message in msg_buffer.get_primary_client_messages():
            if raw_message is None:
                continue
            
            start, end = ROBOT_MSG_TYPE_OFFSET, ROBOT_MSG_TYPE_OFFSET + ROBOT_MSG_TYPE_LEN
            raw_message_type = struct.unpack('!B', raw_message[start: end])[0]
            
            raw_message_data.add((raw_message, raw_message_type))
        
        for data in raw_message_data:
            HpMessageDecoder.put_in_queue(*data, msg_buffer.robot_id, msg_buffer.capture_dt)

        return True

    @classmethod
    def _get_next_robot_msg_buffer(cls) -> DsRobotMsgBuffer:
        try:
            with cls._data_lock:
                msg_buffer = cls._input_buffers.get_nowait()
            return msg_buffer
        except:
            return None

    @classmethod
    def _get_task_manager(cls) -> HpLoopedTaskManager:
        return HpLoopedTaskManager(
                    main_task=cls._parse_messages
                    ,main_interval=PARSING_INTERVAL
                )